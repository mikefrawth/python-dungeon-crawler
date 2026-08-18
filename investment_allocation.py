from character_attributes import CharacterAttributes


class InvestmentAllocation:
    PLAYER_INVESTMENT_POOL = 20  # experiment with this
    PLAYER_INVESTMENT_CAP = 10

    def __init__(self, attributes: CharacterAttributes, investment_pool: int, investment_cap: int):
        self.attributes = attributes
        self.investment_pool = investment_pool
        self.investment_cap = investment_cap
        self.snapshot = {
            name: getattr(attributes, name) for name in CharacterAttributes.ATTRIBUTE_NAMES
        }

    @classmethod
    def for_player_creation(cls) -> "InvestmentAllocation":
        return cls(CharacterAttributes(), cls.PLAYER_INVESTMENT_POOL, cls.PLAYER_INVESTMENT_CAP)

    @property
    def points_spent(self) -> int:
        return sum(
            getattr(self.attributes, name) - self.snapshot[name]
            for name in CharacterAttributes.ATTRIBUTE_NAMES
        )

    @property
    def points_remaining(self) -> int:
        return self.investment_pool - self.points_spent

    def spend(self, attribute_name: str, amount: int = 1) -> None:
        if amount <= 0:
            raise ValueError("amount must be a positive number of points")

        self._adjust(attribute_name, amount)

    def undo(self, attribute_name: str, amount: int = 1) -> None:
        if amount <= 0:
            raise ValueError("amount must be a positive number of points")

        self._adjust(attribute_name, -amount)

    def _adjust(self, attribute_name: str, delta: int) -> None:
        if attribute_name not in CharacterAttributes.ATTRIBUTE_NAMES:
            raise ValueError(f"unknown attribute: {attribute_name}")

        current = getattr(self.attributes, attribute_name)
        new_value = current + delta

        if delta > 0:
            if new_value > self.investment_cap:
                raise ValueError(
                    f"{attribute_name} would exceed the Investment Cap of {self.investment_cap}"
                )

            if delta > self.points_remaining:
                raise ValueError(
                    f"not enough Investment Points remaining: wanted {delta}, have {self.points_remaining}"
                )
        else:
            floor = self.snapshot[attribute_name]

            if new_value < floor:
                raise ValueError(f"{attribute_name} has nothing to undo")

        setattr(self.attributes, attribute_name, new_value)
