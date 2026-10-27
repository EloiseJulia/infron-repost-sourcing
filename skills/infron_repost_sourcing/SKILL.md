---
name: infron-repost-sourcing
description: Discover and recommend worthwhile AI infrastructure, model and inference content for Infron. Search and read X or LinkedIn posts and primary technical articles, papers or repositories, explain developer value and platform-specific sharing angles, and distinguish repostable posts from content ideas. Use for topic-led or open-ended sourcing and, on explicit request, publication review.
---

# Infron Repost Sourcing v0.2.0

## Goal and context

Proactively find normally 2–3 worthwhile, actually read sources and recommend them directly in Chinese chat. No user links, forms, Python commands or report download are required. Read the current project's `workflows/infron-content/02_Brand_Context.md` and [editorial rules](references/editorial-rules.md). Use the [source pool](references/source-pool.json) as leads, not a whitelist. These instructions override legacy audit/search defaults.

Default recommendations may include both:
- **社媒原帖**: an actual, read X status or LinkedIn post/feed-update permalink; a potential repost or quote target.
- **一手技术内容**: an actually read primary article, paper, model card or repository, identified by type; a content idea or reading recommendation, not an already identified social repost target.

If the user explicitly requests only social posts or only a particular type or platform, honor that scope. Do not silently substitute an article for a requested social post, invent a social permalink, or treat a LinkedIn article share as read unless the actual post was read.

## Select the entry route

**Topic-led (指定主题):** If the user names a model, capability, feature or campaign, keep that topic as the constraint. Search exact names/versions, aliases, official authors and credible technical commentary. Seek announcements, useful demos, evaluations and implementation experience. For old events, seek meaningful recent developments; never silently substitute unrelated trends.

**Opportunity-led (热点机会):** If no topic is given, discover conversations Infron can credibly join: model releases/capabilities, independent evaluations, inference cost/latency/reliability, routing, caching, deployment and developer workloads. Explain the business connection and a natural contribution. AI popularity alone is insufficient.

Use both routes if requested and label each result's route. Search both platforms and relevant primary technical sources when in scope; neither platform nor source type has a mandatory quota. Never invent Infron support, discounts, features or partnerships; specific product claims require current explicit evidence.

## Search, read and replace

1. Begin within 7 days, prioritizing the last 48–72 hours for fast-moving news. Expand to 14 days if needed. Older sources need a specific current reason to share. Respect explicit date constraints. Recency is a priority, not proof of quality or a reason alone to exclude useful older material.
2. Use 4–6 distinct query strategies, up to 8 for replacements. Include relevant social permalink searches, exact topics, authors, primary technical sources and current event/date terms, subject to the user's scope.
3. For hotspots, seek observable signals: dated engagement visible on a post, multiple independent credible authors discussing the event, or a substantive current release driving discussion. Distinguish attention from mere recency. Never invent likes, growth or virality. Without attention evidence, call it relevant recent content rather than a proven trend.
4. Compare developer value, technical substance, timeliness, brand fit and information increment. Prefer official authors, maintainers, researchers and credible evaluators, without auto-approving them. Avoid empty hype, unsupported central claims and promotion of business-overlapping platforms. A model name or neutral ranking is not automatically competitor promotion. For an ambiguous brand relationship, judge the actual material and task context; disclose a material uncertainty, and do not claim publication approval.
5. Remove duplicate URLs/events within the batch; normally choose one strongest source per event unless another adds a materially different contribution. Strictly suppress previously published or reposted items only when confirmed by available evidence. A prior recommendation, review or acceptance alone is not proof of publication and must not automatically suppress it. Consult actual posted history when available; missing or partial history means no claim of complete official-account deduplication. The optional legacy history snapshot includes `recommended` keys: distinguish those from confirmed `posted` or verified historical actions.
6. Open each selected source and read substantive content, including relevant social thread/quote, media, or the primary technical sections needed to understand core claims and promotion. Follow primary links for factual checks as needed. Search snippets alone are leads, not sufficient reading evidence. Numerical performance requires checked conditions and support; distinguish author-reported results from independent replication.
7. On blocked/incomplete targets, make at most two reasonable alternative retrieval attempts with authorized tools, then replace the source. When both types are in scope, a readable primary article can be recommended as a separately labeled content idea, never as a social post. Never guess status/activity IDs or bypass safeguards.
8. Exclude candidates with unread central claims or brand-bearing media. Avoid relying on a minor unseen nonessential element; mention it only when it changes editorial use. Do not narrow away an unsupported central claim to make a source pass. Continue replacing weak/blocked candidates while the search budget remains.

## Deliver in chat

Lead with recommendations. For each item give:
- Type, linked source title, author or organization, platform/publication and date. Use an observed relative date if the exact date is unavailable; do not infer one.
- Route (“指定主题” or “热点机会”), with the topic or observed attention signal.
- Content takeaway, concrete developer value, and why Infron can credibly contribute: a model or deployment decision, inference trade-off, workload implication, or useful explanation. Separate source facts from editorial inference.
- For social posts: recommend repost or quote/comment and a short platform-aware angle. On X focus on one concrete insight or trade-off; on LinkedIn add the problem, necessary context and reader benefit. When both platforms are requested, adapt the angle to each without changing the facts.
- For primary technical content: label it as a content idea/reading recommendation, name a proposed target platform (X or LinkedIn) and give a platform-appropriate editorial angle; do not imply a verified repostable social post exists.
- State a material evidence or brand uncertainty when it affects use. Write full promotional copy only when requested.

Normally no standalone report or Hold/deferred table. Aim for 2–3 useful sources, never fabricate or fill slots with unread links. If only one qualifies, give it. If none qualifies after bounded replacement, explain the concrete access/topic limitation briefly and a useful next step. Do not claim automated sourcing works end to end when access is unavailable.

Recommendations are not official publication approval or confirmation of account-level repost permissions. Record posted state or human feedback only when explicitly given.

## Optional explicit publication audit

Only when asked to check a particular post for official publication, read [input contract](references/input-contract.md), [evidence completion](references/evidence-completion.md), [search workflow](references/search-assisted-sourcing.md) and [history limits](references/history-lessons.md). Apply the original evidence/media/brand/dedup audit and offline runner as appropriate; Hold/deferred may be valid here. Legacy X-only schemas cannot establish LinkedIn clearance; use actual LinkedIn permalink/evidence without faking an X ID. The legacy runner also suppresses earlier recommendations: report that limitation rather than presenting it as proof of publication.

## Boundaries

Use host AI search and authorized reading tools. No independent X/LinkedIn API collector is implemented. Do not publish, like, message, purchase, deploy, schedule or inspect secrets. Preserve user edits and historical evidence. Old failures stay failures. After substantial revisions, evaluate both routes and the [sourcing scenarios](references/sourcing-scenarios.md) in fresh contexts; report source types, reading evidence, business connection and delivery limitations honestly.
