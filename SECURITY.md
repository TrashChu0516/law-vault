# Security policy

## Reporting a vulnerability

Please do **not** open a public issue for a security problem.

Use GitHub's private vulnerability reporting: **Security → Report a vulnerability** on this repository. If that option is unavailable, open a minimal issue asking for a private channel — do not include the details.

## Scope

This repository is a static study system: Markdown, Python scripts and agent skill specs. It runs no server and stores no user data.

The realistic risks are:

- a secret committed by mistake;
- a malicious dependency pulled into a fork;
- a prompt-injection payload in a note the agent reads.

## Out of scope

- The private vault's corpus (textbook PDFs, seminar outlines, past papers).
- The legal accuracy of the notes; that is a content issue, not a security issue.

## If a secret is exposed

Rotate it first, then remove it from the repository. Deleting the file is not enough if the secret remains in git history — treat it as burned, then rewrite history if needed.
