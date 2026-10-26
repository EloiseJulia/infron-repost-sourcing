# 证据补读与审核完成度改进

2026-10-26；规则版本0.1.1。初版的问题不只是访问条件：它擅长发现缺口，却没有强制把能够补读的材料读完。上一轮把普通检索失败、尚未打开的引用和真实媒体登录障碍一起写成Hold，降低了实际交付价值。

## 修改

- 新增 `references/evidence-completion.md`，规定截断引用、线程、图片、视频、文章、身份的补读路径与适当停止条件。
- 新审核使用 `review_process_version: 1` 和 completion记录。普通单一路径失败不能宣称访问无解；记录具体method/locator/outcome。真正的登录、删除、媒体不可播放等障碍可以提前停止，未读的其他材料保持真实状态。
- 程序检查新合同，pending/budget-exhausted必须为deferred；简报、JSON、CSV显示完成状态，summary单列deferred，不把它计入Hold。存在deferred时状态为review_incomplete。
- 明确重复、过期、已知否决项可先退出，避免为已经没有推荐价值的帖子无限补材料。兼容旧输入，但输出completion_enforced=false，不能冒充新流程验证通过。
- 更新模板、调用说明、UI提示和测试。保留旧样例及日志，未覆写历史判断，没有自动发布或接通付费采集。

## 本轮真实复核

输入 `samples/real-completion-batch-20261026.json`；输出 `runs/real-completion-20261026-01/`；命令/结果 `validation/real-completion-test.json`。6条复核，1推荐、5Hold、0deferred、0Reject。5Hold由3个硬媒体障碍、1个历史重复、1个超时构成，不能解读为5条仍有可继续做却没做的任务。

| 候选 | 本轮采取的动作与结果 |
| --- | --- |
| SGLang弹性EP | 上轮state已有交付推荐，跳过重复；不覆盖原推荐历史。 |
| vLLM AgentX | 实际点击关键图，显示登录提示；以具体媒体障碍停止，原引用/文章未全部完成的范围仍保留。 |
| SGLang/DeepInfer | 打开原始引用完整正文；博客浏览器可读，撤销“文章不可访问”的旧判断。点击引用图触发登录提示；其余附图未穷尽，保留partial。 |
| Trainium | 原始引用全文、博客正文、beta CTA目标均已读；关键引用图点击后要求登录，仍Hold。不把AWS名字本身当否决理由。 |
| MiniMax模型支持 | 已超48小时默认新闻窗口，没有新的当前分享理由；提前停止，不为过期新闻继续付出视频审核。 |
| SGLang Omni | 博客实际可读；补读核心架构、评测表/脚注、方法与Known Issues，逐张视觉检查六张结构图。进入Recommend Other。 |

Omni的作者报告延迟与文章表格相符，不能写成独立实验复现、通用SLA或没有误打断问题。可选YouTube演示没有播放，不用于证明性能或额外功能；本次核心主张依据一手文章表格/方法与原帖。既不无限展开所有背景链接，也不绕开关键证据。

未重新取得官号完整实时分享历史；推荐仅在现有历史与state范围去重。当前仍为宿主AI主动搜索与审核，CLI自动发现没有实现。Windows原项目未连接或写回。

## 验证

原有17项行为测试通过，新增7项完成度测试通过。新增覆盖：pending不能伪装成终审、普通单路径失败需补读、硬障碍与预算用尽区分、假缺失/提前推荐拒绝、整批无效输入不写库、deferred简报单列。日志见validation中的011文件。官方quick_validate再次通过。

独立新上下文按当前Skill审核原始6条合成材料，得到2推荐、2Hold、1deferred、1Reject，completion_enforced=true，review_incomplete。它识别了时间矛盾；对缺少实际读取尝试的视频不编造认证障碍，标为deferred。产物保存于 `validation/completion-forward/`。合成测试不是真实推荐或mentor认可。

这些检查保证记录约束和已覆盖分支行为；程序不能证明AI真的读过网页，不能消除平台登录限制，也不保证未来推荐采用率。旧版本省略新字段仍可运行，是显式兼容路径；新工作要求启用v1。
