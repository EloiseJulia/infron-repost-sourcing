# Infron Repost Sourcing Skill

中文版使用说明 · v0.1.1 · 更新于2026-10-26

帮助 Infron 在 X 上寻找、审核和整理值得 repost 的内容，减少重复浏览、证据核查和历史查重的工作。日常输出通常为 **Model / Other 各一条，最多两条**；没有合适内容时允许空缺。

当前支持两种使用方式：给 AI 一批帖子进行筛选，或让 AI 使用所在环境的搜索工具主动找候选。独立运行的 X API 自动采集器尚未实现。

## 1. 它是怎么工作的？

这个项目由两部分组成：

| 部分 | 负责的工作 |
| --- | --- |
| Skill + AI | 搜索候选，阅读原帖、必要引用、媒体和文章，判断技术价值、品牌适配与事实依据 |
| Python 程序 | 校验审核记录，执行证据、时效和去重规则，维护历史状态，生成简报 |

Python 程序本身不访问 X、不调用大模型，也不会独立看懂图片或证明实验结果。AI 的判断需要实际阅读材料；程序检查的是这些判断及过程记录是否满足约束。

### 能做什么

- 围绕模型发布、评测、推理优化、开发工具和工程经验寻找候选。
- 检查原帖、引用、必要线程、图片、视频及相关链接，继续补读可访问材料。
- 根据开发者价值、技术实质、时效、品牌适配、增量价值进行比较。
- 区分“提及某模型”和“推广业务重叠平台”，不靠公司名称黑名单机械判断。
- 对帖子ID、编辑版本、事件和文章链接做跨次运行去重。
- 记录明确的人类反馈，并将“接受建议”和“已发布”分别保存。

### 当前边界

AI 主动搜索依赖宿主环境提供搜索和浏览器工具，覆盖范围不完整；它不同于稳定的后台采集服务。当前 CLI 的 `automatic_discovery=false` 仍然有效。没有 X API 接入、无人值守运行或定时任务，也不会自动发布内容。

## 2. 最快的使用方式：直接交给 AI

让能读取项目文件的 AI 打开项目根目录，发送：

> 使用 `skills/infron_repost_sourcing/SKILL.md`，为 Infron 寻找本轮值得 repost 的真实内容。先读取当前品牌背景、来源线索、历史与状态库；我没有提供链接时，请主动搜索。完成原帖、必要引用/线程、核心媒体和文章的核验，按新版合同生成审核记录，使用 `review_process_version: 1`。先补读可访问材料，分别记录真正的访问障碍和未完成工作。复用真实状态库，导出到一个新的运行目录，给出简短推荐理由与覆盖缺口。不发布内容。

如果已有链接，在这段指令后附上即可，不必自己填写审核 JSON。AI 应根据实际读取结果生成它。

原项目可用时，Skill 会读取 `workflows/infron-content/02_Brand_Context.md`。本交付包不包含该原始品牌文件；最新明确指示和品牌背景优先于历史推断。

## 3. 安装与环境

### 直接运行交付包

解压后进入同时包含 `skills`、`10.26` 和本 README 的目录，即项目根目录。使用 Python 3.10 或更新版本；筛选程序仅依赖标准库。

```powershell
python skills/infron_repost_sourcing/scripts/repost.py preflight
```

`preflight` 是离线能力说明，不进行网络连通性测试，也不自动读取凭证。

### 放入现有实习项目

在本包根目录，用 PowerShell 7 / 支持 `System.IO.Path.GetRelativePath` 的现代运行环境执行预览：

```powershell
./Install-To-Project.ps1 -ProjectRoot 'C:\Users\v-elzhang\Desktop\MyFolder\Infron internship' -WhatIf
```

确认路径和预览后，去掉 `-WhatIf` 执行复制。脚本只处理 `skills/infron_repost_sourcing` 和 `10.26/bonus_repost_sourcing`，不会复制本 README 或修改品牌背景；本 README 可单独保留在包根目录。

相同内容的文件跳过；同名但不同内容的文件会使脚本在复制前停止，需要逐个比较合并，不能强制覆盖用户修改。该脚本不会注册全局 Skill，也不会远程推送。原 Windows 项目当前未由本轮会话直接写回；下载更新包不等于本机已安装。

## 4. 输入、运行与输出

### 输入

接受真实 X status 链接或包含具体帖子信息的导出材料。输入格式详见 [输入合同](skills/infron_repost_sourcing/references/input-contract.md)。[模板](skills/infron_repost_sourcing/assets/manual-template.json)是明确标注的合成占位材料，不能直接当真实候选运行。

审核记录主要包括：帖子/作者/时间、Model或Other、具体事件、四类证据、事实与品牌判断、优先级、完成度及读取尝试。新审核必须启用 `review_process_version: 1`。旧输入仍可重放，但结果会标记 `completion_enforced=false`，不能当新版流程验证通过。

### 命令

下列路径均相对于项目根目录。`raw.json` 和 `reviewed.json` 由本轮工作生成；输出名称需替换为每次不同的新目录。

```powershell
# 规范化输入，不自动生成语义审核
python skills/infron_repost_sourcing/scripts/repost.py prepare --input raw.json --output normalized.json

# AI完成实际阅读并生成reviewed.json后运行
python skills/infron_repost_sourcing/scripts/repost.py run --input reviewed.json --state 10.26/bonus_repost_sourcing/state/repost.sqlite --history 10.26/bonus_repost_sourcing/04_History_Seed.json --out 10.26/bonus_repost_sourcing/runs/NEW_RUN
```

每次复用同一真实状态库；不要使用合成测试库。运行目录必须不存在，避免覆盖历史结果。同一状态库按顺序运行，不并发启动多轮业务筛选。

### 输出

| 文件 | 用途 |
| --- | --- |
| `brief.md` | 先看这份：主推荐、理由、排除项、障碍和未完成工作 |
| `result.json` | 完整证据、判断、完成状态、去重原因与版本 |
| `candidates.csv` | 可用表格软件查看的候选索引 |
| `state/repost.sqlite` | 跨次运行历史、去重键和明确的人工反馈 |

## 5. 如何理解结果？

| 状态 | 含义 |
| --- | --- |
| Recommend | 当前证据和规则支持推荐；不等于人工批准或已发布 |
| Hold | 当前暂缓，例如关键媒体要求登录、时间矛盾、重复或超时；具体看原因 |
| Reject | 已有明确否决理由，例如不适合的重叠平台推广或已确认错误 |
| deferred | 还没完成审核；可能仍有可执行的下一步，不能算终审Hold |
| alternate | 审核合格，但本轮没有进入有限主推荐位置 |

程序保留底层兼容的 `verdict`，完成阶段另见 `review_status`；deferred可能同时有底层hold值，应以简报、summary及review_status一起理解。存在deferred时整批状态为 `review_incomplete`。`partial_coverage` 表示覆盖有缺口，不能读成“今天X上没有好帖子”。

证据不足时先补读，再判断是否应暂缓：打开引用原帖、展开必要线程、核查图的单位和条件；普通检索失败可尝试适当的浏览器读取。确实遇到登录、删除或不可播放等障碍时记录具体对象和实际尝试。详情见 [证据补读流程](skills/infron_repost_sourcing/references/evidence-completion.md)。

## 6. 默认规则与历史

默认Model分享窗口为48小时，Other为7天，审核记录有效期为24小时；最多30条输入、20条深读、2条主推荐。具体值位于 [config.json](skills/infron_repost_sourcing/assets/config.json)。这些是初版暂定设置，不是mentor认可的硬标准。较旧但有当前价值的内容，需要具体的 `evergreen_reason`，不能为通过时效检查虚构理由或改日期。

历史分析记录了14条官号动作，但不是完整历史。官号过去分享过某类内容，只能用来校准，不能推出全部同类内容都获认可；没有分享也不等于否决。已推荐、已观察历史或明确已发布会参与去重，单纯见过或暂缓的帖子可在补足证据后复审。

## 7. 测试过吗？

截至2026-10-26，已完成：

- 官方 `quick_validate.py` 基础结构校验通过。
- 17项原有行为测试及7项完成度测试通过，共24项。
- 新上下文审核6条合成材料：2推荐、2Hold、1deferred、1Reject，能够区分未尝试读取和真正障碍。
- 6条真实候选主动搜索与补读：最新一轮1条新推荐、3条关键媒体访问障碍、1条上轮推荐重复、1条超时。旧轮次文件保持原样，不能把各轮推荐数当独立候选累加。

最新真实推荐为SGLang Omni工程内容，核对了一手文章核心章节、评测表和六张架构图；可选演示未播放，未独立复现实验。现有历史未重复不等于完整实时官号历史从未分享，采用前仍应重查。

这些结果说明已覆盖的程序行为与流程可用，不证明真实推荐准确率、mentor采用率或节省的时间。CLI自动采集尚未测试，因为功能未实现。

### 本地复验

```powershell
python -m unittest discover -s skills/infron_repost_sourcing/scripts -p 'test_*.py'
python 10.26/bonus_repost_sourcing/validation/tools/quick_validate.py skills/infron_repost_sourcing
```

仅官方校验器需要PyYAML。若当前解释器缺少它，在该解释器的虚拟环境中执行 `python -m pip install PyYAML`；筛选程序不需要该依赖。测试使用合成数据与独立临时状态，不修改真实业务库。

## 8. 从哪里继续看？

| 内容 | 文件 |
| --- | --- |
| AI执行入口 | [SKILL.md](skills/infron_repost_sourcing/SKILL.md) |
| 历史案例分析 | [04_History_Analysis.md](10.26/bonus_repost_sourcing/04_History_Analysis.md) |
| 数据入口与缺口 | [05_Data_Access_Verification.md](10.26/bonus_repost_sourcing/05_Data_Access_Verification.md) |
| 首轮结构与行为验证 | [06_Validation.md](10.26/bonus_repost_sourcing/06_Validation.md) |
| 详细使用命令 | [07_Usage.md](10.26/bonus_repost_sourcing/07_Usage.md) |
| 主动寻找真实候选 | [08_Real_Search_Trial.md](10.26/bonus_repost_sourcing/08_Real_Search_Trial.md) |
| 最新完成度改进与复核 | [09_Completion_Improvement.md](10.26/bonus_repost_sourcing/09_Completion_Improvement.md) |

后续重点是接入团队授权的只读X接口，补齐请求/资源/费用上限、分页游标与失败处理，并通过真实使用反馈改进编辑规则。当前不需要先请mentor整理一套完整标准；具体接受或否决意见可以在日常使用中逐步积累。
