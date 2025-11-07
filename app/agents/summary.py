"""
Summary Agent

Handles document summarization using LLM.
"""

from typing import Any

from app.agents.base import BaseAgent


class SummaryAgent(BaseAgent):
    """
    Summary Agent - Document summarization and explanation.

    Responsibilities:
    - Generate concise summaries of scientific papers
    - Explain complex concepts in simpler terms
    - Create multi-level summaries (abstract, detailed, technical)
    - Summarize multiple papers together (meta-summary)
    - Extract key takeaways and actionable insights
    - Generate topic-specific summaries (e.g., just methodology)
    """

    def __init__(self, event_bus=None, llm_client=None, vector_db=None):
        """
        Initialize Summary Agent.

        Args:
            event_bus: Event bus for publishing updates
            llm_client: LLM client for text generation
            vector_db: Vector database for retrieving document content
        """
        super().__init__("summary", event_bus)
        self.llm_client = llm_client
        self.vector_db = vector_db

    async def process_task(
        self, task_id: str, params: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Process a summarization task.

        Args:
            task_id: Unique task identifier
            params: Task parameters including:
                - document_ids: List of document IDs to summarize
                - summary_type: Type of summary ('concise', 'detailed', 'technical', 'eli5')
                - focus: Optional focus area (methodology, results, conclusions)
                - max_length: Maximum summary length in words

        Returns:
            Generated summaries with metadata
        """
        document_ids = params.get("document_ids", [])
        summary_type = params.get("summary_type", "concise")
        focus = params.get("focus")
        max_length = params.get("max_length", 250)

        self.logger.info(
            "starting_summarization",
            task_id=task_id,
            document_count=len(document_ids),
            summary_type=summary_type,
        )
        await self.publish_progress(task_id, 10, "Loading documents...")

        if not document_ids:
            error = "No documents provided for summarization"
            await self.publish_error(task_id, error)
            return {"error": error}

        try:
            if len(document_ids) == 1:
                result = await self._summarize_single(
                    task_id, document_ids[0], summary_type, focus, max_length
                )
            else:
                result = await self._summarize_multiple(
                    task_id, document_ids, summary_type, focus, max_length
                )

            await self.publish_progress(task_id, 100, "Summary complete")
            await self.publish_completion(task_id, result)

            return result

        except Exception as e:
            error_msg = f"Summarization failed: {str(e)}"
            self.logger.error("summarization_error", task_id=task_id, error=error_msg)
            await self.publish_error(task_id, error_msg)
            return {"error": error_msg}

    async def _summarize_single(
        self,
        task_id: str,
        document_id: str,
        summary_type: str,
        focus: str | None,
        max_length: int,
    ) -> dict[str, Any]:
        """
        Summarize a single document.

        Args:
            task_id: Task identifier for progress tracking
            document_id: Document ID to summarize
            summary_type: Type of summary to generate
            focus: Optional focus area
            max_length: Maximum summary length

        Returns:
            Generated summary with metadata
        """
        await self.publish_progress(task_id, 30, "Retrieving document...")

        # Retrieve document from vector DB
        if not self.vector_db:
            return {
                "error": "Vector database not available",
                "task_id": task_id,
            }
        
        try:
            # Get document metadata and content (synchronous call)
            document = self.vector_db.get_paper(document_id)
            
            if not document:
                return {
                    "error": f"Document {document_id} not found",
                    "task_id": task_id,
                }
            
            # Extract text content for summarization
            doc_text = document.get("document", "")
            metadata = document.get("metadata", {})
            
            title = metadata.get("title", "Unknown")
            abstract = metadata.get("abstract", "")
            
            # Use abstract if available, otherwise use document excerpt
            text_to_summarize = abstract if abstract else doc_text[:2000]
            
            if not text_to_summarize:
                return {
                    "error": "Document has no content to summarize",
                    "task_id": task_id,
                }
            
            await self.publish_progress(task_id, 50, "Generating summary...")
            
            # Generate summary using LLM
            summary_text = None
            if self.llm_client:
                try:
                    # Map summary_type to LLM style
                    style_map = {
                        "concise": "concise",
                        "detailed": "detailed",
                        "technical": "detailed",
                        "eli5": "concise"
                    }
                    llm_style = style_map.get(summary_type, "concise")
                    
                    # Add context about focus area if specified
                    prompt_text = text_to_summarize
                    if focus:
                        prompt_text = f"Focus on {focus}:\n\n{prompt_text}"
                    
                    summary_text = await self.llm_client.summarize(
                        text=f"Title: {title}\n\n{prompt_text}",
                        max_length=max_length,
                        style=llm_style
                    )
                except Exception as e:
                    self.logger.warning("llm_summarization_failed", error=str(e))
                    summary_text = None
            
            # Fallback if no LLM available or LLM fails
            if not summary_text:
                # Return the abstract or content excerpt directly
                if abstract:
                    summary_text = f"Here's the abstract:\n\n{abstract}"
                else:
                    summary_text = f"Here's an excerpt from the paper:\n\n{text_to_summarize[:500]}..."
                self.logger.info("using_fallback_summary", has_abstract=bool(abstract))
            
            await self.publish_progress(task_id, 90, "Extracting keywords...")
            
            # Extract keywords (only if LLM is available)
            keywords = []
            if self.llm_client:
                try:
                    extracted = await self.llm_client.extract_keywords(text_to_summarize, max_keywords=5)
                    if extracted:
                        keywords = extracted
                except Exception as e:
                    self.logger.debug("keyword_extraction_skipped", reason="llm_error", error=str(e))
            
            result = {
                "task_id": task_id,
                "document_id": document_id,
                "title": title,
                "summary_type": summary_type,
                "focus": focus,
                "summary": summary_text,
                "key_terms": keywords,
                "word_count": len(summary_text.split()) if summary_text else 0,
            }
            
            return result
            
        except Exception as e:
            self.logger.error("summarization_error", task_id=task_id, error=str(e))
            return {
                "error": f"Failed to summarize document: {str(e)}",
                "task_id": task_id,
            }

    async def _summarize_multiple(
        self,
        task_id: str,
        document_ids: list[str],
        summary_type: str,
        focus: str | None,
        max_length: int,
    ) -> dict[str, Any]:
        """
        Generate meta-summary of multiple documents.

        Args:
            task_id: Task identifier
            document_ids: List of document IDs to summarize together
            summary_type: Type of summary
            focus: Optional focus area
            max_length: Maximum summary length

        Returns:
            Meta-summary combining insights from all documents
        """
        await self.publish_progress(task_id, 30, "Generating meta-summary...")

        # TODO: Implement multiple document summarization
        # - Retrieve all document contents
        # - Extract relevant sections from each
        # - Identify common themes and unique contributions
        # - Generate unified summary that:
        #   - Synthesizes findings across papers
        #   - Highlights agreements and disagreements
        #   - Notes evolution of ideas (if chronological)
        # - Call LLM with combined context
        # - Format as coherent narrative

        # Placeholder result
        result = {
            "task_id": task_id,
            "document_ids": document_ids,
            "summary_type": summary_type,
            "focus": focus,
            "meta_summary": f"Meta-summary of {len(document_ids)} documents (placeholder)",
            "common_themes": [],
            "unique_contributions": {},
            "word_count": 0,
        }

        return result

    async def summarize_for_conversation(
        self, query: str, context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Generate summary in response to conversational query.

        Used by conversational agent interface for natural language summary requests.

        Args:
            query: Natural language summary request
            context: Conversation context including documents and preferences

        Returns:
            Summary formatted for conversational response
        """
        self.logger.info("conversational_summary", query=query)

        # If no specific documents selected, search for documents related to the query
        document_ids = context.get("selected_documents", [])
        
        if not document_ids and self.vector_db:
            # Try to find relevant documents based on the query
            try:
                # Extract search terms from the query
                search_terms = self._extract_search_terms(query)
                if search_terms:
                    self.logger.info("searching_for_documents", query=search_terms)
                    # Use the vector DB search method (synchronous)
                    search_results = self.vector_db.search(
                        query=search_terms,
                        n_results=3
                    )
                    
                    if search_results:
                        # Use the most relevant document
                        document_ids = [search_results[0]["id"]]
                        self.logger.info("found_documents", count=len(document_ids), doc_id=document_ids[0])
            except Exception as e:
                self.logger.warning("document_search_failed", error=str(e))

        # If still no documents, provide helpful response
        if not document_ids:
            return {
                "response": "I can help you summarize research papers. You can ask me to:\n\n"
                           "• Summarize a specific paper by name\n"
                           "• Tell you about bioinks, bioprinting, or tissue engineering\n"
                           "• Explain papers in simple terms\n\n"
                           "What would you like to know about?",
                "requires_clarification": True,
            }

        # Parse query for summary type and focus
        summary_type = self._extract_summary_type(query)
        focus = self._extract_focus(query)
        max_length = self._extract_length_preference(query, default=250)

        # Generate task ID and process
        task_id = context.get("conversation_id", "conv_unknown")
        result = await self.process_task(
            task_id,
            {
                "document_ids": document_ids,
                "summary_type": summary_type,
                "focus": focus,
                "max_length": max_length,
            },
        )

        return {
            "response": self._format_summary_response(result, query),
            "summary_data": result,
        }
    
    def _extract_search_terms(self, query: str) -> str:
        """
        Extract search terms from a query.

        Args:
            query: User's query

        Returns:
            Cleaned search terms
        """
        # Remove common question words and summarization keywords
        stopwords = [
            "summarize", "summary", "tell me about", "what is", "what are",
            "explain", "describe", "give me", "show me", "a", "an", "the",
            "can you", "could you", "please", "help", "me", "with"
        ]
        
        query_lower = query.lower()
        for word in stopwords:
            query_lower = query_lower.replace(word, " ")
        
        # Clean up extra spaces
        terms = " ".join(query_lower.split())
        return terms if terms else query

    def _extract_summary_type(self, query: str) -> str:
        """
        Extract summary type from natural language query.

        Args:
            query: User query

        Returns:
            Summary type ('concise', 'detailed', 'technical', 'eli5')
        """
        query_lower = query.lower()

        if any(word in query_lower for word in ["simple", "eli5", "explain like", "basic"]):
            return "eli5"
        elif any(word in query_lower for word in ["detailed", "comprehensive", "thorough"]):
            return "detailed"
        elif any(word in query_lower for word in ["technical", "methodology", "methods"]):
            return "technical"
        else:
            return "concise"

    def _extract_focus(self, query: str) -> str | None:
        """
        Extract focus area from query.

        Args:
            query: User query

        Returns:
            Focus area or None
        """
        query_lower = query.lower()

        if "method" in query_lower:
            return "methodology"
        elif "result" in query_lower or "finding" in query_lower:
            return "results"
        elif "conclusion" in query_lower or "takeaway" in query_lower:
            return "conclusions"
        elif "introduction" in query_lower or "background" in query_lower:
            return "introduction"

        return None

    def _extract_length_preference(self, query: str, default: int) -> int:
        """
        Extract length preference from query.

        Args:
            query: User query
            default: Default length

        Returns:
            Maximum word count for summary
        """
        query_lower = query.lower()

        if any(word in query_lower for word in ["brief", "short", "quick"]):
            return 100
        elif any(word in query_lower for word in ["long", "comprehensive", "detailed"]):
            return 500

        return default

    def _format_summary_response(
        self, summary_result: dict[str, Any], original_query: str
    ) -> str:
        """
        Format summary for conversational response.

        Args:
            summary_result: Raw summary results
            original_query: User's original query

        Returns:
            Natural language summary response
        """
        if "error" in summary_result:
            return f"I encountered an issue: {summary_result['error']}"

        summary_text = summary_result.get("summary") or summary_result.get("meta_summary", "")
        title = summary_result.get("title", "")
        key_terms = summary_result.get("key_terms", [])
        
        # Build response with title and summary
        response = ""
        
        if title and title != "Unknown":
            response += f"**{title}**\n\n"
        
        if summary_text:
            response += f"{summary_text}\n\n"
        
        if key_terms:
            response += f"*Key terms: {', '.join(key_terms)}*"
        
        return response if response else "I couldn't generate a summary for that document."

    async def explain_concept(
        self, concept: str, context: dict[str, Any], complexity: str = "simple"
    ) -> dict[str, Any]:
        """
        Explain a specific concept mentioned in documents.

        Args:
            concept: Concept to explain (e.g., "CRISPR", "bioink", "CAR-T therapy")
            context: Context including relevant documents
            complexity: Explanation complexity ('simple', 'moderate', 'technical')

        Returns:
            Explanation with examples and context
        """
        # TODO: Implement concept explanation
        # - Find mentions of concept in documents
        # - Extract definitions and usage
        # - Generate explanation appropriate to complexity level
        # - Provide examples from the papers

        return {
            "concept": concept,
            "explanation": f"Explanation of {concept} (to be implemented)",
            "examples": [],
            "related_concepts": [],
        }
