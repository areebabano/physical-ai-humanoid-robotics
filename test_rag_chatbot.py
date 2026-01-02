#!/usr/bin/env python3
"""
Test script for the RAG Chatbot functionality
This script tests all components of the RAG system step by step
"""

import asyncio
import os
import sys
from pathlib import Path

# Add backend src to path to import modules
sys.path.insert(0, str(Path(__file__).parent / "backend" / "src"))

import logging
from backend.src.services.qdrant_service import QdrantService
from backend.src.services.free_llm_service import FreeLLMService
from backend.src.services.text_chunking_service import TextChunkingService
from backend.src.config import settings


def setup_logging():
    """Setup logging for the test"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


async def test_free_llm_service():
    """Test the Free LLM Service"""
    print("\n=== Testing Free LLM Service ===")

    try:
        llm_service = FreeLLMService()
        print("[PASS] Free LLM Service initialized successfully")

        # Test embedding generation
        test_text = "This is a test sentence for embedding."
        embedding = await llm_service.generate_embedding(test_text)
        print(f"[PASS] Embedding generated successfully, length: {len(embedding)}")

        # Test response generation
        response = await llm_service.generate_response(
            query="What is Physical AI?",
            context=[{"content": "Physical AI is an approach to robotics that emphasizes the physical interaction between robots and their environment."}],
            selected_text=None
        )
        print(f"[PASS] Response generated successfully: {response[:50]}...")

        return True
    except Exception as e:
        print(f"[FAIL] Error testing Free LLM Service: {e}")
        return False


async def test_text_chunking_service():
    """Test the Text Chunking Service"""
    print("\n=== Testing Text Chunking Service ===")

    try:
        chunking_service = TextChunkingService()
        print("[PASS] Text Chunking Service initialized successfully")

        # Test text chunking
        sample_text = """
        # Introduction to Physical AI

        Physical AI is an approach to robotics that emphasizes the physical interaction between robots and their environment.
        It focuses on how robots can leverage physical properties and dynamics to perform tasks more efficiently.

        ## Key Principles

        The key principles of Physical AI include:

        - Embodiment: The physical form of the robot is crucial to its function
        - Environmental Interaction: Robots should exploit environmental properties
        - Dynamics: Understanding and utilizing dynamic interactions

        This approach differs significantly from traditional AI methods that focus primarily on computation and algorithms.
        Physical AI recognizes that the body and environment can be used as tools for computation and problem-solving.
        """

        chunks = chunking_service.chunk_content(sample_text, "test.md", "test_module")
        print(f"[PASS] Text chunked successfully into {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            print(f"  Chunk {i+1}: {len(chunk.content.split())} words, heading: '{chunk.heading}'")

        return True
    except Exception as e:
        print(f"[FAIL] Error testing Text Chunking Service: {e}")
        return False


async def test_qdrant_service():
    """Test the Qdrant Service"""
    print("\n=== Testing Qdrant Service ===")

    try:
        qdrant_service = QdrantService()
        print("[PASS] Qdrant Service initialized successfully")

        # Test collection stats
        stats = await qdrant_service.get_collection_stats()
        print(f"[PASS] Collection stats retrieved: {stats}")

        # Test embedding generation through Qdrant service
        test_text = "Test document for Qdrant integration"
        embedding = await qdrant_service.create_embedding(test_text)
        print(f"[PASS] Embedding created via Qdrant service, length: {len(embedding)}")

        return True
    except Exception as e:
        print(f"[FAIL] Error testing Qdrant Service: {e}")
        return False


async def test_end_to_end_ingestion():
    """Test end-to-end ingestion process"""
    print("\n=== Testing End-to-End Ingestion ===")

    try:
        qdrant_service = QdrantService()
        chunking_service = TextChunkingService()

        # Sample content to ingest
        sample_content = """
        # Chapter 1: Introduction to Physical AI and Humanoid Robotics

        Physical AI represents a paradigm shift in how we approach robotics and artificial intelligence.
        Rather than relying solely on computational power and complex algorithms, Physical AI leverages
        the physical properties of the robot and its environment to achieve intelligent behavior.

        ## Key Concepts

        The fundamental concepts of Physical AI include:

        1. **Embodiment**: The physical form and material properties of the robot are integral to its intelligence
        2. **Morphological Computation**: Physical structures can perform computations that would otherwise require software
        3. **Environment Interaction**: The environment becomes part of the control system
        4. **Dynamical Systems**: Behavior emerges from the interaction of multiple dynamical systems

        ## Applications in Humanoid Robotics

        In humanoid robotics, Physical AI principles enable more natural and efficient movement patterns.
        By designing robots that work with physical dynamics rather than against them, we can achieve:

        - More energy-efficient locomotion
        - Better balance and stability
        - More natural interaction with objects and humans
        - Improved robustness to disturbances
        """

        # Chunk the content
        chunks = chunking_service.chunk_content(sample_content, "chapter1.md", "physical_ai")
        print(f"[PASS] Content chunked into {len(chunks)} chunks")

        # Prepare chunks for ingestion
        chunk_dicts = []
        for chunk in chunks:
            chunk_dicts.append({
                'id': chunk.id,
                'content': chunk.content,
                'source': chunk.source,
                'module': chunk.module,
                'chunk_index': chunk.chunk_index,
                'heading': chunk.heading,
                'created_at': ''
            })

        # Ingest chunks
        result = await qdrant_service.bulk_ingest_chunks(chunk_dicts)
        print(f"[PASS] Ingestion completed: {result}")

        return True
    except Exception as e:
        print(f"[FAIL] Error in end-to-end ingestion: {e}")
        return False


async def test_search_functionality():
    """Test search functionality"""
    print("\n=== Testing Search Functionality ===")

    try:
        qdrant_service = QdrantService()

        # Test search with a query
        results = await qdrant_service.search("What is Physical AI?", limit=3)
        print(f"[PASS] Search completed, found {len(results)} results")

        for i, result in enumerate(results):
            print(f"  Result {i+1}: Score {result['score']:.3f}, Source: {result['source'][:30]}...")

        # Test search with context (selected text)
        results_with_context = await qdrant_service.search_with_context(
            query="Explain embodiment",
            selected_text="Embodiment: The physical form of the robot is crucial to its function",
            limit=2
        )
        print(f"[PASS] Contextual search completed, found {len(results_with_context)} results")

        return True
    except Exception as e:
        print(f"[FAIL] Error in search functionality: {e}")
        return False


async def run_all_tests():
    """Run all tests"""
    print("Starting RAG Chatbot System Tests...")

    setup_logging()

    tests = [
        ("Free LLM Service", test_free_llm_service),
        ("Text Chunking Service", test_text_chunking_service),
        ("Qdrant Service", test_qdrant_service),
        ("End-to-End Ingestion", test_end_to_end_ingestion),
        ("Search Functionality", test_search_functionality),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)

        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Print summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("[SUCCESS] All tests passed! The RAG chatbot system is working correctly.")
        return True
    else:
        print("[ERROR] Some tests failed. Please check the output above for details.")
        return False


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)