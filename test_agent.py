"""
Simple test script to verify agents are working.
"""
import asyncio
from src.agents.architect_agent import analyze_requirements


async def test_requirements_analysis():
    """Test the requirements analysis agent."""
    business_idea = "A task management app for remote teams with Kanban boards"
    detail_level = "high_level"

    print("Testing requirements analysis agent...")
    print(f"Business idea: {business_idea}")
    print(f"Detail level: {detail_level}\n")

    try:
        result = await analyze_requirements(business_idea, detail_level)
        print("SUCCESS! Requirements analysis completed.")
        print(f"\nCore Features: {result.core_features}")
        print(f"User Types: {result.user_types}")
        print(f"Complexity: {result.complexity_assessment}")
        return result
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = asyncio.run(test_requirements_analysis())
    if result:
        print("\n✅ Agent test passed!")
    else:
        print("\n❌ Agent test failed!")
