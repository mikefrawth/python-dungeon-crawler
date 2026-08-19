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

**Investment Point**:
The currency spent to raise a raw Attribute by exactly 1, always at flat cost regardless of the attribute's current value. Awarded as a fixed starting budget at character creation and again through leveling/training — the same mechanism both times, not two separate systems.
_Avoid_: XP, stat point, ability score improvement

**Investment Pool**:
The total number of Investment Points available to spend in a single allocation pass (a player's starting budget, an NPC/monster's generation budget, or a level-up's increment). Scarcity across the pool is what forces trade-offs between attributes.
_Avoid_: Budget, point pool

**Investment Cap**:
The maximum raw value a single Attribute may reach within one allocation pass, enforced independently of the Investment Pool — a character can be stopped from raising an Attribute further even with unspent pool remaining. Value depends on context (e.g. 10 for player character creation); not a single fixed number.
_Avoid_: Stat cap, max stat

**Investment Allocation**:
One pass of spending an Investment Pool against an Investment Cap, starting from a per-attribute snapshot of raw values taken at the pass's start. Spend and undo are always measured relative to that snapshot, not to universal baseline 0 — player character creation is the special case where the snapshot happens to be all zero. The same mechanism, parameterized differently, drives creation, leveling, and NPC/monster generation.
_Avoid_: Character creation (too narrow — implies creation-only), point buy

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
