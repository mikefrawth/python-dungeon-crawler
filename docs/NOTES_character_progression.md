# Character & Progression Design Notes

Design conversation notes. Not implementation — decisions here still need to be turned
into actual code (`CharacterAttributes`, `Character`, `Skill`, `Feat`, etc.).

Canonical vocabulary lives in [`CONTEXT.md`](../CONTEXT.md); the *why* behind the
harder-to-reverse calls below lives in [`docs/adr/`](./adr/). This file stays the
working narrative draft.

## Levels

- Characters have a level, capped at an undetermined max level (TBD once more content
  ideas exist).
- **Level 0** is a special case, not the default:
  - Used for basic/generic NPCs.
  - Used for an optional tutorial mode: the player starts at level 0 and gains their
    first level as part of the tutorial.
  - Fictionally, levels may be tied to an "awakening" — not every creature has levels;
    only certain creatures/monsters do. Level 1 implies a character already has some
    training or is already a threat.
- **Level 1** is the normal starting point for player characters outside the tutorial.

## Attributes

Universal baseline for every attribute is **0** (not 10). Attributes can go negative.

### Character creation

Creation is not a separate system — it's the same Investment Point mechanism as
leveling/training, just spent before play starts. Every new character gets a **fixed
starting budget** of Investment Points (same for everyone; exact size TBD during
tuning), spent at flat cost — each point raises a raw attribute by exactly +1,
regardless of current value. No progressive/escalating cost per point.

Baseline 0 is a hard floor at creation: no dump-stat trade-down. A character cannot
start below 0 on any attribute to free up points elsewhere — negative attributes are
exclusively a post-creation consequence (curses, debuffs, drain), never a creation-time
build choice. See [ADR-0009](./adr/0009-investment-points-flat-cost.md).

A player character's creation also has a hard **per-attribute ceiling of 10** — no
single attribute may exceed 10 at creation even with starting budget left unspent.
Overspending past either the budget or the per-attribute cap is rejected outright, not
silently clamped.

The spend-tracking mechanism (points spent computed from current raw values, a spend
operation, an undo operation) is **parameterized by budget and cap**, not hardcoded to
the player-creation numbers. This is the same mechanism used to generate NPCs/special
monsters (different budget/cap) and to handle leveling (existing 100 lifetime
investment cap, per-level budget increments, instead of creation's one-time numbers).
See [ADR-0010](./adr/0010-parameterized-spend-tracking.md).

This mechanism is the **Investment Allocation** (see `CONTEXT.md`) — spend/remaining/undo
are measured relative to a per-attribute snapshot taken at the start of the pass, not
universal baseline 0. Creation is the special case where that snapshot is all zero.
See [ADR-0011](./adr/0011-investment-allocation-is-snapshot-relative.md).

- Investment cap: an attribute can be raised via investment (leveling, training, etc.)
  up to **100**.
- Magic equipment can push an attribute **above 100**. Gear bonuses are added to the
  raw attribute value *before* the diminishing-returns curve is applied, and obey the
  same curve as invested points (no separate formula for gear-derived attribute
  points).
- High-end magic equipment is not limited to boosting raw attributes — it can also add
  bonuses directly to a derived formula's output (e.g., a flat bonus to Damage
  Reduction) *after* the attribute curve is applied, bypassing the curve entirely.
  Buffs/abilities can do the same.
- Attributes can go negative (via curses, debuffs, drain effects, etc.). Each attribute
  has its own **negative threshold** at which point the character is "taken out" — not
  necessarily killed. What "taken out" means can differ per attribute (e.g., Toughness
  bottoming out reads as physical death/collapse; Ego bottoming out could read as
  madness/mental break rather than death). Exact thresholds and per-attribute
  consequences are still TBD.

### Attribute list (Pillars of Eternity-inspired, names adjusted)

| Attribute | Governs |
|---|---|
| Might | Damage and healing |
| Toughness | HP |
| Agility | Speed |
| Perception | Accuracy |
| Intellect | Area of effect |
| Ego | Charisma, mental fortitude, lowering hostile effects |

Intellect's row previously read "Area of effect and damage" — the "damage" half was
vestigial. Might owns all damage magnitude, physical or magical; Intellect scales
reach (AoE radius/target count) only. See [ADR-0005](./adr/0005-might-owns-all-damage.md).

### Leftover domains from the old Strength/Dexterity/Constitution/Intelligence/Wisdom/Ego list

These mechanics existed under the old stat table but didn't fall cleanly under any of
the six domains above. Homes and calculation shapes are now **decided**:

| Old mechanic | Home | Calculation shape |
|---|---|---|
| Carry capacity | Might | Linear (`base + raw_might * multiplier`), not a diminishing-returns curve — see [ADR-0003](./adr/0003-formula-family-per-stat.md) |
| Weapon/armor requirements | Might | Hard gate, continuously re-evaluated (not a snapshot at equip time) — see [ADR-0004](./adr/0004-continuous-equip-gate.md) |
| Damage Reduction | Toughness | Bounded curve, own instance — see "Damage Reduction specifics" below and [ADR-0002](./adr/0002-independent-curve-instances.md) |
| Evasion/dodge | Agility | Feeds the Accuracy vs. Evasion hit-resolution contest — see [ADR-0001](./adr/0001-combat-hit-resolution.md) |
| Poison/stun resistance | Toughness | Bounded curve, own instance separate from Damage Reduction's — see [ADR-0002](./adr/0002-independent-curve-instances.md) |
| Problem-solving/lore gathering | Intellect | Skill-check/threshold (`effective_intellect >= fixed per-node DC`), not a curve — see [ADR-0003](./adr/0003-formula-family-per-stat.md) |
| Stamina/mana cost reduction | Intellect | Bounded curve, own instance, coexists with Intellect's unbounded AoE duty — see [ADR-0002](./adr/0002-independent-curve-instances.md) |
| Magic power (offense) | Might | Folds directly into Might's existing unbounded damage/healing curve; no separate spell-power track — see [ADR-0005](./adr/0005-might-owns-all-damage.md) |

Carry-weight overflow (Encumbered — see `CONTEXT.md`) reduces effective Agility, which
cascades into the existing Speed and Evasion outputs rather than introducing a
standalone encumbrance status system.

Leveling speed (previously under Intelligence) has been **cut** — not carried forward
to any attribute.

## Diminishing returns (core formula system)

Diminishing returns live at the **attribute** level, not the skill level — skills
simply read an attribute's already-transformed ("effective") value. Two distinct
curve families, both centered on baseline 0:

### 1. Unbounded diminishing returns (power-scaling attributes)

For attributes/effects where more should always help at least a little, with no hard cap
(e.g., raw damage/power scaling). No cap was an intentional choice — open-ended growth,
just with each additional point worth less than the last.

```python
import math

def signed_diminishing(value: int, baseline: int, coefficient: float) -> float:
    delta = value - baseline
    return math.copysign(coefficient * math.sqrt(abs(delta)), delta)
```

`sqrt` gives a punchier early curve; `log1p` tapers harder. Either works — exact
coefficients TBD during tuning.

### 2. Bounded diminishing returns (mitigation/resistance attributes)

For percentage-style mitigation attributes (Damage Reduction, Evasion, resistances) where
there must be a hard ceiling (nobody reaches 100% reduction) *and* a hard floor
(nobody takes unbounded bonus damage from being catastrophically weak). Symmetric
around baseline 0.

```python
import math

def bounded_curve(attribute_value: int, cap: float, steepness: float) -> float:
    return cap * math.tanh(steepness * attribute_value)
```

Key design intent: the attribute-driven curve alone should **not** be able to reach
the cap even at 100 invested attribute — e.g. tuned so 100 Toughness only reaches
~70-80% of the Damage Reduction cap. Reaching the actual ceiling requires stacking additional
flat bonuses on top (from feats, buffs, or high-end gear) *after* the curve, then
clamping the total to `[-cap, +cap]`. This keeps "nobody has 100% DR" true by default
while still leaving room for a fully-built, buffed character to approach it.

Exact cap values are undecided — TBD during tuning.

### Damage Reduction specifics

- Baseline is 0 (matches universal attribute baseline): below 0 effective Toughness, a
  character takes a diminishing-returns *penalty* (more damage); above 0, a
  diminishing-returns *bonus* (less damage).
- Low Toughness is only one source of negative Damage Reduction — curses, skills, and
  other effects can also push DR negative, so the formula must handle negative inputs
  generally, not just "Toughness below baseline."
- DR is bounded (see "Bounded diminishing returns" above) — no one should ever reach
  100% reduction from attributes alone.
- Poison/Stun Resistance shares Toughness as its home but is a **separate bounded
  curve instance** from DR (own cap/steepness) — see
  [ADR-0002](./adr/0002-independent-curve-instances.md).

## Combat resolution

- **Hit chance**: `bounded_curve(raw_accuracy - raw_evasion, cap, steepness)` — the
  curve is applied once, directly to the raw delta between Accuracy (Perception) and
  Evasion (Agility), not to two already-curved "effective" values. See
  [ADR-0001](./adr/0001-combat-hit-resolution.md).
- **Debuff procs**: not a universal stat — no attribute grants a baseline "chance to
  proc a debuff on any attack." Procs are purely ability-level, granted only by
  skills/feats specifically designed to inflict one. A proc roll only happens after
  the attack has already succeeded on the hit-chance roll above. A proc-capable
  ability reads **one** governing attribute for both its proc chance and the debuff's
  magnitude/duration — chosen per-ability, no fixed default. See
  [ADR-0007](./adr/0007-debuff-procs-are-ability-level.md) and
  [ADR-0008](./adr/0008-single-attribute-only.md).
- **Resisting debuffs**: Ego gives the defender two independent bounded-curve layers —
  a **Resist Chance** (chance to fully negate the debuff on application) and a
  **Debuff Dampening** (reduces magnitude/duration of whatever gets through), mirroring
  how Toughness gets both raw HP and DR. See
  [ADR-0002](./adr/0002-independent-curve-instances.md).

## Skills

No class system (explicitly not D&D-style). Characters learn skills/abilities over
time; access is gated and scaled by attributes rather than by class.

- **Gating**: each skill has a **minimum attribute requirement** to use at all (hard
  gate, not soft). Below the minimum, the skill is simply unusable.
- **Scaling**: once unlocked, a skill's power scales using the governing attribute's
  own effective (post diminishing-returns) value — skills don't define their own
  curve, they read the attribute's.
- **No cap on skill power** — intentionally left open-ended (this is the "unbounded"
  curve family).
- Every skill has **exactly one governing attribute** — used for both the gate and
  the scaling. No hybrid/dual-attribute skills, no either/or (best-of-two)
  requirements. See [ADR-0008](./adr/0008-single-attribute-only.md).

## Feats

- Level-gated (not attribute-gated).
- Generic/universal — any character can learn a feat that meets the level
  requirement, unlike skills which are attribute-limited.
- Represent special passives.
- **Feats can still scale off attributes.** No minimum-requirement gate exists for
  feats, but a feat's *effect magnitude* can read an attribute's effective
  (curve-transformed) value exactly like a skill does. Like skills, a feat has
  **exactly one governing attribute** — no multi-attribute combos. See
  [ADR-0006](./adr/0006-feats-scale-without-gating.md) and
  [ADR-0008](./adr/0008-single-attribute-only.md).

## Implementation approach (agreed direction)

- Skills and Feats are **structured data** in a table, not one-off classes per skill.
- Dedicated `Skill` and `Feat` classes exist to give that data structure/behavior
  (e.g., checking requirements against a `CharacterAttributes`/`Character`, computing
  scaled output).
- `Skill` and `Feat` share a common base/mixin for "read the governing attribute,
  compute scaled output" — that logic is now identical between them.
  Minimum-requirement gating stays a separate, optional behavior specific to `Skill`
  only. See [ADR-0006](./adr/0006-feats-scale-without-gating.md) and
  [ADR-0008](./adr/0008-single-attribute-only.md).
- Each `Skill`/`Feat` entry supports an **override hook** — an escape valve for cases
  that need bespoke logic beyond what the structured data can express (e.g., a
  complex feat effect).
- Skills and Feats are specifically taken/held by the `Character` class (not by
  `CharacterAttributes`, which just holds raw attribute values).

## Open questions / TBD

- Exact size of the starting Investment Point budget (see "Character creation" above).
- Exact per-attribute negative ("taken out") thresholds and what happens at each.
- Max character level.
- Exact diminishing-returns coefficients/steepness values for each formula (power
  curves and bounded curves alike, including the now-separate instances for DR,
  Status Resistance, Cost Reduction, the hit-resolution contest, Resist Chance, and
  Debuff Dampening) — to be tuned once there's content to balance against.
- Exact cap values for each bounded stat.
- Exact carry-capacity linear formula constants (`base`, `multiplier`).
