<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

## The severity model

| Severity | Meaning |
|----------|---------|
| `warn` | Something to act on. Three different things arrive this way, and `kind` tells them apart: a live obligation applies to the declared profile (`obligation`); a jurisdiction-wide crawl-law attribute LexLint flags as worth acting on, such as an unsettled or restrictive posture (`posture`); or LexLint lacks current data for a declared jurisdiction (`coverage`). |
| `info` | Context, not a live duty on you. Three different things arrive this way, and `kind` tells them apart: an instrument LexLint cannot say is in force today (`pending`); a jurisdiction-wide statement of how the local law treats crawling as a whole (`posture`), which cites nothing and binds nobody on its own; and a note about what was not reported (`coverage`), such as instruments that exist but no longer bind. With `public_sector` declared, a duty that is your customer's or is owed elsewhere arrives here too: as a `customer_duty` finding, or as an instrument finding whose `owed` is `customer` or `elsewhere` (step 5). With `derived: true` in the profile, every `derived` finding arrives here as well. |

LexLint never reports an `error` severity. A lint cannot be sure an activity is
prohibited rather than merely regulated, and it will not assert unlawfulness on
the strength of a matched instrument. Treat a live `warn` obligation as the
thing to act on.

Every finding carries `as_of_date` and `stale`, because laws change faster than
law libraries do. A stale finding is still worth acting on; it just may lag the law.

Findings also carry a `kind`:

| `kind` | Meaning |
|--------|---------|
| `obligation` | A specific instrument binds the declared profile. With `public_sector` or `regulated_sector` declared, `owed` says whether it binds you. |
| `coverage` | A note about what was not reported, never a pass: LexLint could not read something, holds no data, cannot map what it holds to a declared activity, or holds an instrument that no longer binds. |
| `posture` | How this jurisdiction's law treats crawling as a whole: whether browsewrap binds, what weight robots.txt carries, whether a public page is outside computer-crime law. Jurisdiction-wide attributes rather than instruments, so they bind nobody on their own and cite nothing. They appear only when `crawls_web` is declared. |
| `pending` | An instrument LexLint cannot say is in force today: proposed, not yet in force (from a later day, or from a date not yet set), blocked by a court, or carrying a status LexLint has no policy for. An injunction can be lifted, and a start date missing from the record does not mean the law is not in force, so treat this as a duty to watch, not one to ignore. |
| `customer_duty` | With `public_sector` or `regulated_sector` declared: a duty your customer owes, a public body or a financial institution, and meets through your software. It follows the instrument finding it was split from, names it in `instrument_id`, and goes to the `product` lane. |
| `derived` | With `derived: true` in the profile: one finding per record an app holds to meet the deadlines the matched laws set. It is about the run rather than one jurisdiction, so `jurisdiction` and `citation` are null, and it is always `info`. `capability` names the record, `derived_from` lists each law it rests on, and `stated_by` and `inferred_from` count the laws that name the record themselves and the laws it is inferred from. It goes to the `code` lane (step 5). A derived finding is LexLint's inference, not a law's statement: a record an app holds in order to meet a deadline the listed laws set. No law names the record unless the finding marks it as stated. |

A `posture` finding whose value is `unsettled` is a warning, not a pass. "The
law here is silent, untested, or in flux" is among the most actionable things a
crawler author can be told.
