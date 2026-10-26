# Complete evidence before ending a review

Treat `pending` as unfinished work, not a final Hold. Use this workflow for each plausible candidate. Do not claim that a failed search fetch proves that the public browser cannot read a page.

## Recover by object

| Missing object | Next action | Genuine stopping point |
| --- | --- | --- |
| Truncated quote | Open its concrete status URL; read original text and its necessary media | Original requires unavailable access, deleted/private, or bounded attempts exhausted |
| Thread marked 1/N | Open main post, expand Show more, follow visible same-author continuation IDs needed for claims/CTA | Required continuation inaccessible; do not demand unrelated replies |
| Search fetch 403/error | If browser independently authorized/available, inspect public page there | Observed auth/security barrier or second appropriate route fails |
| Figure | Open visible media link and inspect actual pixels, axes, units and footer; inspect other claim-bearing slides | Login/media barrier or unreadable resolution after appropriate attempt |
| Video | Try normal playback; use accessible source transcript/captions for spoken content, inspect visuals for performance/brand claims | Unplayable or necessary visuals unavailable; transcript alone does not verify visuals |
| Article | Open resolved article and read relevant sections, figures, limits and CTA; primary repo/official report may corroborate claims | Necessary article absent or inaccessible after appropriate alternate route |
| Identity | Follow primary site/repo social link, compare exact handle and cross-links | No sufficient identity chain; badge alone is insufficient |

Respect site safeguards: no alternate-route probing after an identified bot/security block, no repeated login attempts, no unofficial mirrors or guessed URLs. An ordinary search-tool fetch error permits an authorized public-browser read. Never infer a missing link, timestamp, claim or absence of media from snippets.

## Allocate effort and finish

v0.1.2: Define the original post's core claims and material brand risks before deep reading a linked article. Check the sections/tables/figures needed to settle them. `links=full` may describe completed decision-critical scope, not every supplemental figure; name inspected material and nonessential exclusions with reasons. Never claim to have read the entire article if only a scoped subset was inspected. Do not exclude source-post media, key performance charts, unsupported original claims or brand-bearing CTA to pass. A kernel-design post may need a method description and E2E table without every other-hardware microbenchmark. A headline claiming those other benchmarks still needs those figures. No evidence gate is waived.

First pass: six evidence-opening actions per candidate, then switch to a different queued candidate. Inspect the other available lane and replacements before revisiting a difficult item; twelve opening actions remain the total ceiling per candidate. Repeated screenshot timeouts require a route change, not indefinite retries. Keep unresolved items deferred while alternatives are attempted. Prioritize completing useful decisions over exhaustive background reading.

1. Triage exact known duplicates, out-of-window news without a current rationale, and clear disqualifiers before expensive media work. Record `early_exit` with concrete reason/reference. Do not pretend those objects were inspected.
   Also allow `early_exit.reason: evidence_blocked` after an observed hard barrier to a necessary object, with `blocker`, `method`, `outcome` and `reference`. Leave other skipped objects honestly partial/unavailable; a hard blocker does not require reading every unrelated remaining object. A failed search fetch alone is not such a barrier.
2. For viable candidates, create a small evidence queue. Resolve direct originals and accessible articles first. Make at most three appropriate attempts per missing object and at most twelve evidence-opening actions per candidate, excluding ordinary reading/scrolling. Stop earlier at a hard access barrier. These are provisional operational budgets, not mentor standards.
3. Finish the strongest candidates before opening many more. If one is irrecoverably blocked, try a replacement event/source within the overall discovery budget. Do not end a batch of promising candidates with unattempted obvious next actions.
4. Classify each evidence object as resolved, blocked or pending. Only blocked supports a terminal evidence Hold; pending means the task is not finished. If the session budget ends, label `deferred` and state remaining work explicitly, never report the batch as completely audited.
5. Record actual `method`, `locator`, `outcome` for each attempt. A screenshot/AX read is evidence of access, not empirical replication. Use author-reported, independently corroborated, and experimentally replicated distinctions in claim notes. Do not demand rerunning every published experiment, or mark author-reported performance as universally independently verified.
6. For new work use `review_process_version: 1` and per-candidate `completion` per input contract. Old bundles remain replayable but have `completion_enforced=false`. The engine checks declared process records; it cannot prove browsing happened.

Keep final outputs useful: show actual recommendations, reviewed exclusions, blocked Hold, and unfinished work separately. Zero recommendations is allowed, but do not present unfinished investigation as a completed sourcing run. Preserve all earlier run files; never revise them in place to improve apparent metrics.
