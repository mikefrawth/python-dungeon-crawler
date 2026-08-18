# Character & Combat System

Governs how a character's six core attributes drive combat math, gear, skills, feats, and status effects.

## Language

### Attributes & Values

**Attribute**:
One of the six core character stats (Might, Toughness, Agility, Perception, Intellect, Ego) that all derived combat and character values are computed from. Baseline is 0, not 10; can go negative.
_Avoid_: Stat, ability score

**Effective Value**:
An attribute's value after its diminishing-returns curve has been applied — the number skills, feats, and derived stats actually read. Never the raw attribute.
_Avoid_: Modified value, adjusted stat

### Combat

**Accuracy**:
Perception-derived measure of an attack's likelihood to land.
_Avoid_: Hit chance, to-hit

**Evasion**:
Agility-derived measure of a character's likelihood to avoid being hit.
_Avoid_: Dodge, evade rating

**Damage Reduction (DR)**:
Toughness-derived percentage mitigation of incoming damage.
_Avoid_: Armor, defense

**Status Resistance**:
Toughness-derived percentage resistance to poison/stun-type effects. Distinct from Damage Reduction even though both derive from Toughness.
_Avoid_: Resist, save

**Proc**:
An ability-level chance, granted only by specific skills or feats, to inflict a debuff on a successful hit. Not a universal property of all attacks — a plain attack procs nothing unless a specific ability grants it that chance.
_Avoid_: Trigger chance, on-hit effect (as a universal mechanic)

**Resist Chance**:
Ego-derived chance to fully negate an incoming debuff before it takes effect.
_Avoid_: Save, resist roll

**Debuff Dampening**:
Ego-derived reduction to the magnitude or duration of a debuff that wasn't fully resisted.
_Avoid_: Debuff reduction

### Character Systems

**Carry Capacity**:
Might-derived limit on how much a character can carry before becoming Encumbered.
_Avoid_: Weight limit, inventory cap

**Encumbered**:
The state of exceeding Carry Capacity. Reduces a character's effective Agility, which cascades into their Speed and Evasion.
_Avoid_: Overloaded, overweight

**Skill Check**:
A threshold comparison (effective attribute vs. a fixed difficulty set by content design) used for pass/fail moments like problem-solving or lore. Distinct from the continuously-scaling curves used elsewhere.
_Avoid_: Ability check

**Governing Attribute**:
The single attribute a skill or feat resolves around — the one it's gated by (skills only) and the one whose effective value drives its scaled output. Every skill and feat has exactly one; there are no multi-attribute (hybrid) skills or feats.
_Avoid_: Combine mode, hybrid pattern, scaling mode
