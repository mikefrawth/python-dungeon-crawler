# Combat hit resolution: bounded contest on raw Accuracy − Evasion

Three architectures were on the table for resolving whether an attack lands: (A) a single bounded curve applied to the raw delta between Accuracy and Evasion, (B) two independent bounded rolls (base hit% from Accuracy, separately reduced by Evasion), or (C) unbounded Accuracy/Evasion values compared via an opposed threshold check (D&D attack-roll-vs-AC style).

We chose (A): `hit_chance = bounded_curve(raw_accuracy - raw_evasion, cap, steepness)`, applied once, directly to raw attribute values — not to attribute values that have already been run through a separate curve. This reuses the same "symmetric bounded curve around baseline 0" shape already established for Damage Reduction, guarantees hit chance never truly hits 0% or 100%, and avoids stacking two curves in sequence (which would double-dampen investment).

Evasion is homed entirely on Agility (not split with Perception), for the same "one home per mechanic" simplicity already applied elsewhere in the attribute table.
