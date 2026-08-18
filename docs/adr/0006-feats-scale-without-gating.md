# Feats scale off attributes without being attribute-gated

Feats are explicitly level-gated, not attribute-gated — unlike skills, any character who hits the level requirement can take any feat. It would be reasonable to assume from that split that feats don't interact with attributes at all. They do: a feat's *effect magnitude* can still scale off an attribute's effective value, using the exact same curve rules skills use — just without a minimum-requirement check.

Consequence for code structure: `Skill` and `Feat` share a common base for "read the governing attribute, compute scaled output," since that logic is now identical between them. Minimum-requirement gating stays a separate, optional behavior that only `Skill` has — a future reader should not expect to find (or need) gating logic inside `Feat`.

> **Amended by [ADR-0008](./0008-single-attribute-only.md):** the original version of this ADR said feats reuse skills' combine-mode vocabulary (`sum_independent`, `chance_and_magnitude`) for multi-attribute effects. That's no longer true — skills and feats now resolve around exactly one attribute each, full stop.
