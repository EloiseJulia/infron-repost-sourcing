# Infron Repost Sourcing v0.1

**手工输入复核 — 未实现自动发现。**

Run `20261026T083632Z-d5feb6a1` · 2026-10-26T08:36:32.723816+00:00 · rules `0.1.1-2026-10-26`

状态：partial_coverage；输入 6，同批重复 0，深读 6。
主推荐 1；Hold 5；未完成 0；Reject 0；合格备选 0。

本结果仅覆盖所供材料；不代表全 X 搜索结论。recommend 不等于批准或已发布。

## 主推荐

### Other · [@lmsysorg](https://x.com/i/web/status/2112625536350740896)

发布时间：2026-10-20T19:22:33.207000+00:00；核查：2026-10-26T08:36:32.691236+00:00。

SGLang Omni全双工运行时

分享理由：近7日工程深读，适合向开发者解释全双工不只看延迟，也要看打断策略与session状态。

建议：pure_repost。增量：未命中现有14条历史与state；仍未取得官号完整实时历史。

品牌：围绕开源交互运行时和架构取舍；模型/工具作为技术对象，不是重叠推理平台的注册推广。

事实：作者报告的0.17s/1.32s与表格一致，单H200/单会话/关闭thinking条件明确；小样本噪声与VAD误打断限制已读。未复现实验、未观看可选演示。

身份：官方sgl-project/sglang仓库README的X链接指向lmsysorg；LMSYS站点确认项目关联

证据范围：text=full (浏览器原帖详情完整正文；发布时间由X ID时间戳计算，与页面日期对照，非搜索摘要时间。); quote=not_present (原帖详情未见引用卡); media=not_present (原帖仅文章预览卡，没有独立上传图/视频); links=full (已读核心架构/评测方法、完整结果表/脚注、使用与Known Issues；六张架构图逐张视觉核查。可选YouTube演示未播放，不用于支持评测数字或额外功能主张。)

- audience_value: medium — 可读内容有技术线索，证据尚不完整
- substance: medium — 可读内容有技术线索，证据尚不完整
- timeliness: medium — 可读内容有技术线索，证据尚不完整
- brand_fit: medium — 可读内容有技术线索，证据尚不完整
- increment: medium — 可读内容有技术线索，证据尚不完整

关键主张：
- 原帖单会话H200级联配置的作者报告延迟与文章结果表相符；不外推为通用SLA或独立复现实验。：verified；https://www.sglang.io/blog/omni-interactive-runtime#results

剩余缺口：无核心读取缺口；发布前仍需重开原帖复核。

## Hold / Reject / 备选

| 帖子 | 结论 | 原因 |
|---|---|---|
| [@lmsysorg](https://x.com/i/web/status/2113093747261243448) | hold | editorial_hold; historical_duplicate — 上轮已选入主推荐，本轮跳过重复。 |
| [@vllm_project](https://x.com/i/web/status/2114135647040778667) | hold | incomplete_evidence; identity_unverified; facts_unverified; brand_unknown; editorial_hold — 存在实际观察到的关键媒体登录障碍；其余未读对象保持原状，不算访问失败。 |
| [@lmsysorg](https://x.com/i/web/status/2114080639381320028) | hold | incomplete_evidence; facts_unverified; brand_unknown; editorial_hold — 存在实际观察到的关键媒体登录障碍；其余未读对象保持原状，不算访问失败。 |
| [@lmsysorg](https://x.com/i/web/status/2113301090502639666) | hold | incomplete_evidence; facts_unverified; brand_unknown; editorial_hold — 存在实际观察到的关键媒体登录障碍；其余未读对象保持原状，不算访问失败。 |
| [@vllm_project](https://x.com/i/web/status/2113451250264240545) | hold | incomplete_evidence; identity_unverified; facts_unverified; brand_unknown; outside_editorial_window; editorial_hold — 已超Model默认48小时；保留原视频/线程缺口，不继续为过期新闻消耗审核。 |

## 覆盖与资源

窗口：2026-10-26主动公开搜索发现6条新真实候选；非X API自动采集或完整全站覆盖。

已成功：三组来源搜索得到真实status链接，逐条浏览器读取6篇原帖, 弹性EP文章正文及四图完成核验；vLLM工程文章正文读取, 对照本地14条历史动作与持久状态去重, 补读Trainium和DeepInfer引用全文及博客正文, 补读Omni文章核心章节、评测表/限制并视觉核查六张架构图。

未覆盖/失败：公开媒体点击显示登录提示，三条候选的关键媒体仍被阻挡；有明确对象/尝试记录; 完整实时官号历史未取得；CLI自动发现未实现；可选Omni YouTube演示未播放，不以其证明指标。

自动发现：not_implemented；API 请求 0；本地脚本模型调用 0；本地脚本付费消耗 0。

预算：输入上限 30；深读上限 20。

语义判断由运行该 skill 的 agent/editor 提供，未测量其 token、耗时或成本。

反馈：使用 feedback 命令记录 accept/reject/defer/posted；只记录用户明确给出的事实。
