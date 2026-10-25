---
name: miyo-search
description: Semantic (meaning-based) search over the user's Obsidian vault via the local Miyo app. For any vault-search intent, use it when builtin grep search is too slow or doesn't surface enough relevant notes, or when the user explicitly asks for Miyo search. Needs the Miyo desktop app installed and running.
metadata:
  copilot-enabled-agents: opencode, claude, codex
  copilot-builtin-version: "5"
---

# Miyo vault search

Search the user's indexed Obsidian vault through Miyo, the user's own companion
app for semantic search over their notes. It finds relevant notes by meaning
(not just filename). Searches go only to the user's own Miyo service — the local
app by default, or the remote Miyo server they configured in settings — never a
third-party API, and no API key.

When to use it: for any vault-search intent, reach for Miyo when your builtin
`grep` search is too slow or doesn't surface enough relevant notes, or when
the user explicitly asks for Miyo search.

## How to run

Find the absolute path to this SKILL.md file on disk, then run the script next
to it that matches the operating system. Run it as a shell command with your shell command tool (for example
`Bash` in Claude Code, `shell` in OpenCode, `exec_command` in Codex). The command
is shell syntax, not JavaScript or TypeScript: never pass it as the code of a
code-execution tool.
No extra runtime is needed — `sh` (macOS/Linux) and `cmd`/PowerShell (Windows)
are always present.

On macOS or Linux:

```bash
sh "/absolute/path/to/this/skill/directory/miyo-search.sh" "<the user's question>"
```

On Windows, run the `.cmd` wrapper. In PowerShell you must prefix it with the
call operator `&` (PowerShell treats a quoted path on its own as a string and
won't run it); from cmd, run the quoted path without the `&`:

```powershell
& "/absolute/path/to/this/skill/directory/miyo-search.cmd" "<the user's question>"
```

Pass the user's full question as the query.

Both print the result to stdout.

The script locates the Miyo binary itself — you do not need to know where Miyo
is installed or which shell you are in. Run the script as your single search
step; do not fall back to other search tools unless it reports that Miyo is
unavailable. Read the JSON straight from stdout; do not pipe it through other
tools (no `jq`, no `|`).

Search scope comes from Copilot settings. **Current vault** applies Miyo's exact
folder boundary for the active vault and any other Miyo folders ticked in Copilot
settings, including from Project chats.
**Unrestricted** searches every folder registered with Miyo.

## Reading the results

The script prints `{ "results": [ { "path": ..., "content": ... } ], "count": N }`.
Cite the `path` of any note you use so the user can open it.

## If it reports a problem

The script exits with a clear message when Miyo can't be used:

- **Not installed** (CLI not found): the Miyo desktop app isn't installed on
  this machine. Tell the user to install and open Miyo, then try again. Do not
  retry in a loop.
- **Not running** (search failed / can't reach the service): the app is
  installed but not running. Tell the user to open Miyo, then continue without
  vault search if they can't.
