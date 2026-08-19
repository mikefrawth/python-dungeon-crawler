from governed_ability import GovernedAbility


class Skill(GovernedAbility):
    def __init__(
        self,
        name: str,
        governing_attribute: str,
        minimum_requirement: float,
        magnitude_coefficient: float = GovernedAbility.DEFAULT_MAGNITUDE_COEFFICIENT,
        override=None,
    ):
        super().__init__(name, governing_attribute, magnitude_coefficient, override)
        self.minimum_requirement = minimum_requirement

    def is_usable_by(self, character) -> bool:
        effective = character.attributes.effective_value(self.governing_attribute)

        return effective >= self.minimum_requirement
