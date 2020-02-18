"""
Generic unit of currency.

Unlike most units, each currency is its own dimension.

Noether implements conversion itself, though you may re-implement
it, given that there is no general Most Reliable Source.
"""

from decimal import Decimal

# TODO: implement settings & storage first!
# TODO: force use of Decimal or Int before releasing this!!
# TODO: use locale.currency ..?

class Money:
    converter = None

class MoneyConverter:
    def convert(self, code_from: str, code_to: str) -> Decimal:
        """
        Convert between currencies given their codes.
        
        CAN use caching.
        """

    def refresh(self):
        """
        SHOULD refresh cache, if there is any.
        """

class NoetherMoneyConverter(MoneyConverter):
    """
    Noether's own money converter.
    
    Uses a cache, and automatically refreshes it if it's
    more than 24 hours out of date.
    """

    URL = ""
    def __init__(self):
        self.cache = {}
        self.last_updated = 0
    
    def convert(self, code_from: str, code_to: str) -> Decimal:
        pass

    def refresh(self):
        pass

Money.converter = NoetherMoneyConverter()
