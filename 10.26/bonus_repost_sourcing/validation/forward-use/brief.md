# Forward-use fixture review

Synthetic validation only. Read all six supplied_material fields; no browsing, actual post lookup, media playback, real history import, posting or feedback. As of 2026-10-26T15:30:00+08:00.

| Fixture suffix | Verdict | Reason |
|---|---|---|
| 101 | Hold | Publication timestamp conflicts: structured 12:00 vs supplied text 11:00; unresolved. |
| 102 | Recommend — Model | Independent 100-task coding comparison with per-task results and cost methodology; no ad. |
| 103 | Reject | MergeAPI registration CTA in supplied image transcription; fixture explicitly establishes overlapping aggregation business. |
| 104 | Hold | Only setup/results video unavailable; 4x reliability claim and complete brand behavior unverified. |
| 105 | Recommend — Other | Reproducible 40-request prefix-cache experiment, separate cache-hit/TTFT reporting and cold-start limitation. |
| 106 | Hold | Repeats 101 without material progress; timestamp conflicts: structured 12:00 vs supplied text 13:00. |

Two selected, three Hold, one Reject, no alternates. Coverage is partial because the video and conflicting dates remain unresolved. Publication conflicts are preserved in input_published_at and publication_time_conflict; normalized published_at is null. No engine decision differs from the reviewed decision. Shared placeholder handles do not prove identical actual authors; fixture identities alone were used.

The image has a complete textual transcription but no viewable original. Media status for 103 remains partial; the known overlapping CTA suffices for rejection. No media was visually inspected, and no experiment was executed. No true historical-duplicate hit is claimed: the fixture database starts empty; 106 is an editorial Hold for redundant content plus unresolved date, not a state-confirmed previous share.

Files: reviewed.json (agent-reviewed input); run/result.json (full audit); run/brief.md (engine export); run/candidates.csv; fixture.sqlite (fixture-only state).

## Execution

From outputs/Infron_Repost_v0_1:

```powershell
python skills/infron_repost_sourcing/scripts/repost.py preflight
python skills/infron_repost_sourcing/scripts/repost.py prepare --input 10.26/bonus_repost_sourcing/validation/forward-input.json --output 10.26/bonus_repost_sourcing/validation/forward-use/normalized.json
python skills/infron_repost_sourcing/scripts/repost.py run --input 10.26/bonus_repost_sourcing/validation/forward-use/reviewed.json --state 10.26/bonus_repost_sourcing/validation/forward-use/fixture.sqlite --out 10.26/bonus_repost_sourcing/validation/forward-use/run --fixture --as-of 2026-10-26T15:30:00+08:00
```

Preflight, prepare and run succeeded. Inspected the exported brief and all six result verdicts; SQLite integrity_check=ok, mode=fixture, one run, six decisions, four dedup keys for the two selected items, zero feedback. No skill implementation changes; no implementation tests required by the skill.

The exported project has no workflows/infron-content/02_Brand_Context.md; used the supplied editorial rules instead. Initial inspection commands had a working-directory path mistake and a local PowerShell profile emitted startup errors; reads were corrected and all task commands ran with login disabled. No engine execution error occurred. Preflight reports automatic discovery unavailable; it was neither needed nor attempted.

The generated run/brief.md includes generic pre-publication wording about reopening originals. Here the URLs are synthetic and must not be treated as real posts; this brief remains fixture-only.
