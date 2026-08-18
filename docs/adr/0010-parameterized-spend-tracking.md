# Attribute spend-tracking is one parameterized mechanism, not separate ones per use case

ADR-0009 established Investment Points as a single mechanism spanning creation and leveling. Left open: whether player creation needs a hard per-attribute ceiling on top of the shared budget, and whether NPC/monster generation and leveling get their own implementations or reuse creation's.

We decided player creation uses **both** a shared starting budget (Investment Points distributed across the six attributes) **and** a hard per-attribute ceiling of **10** — no single attribute may exceed 10 at creation even with budget left unspent. Crossing either limit is rejected outright (an error), never silently clamped.

The spend-tracking mechanism itself — points spent computed from current raw values relative to baseline (no separate counter to keep in sync), a spend operation validated against budget and cap, and an undo operation to give a point back — is built once and takes **budget and cap as parameters** rather than hardcoding the player-creation numbers (30-ish budget, cap 10 — exact budget still TBD per ADR-0009). This is what lets it double as an NPC/special-monster generator (higher budget/cap, or none at all) without a second implementation, and it's also what leveling reuses: same spend/undo/tracking shape, called against the existing 100 lifetime investment cap and a per-level budget increment instead of creation's one-time numbers.

Consequence: there is exactly one place that knows how to "track points spent against a limit, reject overspend, allow undo." Player creation, NPC/monster generation, and leveling are all callers that supply different `(budget, cap)` values — not three parallel systems to keep in sync.
