---
name: infron-repost-sourcing
description: Find worthwhile AI model and inference-engineering posts or primary-source articles for Infron and return useful links with concise editorial reasons. Use when asked to find content to read, share, or consider for reposting, without requiring user links. Default to content curation, not publication clearance. Only use the strict audit pipeline when the user explicitly requests publication-readiness verification.
---

# Infron Repost Sourcing v0.1.3

## Default task: find useful content and deliver links

The user's goal is to say one prompt and receive worthwhile posts or URLs. Default to **curation**: proactively search, read and compare, then deliver normally 2–3 concrete recommendations in chat. No user-supplied links, JSON form, command invocation or report download is needed.

Read current `workflows/infron-content/02_Brand_Context.md` and the editorial principles in [editorial rules](references/editorial-rules.md). Use [source pool](references/source-pool.json) as starting leads, not an account whitelist. Apply the curation rules below instead of the legacy audit workflow's 48h gates, fixed category slots, mandatory completion schema or report exports.

### Select for the reader

Recommend items with a specific developer takeaway: model capability/choice, inference performance and cost mechanisms, reliability, tool use, deployment or a reproducible engineering lesson. Prefer primary sources and substantial explanation over hype. Check actual target content for brand fit: a model mention or open-source implementation is different from promoting a business-overlapping API platform. Do not invent Infron capabilities, prices or partnerships. No likes threshold or invented quality score.

Prefer recent content, initially the last 14 days. Recency is a preference, not an automatic veto for useful engineering material. Label publication dates accurately; older timeless material needs a specific current-use reason and must not be presented as breaking news. Try to cover models and engineering, but do not force one item in each slot if better items are in one category.

### Search, read, replace

1. Start with both model and engineering sources. Use the strongest available current search engine, source-specific month/year searches and official blog/release indexes. Normally use 4–6 query strategies, up to 8 only when replacement is needed; consolidate searches rather than browsing indefinitely.
2. Skim a shortlist, compare value and remove known duplicates before deep reading. Consult existing history through `sourcing_plan.py history` if useful; do not read old decision payloads as evidence for new recommendations.
3. Open each selected target and read the substantive text and decision-critical claims/limitations. Search snippets, inaccessible URLs or titles alone are not a recommendation. Normally finish the strongest 2–3, with at most two extra evidence-opening attempts on a blocked target before switching.
4. **If X cannot be read, change the delivery target**: follow an observed original-author blog/repo/paper link, verify that page, and recommend that actual URL as an article/repo/paper. Do not invent an X status, say unseen media was checked, or claim the original X post is cleared. If no readable primary alternative exists, replace the item with another event/source.
5. For an article recommendation, confirm its core message and why it is useful; use method/text/table evidence and relevant limits. Do not audit every supplementary hardware chart, code dependency or demo by default. Quote numerical performance only when the reported setting and supporting material were actually checked; otherwise discuss the supported engineering concept, not an unverified number. Do not narrow away misleading central claims or material promotion to pass the content.
6. Inspect media when it is needed to understand the actual recommended target's central claim or brand behavior. Unread X media prevents certifying that X post for reposting, but does not automatically block a separately read, independently suitable article. Record target/scope honestly internally.
7. Allocate effort across alternatives. Don't deliver a list of Hold/deferred tasks as the normal curation answer while readable worthwhile sources remain. Switch domains and then consider clearly labelled evergreen material rather than stopping at one blocked site. If all genuinely available sources remain unreadable or irrelevant, state the concrete limitation briefly; do not fabricate recommendations to guarantee a nonempty answer.

### User-facing output

Lead directly with the recommendations, not access failures, counts, tests or rules. For each item:
- Human-readable title linked to the **actual inspected target**.
- Source/date and type (X post, engineering article, model card, paper or repo).
- Two concise Chinese sentences: what the reader learns and why it is worth sharing/reading for Infron.
- One concrete angle the team could use, when useful.

Keep source facts separate from editorial inference. A recommendation is an editorial lead, not a claim of publication authorization or completed empirical replication. Mention a narrow limitation only when it changes how this particular item should be used; do not add boilerplate to every item.

Normally no standalone report or developer checklist. The AI may retain concise source/provenance notes internally. Save a user-facing report only when requested; do not make a download the main result. Record new human feedback only when explicitly given. Do not silently mark a curated article as published or import it into the legacy state as an approved X repost.

## Optional task: strict publication-readiness audit

Only when the user explicitly asks to check a specified post for official-account repost/quote approval, read [input contract](references/input-contract.md), [evidence completion](references/evidence-completion.md), [search workflow](references/search-assisted-sourcing.md) and [history limits](references/history-lessons.md). Then use the existing offline `repost.py` validation/state/export pipeline and completion v1. Its stricter dates/media/brand/duplicate gates and Hold/deferred outputs apply to this optional mode, not ordinary content discovery.

State which mode is used when an explicit task is ambiguous; default to curation for "find worthwhile posts/URLs". Do not ask the user to choose a mode for an ordinary request.

## Runtime boundaries

Host AI search is the default discovery mechanism. The Python scripts do not perform standalone X API collection; that adapter remains unimplemented. Do not purchase services, inspect secrets, schedule work, deploy, publish, like or message. Respect site safeguards and actual tool availability.

Preserve previous files, user edits and evidence. A failed old trial must remain in history, not be rewritten as success. Tests of code structure are not tests of editorial usefulness. For skill revisions, forward-test a plain no-link request in a fresh context and inspect its actual chat answer and sources; do not give expected recommendations to the evaluator.

