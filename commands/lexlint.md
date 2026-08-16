---
description: Lint this app against the AI and scraping law of the jurisdictions it operates in
---

Run the LexLint loop against this repository.

1. Read `lexlint.yml` at the repo root, or the path given in `$ARGUMENTS` if
   one was provided. If no manifest exists, create one by asking what the app
   does and where it will operate. Never infer the declaration from the code.
2. Resolve any domains named in the manifest with `resolve_domain_jurisdiction`.
3. Call `lint_app_profile` with the declared activities and jurisdictions.
4. Merge the findings into the manifest, carrying `state`, `where`, and `note`
   across for every finding id that persists, and moving vanished
   acknowledgments to `lint.vanished` rather than deleting them.
5. Report the findings, map each one onto the code it implicates, and offer to
   fix what is cheap to fix now.

The passing state is "no basic issues found". Never restate it as clearance or
certification, and never report a jurisdiction with no data as a pass.

The full procedure, including the severity model and the honesty rules, is in
the `lexlint` skill.
