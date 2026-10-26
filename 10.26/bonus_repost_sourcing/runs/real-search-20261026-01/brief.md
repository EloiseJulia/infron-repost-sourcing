# Infron Repost Sourcing v0.1

**手工输入复核 — 未实现自动发现。**

Run `20261026T082520Z-f3bd9e6d` · 2026-10-26T08:25:20.461520+00:00 · rules `0.1.0-2026-10-26`

状态：partial_coverage；输入 6，同批重复 0，深读 6。
主推荐 1；Hold 5；Reject 0；合格备选 0。

本结果仅覆盖所供材料；不代表全 X 搜索结论。recommend 不等于批准或已发布。

## 主推荐

### Other · [@lmsysorg](https://x.com/i/web/status/2113093747261243448)

发布时间：2026-10-22T02:23:03.387000+00:00；核查：2026-10-26T08:25:20.427317+00:00。

SGLang弹性EP扩容

分享理由：近7日工程内容，围绕MoE扩容的实际运维问题

建议：pure_repost。增量：未命中本地14条历史动作及状态；未证明完整实时官号历史均无重复

品牌：开源推理工程设计，无推理聚合平台注册CTA；NVIDIA与Mooncake为技术依赖/贡献方

事实：原帖全文、文章全文及四图已检查；扩容准备期间维持服务，但提交转换阶段token有暂停，不能写成零中断。

身份：官方sgl-project/sglang仓库README的X链接指向lmsysorg；LMSYS站点确认项目关联

证据范围：text=full (浏览器原帖详情完整正文；发布时间由X ID时间戳计算，与页面日期对照，非搜索摘要时间。); quote=not_present (原帖详情未见引用卡); media=not_present (原帖仅文章预览卡，没有独立上传图/视频); links=full (原帖全文、文章全文及四图已检查；扩容准备期间维持服务，但提交转换阶段token有暂停，不能写成零中断。)

- audience_value: high — 解决扩容粒度与重启代价问题，有工程约束和实现说明
- substance: high — 解决扩容粒度与重启代价问题，有工程约束和实现说明
- timeliness: medium — 解决扩容粒度与重启代价问题，有工程约束和实现说明
- brand_fit: medium — 解决扩容粒度与重启代价问题，有工程约束和实现说明
- increment: medium — 解决扩容粒度与重启代价问题，有工程约束和实现说明

关键主张：
- 文章说明MoE部署在线扩容的设计，同时明确转换阶段存在token暂停：verified；https://www.lmsys.org/blog/2026-10-21-elastic-ep-scaling-nixl

剩余缺口：无核心读取缺口；发布前仍需重开原帖复核。

## Hold / Reject / 备选

| 帖子 | 结论 | 原因 |
|---|---|---|
| [@vllm_project](https://x.com/i/web/status/2114135647040778667) | hold | incomplete_evidence; identity_unverified; facts_unverified; brand_unknown; editorial_hold — 主帖和工程文章已读；主帖性能图及必要引用未独立读全，不能把总token吞吐当输出吞吐或收入当利润。 |
| [@lmsysorg](https://x.com/i/web/status/2114080639381320028) | hold | incomplete_evidence; facts_unverified; brand_unknown; editorial_hold — 主帖全文可读，引用原帖截断且图未核验；文章检索访问失败。 |
| [@lmsysorg](https://x.com/i/web/status/2113301090502639666) | hold | incomplete_evidence; facts_unverified; brand_unknown; editorial_hold — 主帖全文可读，引用与图未读全，beta报名去向及品牌边界待核实；不因AWS名称直接否决。 |
| [@vllm_project](https://x.com/i/web/status/2113451250264240545) | hold | incomplete_evidence; identity_unverified; facts_unverified; brand_unknown; outside_editorial_window; editorial_hold — 主帖全文可读，但1/5线程未读全、视频显示无法播放、引用截断；模型材料未核验，且超过48小时默认窗口。 |
| [@lmsysorg](https://x.com/i/web/status/2112625536350740896) | hold | incomplete_evidence; facts_unverified; brand_unknown; editorial_hold — 主帖全文可读，限定单会话和H200；关键博客与演示未读取，延迟结论未完成核查。 |

## 覆盖与资源

窗口：2026-10-26主动公开搜索发现6条新真实候选；非X API自动采集或完整全站覆盖。

已成功：三组来源搜索得到真实status链接，逐条浏览器读取6篇原帖, 弹性EP文章正文及四图完成核验；vLLM工程文章正文读取, 对照本地14条历史动作与持久状态去重。

未覆盖/失败：搜索引擎覆盖不完整；未重新取得完整Infron实时分享历史; 5条存在引用/媒体/相关文章缺口; 没有授权X API配置及费用上限；未调用付费API。

自动发现：not_implemented；API 请求 0；本地脚本模型调用 0；本地脚本付费消耗 0。

预算：输入上限 30；深读上限 20。

语义判断由运行该 skill 的 agent/editor 提供，未测量其 token、耗时或成本。

反馈：使用 feedback 命令记录 accept/reject/defer/posted；只记录用户明确给出的事实。
