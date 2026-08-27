---
description: Lint this app against the AI, scraping, and privacy law of the jurisdictions it operates in
---

Run the LexLint loop against this repository.

1. Run `check_access` first and show the result. A missing or spent key needs
   handling before any question is worth asking. The same response says which
   models this procedure is tested against: if your own is not one of them, show
   `model_notice` and let the developer decide whether to continue. It is an
   advisory, so the lint runs either way.
2. Read `lexlint.yml` at the repo root, or the path given in `$ARGUMENTS` if
   one was provided. If no manifest exists, create one by asking what the app
   does and where it will operate, quoting every jurisdiction slug. Never
   infer the declaration from the code.
3. Resolve any domains named in the manifest with `resolve_domain_jurisdiction`.
4. Call `run_lint` with the declared activities and jurisdictions.
5. Merge the findings into the manifest, carrying `state`, `where`, `note` and
   `handled_by` across for every finding id that persists, carrying
   `lint.work_items` across untouched, and moving vanished acknowledgments to
   `lint.vanished` rather than deleting them.
6. Triage the findings into `lint.work_items`, one per thing to actually do,
   and get the developer's approval before touching a file.
7. Work the plan: ship the code diffs, draft the doc artifacts into the repo,
   and route what belongs to counsel.

The passing state is "no basic issues found". Never restate it as clearance or
certification, and never report a jurisdiction with no data as a pass.

The full procedure, including the preflight, the triage lanes, the severity
model, and the reporting rules, is in the `lexlint` skill.
