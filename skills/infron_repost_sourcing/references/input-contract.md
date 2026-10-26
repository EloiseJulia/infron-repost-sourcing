# Manual input contract · schema 1.0

The runner executes no network/model calls. An agent/editor supplies semantic reviews based on actually read material. `prepare` only normalizes; `run` enforces declarations and state gates. See `assets/manual-template.json` and the real reviewed input under `10.26/bonus_repost_sourcing/samples/`.

## Bundle

Use UTF-8 JSON: `schema_version: "1.0"`, `mode: "manual"`, `coverage`, `candidates`.

Coverage: `discovery: "not_implemented"`; `status: blocked | partial | supplied_complete`; human-readable `window`; `success` and `failed` string arrays. `supplied_complete` refers only to supplied material, never X-wide discovery. Failed sources cannot coexist with this status. No cursor advances in v0.1.

## Candidate

| Field | Meaning |
|---|---|
| url, post_id | Actual X/twitter status URL; optional ID must match and remain a string |
| author | Actual handle, matching URL when the URL contains a handle |
| synthetic | Required boolean; all records must match `--fixture` |
| lane | Model / Other, judged semantically |
| post_type | original / quote / reply / repost / unknown |
| published_at | ISO-8601 with timezone, or null → Hold |
| event_key | Specific semantic release/version/finding key, consistent across days |
| article_urls | Relevant resolved URLs; tracking removed, meaningful parameters retained |
| edit_ids | Known edit chain IDs as strings; runner adds current ID |
| quote_url | Actual quoted status URL, never guessed |
| evidence | Exactly text, quote, media, links; fields below |
| review | Semantic audit below |

Each evidence part needs `presence: yes | no | unknown`, `status: full | partial | unavailable | not_present`, `note`, and `locator` when full/partial. `not_present` requires confirmed absence. A quote or article URL cannot be marked absent. Inspect media visually; use an appropriate playable/transcribed representation for videos/audio. Record scope and material missing information, not just "checked". Aggregate all relevant objects in each part; any necessary unread object prevents full status.

Review needs nonempty `reviewer`, `checked_at` with timezone, `summary_zh`, `why_now`, `brand_reason`, `fact_reason`, `identity_reason`, `reason`, `novelty_reason`.

Set `decision: recommend | hold | reject`, `identity: verified | unknown`, `facts: verified | unknown | false`, `brand: acceptable | overlap_promotion | unknown`, `action: pure_repost | quote | none`.

Set `priority` to a positive editor ordinal (lower first), not a quality probability. In `quality`, provide `audience_value`, `substance`, `timeliness`, `brand_fit`, `increment`, each `{level: high | medium | low, reason: ...}`. Keep evidence completeness separate.

Provide `entities: [{name, role, behavior, evidence}]` and nonempty `claims: [{claim, status: verified | unknown | false, evidence}]`. Locators are URLs or explicit fixture sources. All core claims must be verified to pass. `evergreen_reason` permits older useful content with a specific current sharing rationale. Defaults Model 48 h / Other 168 h, review freshness 24 h, are provisional configuration, not mentor rules.

Material progress on a shared event needs `material_update: true`, `previous_reference`, `update_evidence` and a real difference. Exact post/edit duplicates cannot bypass dedup. Judge a quote's independent increment separately; quoted original IDs do not automatically collapse every derivative quote.

## Exports and state

An additional early-exit reason `evidence_blocked` requires `blocker: authentication | deleted_private | security_block | unplayable`, `method`, `outcome` and a concrete `reference` to the necessary object. Other skipped objects retain honest partial status. It cannot recommend or treat a single ordinary fetch failure as a hard barrier.

For newly produced bundles set `review_process_version: 1`. Every candidate needs `completion: {state: ready | blocked | deferred | early_exit, note, checks}`. `checks` contains exactly text/quote/media/links, each `{disposition: resolved | blocked | pending | not_present, attempts: [{method, locator, outcome}], blocker?}`. Use `not_present` only with matching evidence absence. Use `resolved` only with matching full evidence. For an unresolved object use a blocker of `authentication`, `deleted_private`, `security_block`, `unplayable`, `budget_exhausted`, or `access_failed`. Access-failed requires two distinct appropriate methods; hard barriers need one observed attempt; a budget limit is unfinished work, not a terminal Hold. Pending requires `state: deferred`. A ready candidate must have all objects resolved/absent. Early exits additionally need `early_exit: {reason: historical_duplicate | stale | disqualified, reference}`; this permits stopping before expensive reads without inventing access. The script validates declared process, not external observations. Old bundles omit the version and export `completion_enforced=false`.

- `brief.md`: 0–2 main choices, Hold/Reject/alternate table, coverage/resources.
- `result.json`: full audit, computed verdict/reasons alongside preserved reviewer decision, rule/source version.
- `candidates.csv`: compact UTF-8 BOM index; formula-like strings escaped.
- SQLite: runs with input SHA-256, decisions, dedup keys, historical action references, feedback.

Only selected recommendations/observed history/explicit posted feedback suppress repeats; seen/held items can be re-reviewed. Alternates are not delivered main recommendations. Pass the same database across days. Fixture and real state cannot mix. Run directories refuse overwrite.

`discovery_blocked`: automated sourcing unavailable even when manual records reviewed. `partial_coverage`: missing scope recorded. `manual_no_qualified_candidates`: supplied batch covered, zero qualifying recommendations. None means "no good posts on X today".

Use sequential runs per state/output directory. SQLite transactions serialize state writes. Invalid input exits 2 before state mutation. If export fails after directory creation, state rolls back but a partial directory may remain; never report it as successful. Use a fresh directory after fixing I/O.

