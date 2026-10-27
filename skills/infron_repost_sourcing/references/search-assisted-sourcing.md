# Agent-led candidate discovery

Use the host's available web-search tools when the user asks to find repost candidates without supplying links. This workflow needs an agent with web search, and browser access for bounded verification; it is not a standalone Python collector. Keep `coverage.discovery: not_implemented` for the absent automatic API adapter; describe agent-led searches explicitly in coverage.window/success. Never imply that the user must first find links.

## Search and bound

v0.1.2 scheduling: reserve at least two actual queries per lane, up to two adaptive queries. Prefer the strongest fresh-information engine and provider recency filters. Start with source-anchored queries using the actual month/year, e.g. `site:x.com/vllm_project/status "Oct" "2026"`, `site:x.com/lmsysorg/status "Oct" "2026"`, and model-maker accounts from the source pool. Web engines need not support X-native since/until syntax. Do not spend all six queries on a weak engine or overconstrained format. Search Model releases/evaluations separately from inference-engine news. If no 48h Model candidates, follow official release-page events to actual X originals; seven-day discovery fallback does not waive timeliness or justify invented evergreen reasons.

For the legacy X-only audit, save observed triage before deep reading and use `sourcing_plan.py` if its Model/Other queue is appropriate. Its required inputs are defined in the script and its synthetic tests. Alternate viable lanes and try a replacement when the first candidate exceeds its first-pass budget. Use the dedicated history snapshot instead of dumping prior run/decision payloads. This is agent-led discovery; CLI automatic_discovery remains false.

1. Read the source pool, current brand context, local historical seeds and state. Use source links as leads, never an author whitelist.
2. Start with a seven-day Other window and 48-hour Model window. Search date-sensitive queries through the host's search tools, prioritizing official accounts and precise events. Example queries: `site:x.com/vllm_project/status inference`, `site:x.com/lmsysorg/status serving`, and official model-account release searches. Include current date/month in queries and available recency filters, but verify publication time independently.
3. Use at most six search queries, gather at most 30 distinct concrete status URLs, and deeply review at most 20. If one search engine returns stale results or trending summaries, use a second engine when available; record the difference. Stop at the bound and report remaining gaps. Do not claim complete coverage.
4. Reject trending summaries and profile URLs as repost candidates. Keep them only as discovery leads. Resolve a specific original post; do not invent IDs or canonical originals from quoted text.
5. Normalize and review using the existing input contract. Open each selected post. Distinguish search snippets from full text and API object metadata from actually inspected media. Read necessary thread/quote, linked article and claim-bearing figures. Check the author's identity against a primary site/repository link.
6. Compare with history and actual state. Report "not in the available history" if the current account's complete history could not be obtained; never assert "never shared" from a partial seed set. Recheck current account history before publishing, which this skill never performs.
7. Export search provenance with query, engine/tool, time, concrete selected URLs, failed access and reading scope. Store short evidence notes, not full copied posts or media. Submit the reviewed bundle to `repost.py run` with the same real state across sessions. Do not weaken evidence gates to fill slots.

## Route toward a standalone collector

Preferred: a team-authorized read-only X API or existing internal service. Official recent search uses `/2/tweets/search/recent`, an approved App and Bearer Token, and a seven-day window. Ask for approved integration/configuration location and a trial cap; never ask for a secret in chat. No calls until authorization and budget are established.

Implement bounded query plans, post/author/reference/media fields and expansions, pagination, successful-page cursors, cross-query dedup, explicit request/resource/cost caps, rate-limit and partial-failure reporting. Treat media URLs as unread until verified. Do not use blind retry loops or charge requests without a cap. Use a response adapter to feed existing review contracts; API collection does not replace semantic review.

Alternative: a team-approved external data provider with verified source provenance, deletion behavior and pricing. Do not purchase or assume access. GitHub releases/Hugging Face/blogs can find events, but need a verified X original before they become repost candidates.

Official references checked 2026-10-26:
- https://docs.x.com/x-api/posts/search/quickstart/recent-search
- https://docs.x.com/x-api/getting-started/pricing

The public-search workflow was used for six real posts on 2026-10-26; the historical trial records are not distributed in this repository. Standalone/API discovery remains unimplemented and untested.
