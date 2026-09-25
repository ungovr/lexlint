---
description: Lint this app against the AI, scraping, privacy, and cybersecurity law of the jurisdictions it operates in, drawn from LexLint's AI, scraping, privacy, cybersecurity, communications, age-gating, and news-aggregation law corpus
---

Run the LexLint loop against this repository.

1. Run `check_access` first and show the result. A missing or spent key needs
   handling before any question is worth asking. When `key_present` is false,
   do not offer a route to a key yet: a key that is saved on this machine and
   did not reach the server reads exactly the same from here. Do what "When
   the preflight says there is no key" in the `lexlint` skill says first,
   which is one command that prints file names and never a value. If it finds
   a saved key, say where, say why it did not arrive, and do not mint another.
   Only when it finds nothing, read `setup.steps`: it names both routes to a
   key, the no-account trial (`claim_trial_key`, run only after the developer
   picks it, and never twice) and the account sign-in, and offer the trial
   first since it needs nothing from the developer but a yes. The same
   response says which models this procedure is
   tested against: if your own is not one of them, show `model_notice` and let
   the developer decide whether to continue. It is an advisory, so the lint
   runs either way.
2. Read `lexlint.yml` at the repo root. If no manifest exists, build a
   candidate declaration from the code, show it as a table (value, evidence,
   your call) and ask the developer to confirm or correct it, quoting every
   jurisdiction slug. Nothing unconfirmed is ever sent: the code is evidence
   for the proposal, never the declaration itself. Make the call where the
   definition decides it; an `ask` row the developer did not answer is asked
   again before the lint runs, never dropped.

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
4. Show the developer the two lists before you send them, with every value
   you are unsure of marked as such, and wait for their answer. In a headless
   or CI session nobody can answer: send the lists as you read them, and name
   the values you were unsure of in the report. Then call `run_lint` with the
   declared activities and jurisdictions.
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
