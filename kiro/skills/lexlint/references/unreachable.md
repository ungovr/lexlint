<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

### When you cannot reach the server

**Every LexLint finding comes from a payload the server sent you in this
session. When no payload arrived, there is no lint, and there is nothing to
report.**

**The line is whether the server answered.** A connection refused, a host that
does not resolve, a request that times out, a sandbox that denies egress, a
tool call that comes back with no response at all, a 5xx: nothing answered, so
stop at that point. Say which call failed and quote the error you actually got,
and **report no findings at all**. No table, no severities, no instrument
names, no coverage section, no list of law that is "likely" to apply.

**A refusal is an answer, and it is not this case.** A slug `set_profile` sends
back as malformed, a key the server rejects, a spent quota, a declaration
returned with the allowed values: the server read what you sent and told you
what is wrong with it. Every one of those is recoverable, each has its own
instruction elsewhere in this document, and stopping on one turns a typo into a
dead end.

**Your own client declining to make a call is a third case, and it is the one
somebody can fix from this session.** A tool call the developer did not
approve, a shell you were not granted, a command your client would not run: the
request never left the machine, so nothing about the server is known, and
reporting it as an outage sends the developer to look at a host that is fine.
Say plainly that your client would not make the call and **not** that the
server was down, print the exact call or command, and offer the developer the
one thing that actually moves it: approve it and you retry. A host that does
not resolve cannot be fixed from here. A permission prompt can. Do not work
around the refusal, do not reach for a different tool, and do not ask the
developer to run the call by hand: what happens next is theirs to decide, not
something to route through you. Name no setting, rule or flag that would let
you make the call yourself: what the client allows is the developer's to
change, unprompted, and offering it as an option is coaching. This covers the shell
routes for an oversized response in step 3 of the loop as much as it covers a
`run_lint` or an `upload_lint_run` the client would not call.

**Route 3 in step 3 is the one exception, and it is not an exception to the
rule so much as a case the rule does not describe.** When a shell is refused
and the response was oversized, splitting the declaration across several
`run_lint` calls is not reaching around the refusal: it is the route that
step 3 names for exactly that state, it uses the tools already in front of
you, and it produces the same lint. Take it, and say in the report that you
did and why. What stays forbidden is reaching for a shell the developer
declined, by another name or another host.

Name the declaration you were about to send, so the developer can re-run once
the network is there. **Give it as a plain list, one value per line, and never
as a table.** A bordered table with an evidence column is the shape a developer
reads as a result, whatever the caption above it says, and this document asks
for exactly that table on the path where the lint did run, so the two are one
glance apart. **If the preflight is what failed, you do not have one
yet: say that instead of guessing one to fill the line.** `check_access` runs
before you have read the repository, and a declaration invented to round out a
failure report is the same defect as an invented finding, one field over.

**Do not fill the gap.** Not from your own memory of what these laws say, not
from training data, not from a web search, not from any other copy of the law
library you find on disk. Asked for a lint it cannot run, a model will reach for
whichever route still produces an answer, and every one of those routes returns
something that looks exactly like a lint result and is not one: plausible
instrument names, plausible severities, nothing behind any of them. A developer
reading the report cannot tell the two apart, which is why this is a rule and
not a matter of judgment.

This is the sibling of "a truncated tool result is not the run" in step 3 of
the loop. **A call that did not return is not the run either**, and neither one
is visible in the report unless you put it there.

Name what it looks like from where you are sitting, because the developer can
act on the difference: a refusal that names LexLint is ours to fix, a network
your client is not allowed to use is theirs, and a call your own client would
not make is the one paragraph above, where there is something to offer them.
Then stop.
