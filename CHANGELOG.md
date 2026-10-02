# Changelog

Each release of the LexLint plugin bundle since 1.40.0, newest first. Update
the plugin in your client to get the newest. In Claude Code that is
`claude plugin update lexlint@lexlint`, then restart your session. The bundle
is published at https://github.com/ungovr/lexlint

## 1.46.2 (2026-10-01)

- LexLint's body of law is now called the law library wherever you and your
  agent read it: the tool and schema descriptions, the text the server
  returns, the written procedure, the plugin's commands and README. It used
  to be called the corpus. Only the word changes. No key, field name, value
  or step is different, and `corpus_built_at` keeps its name, so a client
  that reads it is not affected. The run block the procedure prints labels
  its third line `law library`, where it read `corpus`.

## 1.46.1 (2026-09-30)

- The bundle's descriptions now name content-moderation law among the topics the lint
  reads: the liability of a service for what its users post,
  notice-and-takedown, and moderation transparency. A profile that declares
  `operates_social_platform` meets it. Nothing you declare or call changes.

## 1.46.0 (2026-09-30)

- A run now opens in the shape https://lexlint.io and
  https://developer.lexlint.io show a run in, printed straight after
  `run_lint` and before anything is merged:
  what was declared, where the app operates, by flag and name, and the date
  of the corpus; then a block for the lead finding in each declared place and
  for every finding for counsel, each with its place, the law, when it binds,
  the duty in full, the date it was read against its source and the address
  of its law page; then a count of what the block shows and of the rest.

## 1.45.1 (2026-09-29)

- The bundle now carries this changelog, CHANGELOG.md, with one entry per
  release, newest first. Read it in the bundle or at
  https://developer.lexlint.io/changelog on the developer site.
- The procedure's pointer to LexLint's law pages, which had been a bare domain
  name, is now the full address https://lexlint.io/law

## 1.45.0 (2026-09-29)

- A profile can now declare a public-sector role, `profile.public_sector`:
  `body` for software a public body runs, `supplier` for software sold to or
  run for public bodies, both, or `none`. `set_profile`, `run_lint` and
  `upload_lint_run` all accept it.
- With the role declared, each requirement is routed by who owes it. Every
  instrument finding carries `owed`. A duty that binds you stays in the
  finding's `requires`. A duty that binds only bodies you are not is reported
  as information, with its lines kept in `requires_elsewhere`.
- A duty that your public-sector customer owes and meets through your software
  arrives as its own `customer_duty` finding, placed right after the
  instrument finding it was split from.
- A caller that does not declare a role gets exactly the output it got before.

## 1.44.0 (2026-09-29)

- A state or other sub-national place now reads with its country code first, as
  "US-California", where it used to read "California (US)". The code, a hyphen
  and the name take about as much room as a flag emoji and its space, so a
  Place column lines up in both command-line clients. No field is added or
  renamed.
- The procedure's flag rule and its examples use the new form, and the plugin
  schema's description names both.

## 1.43.1 (2026-09-29)

- The copyright line in the bundle's LICENSE file now names the holder as
  UnGovr, with no company-type suffix. No tool, schema or procedure behaviour
  changes.

## 1.43.0 (2026-09-28)

- Every `run_lint` finding and every `set_profile` coverage row for a country,
  the European Union or the United Nations now also carries `jurisdiction_flag`,
  the flag emoji for that place. A state or a city carries none and never
  borrows its country's. The field is declared in the plugin's schema, and a
  merged manifest keeps it.
- The procedure prints the flag, then a space, before the place name in every
  table and list, and the keyless first-run preview table prints it too.

## 1.42.0 (2026-09-26)

- Every `run_lint` instrument finding, and every instrument `get_law` returns,
  now carries `in_force`, which says when the law binds. It is declared in the
  plugin's schema, a merged manifest keeps it, and `lifecycle` stays for
  existing clients.
- The procedure prints each finding's in-force words, `in_force.words`,
  wherever it says when a law binds.

## 1.41.1 (2026-09-26)

- The aggregation topic is labelled "Reuse law", not "News aggregation law".

## 1.41.0 (2026-09-24)

- The procedure names the communications topic and the three facts it adds.
- The `automated_outreach` activity no longer borrows `deploys_chatbot`'s
  categories. It now reaches the communications topic's rows, so a profile that
  declares it gets those rows in place of chatbot-disclosure rows, and its
  findings change.

## 1.40.3 (2026-09-23)

- `/lexlint-key` checks a key with `check_access`.
- LexLint no longer says your key is forwarded to a separate data service.
  The LexLint server checks it itself. Where `get_law` holds no data for a
  jurisdiction, its note now points at https://lexlint.io/law for coverage.

## 1.40.2 (2026-09-21)

- Step 1 no longer leaves a row marked ask when the evidence in hand settles
  it, and it asks an open ask row again before it sets the profile, so a
  one-word yes can no longer silently drop that row.
- Step 1 resolves the app's domains before it shows the declaration table.

## 1.40.1 (2026-09-21)

- Step 1 proposes the declaration from the code, and you confirm it, on every
  client.

## 1.40.0 (2026-09-21)

- A compact upload's `app_scope` reaches the portal as the scope object its
  schema requires.
