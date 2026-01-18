"""
Factory for creating margin data providers.
"""

from typing import Any, Dict

from .jin10 import Jin10


class MarginFactory:
    """
    Factory for creating margin data providers.
    """

    _providers: Dict[str, Any] = {
        "jin10": Jin10,
    }

    @classmethod
    def get_provider(cls, source: str = "jin10", **kwargs) -> Jin10:
        """
        Get a margin data provider.

        Args:
            source: Data source name (e.g., "jin10")
            **kwargs: Additional arguments for the provider

        Returns:
            Margin data provider instance
        """
        if source not in cls._providers:
            raise ValueError(f"Unknown margin data provider: {source}")
        return cls._providers[source](**kwargs)

    @staticmethod
    def create(provider: str = "jin10") -> Jin10:
        """
        Create a margin data provider.

        Args:
            provider: Data source name (e.g., "jin10")

        Returns:
            Margin data provider instance
        """
        if provider == "jin10":
            return Jin10()
        raise ValueError(f"Unknown provider: {provider}")
