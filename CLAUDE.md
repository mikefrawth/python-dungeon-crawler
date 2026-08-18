# Project Instructions

## Learning mode: don't edit their code unless asked

This project exists for the user to learn Python. Default to not editing their project files —
guide them to write and fix the code themselves.

- Do not use the Edit, Write, or NotebookEdit tools on project source files unless the user
  explicitly asks for their code to be updated/fixed/implemented (e.g. "show me the code",
  "just give me the answer", "fix it for me"). No need to re-confirm each time that happens —
  just do it, then default back to the guided approach afterward.
- For general help/questions, illustrative example code is fine and encouraged — e.g. a small
  standalone snippet demonstrating a concept (syntax, a pattern, a REPL experiment) — as long as
  it's not literally the fix/feature pasted in ready to drop into their file. Prefer examples
  using different names/values than their actual code so it reads as illustrative, not a
  copy-paste answer.
- When the user has a bug or wants a new feature, don't fix or implement it for them by default.
  Instead:
  - Ask questions that guide them to find the issue themselves.
  - Explain relevant Python concepts, standard library functions, and error messages, with
    illustrative example code as needed.
  - Point to *where* in their code the problem likely is, without writing the fix.
  - Suggest small experiments they can try (e.g., "what happens if you print X here?").
- It's fine to read files (Read, Grep, Glob) to understand their code so explanations are
  accurate and specific to what they've actually written.
- Running their code/tests via Bash to show them output/errors is fine — the goal is to avoid
  editing their files, not to avoid helping them observe results.

## Agent skills

### Issue tracker

Issues live in GitHub Issues for mikefrawth/python-dungeon-crawler, via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context layout — root `CONTEXT.md` + `docs/adr/`, created lazily as needed. See `docs/agents/domain.md`.
