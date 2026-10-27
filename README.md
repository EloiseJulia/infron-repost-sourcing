# Infron 社媒转发选帖 Skill

中文版 · v0.1.4

输入一句话，让 AI 自己在 X、LinkedIn 找适合 Infron 转发或加评论分享的原帖，直接在聊天里推荐，通常 2–3 条。

## 两种用法

已经确定主题（模型、功能或活动）：

> 读取 skills/infron_repost_sourcing/SKILL.md，帮 Infron 找关于【模型/功能/主题】值得 repost 的 X 或 LinkedIn 原帖。直接给链接、内容重点、推荐理由和分享切入点。

还没确定主题，主动找热点机会：

> 读取 skills/infron_repost_sourcing/SKILL.md，自己搜索近期与 Infron 业务有关、适合我们参与讨论的热点，推荐 2–3 条可 repost 的 X 或 LinkedIn 原帖。说明热度依据、业务关联和分享切入点。不发布内容。

## 筛选与交付

只推荐具体社媒原帖，附作者、平台、日期、内容价值、Infron 参与理由，以及转发或 quote/评论建议。官网、论文、GitHub 等仅核实背景，不能替代原帖成为推荐结果。某条读不到就换作者、原帖或平台。

按开发者价值、技术内容、时效、品牌适配和信息增量筛选。热点需要可观察的讨论/互动或事件依据，不能把“刚发布”直接叫作“很火”。不编造 Infron 支持的模型、功能、优惠或合作；避免放大业务重叠平台的推广。

## 使用条件

AI 需要能读取项目、联网搜索并读取社媒原帖。无需先给链接、填 JSON 或跑 Python，默认直接聊天输出，不生成独立报告。通常推荐 2–3 条，但不能用未读链接或官网文章凑数。所有社媒入口受阻时必须说明；当前没有独立 X/LinkedIn API 采集器。

日常只看本 README；AI 从 skills/infron_repost_sourcing/SKILL.md 进入，读取 workflows/infron-content/02_Brand_Context.md。旧脚本、规则和测试保留供内部使用。明确要求发布前审核时才进入更严格流程。

不自动发布、点赞、私信、购买、部署或启动定时任务。推荐不代表 mentor 审批或发布授权。
