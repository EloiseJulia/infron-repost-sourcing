# Repost Sourcing v0.1 使用说明

当前版本为 **项目内手工输入筛选模式**。自动发现未实现；没有发布、购买、部署或调度。

2026-10-26接续验证：用户上传包在Linux环境已通过官方quick_validate和17项行为测试，合成重放为2推荐、3Hold、1Reject。见 `06_Validation.md` 和 `validation/*-current.json`。原Windows缺少PyYAML的日志仅表示当时状态；本轮未连接或写回Windows目录。

## 文件位置与写回状态

原项目：`C:\Users\v-elzhang\Desktop\MyFolder\Infron internship`。

本轮暂存项目：
`C:\Users\v-elzhang\Documents\Codex\2026-10-26\prompt-10-26-bonus-repost-sourcing\outputs\Infron_Repost_v0_1`。

桌面项目可读，但新建目录返回 WinError 5。**未宣称已写回桌面。** 当前目录可直接运行。结构与预期一致：

- `skills/infron_repost_sourcing/`：skill、语义规则、12条来源线索、输入模板、脚本与测试。
- `10.26/bonus_repost_sourcing/`：14条历史分析/机器记录/去重种子、入口验证、真实试跑、验证和状态。
- `Install-To-Project.ps1`：只补本任务新增文件；同名同内容跳过，同名不同内容在复制前停止，保留手改。不会修改原设计、品牌背景或设计系统skill。

在正常PowerShell中，从暂存项目运行：
`./Install-To-Project.ps1 -ProjectRoot 'C:\Users\v-elzhang\Desktop\MyFolder\Infron internship'`。
可加 `-WhatIf` 先看复制范围。该脚本不会推送、发布或全局安装skill。

## 新 session 直接调用

把下面这段交给在项目根目录工作的AI：

> 读取 skills/infron_repost_sourcing/SKILL.md 和当前 workflows/infron-content/02_Brand_Context.md。对我提供的X链接做手工输入筛选，实际读取原帖/必要引用/媒体/相关链接，按合同填写 reviewed.json；使用现有 10.26/bonus_repost_sourcing/state/repost.sqlite 和 04_History_Seed.json 去重，导出新run。通常Model/Other各一，最多两条，缺证据进入Hold，不凑数。说明覆盖范围与自动发现尚未实现；不发布。

若桌面仍不可写，可直接指定本轮暂存项目的绝对路径。没有新链接时，不凭空生成真实候选；可重放已存真实样例或运行fixture验证。

## 命令

从本说明对应项目根目录运行：

```powershell
python skills/infron_repost_sourcing/scripts/repost.py preflight
python skills/infron_repost_sourcing/scripts/repost.py prepare --input raw.json --output normalized.json
```

`prepare`不生成语义判断。AI读完材料后，根据输入合同生成 `reviewed.json`，再运行：

```powershell
python skills/infron_repost_sourcing/scripts/repost.py run --input reviewed.json --state 10.26/bonus_repost_sourcing/state/repost.sqlite --out 10.26/bonus_repost_sourcing/runs/NEW_RUN --history 10.26/bonus_repost_sourcing/04_History_Seed.json
```

输出目录必须是新路径，防止覆盖历史。复用同一真实state；不要使用fixture.sqlite。运行时间默认真实当前时间，超过核查TTL/分享窗口会转Hold，需重新读取而不是改日期绕过。

重放本次真实历史样例（固定历史as-of，不是今天的新推荐）：

```powershell
python skills/infron_repost_sourcing/scripts/repost.py run --input 10.26/bonus_repost_sourcing/samples/real-reviewed-current.json --state 10.26/bonus_repost_sourcing/state/repost.sqlite --out 10.26/bonus_repost_sourcing/runs/REPLAY_NEW --history 10.26/bonus_repost_sourcing/04_History_Seed.json --as-of 2026-10-26T15:40:00+08:00
```

最新真实结果：`runs/real-20261026-02/brief.md`，1输入、0推荐、1Hold。其理由包括未完成的引用/完整图表核验、事实/身份缺口、窗口与历史重复。不是“今天X没有好帖”。

完整审核见 `result.json`；短索引见 `candidates.csv`。推荐与人工批准/实际发布分开记录。只有用户明确反馈时才执行：

```powershell
python skills/infron_repost_sourcing/scripts/repost.py feedback --state 10.26/bonus_repost_sourcing/state/repost.sqlite --post-id POST_ID --action defer --actor ACTOR --reason EXPLICIT_REASON --reference FEEDBACK_REFERENCE
```

可用反馈为accept/reject/defer/posted；accept不会标posted。上述大写项是待填写参数，不能把它们当真实反馈运行。

## 复验与边界

`python skills/infron_repost_sourcing/scripts/test_repost.py` 运行显式合成行为测试。独立新上下文的6条fixture审核位于 `validation/forward-use/`，结果为2推荐、3Hold、1Reject，**不是真实候选或mentor认可**。

首次真实运行 `real-20261026-01` 保留了初期访问缺口与人为指定的历史测试as-of；后续 `-02` 使用真实执行时间并更新媒体读取状态、纯repost读取结果与历史种子。以 `-02` 作为交接样例，不把初期登录缺口当作最终状态。

程序只校验审核声明，不能独立理解语义、辨认图片竞品或核验实验真实性。真实发现能力、采用率和节省人工时间仍待后续接入与人工反馈验证。

