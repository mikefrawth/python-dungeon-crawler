# Character & Progression Design Notes

Design conversation notes. Not implementation — decisions here still need to be turned
into actual code (`CharacterAttributes`, `Character`, `Skill`, `Feat`, etc.).

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
| Intellect | Area of effect and damage |
| Ego | Charisma, mental fortitude, lowering hostile effects |

### Leftover domains from the old Strength/Dexterity/Constitution/Intelligence/Wisdom/Ego list

These mechanics existed under the old stat table but don't fall cleanly under any of
the six domains above. Recommended homes below — **not decided, still TBD**:

| Old mechanic | Recommended home | Note |
|---|---|---|
| Carry capacity | Might | strength-adjacent |
| Weapon/armor requirements | Might | same reasoning, one home for simplicity |
| Damage Reduction | Toughness | pairs naturally with HP |
| Evasion/dodge | Agility | intuitive fit, though a judgment call |
| Poison/stun resistance | Toughness | physical resilience |
| Problem-solving/lore gathering | Intellect | direct carryover |
| Stamina/mana cost reduction | Intellect | keeps Ego purely resistance/social, not resource economy |
| Magic power (offense) | Might | folds into "damage and healing" broadly, regardless of source |

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
- Most skills key off a **single attribute**.
- Some skills offer **either/or** requirements (multiple attributes, best one counts).
- Some skills are **hybrid**, requiring/using multiple attributes together. Identified
  hybrid patterns so far (kept as a small fixed vocabulary rather than one-off code
  per skill):
  1. **`gate_both`** — dual-attribute requirement; character must clear the minimum
     for *both* attributes to use the skill at all.
  2. **`sum_independent`** — two components scale off two different attributes
     independently and their outputs are summed/combined (e.g., a magic-swordsman
     feat where weapon damage scales off a physical attribute and spell damage scales
     off a magic attribute as separate additive components).
  3. **`chance_and_magnitude`** — one attribute governs the *chance* of producing a
     result (e.g., an attacking/accuracy attribute), a different attribute governs
     the *magnitude* of that result when it triggers (e.g., a magic attribute scaling
     the damage of a proc'd effect). This was the resolved design for the
     magic-swordsman example.
  - Dual-attribute hybrid skills are intended to **reward spreading investment**
    across both attributes rather than dumping into one — this falls out naturally
    from using diminishing-returns curves per attribute and summing them (concave
    curves: splitting a fixed point budget across two attributes yields a higher
    combined total than dumping it all into one).
  - More hybrid patterns will likely emerge once actual feats/skills are designed;
    not worth speculating further in the abstract. A per-skill **override hook** is
    planned for cases that don't fit the fixed vocabulary.

## Feats

- Level-gated (not attribute-gated).
- Generic/universal — any character can learn a feat that meets the level
  requirement, unlike skills which are attribute-limited.
- Represent special passives.

## Implementation approach (agreed direction)

- Skills and Feats are **structured data** in a table, not one-off classes per skill.
- Dedicated `Skill` and `Feat` classes exist to give that data structure/behavior
  (e.g., checking requirements against a `CharacterAttributes`/`Character`, computing
  scaled output).
- Each `Skill`/`Feat` entry supports an **override hook** — an escape valve for cases
  that need bespoke logic beyond what the structured data + combine-mode vocabulary
  can express (e.g., a complex feat effect).
- Skills and Feats are specifically taken/held by the `Character` class (not by
  `CharacterAttributes`, which just holds raw attribute values).

## Open questions / TBD

- Exact per-attribute negative ("taken out") thresholds and what happens at each.
- Max character level.
- Exact diminishing-returns coefficients/steepness values for each formula (power
  curves and bounded curves alike) — to be tuned once there's content to balance
  against.
- Exact Damage Reduction (and other bounded attributes) cap values.
- Whether more hybrid skill combine-modes beyond the three identified are needed —
  deferred until concrete feats/skills are designed.
- Recommended homes for leftover mechanics (see table above) — not decided, still TBD.
