"""
Test script for Jin10 Margin data.
"""

from akshare_two.modules.market.jin10 import Jin10


def test_margin_data():
    """Test getting margin data."""
    margin = Jin10()

    # Test getting margin history
    print("Testing get_margin_history...")
    history = margin.get_margin_history(days=5)
    print(f"History shape: {history.shape}")
    print(history.head())

    print("\n" + "="*50)
    print("Test completed successfully!")


if __name__ == "__main__":
    test_margin_data()
