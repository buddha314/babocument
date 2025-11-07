"""
Pytest configuration and fixtures.
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from app.services.vector_db import VectorDatabase


@pytest.fixture
def temp_db_path():
    """Create a temporary directory for test database."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    # Cleanup after test
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def vector_db(temp_db_path):
    """Create a fresh VectorDatabase instance for testing."""
    db = VectorDatabase(storage_path=str(temp_db_path))
    yield db
    # Cleanup is handled by temp_db_path fixture


@pytest.fixture
def sample_papers():
    """Sample paper data for testing."""
    return [
        {
            "id": "paper1",
            "title": "CRISPR Gene Editing in Bioink Scaffolds",
            "abstract": "We demonstrate CRISPR-Cas9 gene editing capabilities in 3D bioprinted scaffolds for tissue engineering applications.",
            "full_text": "CRISPR Gene Editing in Bioink Scaffolds. We demonstrate CRISPR-Cas9 gene editing capabilities in 3D bioprinted scaffolds for tissue engineering applications. The results show improved cell viability and differentiation.",
            "authors": ["Smith, J.", "Johnson, A."],
            "year": 2023,
            "source": "test",
            "doi": "10.1234/test.001",
        },
        {
            "id": "paper2",
            "title": "Hydrogel-Based Bioinks for 3D Printing",
            "abstract": "Novel hydrogel formulations for improved printability and cell encapsulation in bioprinting.",
            "full_text": "Hydrogel-Based Bioinks for 3D Printing. Novel hydrogel formulations for improved printability and cell encapsulation in bioprinting. We tested various crosslinking methods.",
            "authors": ["Lee, K.", "Wang, M."],
            "year": 2022,
            "source": "test",
        },
        {
            "id": "paper3",
            "title": "Neural Network Applications in Manufacturing",
            "abstract": "Machine learning approaches for optimizing manufacturing processes using neural networks.",
            "full_text": "Neural Network Applications in Manufacturing. Machine learning approaches for optimizing manufacturing processes using neural networks. Focus on quality control.",
            "authors": ["Brown, R."],
            "year": 2024,
            "source": "test",
            "arxiv_id": "2401.12345",
        },
    ]
