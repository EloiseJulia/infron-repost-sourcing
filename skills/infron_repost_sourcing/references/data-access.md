# Data access and adapter contract · 2026-10-26

## Verified versus blocked

Public profile/details initially showed login gates. Later the same browser session exposed the normal timeline and Reposts tab; 14 actions were manually verified, and part of the Arena chart became visible. Complete media/older-quote verification remains unfinished. Web-service direct profile request returned 403. Search returned some X links but cannot establish complete text or a sharing relationship. No real API request was issued: no team-authorized X configuration or trial spending cap was supplied. No private credentials, browser cookies or environment secrets were scanned.

Official Recent Search documentation specifies the last 7 days and an approved App with Bearer Token. Public pricing describes prepaid usage-based billing; verify actual rates/expansion charges and access in the team's console before a trial. A 30-day history audit cannot be claimed from a 7-day search alone.

References, read 2026-10-26:
- https://docs.x.com/x-api/posts/search/quickstart/recent-search
- https://docs.x.com/x-api/getting-started/pricing
- https://docs.x.com/x-api/posts/timelines/integrate
- https://docs.x.com/x-api/fundamentals/expansions
- https://docs.x.com/developer-guidelines

## Future adapter handoff, not an implemented collector

Implement a read-only adapter only after authorized configuration and a cap are explicit. Use X official API or team-authorized service; Infron inference credentials cannot read X.

Adapter output must enter the manual candidate contract as unreviewed records. Preserve string post/edit IDs, author/time, referenced object IDs/types, canonical expanded URLs and media metadata. Never mark media full from metadata or missing includes as absent.

| Discovery route | Minimal request plan | Coverage record |
|---|---|---|
| Source updates | Confirmed user-ID timeline or existing authorized List | source_id, start/end, last successful interval, pending pagination |
| Topic exploration | Bounded Recent Search, candidate query templates in source-pool.json | exact query, window, page count, oldest/newest IDs, next token, errors |
| Event reverse lookup | Find author's actual X original from official article/release | origin URL, matching evidence, status URL or off-platform lead |

Use `GET /2/users/by/username/:username`, `GET /2/users/:id/tweets`, `GET /2/tweets/search/recent`, and `GET /2/tweets/:id` only where supported by the authorized account; validate endpoint fields/permissions at implementation. Request author, referenced-post and media expansions with relevant fields. Treat templates as untested, not working API examples.

Pre-authorize max requests, max returned resources including expansions, max deep reads and dollars. Record reserved worst-case cost before each request and actual usage after; stop at any cap. Retry network/429 at most once only if Retry-After fits cap and run deadline. Do not retry auth/credit failures; do not rotate accounts.

Persist source cursors separately from editorial state. Advance an interval only after all pages and errors for that interval are accounted for; on partial paging preserve next_token and original window. Overlap a small period and deduplicate. If interruption exceeds available lookback, report the gap. No v0.1 cursor is advanced because no collection occurred.

Coverage status must distinguish completed contracted scope with zero candidates, partial scope, and core-access blocked. An empty response alone is insufficient evidence of successful coverage. Version raw adapter contract, fields, errors, rule set and source pool.

Current preflight is a no-network implementation report, not an API connectivity test. A future connector must add credential-safe endpoint checks and real small-budget acceptance evidence. The v0.1 runner intentionally exposes no discover command or paid execution path.

