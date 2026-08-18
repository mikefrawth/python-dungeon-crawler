# Not every derived stat uses a diminishing-returns curve

The core design has two curve families — unbounded (power-scaling) and bounded (percentage mitigation) — and it would be consistent to force every derived stat through one of them. We decided against that for stats where a curve doesn't fit the thing being modeled:

- **Carry Capacity** is a practical logistics number (how much you can carry), not a power stat or a percentage. It uses a third, plain **linear** formula off raw Might (`capacity = base + raw_might * multiplier`), bypassing both curve families entirely. Diminishing returns on carry capacity would just read as an arbitrary inventory-management penalty, and it doesn't need a "nobody reaches the ceiling" narrative the way Damage Reduction does.
- **Problem-solving / lore checks** are pass/fail moments ("did you notice/understand this"), not a magnitude that scales smoothly. They use a **skill-check/threshold** mechanic — effective Intellect compared against a fixed per-node difficulty set by content design — rather than either curve.

Consequence: the formula family is a per-stat decision, not a system-wide rule. When a new derived stat is designed, the first question is which of the three shapes (unbounded curve, bounded curve, or something else — linear, threshold) actually matches what's being modeled, rather than defaulting to one of the two existing curves.
