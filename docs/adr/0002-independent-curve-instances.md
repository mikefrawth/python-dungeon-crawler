# Every bounded derived stat gets its own curve instance, even when sharing an attribute

Multiple bounded-percentage stats end up sharing a source attribute: Damage Reduction and Status Resistance both derive from Toughness; Resist Chance and Debuff Dampening both derive from Ego. The obvious shortcut would be to reuse one curve (one cap/steepness pair) per attribute and read it for every stat that attribute drives.

We rejected that shortcut. Each derived stat — DR, Status Resistance, the hit-resolution contest curve, mana/stamina Cost Reduction, Ego's Resist Chance, and Ego's Debuff Dampening — gets its own independently-tunable `bounded_curve(value, cap, steepness)` instance, even when two of them read the same raw attribute. They're different enough in gameplay feel (e.g. "how much less damage do I take" vs "how often do I fully avoid a status effect") to warrant separate tuning knobs, and coupling them would mean a balance change to one silently reshapes the other.

Consequence: one attribute can — and routinely does — drive several independently-shaped derived stats at once (e.g. Intellect drives both an unbounded AoE-size curve and a bounded Cost Reduction curve). Nothing in the design restricts an attribute to a single derived formula.
