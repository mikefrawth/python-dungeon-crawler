# Debuff procs are ability-level only, not a universal attribute-driven stat

The instinct going into this decision was to give Intellect a "proc chance" — a universal percentage, read off one attribute, that lets *any* attack have a chance to inflict a debuff. We rejected that. Proc chance is not a new derived stat at all; it's a property of specific abilities. Only skills/feats explicitly designed with a proc component can proc a debuff — a plain weapon swing procs nothing unless a specific ability grants it that chance. This keeps "can this attack inflict a status effect" an explicit per-ability design choice instead of an ambient property of every attack in the game, and avoids adding a 7th universal formula to the core attribute table.

One follow-on decision rounds this out:

- The proc roll only fires **after** the underlying attack has already succeeded on the hit-resolution roll (ADR-0001) — a debuff represents "you connected *and* additionally inflicted something," not an independent event. An ability wanting an effect regardless of hit/miss (a ground hazard, a guaranteed AoE) is a different ability shape, not modeled as an on-attack proc.

> **Amended by [ADR-0008](./0008-single-attribute-only.md):** the original version of this ADR split a proc-capable ability's "chance" (defaulting to Perception) from its "magnitude" (varies per-ability) across two attributes, via the now-cut `chance_and_magnitude` combine mode. That split is gone — a proc-capable ability now reads **one** governing attribute for both its proc chance and its debuff magnitude/duration, chosen per-ability like any other skill or feat.
