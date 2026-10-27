---
name: infron-repost-sourcing
description: Find X and LinkedIn original posts suitable for Infron to repost or quote, either for a specified model/feature/topic or through relevant trending conversations. Search proactively without user links and return social-post permalinks with concrete business relevance and editorial reasons. Never substitute websites or articles for repost targets.
---

# Infron Repost Sourcing v0.1.4

## Goal and context

Proactively search and return normally 2–3 worthwhile X or LinkedIn original posts directly in Chinese chat. Require no links, forms, Python commands or report download from the user. Read current project `workflows/infron-content/02_Brand_Context.md` and [editorial rules](references/editorial-rules.md). Use [source pool](references/source-pool.json) as leads, not a whitelist. These instructions override legacy audit/search defaults.

## Select the entry route

**Topic-led (指定主题):** If the user names a model, capability, feature or campaign, keep that topic as the constraint. Search exact names/versions, aliases, official authors and credible technical commentary on both platforms. Seek announcements, useful demos, evaluations and implementation experience. For old events, seek meaningful recent developments; never silently substitute unrelated trends.

**Opportunity-led (热点机会):** If no topic is given, discover conversations Infron can credibly join: model releases/capabilities, independent evaluations, inference cost/latency/reliability, routing, caching, deployment and developer workloads. Explain the actual business connection and a natural contribution: model-choice lesson, workload implication or engineering tradeoff. AI popularity alone is insufficient.

Use both routes if requested, label each result's route, and do not ask the user to choose for ordinary requests. Never invent Infron support, discounts, features or partnerships; specific product claims require current explicit evidence.

## Search, read and replace

1. Begin within 7 days, prioritizing the last 48–72 hours for fast-moving news. Expand to 14 days if needed. Older posts need a current trigger and accurate date. Respect explicit date constraints.
2. Use 4–6 distinct query strategies, up to 8 for replacements. Include X/twitter status and LinkedIn posts/feed-update searches, exact topics, authors and current event/date terms. Neither platform has a mandatory quota.
3. For hotspots, seek observable signals: dated engagement visible on the post, multiple independent credible authors discussing the event, or a substantive current release driving discussion. Distinguish attention from mere recency. Never invent likes, growth or virality. Without attention evidence, call it a relevant recent post rather than a proven trend.
4. Compare developer value, technical substance, timeliness, brand fit and information increment. Prefer official authors, maintainers, researchers and credible evaluators. Avoid empty hype, unsupported central claims and promotion of business-overlapping platforms. A model name or neutral ranking is not automatically competitor promotion.
5. Remove duplicate URLs/events; consult available actual posted history, using the read-only history helper if useful. Missing history means no claim of official-account deduplication. Normally choose one strongest post per event unless a second adds a materially different contribution.
6. Open each selected social permalink and read substantive text, relevant thread/quote, and media necessary to understand central claims or promotion. Follow primary links for factual checks as needed. Search snippets alone are leads, not sufficient reading evidence. Numerical performance requires checked conditions and support.
7. On blocked/incomplete social targets, make at most two reasonable alternative retrieval attempts with authorized tools, then replace the post/author/platform. Websites may verify background or expose an observed social permalink, but must never replace the final repost target. Never guess status/activity IDs or bypass safeguards.
8. Exclude candidates with unread central claims or brand-bearing media. Avoid relying on a minor unseen nonessential element; mention it only when it changes editorial use. Do not narrow away an unsupported central claim to make a post pass. Continue replacing weak/blocked candidates while the search budget remains.

## Deliver in chat

Lead with recommendations. For each item give:
- Title linked to the actual X status or LinkedIn post/feed-update permalink; author, platform and date.
- Route (“指定主题” or “热点机会”), with the topic or observed attention signal.
- Content takeaway and a specific reason Infron should participate.
- Suggested repost or quote/comment action and a short editorial angle. Write full promotional copy only when requested.

Only social posts belong in recommendation slots. Blogs, product pages, repos, papers, model cards, account profiles and search pages are not repost targets. A LinkedIn share of an external article qualifies only when the actual LinkedIn post is read and its permalink is recommended. External sources may appear as subordinate evidence.

Normally no standalone report or Hold/deferred table. Aim for 2–3 useful posts; never fabricate or fill slots with websites/unchecked links. If only one qualifies, give it. If none qualifies after bounded replacement, explain the concrete access/topic limitation briefly and a useful next step. Do not claim automated sourcing works end to end when social access is unavailable.

Keep source facts separate from editorial inference. Recommendations do not constitute official publication approval or confirmation of account-level repost permissions. Record posted state or human feedback only when explicitly given.

## Optional explicit publication audit

Only when asked to check a particular post for official publication, read [input contract](references/input-contract.md), [evidence completion](references/evidence-completion.md), [search workflow](references/search-assisted-sourcing.md) and [history limits](references/history-lessons.md). Apply the original evidence/media/brand/dedup audit and offline runner as appropriate; Hold/deferred may be valid here. Legacy X-only schemas cannot establish LinkedIn clearance; use actual LinkedIn permalink/evidence without faking an X ID.

## Boundaries

Use host AI search and authorized reading tools. No independent X/LinkedIn API collector is implemented. Do not publish, like, message, purchase, deploy, schedule or inspect secrets. Preserve user edits and historical evidence. Old failures stay failures. Forward-test both routes in fresh contexts after substantial revisions; assess actual social permalinks, reading evidence, business connection and useful chat delivery.

