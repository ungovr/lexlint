<!-- Generated file. Do not edit this copy: edit the LexLint procedure source and regenerate. -->

### Client setup

The tools are identical in every client. Registering the server, updating the
bundle, and persisting the key are not. Use the entry for the client you are
running, and never offer a command from another entry.

**Claude Code**

- **Install**
  `claude plugin marketplace add ungovr/lexlint && claude plugin install lexlint@lexlint`

  The bundle carries the four skills and this server already configured.
- **Key** `/lexlint:lexlint-key`, which persists it to the `env` block of the
  user settings file, which is `$CLAUDE_CONFIG_DIR/settings.json` when
  `CLAUDE_CONFIG_DIR` is set and `~/.claude/settings.json` otherwise

  That skill hands over the sign-in link, checks the key, and writes it into
  the user settings file as a top-level `{"env": {"UNGOVR_API_KEY": "..."}}`,
  merged into the existing JSON with every other key kept, then runs
  `chmod 600` on the file. Ask before choosing the file:
  `echo "${CLAUDE_CONFIG_DIR:+set}"` prints `set` or an empty line, and with
  the variable set a key written to `~/.claude/settings.json` is saved in a
  file this client never reads. The user file and no other scope: never
  `.claude/settings.json`, never `.claude/settings.local.json` and never
  `.env`. `.claude/settings.local.json` is gitignored, so it passes that test,
  and it is still the wrong place: Claude Code opens two connections to each
  server, and an `env` value from the project or the local settings file
  reaches the server on one of them and arrives empty on the other (measured
  on Claude Code 2.1.278). A shell profile reaches only a Claude Code started
  from a terminal opened after the line is in, and the Claude desktop app
  never reads one, not even after a full quit and reopen (measured
  2026-10-15).

- **Saved-key check**
  `grep -l UNGOVR_API_KEY "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json" ~/.claude/settings.json .claude/settings.json .claude/settings.local.json ~/.zshrc ~/.bashrc ~/.bash_profile ~/.profile ~/.config/fish/config.fish 2>/dev/null`

  For "When the preflight says there is no key" (`references/no-key.md`),
  which has the rules: file names only, never a value. The first path is the
  user settings file: the one under `CLAUDE_CONFIG_DIR` when that variable is
  set, and `~/.claude/settings.json` otherwise.
  `echo "${CLAUDE_CONFIG_DIR:+set}"` says which, printing `set` or an empty
  line. When it is not set the first two paths are one file, which is then
  listed twice.

  - The name is in the user settings file. A key is saved where this client
    reads it, and it still did not reach the server. Work down the causes
    listed below, in order.
  - The name is in `~/.claude/settings.json`, while `CLAUDE_CONFIG_DIR` is
    set. A key is saved in a settings file this client does not read. With
    that variable set, the user settings file is the one under it. The
    developer moves the `env` entry into `$CLAUDE_CONFIG_DIR/settings.json`
    themselves, then restarts. It is their secret, and moving it means reading
    it.
  - The name is in `.claude/settings.json` or `.claude/settings.local.json`,
    and not the user settings file. A key is saved at project or local scope.
    Claude Code opens two connections to each server, and an `env` value from
    either file reaches the server on one of them and arrives empty on the
    other (measured on Claude Code 2.1.278). The developer moves the `env`
    entry into the user settings file themselves, takes it out of the project
    file, then restarts.
  - The name is in a shell profile, and no settings file. A key is saved
    there, and this client was not started from a shell that read that file. A
    terminal reads its profile only when it opens, and the Claude desktop app
    never reads one, not even after a full quit and reopen (measured
    2026-10-15). The developer runs `/lexlint:lexlint-key` with the key, which
    saves it where every start of Claude Code reads it, the desktop app
    included, then restarts. A developer who starts Claude Code from a
    terminal can instead open a new terminal and start it from there.
  - The name is in none of them. There really is no key on this machine. Run
    the setup flow in `SKILL.md`.

  When it is the user settings file, the causes, most likely first:

  1. The session was not restarted as a new process. A `/clear`, or a
     conversation resumed inside the same process, re-reads nothing: quit the
     client and start it again.
  2. The settings file no longer parses as JSON, and an unparseable settings
     file is ignored whole, so every setting in it is gone and not only this
     one.
     `python3 -m json.tool "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json" >/dev/null && echo ok`
     answers without printing any of it: `ok`, or the line and column of the
     first error.
  3. The `env` block is nested in the wrong place. It is a top-level key of
     the file, as `{"env": {"UNGOVR_API_KEY": "..."}}`, and the same block one
     level down, inside `permissions` for instance, is read by nothing.
  4. This surface does not expand a plugin's header variables. Cowork, the
     Claude desktop app's agentic mode, refuses every variable that is not one
     of its own, so a plugin server there is sent no key wherever it is saved.
     Claude Code in the desktop app is a different surface and reads the user
     settings file. Run LexLint from Claude Code instead.
  5. This Claude Code build sends a plugin's header variable empty whatever it
     holds, which some builds have done. Update Claude Code, then restart.

  When none of those is it, one fix has been observed to work where nothing
  else did, and it is the developer's to do: they export `UNGOVR_API_KEY` in
  the shell they start the client from, copying the value themselves, and
  start the client from that shell.
- **Update** `claude plugin update lexlint@lexlint`

  `--scope` defaults to `user`, so a project that installed LexLint locally
  needs `claude plugin update lexlint@lexlint --scope local` run from that
  project's directory or it keeps loading the old copy.
- **Restart** after a key is saved or the bundle is updated: restart Claude
  Code.
- **Skills** `/lexlint:lexlint`, `/lexlint:lexlint-key`,
  `/lexlint:lexlint-upload` and `/lexlint:lexlint-feedback`, the only names
  Claude Code lists (measured on Claude Code 2.1.309, 2026-10-23, off the init
  message of one headless run). A typed short name can still reach its skill:
  `/lexlint-key` loaded the key skill in a second measured run. Use the listed
  names; a developer can also just ask, and the skill whose description fits
  loads.
- **Sign-in** when a tool answers that sign-in is needed, run `/mcp`, choose
  lexlint, and sign in.
- **One run's scope** `/lexlint:lexlint <path>` passes the path with the
  request: the manifest when it ends `.yml` or `.yaml`, the scope for one run
  otherwise, as step 1 says.
- **Skill directory** the Skill tool prints
  `Base directory for this skill: <path>` when the skill loads; that path is
  the `SKILL_DIR` step 4 sets before it runs `scripts/merge.py`.

**Codex**

- **Install** `codex mcp add lexlint --url https://mcp.lexlint.io/mcp`

  That registers the transport and not the key: `mcp add` has no flag for a
  custom header, and `--bearer-token-env-var` sends `Authorization`, which
  this server does not read. Add two lines by hand to the
  `[mcp_servers.lexlint]` entry the command just wrote in
  `~/.codex/config.toml`: `http_headers = { "X-API-Key" = "" }` and
  `env_http_headers = { "X-API-Key" = "UNGOVR_API_KEY" }`. The first is what
  lets the server answer before there is a key: with the variable unset Codex
  sends no header at all, this server reads no header as a sign-in it cannot
  offer, and no tools appear (measured on Codex 0.155, 2026-09-20). An empty
  header is read as no key, the tools appear, and the variable's value
  replaces it the moment it is set.
- **Key** persisted to `UNGOVR_API_KEY` in the environment Codex starts from,
  named by the `env_http_headers` line in `~/.codex/config.toml`

  The value in that line is the variable's NAME, not the key itself. Codex
  reads it at connect time, so a key exported into a running session is read
  by nothing, and so is a key saved anywhere but the shell profile Codex
  starts from: a private file or a note of the agent's own is a stranded key,
  which is how run 17 of the first-run funnel ended.

- **Saved-key check**
  `grep -l UNGOVR_API_KEY ~/.codex/config.toml ~/.zshrc ~/.bashrc ~/.bash_profile ~/.profile ~/.config/fish/config.fish 2>/dev/null`

  For "When the preflight says there is no key" (`references/no-key.md`),
  which has the rules: file names only, never a value. `~/.codex/config.toml`
  is in the list for the opposite reason to the rest: it is supposed to name
  the variable, and it never holds the key.

  - The name is in a shell profile and `~/.codex/config.toml`. A key is saved
    in the profile and the header is mapped to it, and the Codex session was
    not started from a shell that read that profile. Open a new terminal and
    start Codex from it.
  - The name is in a shell profile, and not `~/.codex/config.toml`. A key is
    saved, and Codex sends no `X-API-Key` header at all, because the
    `env_http_headers` line that names the variable is missing. Add the line
    the Install entry above gives to the `[mcp_servers.lexlint]` entry, then
    start Codex again.
  - The name is in no shell profile. There really is no key on this machine.
    `~/.codex/config.toml` on its own is the header mapping, which names the
    variable and is never a key. Run the setup flow in `SKILL.md`.
- **Update** not available here.

  There is no installed client to update: the tools are served remotely and
  are always current. What goes stale is this procedure itself. Re-read it
  from the current bundle at https://github.com/ungovr/lexlint
- **Restart** after a key is saved or the bundle is updated: restart the Codex
  session.

**Codex in the browser**

- **Install** not available here.

  The Codex web app at https://chatgpt.com/codex is the one Codex surface with
  nowhere to put this: it exposes no server configuration, so there is no
  version of these steps that can be done there. Set LexLint up in the Codex
  CLI, the IDE extension, or the desktop app, which share one
  `~/.codex/config.toml`. That is a statement about this one surface and not
  about ChatGPT's own connector settings, which are a different product
  LexLint has not tested.
- **Key** not available here.

  There is nowhere on this surface to put a header or an environment variable.
  The no-account trial key does not help here either, because it still has to
  land somewhere the connection reads it from; say that plainly rather than
  walking a developer through steps their surface cannot take.
- **Update** not available here.

  Nothing is installed there to update.

**Cowork, the Claude desktop app's agentic mode**

- **Install** not available here.

  Cowork, the Claude desktop app's agentic mode, is the one Claude surface the
  plugin cannot be keyed on, and Claude Code inside the desktop app is not it:
  the bundle's server entry sends `X-API-Key: ${UNGOVR_API_KEY:-}`, and this
  surface never expands a plugin's header variable, whatever the value is
  saved in, and shows nothing when it declines to (upstream report
  anthropics/claude-code#94395, open on 2026-09-19). What it sends in the
  header's place is unmeasured, so there is no version of these steps LexLint
  can stand behind here. Set LexLint up in Claude Code in a terminal or an
  IDE, which is the Claude Code entry, or paste the first-run line into a
  Claude Code session there; the document is https://lexlint.io/first-run
  either way.
- **Key** not available here.

  There is nowhere on this surface a key can reach the plugin from: the header
  variable is not expanded here, so a key saved in the user settings file, the
  shell profile or the environment is sent to the server by nothing. The
  no-account trial key does not help either, because it still has to land
  somewhere the connection reads it from; say that plainly rather than walking
  a developer through steps their surface cannot take, and send them to Claude
  Code in a terminal or an IDE.
- **Update** not available here.

  Nothing LexLint can key is installed here to update. Update from a terminal,
  as the Claude Code entry says.

**Any other MCP client**

- **Install** `https://mcp.lexlint.io/mcp`

  Any client that speaks streamable HTTP works. Register that endpoint with an
  `X-API-Key` header carrying the key; an `Authorization` header is ignored.
  The server is stateless and holds no session of its own, so nothing has to
  be kept between calls.
- **Key** persisted to `UNGOVR_API_KEY` in the environment the client starts
  from

  Some clients expand `${UNGOVR_API_KEY}` inside a config file and some do
  not. If yours does not, the key is written literally and the file is then
  the secret it contains.

- **Saved-key check**
  `grep -l UNGOVR_API_KEY ~/.zshrc ~/.bashrc ~/.bash_profile ~/.profile ~/.config/fish/config.fish 2>/dev/null`

  For "When the preflight says there is no key" (`references/no-key.md`),
  which has the rules: file names only, never a value. If you know the file
  your client keeps its MCP servers in, add its path to the command: a header
  written there, literally or as a variable, is part of the answer too.

  - The name is in a shell profile. A key is saved there, and this client was
    not started from a shell that read that file, or its server entry does not
    pass the variable on as `X-API-Key`. Open a new terminal and start the
    client from it. If the key still does not arrive, the server entry is what
    to read next.
  - The name is in none of them. There really is no key on this machine. Run
    the setup flow in `SKILL.md`.
- **Update** not available here.

  There is no installed client to update: the tools are served remotely and
  are always current. What goes stale is this procedure itself. Re-read it
  from the current bundle at https://github.com/ungovr/lexlint
- **Restart** after a key is saved or the bundle is updated: restart the
  session.
