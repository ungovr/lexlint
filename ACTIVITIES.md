---
version: 1
registry: https://lexlint.io/activities/v1
date: 2026-10-15
declared_by: the LexLint maintainers
components:
  - purl: pkg:github/ungovr/lexlint
    shape: library
    aggregate: complete
    activities: []
    talks_to:
      - host: mcp.lexlint.io
        party: LexLint
        jurisdiction: us
        required: true
        why: Every lint, law lookup and upload runs on the LexLint server at this host.
---

# What this plugin does, by feature

This plugin is four skills, two schemas and a server address. It runs
no code of its own, so it performs none of the activities listed at
https://lexlint.io/activities and declares none. It is published as a package, so it distributes
software, which a validator adds from the package URL above.

**The lint.** The skill reads a repository to inform the questions it asks,
and sends the developer's answers (activities, jurisdictions, domains) to the
LexLint server at mcp.lexlint.io, which returns the findings. Nothing is sent
until the developer has answered. The server is the one party every run talks
to, so its jurisdiction is in every run that uses the plugin.

**The upload.** The `lexlint-upload` skill sends a completed run to the
developer's LexLint portal, after showing exactly what leaves the repository.
