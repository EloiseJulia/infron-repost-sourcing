# Infron Repost Sourcing Skill
中文版 · v0.1.2 · 2026-10-26

**你说“帮 Infron 找今天值得 repost 的内容”，AI自己搜索、读帖、比较、查重，最后给你最多两条推荐。你不用先找链接或填写JSON。**

## 日常怎么用

在可以读取本项目、具备搜索和浏览器工具的AI中发送：

> 使用 skills/infron_repost_sourcing/SKILL.md，帮 Infron 找今天值得 repost 的真实内容，通常Model和Other各一条。自己搜索，说明原帖链接、为什么值得分享及核验情况。没有合适的就说明，不凑数。不发布内容。

Model包括模型发布、能力变化和评测；Other包括推理优化、开发工具、部署和工程经验。允许空缺。

## 看哪个文件？

日常看聊天里的推荐摘要即可。需要保存或回看时，打开本轮的brief.md。

| 文件 | 谁使用 / 用途 |
| --- | --- |
| README.md | 你：了解如何使用 |
| skills/infron_repost_sourcing/SKILL.md | AI：唯一执行入口 |
| workflows/infron-content/02_Brand_Context.md | AI：品牌背景；原项目更新版本优先 |
| 10.26/bonus_repost_sourcing/runs/ | 每轮结果，通常只看对应brief.md |
| references、scripts、assets | AI/程序的内部规则、代码和配置 |
| state、validation和编号文档 | 历史记忆、测试、分析，不需每次阅读 |

## 推荐标准

- 开发者价值：读者能学到什么、改善什么工作或选择？
- 内容实质：是否有具体方法、数据、代码和限制，而不是只有口号？
- 时效：为什么现在值得分享？
- 品牌适配：模型和工程知识可以考虑；推广业务重叠产品时优先换帖，官方账号不自动放行。
- 增量：相比官号历史及已推荐内容，有没有新信息？

你的最新要求和当前品牌背景优先。14条历史动作只是小样本，不是mentor全面认可。不按点赞阈值或自动总分推荐。

AI负责阅读和编辑判断；Python检查记录、时间、重复和完成状态，不能证明AI真的读过网页。

## v0.1.2改进

上轮真实任务发现19条线索却耗在一篇多图文章上，0推荐，业务目标未达成。这次针对性修改：

1. Model和Other分别至少两次搜索，使用来源账号+月份查询，不把调用全耗在窄关键词或单一弱引擎。
2. 深读前先比较候选价值、重复和阅读成本，排交替队列。
3. 首轮单条六次证据打开后换备选，不让一篇文章占满整轮。
4. 先确定原帖核心主张，再读决定推荐的证据；不机械审核所有补充硬件图。核心性能图、原帖媒体和推广信息仍不能跳过。
5. 历史快照仅取去重键，避免旧审核内容混入新判断。
6. 聊天先给推荐和简报链接，详细日志留在文件中。

## 每次输出什么？

完整执行一次会保存brief.md简报、result.json审核记录、candidates.csv索引及SQLite历史。普通解释问题不需要另跑报告。

| 结果 | 含义 |
| --- | --- |
| Recommend | 当前支持推荐，不等于批准或已发布 |
| Hold | 暂缓，具体可能是访问障碍、重复、超时或时间矛盾 |
| Reject | 有明确否决理由 |
| deferred | 还没审核完，不能算完成的Hold |

有deferred时整轮标为review_incomplete。发现数、分流数、真正深读数分别记录。成功导出文件不代表成功找到推荐。

## 维护者命令

Python 3.10+，业务程序只需标准库；从项目根目录执行：

```powershell
python skills/infron_repost_sourcing/scripts/repost.py preflight
python skills/infron_repost_sourcing/scripts/sourcing_plan.py history --state 10.26/bonus_repost_sourcing/state/repost.sqlite --output history-snapshot.json
python skills/infron_repost_sourcing/scripts/sourcing_plan.py plan --input triage.json --output plan.json
python skills/infron_repost_sourcing/scripts/repost.py run --input reviewed.json --state 10.26/bonus_repost_sourcing/state/repost.sqlite --history 10.26/bonus_repost_sourcing/04_History_Seed.json --out 10.26/bonus_repost_sourcing/runs/NEW_RUN
python -m unittest discover -s skills/infron_repost_sourcing/scripts -p 'test_*.py'
```

JSON由AI生成，格式见Skill入口和input-contract。使用新输出路径，真实工作复用同一state；合成测试用独立库和--fixture。preflight是离线说明，不是网络测试。

默认Model 48小时、Other 7天、审核记录24小时有效，最多30输入、20审核、2条主推荐。这些是初版参数，不是mentor硬标准。旧内容要有真实具体的当前价值才能例外，不能改日期凑数。

安装脚本只复制Skill与bonus目录；README和品牌背景需比较后单独合并。同名不同内容会停止，不能强制覆盖。不会全局注册Skill。当前Windows工作目录可访问，不等于桌面原项目已经更新。

## 当前边界

独立X API采集尚未实现，当前靠AI调用宿主工具主动搜索。搜索覆盖、媒体登录和事实核验可能受限。业务采用率尚未验证，测试通过不能代表mentor认可。没有发布、购买、部署、远程推送或定时任务。当前验证与恢复情况见10.26/bonus_repost_sourcing/10_v012_Validation.md。
