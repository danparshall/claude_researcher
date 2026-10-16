# Translation corrections log

**What this is:** the append-only raw trail of translation naturalness corrections — every pair captured at a translation review's close-out (`translation_review_skill.md`), as *unnatural → natural → why*. This is the corpus the distilled-patterns section of that skill grows from. Entries are **never edited or pruned**; the log only grows.

**Lifecycle:** the log accumulates locally as review rounds happen. Over time, recurring kinds of correction are folded into `translation_review_skill.md`'s patterns section, so the skill gets better at avoiding them in the first place. If you keep a canonical skills repo, the log travels back to it and merges into a shared corpus — portable learning, where every project inherits every project's corrections.

**Entry format:**

```
## YYYY-MM-DD — <document or branch-ref>
- **Unnatural:** <Claude's original translation>
- **Natural:** <the user's correction>
- **Why:** <one line naming the kind of problem>
```

One `##` block per review round; multiple pairs under one block are fine (repeat the three-line group). The why is drafted by Claude and confirmed by the user at the close-out.

---

*This log ships empty. The first review round that produces corrections starts the corpus — append the first `##` block below this line.*

---

*Last updated: October 10, 2026 — starter-package edition, mirrored from kit v6.11. The version history that preceded this line recorded maintenance internal to the canonical kit and has been dropped. From here on, record your own changes to this file in this marker, newest first, one clause per change, so a later session can see what moved and why.*
