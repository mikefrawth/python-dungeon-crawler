from character_attributes import CharacterAttributes
from investment_allocation import InvestmentAllocation


class Character:
    DEFAULT_LEVEL = 0
    STARTING_PLAYER_LEVEL = 1

    def __init__(
        self,
        name: str,
        attributes: CharacterAttributes,
        level: int = DEFAULT_LEVEL,
    ):
        self.name = name
        self.attributes = attributes
        self.level = level
        self.skills = []
        self.feats = []

    @classmethod
    def create_player(cls, name: str, allocation: InvestmentAllocation) -> "Character":
        if allocation.points_remaining != 0:
            raise ValueError(
                f"Investment Allocation must be fully spent before creation: "
                f"{allocation.points_remaining} points remaining"
            )

        return cls(name, allocation.attributes, level=cls.STARTING_PLAYER_LEVEL)
