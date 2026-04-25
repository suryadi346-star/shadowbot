---
name: memory-curator
description: >
  Extracts new facts from conversation history and deduplicates memory files.
  Use this skill whenever asked to update memory, curate notes, extract facts from a conversation,
  clean up redundant entries across USER/SOUL/MEMORY files, or flag stale content.
  Also trigger when the user says "update my memory", "clean up notes", or "what should be remembered from this".
---

# Memory Curator

Extracts new atomic facts from conversation history **and** deduplicates existing memory files in one pass.

---

## Output Format

One line per finding. Use exactly these prefixes:

```
[USER]       New atomic fact → goes into USER.md (identity, preferences)
[SOUL]       New atomic fact → goes into SOUL.md (bot behavior, tone)
[MEMORY]     New atomic fact → goes into MEMORY.md (knowledge, project context)
[FILE-REMOVE] <file>: reason for removal
[SKILL]      kebab-case-name: one-line description of reusable pattern
[SKIP]       if nothing needs updating
```

---

## Task 1 — Extract New Facts

Scan conversation history for confirmed, durable facts not already in memory.

**Atomic fact rules:**
- Write specific, self-contained facts: `has a cat named Luna` not `discussed pet care`
- Corrections override existing entries: `[USER] location is Tokyo, not Osaka`
- Only capture facts the user confirmed or demonstrated (not speculated)
- Skip: current weather, transient errors, conversational filler, temporary status

**File routing:**
| Content type | Target file |
|---|---|
| Identity, preferences, location, tools used | USER.md |
| Bot behavior, tone, interaction style | SOUL.md |
| Project context, knowledge, technical decisions | MEMORY.md |

---

## Task 2 — Deduplicate Existing Memory

Scan ALL memory files for these patterns and output `[FILE-REMOVE]` for the less-authoritative copy:

**Redundancy patterns to catch:**
- Same fact stated in multiple files (e.g., "communicates in Indonesian" in both USER.md and MEMORY.md)
- Overlapping or nested sections covering the same topic
- MEMORY.md entries that duplicate content already in USER.md or SOUL.md
- Verbose multi-sentence entries that can be condensed without losing info

**Staleness rules (for MEMORY.md entries with `← Nd` age suffix):**
- Age = days since last modification, NOT automatic removal signal
- USER.md and SOUL.md: permanent files, no age annotations, only update with corrections
- **Keep**: user habits, preferences, personality traits — these are permanent regardless of age
- **Prune**: passed events, resolved tracking, superseded approaches, outdated decisions
- Entries with `← Nd` (N > stale_threshold_days): review individually, never auto-delete
- Prefer deleting individual items over entire sections

---

## Task 3 — Flag Reusable Skills

Output `[SKILL]` only when ALL of these are true:
1. A specific, repeatable workflow appeared **2+ times** in the conversation history
2. It involves clear sequential steps (not vague preferences like "likes concise answers")
3. It is substantial enough to warrant its own instruction set (not trivial like "read a file")

Don't check for duplicates against existing skills — that's handled in the next phase.

---

## Example Output

```
[USER] primary language is informal Indonesian (gue/lo register)
[MEMORY] shadowbot rename: breaking changes include SHADOWBOT_API_KEY env var
[MEMORY] nanobot → shadowbot: pyproject.toml entry point updated to shadowbot.cli:main
[FILE-REMOVE] MEMORY.md line 12: duplicates USER.md "communicates in Indonesian"
[FILE-REMOVE] MEMORY.md line 34: stale — nanobot v1 architecture superseded by shadowbot refactor
[SKILL] safe-rename-refactor: bash script workflow for multi-tier codebase rename with test migration
[SKIP]
```
