# Skills and feats resolve around exactly one attribute — no hybrid combine modes

ADR-0006 established that feats reuse skills' combine-mode vocabulary (`sum_independent`, `chance_and_magnitude`) for effects that span two attributes, and ADR-0007's proc mechanism split a debuff-proc ability's "chance" and "magnitude" across two different attributes. Skills additionally had an "either/or" shape (usable off whichever of two attributes is higher).

We reversed this: **every skill and feat has exactly one governing attribute**, full stop — for both gating (skills) and scaling. There is no `gate_both`, `sum_independent`, `chance_and_magnitude`, or either/or anymore. One attribute per ability, everywhere, no exceptions.

Consequences:

- The "reward spreading investment across two attributes" mechanic (summing two concave curves beats dumping into one) no longer exists. Full point efficiency now always comes from stacking a single attribute.
- The magic-swordsman example that originally motivated `sum_independent` (weapon damage off a physical attribute + spell damage off a magic attribute, summed) is no longer a valid ability shape — an ability like that must now pick one attribute to govern its entire output.
- Debuff-proc abilities (ADR-0007) now read **one** attribute for both the proc chance and the debuff's magnitude/duration, rather than splitting chance (Perception, by convention) from magnitude. ADR-0007's core conclusion — procs are ability-level, not a universal stat, and gated behind a landed hit — is unchanged; only the two-attribute split is cut.
- This supersedes the combine-mode portion of ADR-0006 (the "feats reuse skills' hybrid vocabulary minus `gate_both`" claim). ADR-0006's other conclusion — feats can scale off an attribute despite having no attribute-minimum gate — still stands.
