from character_attributes import CharacterAttributes


class Character:
    DEFAULT_LEVEL = 1

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
