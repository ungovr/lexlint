<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

## Two tools that make this cheaper, and neither of them required

Everything below works with no shell at all. Two ordinary tools make it
cheaper, and it is worth knowing which you have before you need them:

| Tool | What it saves | Where |
|---|---|---|
| `jq` | keeps a `run_lint` response out of your context entirely | step 3 |
| `python3` with PyYAML | writes the merged `lint:` block without it passing through your output | step 4 |

The upload needs neither: it is one tool call carrying the declaration, and
the server rebuilds the findings, so nothing of size ever passes through your
output on the way out.

**Check once, lazily, and remember the answer.** The first time you want one of
them, ask in a single command rather than probing per call:

```bash
command -v jq python3
python3 -c 'import yaml'
```

**PyYAML is the thing being asked about in the second line, not `python3`.**
It is not in the standard library, so an interpreter on the PATH is not an
answer on its own, and the second line exits non-zero on the machines where
they part. Nothing else in this procedure needs it.

**If the command itself cannot run, you have no shell**, which is a different
situation from a missing tool and is answered in step 3 by a route that needs
neither.

**When one is missing, the flows still work.** Every place these appear names
the route to take without them, and none of those routes is a degraded lint:
they cost more tokens or more upstream requests, never accuracy. Take the route
you have and say which one you took.

### Say so once, and only when it actually cost something

A developer who would never notice the difference should never be told about
it. So **do not report a missing tool because it is missing.** Report it in the
run where its absence had a measurable cost, with the number from that run, and
then not again:

- The response went past the tool-result limit and you had no `jq`, so you
  split the declaration across calls and spent three upstream requests per
  call.
- You wrote the manifest and had no `python3` with PyYAML, so the whole
  `lint:` block came out through your own output.

One line, in the report, phrased as the fact it is:

    This run's response was 147 KB and had to come back through my own
    context. `jq` would have kept it out of it. Not required, and nothing
    here failed.

**Once per session, never repeated**, on the same reasoning as the
newer-version notice: it is a footnote to their lint, not the reason they came.
Never make it a recommendation to act on before the findings, never list tools
they already have, and never say a run was degraded, because it was not.

**Two cases get no line at all.** A headless or CI session, where nobody is
there to install anything. And a client with no shell, where installing `jq`
changes nothing, because an agent that cannot run a command cannot run that
one either: telling someone to install a tool their client cannot invoke is
noise wearing the clothes of advice.
