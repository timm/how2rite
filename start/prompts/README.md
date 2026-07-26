# Prompts

One prompt per file, markdown, named for its task
(e.g. `critique-draft.md`, `mine-corpus.md`,
`reverse-engineer-strengths.md`). Paste them into
claude.ai (rung 1) or invoke them from Claude Code
(rung 4); either way, the same prompt text serves every
rung.

A prompt file states, in order: what it needs as input,
the prompt itself, what output to expect. Keep prompts
short enough to audit at a glance.

The rite engine (github.com/timm/rite) holds the
pipeline's own prompt divisions; this directory is for
the extra prompts this team uses around that pipeline.
Copy nothing from rite into here; point to it instead.
