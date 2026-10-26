# Curation trial — 2026-10-26

Mode: default curation under skills/infron_repost_sourcing/SKILL.md v0.1.3. No publication, audit approval, replication, history mutation or skill modification. Read only this isolated project's brand context, editorial rules, source pool and history-snapshot.json. No sibling projects or older recommendation artifacts read.

## Search bounds

Host strongest search (system1), initial last-14-day preference. Six queries total:
1. site.qwen.ai OR site.huggingface.co/Qwen October 2026 model release
2. site.deepseek.com OR site.github.com/deepseek-ai October 2026 model release
3. site.blog.vllm.ai October 2026 inference prefix caching speculative decoding
4. site.sglang.ai/blog October 2026 inference engineering
5. Qwen "October" "2026" "release" model
6. DeepSeek "October" "2026" "V4.1" release

Also opened official indexes https://vllm.ai/blog and https://www.sglang.io/blog. Direct model searches mainly yielded secondary sources, not used as final evidence. Official SGLang index supplied readable current alternatives. No X target recommended or certified. UlaCache https://arxiv.org/html/2610.29820v1 was skimmed through introduction/background, then deprioritized for a more varied final selection; no performance claim drawn into answer.

## Dedup and scope

Consulted only history-snapshot.json. Excluded known previously recommended Elastic EP/NIXL (2026-10-21) and Omni interactive runtime (2026-10-20). None of the three final target URLs/events is explicitly listed in the snapshot; opaque historical post IDs are not assumed to establish unseen event identities.

## Selected sources and decision evidence

1. https://www.sglang.io/blog/unified-memory — official SGLang engineering article, dated 2026-10-22 in official blog index. Read substantive page through Results and Further reading, web refs turn36view1 / turn37view1; index turn34view1. Explains full-attention KV and recurrent states sharing one same-GPU buffer, page-major envelopes, stable virtual IDs, compaction and allocation-aware eviction. Not CPU offload (article line 96). Critical qualification: both comparison arms already use Unified Memory; 28 cached ~390-token prefixes followed by 7000-token pressure request and replay, Qwen3.5-4B / RTX5090 / Triton, median of six runs; large single allocation needed. Chunked 2048-token prefill removed eviction-rule difference and overall throughput had no stable change (190–211). Final recommendation focuses on memory-utilization mechanism and includes this narrow limitation, not generalized headline speedup. No signup/platform promotion in substantive page. Interactive explanatory widgets were read as extracted text; not executed and no visual chart audit claimed.

2. https://www.sglang.io/blog/minimax-m3.1-flash-day0-support — official SGLang & Miles engineering article, 2026-10-22, refs turn36view0 / turn37view0 / turn38view0. Read from model overview through hardware table, speculative decoding, AgentX measurement definitions, MegaAttention/MegaMoE mechanisms and Miles validation/acknowledgments. Sparse attention, quantization and DSpark/DFlash2 combine with hardware-specific kernels; Hopper/Blackwell/AMD have different cache dtypes and kernel paths (114–130). High AgentX throughput includes input, output and cached prompt tokens, not output-only speed (143); ~1000 TPS setting uses fixed speculative acceptance length 5 on 4x B300 (192). Final answer does not repeat headline performance numbers. Source promotes open framework/model engineering, not an overlapping hosted API signup. Followed observed model-card link https://huggingface.co/MiniMaxAI/MiniMax-M3.1-Flash (turn38view1): read model-card opening and specs at 244–258 supporting text/image/video, sparse attention throughout, DSpark head. Did not certify all model-card benchmark claims, graphics, license terms or code recipes. Final target remains independently read engineering article.

3. https://arxiv.org/html/2610.25136v1 — VisMemo paper, Visual Cache Reuse for Efficient Multimodal Inference; submitted 2026-10-18 per https://arxiv.org/abs/2610.25136 (turn39view0). Read motivation/methods, memory/storage backend, evaluation setup, quality table and efficiency/sensitivity/conclusion, refs turn35view1 / turn36view2 / turn37view2 / turn38view2. Uses entropy for patch reuse candidates and warmup attention for query-dependent recomputation, plus differentiated exact/approximate cache policies. Evaluation: two H100 GPUs, Qwen3-VL and GLM-4.6V, VisionArena + four public datasets. Approximate reuse has quality and latency tradeoffs; GLM-4.6V-Flash at 2K input was slower than a cache miss (278), and benefit crossover depends on model/length. Hit-rate numbers differ between abstract and detailed workload discussion; no hit-rate or speedup numbers used in final answer. Paper/research recommendation, not guaranteed lossless caching or production-readiness claim. No hosted-platform CTA central to paper. Read table/text and captions; no claim of independent replication or complete figure inspection.

Final chat: three linked recommendations with source/date/type, concrete learning, Infron editorial value, and suggested angle; no downloadable report.
