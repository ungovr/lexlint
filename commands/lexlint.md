---
description: Lint this app against the AI, scraping, privacy, and cybersecurity law of the jurisdictions it operates in, drawn from LexLint's AI, scraping, privacy, cybersecurity, age-gating, and news-aggregation law corpus
---

Run the LexLint loop against this repository.

1. Run `check_access` first and show the result. A missing or spent key needs
   handling before any question is worth asking. When `key_present` is false,
   read `setup.steps`: it names both routes to a key, the no-account trial
   (`claim_trial_key`, run only after the developer picks it) and the account
   sign-in, and offer the trial first since it needs nothing from the
   developer but a yes. The same response says which models this procedure is
   tested against: if your own is not one of them, show `model_notice` and let
   the developer decide whether to continue. It is an advisory, so the lint
   runs either way.
2. Read `lexlint.yml` at the repo root. If no manifest exists, create one by
   asking what the app does and where it will operate, quoting every
   jurisdiction slug. Never infer the declaration from the code.

   `$ARGUMENTS`, when given, is one path, and which of two things it means is
   read off the path itself: a `.yml` or `.yaml` file is the manifest to use
   instead of the repo-root one, and anything else is the **scope** for this
   run, narrowing which files you read to that subtree. Both at once is two
   arguments, manifest first. A path that is neither an existing file nor an
   existing directory is a typo worth stopping on, because the alternative is
   linting the whole repository while reporting a scope.

   A scope from the command is not written to the manifest. Say in the report
   that it came from the command, and say what it was.
3. Resolve any domains named in the manifest with `resolve_domain_jurisdiction`.
4. Call `run_lint` with the declared activities and jurisdictions.
5. Merge the findings into the manifest, carrying `state`, `where`, `note` and
   `handled_by` across for every finding id that persists, carrying
   `lint.work_items` across untouched, and moving vanished acknowledgments to
   `lint.vanished` rather than deleting them.
6. Triage the findings into `lint.work_items`, one per thing to actually do,
   and get the developer's approval before touching a file.
7. Work the plan: ship the code diffs, draft the doc artifacts into the repo,
   and route what belongs to counsel with a brief the developer can hand to a
   lawyer.

The passing state is "no basic issues found". Never restate it as clearance or
certification, and never report a jurisdiction with no data as a pass.

The full procedure, including the preflight, the triage lanes, the severity
model, and the reporting rules, is in the `lexlint` skill.
