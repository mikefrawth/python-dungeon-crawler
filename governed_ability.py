from character_attributes import CharacterAttributes


class GovernedAbility:
    DEFAULT_MAGNITUDE_COEFFICIENT = 1.0

    def __init__(
        self,
        name: str,
        governing_attribute: str,
        magnitude_coefficient: float = DEFAULT_MAGNITUDE_COEFFICIENT,
        override=None,
    ):
        if governing_attribute not in CharacterAttributes.ATTRIBUTE_NAMES:
            raise ValueError(f"unknown attribute: {governing_attribute}")

        self.name = name
        self.governing_attribute = governing_attribute
        self.magnitude_coefficient = magnitude_coefficient
        self.override = override

    def scaled_output(self, character) -> float:
        if self.override is not None:
            return self.override(self, character)

        effective = character.attributes.effective_value(self.governing_attribute)

        return self.magnitude_coefficient * effective
