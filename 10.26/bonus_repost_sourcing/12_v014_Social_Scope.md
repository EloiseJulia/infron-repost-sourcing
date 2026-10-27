# v0.1.4 社媒选帖范围调整

日期：2026-10-27。

用户明确：只找 X/LinkedIn 能 repost 的原帖。入口为指定模型/功能主题，或与 Infron 业务有关的热点机会。

已修改 SKILL.md、界面提示、编辑规则优先级和中文 README。移除默认“官网文章替代社媒原帖”出口；官网仅作事实核实。新增两路发现、热度证据与业务参与角度。保留旧脚本和历史证据。

结构校验：quick_validate.py 实际运行通过；git diff --check 通过。本次未改运行代码，未重跑旧代码测试。

独立上下文实测：指定主题“推理成本/缓存”，4个查询策略，覆盖两平台，实际读取5条 LinkedIn 正文，最终推荐1条 Pulkit Tyagi《The prefix stability test》：https://www.linkedin.com/posts/pulkit0111_the-prefix-stability-test-activity-7516809772109565953-0jWK 。页面显示2d，未核验精确发布日期。推荐理由为稳定前缀、缓存token/TTFT/费用验证；没有官网推荐或未经证实的 Infron 支持承诺。主线程重新打开核对了正文。未检查官号历史，未建立热点结论。

热点机会独立实测：4个查询策略，读取3条LinkedIn全文和1篇vLLM官方背景博客。推荐1条 Joydeep Bhattacharjee 的 Kimi K3 decode 优化解读：https://www.linkedin.com/posts/joydeep-bhattacharjee-934a1157_vllm-unlock-major-kimi-k3-speed-gains-a-activity-7519200673326927872-vjBF 。页面显示4d。以多作者讨论作为有限注意力信号，不称爆款。另一候选把130/69微秒写为毫秒而被排除；另有平台推广候选未采用。正文推荐连接到推理工作负载和配置判断，没有宣称Infron性能收益。

两次均已验证能交付真实社媒链接与具体业务关联，但每次只有1条，尚未证明每次稳定返回2–3条，也没有X成功推荐样本。部分 X 及外链访问失败；没有绕过登录限制，也没有发布操作。
