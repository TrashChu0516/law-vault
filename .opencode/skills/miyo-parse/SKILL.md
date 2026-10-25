---
name: miyo-parse
description: Parse a local PDF or EPUB file into Markdown/text with the local Miyo CLI. Use this for document reading when Miyo is the selected Document Processor. The file can be anywhere on the filesystem and does not need to be indexed or copied into the vault.
metadata:
  copilot-enabled-agents: opencode, claude, codex
  copilot-builtin-version: "2"
---

# Parse a document locally with Miyo

Use Miyo to extract Markdown/text from one PDF or EPUB. Parsing runs locally,
works for files anywhere on the filesystem, and does not require the Miyo
service to be running.

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
sh "/absolute/path/to/this/skill/directory/miyo-parse.sh" "/absolute/path/to/document.pdf"
```

On Windows, run the `.cmd` wrapper. In PowerShell you must prefix it with the
call operator `&` (PowerShell treats a quoted path on its own as a string and
won't run it); from cmd, run the quoted path without the `&`:

```powershell
& "/absolute/path/to/this/skill/directory/miyo-parse.cmd" "/absolute/path/to/document.pdf"
```

Pass exactly one quoted path to the PDF or EPUB file.

Both print the result to stdout. Use that Markdown/text to answer the user's question.

## If it reports a problem

Report the error clearly and stop parsing that document. Never fall back to
`copilot-read-pdf` or any other cloud document parser: selecting Miyo is an
explicit local-processing choice. Do not retry in a loop.

If it reports that the Miyo CLI is not installed, say that pointing Copilot at a
remote Miyo server does not help here, and that the user's options are to
install Miyo on this machine or switch Settings → Copilot → Miyo → Document
Processor to Plus.
