# Grill Me — SIN-Code Skill

Adversarial design-review interview skill. Relentlessly questions plans, surfaces hidden assumptions, resolves decision trees before implementation.

## What it does

- Interviews the user about a plan/design
- One question at a time, with a recommended answer
- Explores codebase to avoid asking what can be looked up
- Synthesizes decisions at the end
- Hands off to gsd-discuss-phase / sin-doc-coauthoring / sin-goal-mode

## When to use

- User says: "grill me", "stress test this", "interrogate my design", "poke holes"
- Before any architectural decision
- Companion to ceo-audit (which is technical, this is design)

## How to invoke

Just say: **"grill me on this plan"** or **"use grill-me"**

The skill auto-loads on these triggers.

## Full documentation

See [`SKILL.md`](./SKILL.md) for the complete spec (mindset, process, anti-patterns).

## Part of the SIN-Code stack

- **Upstream**: Joanium/Skills (GrillMe pattern)
- **Downstream**: gsd-discuss-phase, sin-doc-coauthoring, sin-goal-mode, ceo-audit
- **Trigger words**: "grill me", "stress test", "interrogate", "poke holes", "challenge"
