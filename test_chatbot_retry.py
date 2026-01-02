"""
Test script to verify chatbot retry logic works correctly
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.services.chatbot_service import chatbot_service

async def test_single_query():
    """Test a single query"""
    print("\n" + "="*60)
    print("TEST 1: Single Query")
    print("="*60)

    query = "What is Physical AI?"
    print(f"Query: {query}")

    try:
        result = await chatbot_service.process_chat(query=query)
        print(f"\n✅ Success!")
        print(f"Response: {result['response'][:200]}...")
        print(f"Sources: {len(result['sources'])} found")
        return True
    except Exception as e:
        print(f"\n❌ Failed: {e}")
        return False

async def test_multiple_rapid_queries():
    """Test multiple queries in rapid succession to trigger rate limiting"""
    print("\n" + "="*60)
    print("TEST 2: Rapid Fire Queries (Testing Retry Logic)")
    print("="*60)

    queries = [
        "What is Physical AI?",
        "Explain ROS2 fundamentals",
        "How does Gazebo simulation work?",
        "What are humanoid robots?",
        "Describe Isaac Sim basics"
    ]

    results = []
    for i, query in enumerate(queries, 1):
        print(f"\n[Query {i}/5] {query}")

        try:
            result = await chatbot_service.process_chat(query=query)
            success = "error" not in result['response'].lower()
            status = "✅" if success else "⚠️"
            print(f"{status} Response length: {len(result['response'])} chars")
            results.append(success)
        except Exception as e:
            print(f"❌ Exception: {e}")
            results.append(False)

        # Small delay between queries
        await asyncio.sleep(0.5)

    success_rate = sum(results) / len(results) * 100
    print(f"\n{'='*60}")
    print(f"Success Rate: {success_rate:.0f}% ({sum(results)}/{len(results)} queries)")
    print(f"{'='*60}")

    return success_rate >= 80  # At least 80% should succeed with retry logic

async def test_invalid_query():
    """Test handling of queries with no results"""
    print("\n" + "="*60)
    print("TEST 3: Query with No Results")
    print("="*60)

    query = "xyzabc123randomnonexistentquery"
    print(f"Query: {query}")

    try:
        result = await chatbot_service.process_chat(query=query)
        has_fallback = "don't know" in result['response'].lower() or "no relevant" in result['response'].lower()
        status = "✅" if has_fallback else "⚠️"
        print(f"{status} Response: {result['response'][:200]}...")
        return has_fallback
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  CHATBOT RETRY LOGIC TEST SUITE")
    print("="*70)
    print("\nThis will test:")
    print("1. Single query (baseline)")
    print("2. Rapid queries (retry logic)")
    print("3. Invalid query (fallback handling)")

    # Run tests
    test1_pass = await test_single_query()
    await asyncio.sleep(2)  # Cooldown

    test2_pass = await test_multiple_rapid_queries()
    await asyncio.sleep(2)  # Cooldown

    test3_pass = await test_invalid_query()

    # Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    print(f"Test 1 (Single Query):        {'✅ PASS' if test1_pass else '❌ FAIL'}")
    print(f"Test 2 (Rapid Queries):       {'✅ PASS' if test2_pass else '❌ FAIL'}")
    print(f"Test 3 (Invalid Query):       {'✅ PASS' if test3_pass else '❌ FAIL'}")

    all_pass = test1_pass and test2_pass and test3_pass
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_pass else '⚠️ SOME TESTS FAILED'}")
    print("="*70 + "\n")

    if not all_pass:
        print("⚠️  If tests failed due to rate limiting:")
        print("   1. Wait 60 seconds and run again")
        print("   2. Check Cohere API key is valid")
        print("   3. Consider upgrading Cohere plan")
        print("   See CHATBOT_RATE_LIMIT_FIX.md for solutions\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
