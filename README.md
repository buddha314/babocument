# Babocument

Another take on the document manager in VR/XR.

We are building an agentic application that will allow users to review documents concerning synthetic biology and biomanufacturing.

Core Components
Client Layer (/client): BabylonJS application with animated Librarian character
Server Layer (/server): FastAgent API with multi-agent coordination
Integration Layer: MCP (Model Context Protocol) plugins for Blender and Godot
Documentation (/specs): Comprehensive planning and implementation guides


👩‍🔬 Primary User Persona
Beabadoo - Computational Research Scientist (click to expand)
Beabadoo is a computational researcher in biomanufacturing at a major synthetic biology corporation. She has:

* Background: Graduate degree in computational chemistry, works in biology
* Daily Tasks: Supporting researchers, bioinformatics, computational drug discovery models
* Expertise: Chemistry, biology, biomanufacturing, mathematics

User Capabilities
Research & Discovery:

Query bioinks and academic journals with timeline visualization
Access sorted journal articles by publication year
Generate word clouds and trend analyses of research over time
Search and correlate ClinicalTrials.gov data with current research
Document Management:

Open articles and begin research from embedded ideas
Create and manage research workspaces
View workspace associations for articles
Save and analyze article summaries for trends
Interactive Experience:

Navigate a virtual "file room" descending through time with glass-paned years
Enter virtual labs for collaboration
Upload videos for text and image extraction
View 3D models of laboratory equipment
Data Sources:

Public journal repositories (editable list)
Web search capabilities for scientific topics
Full-text academic articles from sources like arXiv
ClinicalTrials.gov API integration
🤖 Agentic System
Multi-Agent Architecture Overview (click to expand)
🎮 Client Experience
Virtual Environment & User Interface (click to expand)
Virtual Environment Design
File Room: Continuous hallway descending through time
Glass Partitions: Separate different publication years
Timeline Navigation: Walk through research evolution
Virtual Labs: Collaborative spaces for team research
Equipment Showcase: 3D models of biomanufacturing tools

Visual Style
Inspired by curated images in ./data/lookbook
Clean, scientific aesthetic with modern UI elements
Smooth animations and transitions
Responsive design for various screen sizes