# Equip requirements are a continuously-evaluated hard gate, not a one-time check

Weapon/armor minimum-attribute requirements mirror skill gating: a hard floor, not a soft performance penalty. The open question was *when* that gate is checked — most games only check it at the moment of equipping (a snapshot), which is the obvious default.

We chose otherwise: equippability is a **live, computed property** re-evaluated from current attributes, not a flag set once at equip time. Attributes can go negative via curses, drains, and debuffs (per the core attribute design), so a snapshot check would let a character keep using gear they no longer qualify for after being cursed mid-fight — quietly undermining the point of the gate being "hard." A future reader seeing gear silently become unusable (or get force-unequipped) after a stat drain should know this was deliberate, not a bug: the gate is meant to track current state, always.
