# 主动搜寻与六条真实候选试用

日期：2026-10-26。用户未提供候选链接；本轮由AI公开搜索发现，逐条在浏览器原帖详情读取。没有使用Arena旧帖或合成数据替代。

## 实际结果

程序真实执行退出码0：6输入、1推荐、5Hold、0Reject，partial_coverage。输入见 `samples/real-search-batch-20261026.json`，输出见 `runs/real-search-20261026-01/`，命令结果见 `validation/real-search-batch-test.json`。使用已有真实state与14条历史种子；未导入fixture或人工认可。

| 原帖ID / 作者 | 内容 | 结果与阅读范围 |
| --- | --- | --- |
| 2113093747261243448 / lmsysorg | 弹性EP扩容 | Recommend Other。主帖、文章正文与四图已查；官方仓库README的X链接验证作者。可分享部署设计；不能写成无暂停、零故障。 |
| 2114135647040778667 / vllm_project | AgentX性能优化 | Hold。主帖及工程文章正文已读；主帖图和引用细节未核完。 |
| 2114080639381320028 / lmsysorg | SGLang/DeepInfer | Hold。原帖全文已读，引用截断、图未核完，文章访问失败。 |
| 2113301090502639666 / lmsysorg | Trainium beta | Hold。原帖已读，引用/图、文章和报名去向未核完。 |
| 2113451250264240545 / vllm_project | MiniMax模型支持 | Hold。视频不能播放、线程和引用不完整；超Model默认48小时窗口。 |
| 2112625536350740896 / lmsysorg | Omni交互运行时 | Hold。主帖已读，关键文章/演示访问不足。 |

推荐表示在当前编辑规则与已取得历史范围内值得进一步采用，不是mentor认可或发布授权。没有发现与本地历史相同的帖子/事件，但没有重新取得官号完整实时历史，不能保证从未分享；发布前需再查。Model位置空缺，不用旧发布凑数。

## 搜索与访问记录

初轮公开搜索（四个查询）：`site:x.com vllm release October 2026`、`site:x.com Qwen model October 2026 release`、`site:x.com SGLang inference benchmark October 2026`、`site:docs.x.com recent search pricing pay per use`。结果偏旧且含trending摘要，未将这些摘要作为候选正文。

第二引擎三个来源查询，recency=14：`site:x.com/vllm_project/status "Oct" "2026"`、`site:x.com/Alibaba_Qwen/status "Oct" "2026"`、`site:x.com/lmsysorg/status "Oct" "2026"`。从结果选取六条具体status URL。上述为本次实际探索查询，后续工作流采用六查询上限，本次共七查询含一条API文档查询。

搜索检索直接打开六条X均返回403；浏览器原帖详情则可读。浏览器无登录的公开预览显示部分引用截断与不可播放视频，没有登录或读取凭证。本轮媒体截图仅用于内部核验，未保存到交付物。

发布时间由实际X post ID按Snowflake规则解码并对照页面日期；避免把搜索引擎时区展示当作北京时间。审核时间用实际执行UTC时间，显示层可换算北京时间。

## 自动候选的实施路线

已加入 `references/search-assisted-sourcing.md`：用户不给链接时，AI主动调用宿主搜索工具发现候选，再阅读审核。六条真实试用证明本轮能主动找链接并产出一个推荐，但不是无人值守自动采集。

稳定独立运行应接团队授权X只读API/已有内部服务。官方recent search需approved App和Bearer Token，查询近7日；按用量计费，需要明确费用上限。后续需实现分页、游标、资源预算、失败状态与结构适配，再做真实接入测试。本轮未实现或调用该采集器，没有费用、购买或定时任务。

Skill与Python程序边界保持清晰：宿主AI主动搜寻已经试用；CLI自动发现仍未实现。现有配置与JSON中的automatic_discovery=false保留，不把搜索试用包装成API接入成功。

主要一手核验链接：
- https://www.lmsys.org/blog/2026-10-21-elastic-ep-scaling-nixl
- https://github.com/sgl-project/sglang （README的X链接指向lmsysorg）
- https://vllm.ai/blog/2026-10-23-deepseek-v41-flash-pd-wide-ep
- https://docs.x.com/x-api/posts/search/quickstart/recent-search
- https://docs.x.com/x-api/getting-started/pricing
