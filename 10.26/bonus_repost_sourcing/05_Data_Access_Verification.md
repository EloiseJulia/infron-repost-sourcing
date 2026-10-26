# 数据入口验证 · 2026-10-26

**已验证：手工页面读取和离线筛选可用。未实现：持续自动发现、API连接、分页和采集游标。**

| 入口 | 本次实际操作 | 结论 |
|---|---|---|
| 官方GitHub | 读取主页中的X链接 | @InfronAI关联已核验 |
| 搜索/网页直读 | 搜索X链接，直接打开官号 | 搜索可作线索；直读返回403，不等于帖子不存在 |
| 浏览器公开预览 | 读官号/个别原帖；点击转帖/图片 | 初期出现登录门槛，已及时说明 |
| 同一浏览器后续正常页面 | 人工读Posts、Reposts及原帖/部分图 | 历史访问后来恢复，最终确认14条动作；不是自动数据入口 |
| 官方X API文档 | 阅读认证、近期搜索、时间线、expansions、计费 | 文档可读；实际账号权限、余额和调用未测试 |
| 团队内部服务 | 启动文件和明确配置说明未提供可用入口 | 未扫描私人key、cookie、密码或全盘配置；不能断言团队没有服务 |
| v0.1 preflight | 实际运行本地命令 | 只报告实现边界/缺口；不伪装API连通性测试 |

目前唯一必要接入问题：**团队是否有可复用、已授权的 X 只读 App／数据服务？若有，请给安全配置方式或接入文档，并明确一次试跑的费用上限。** 不需要把 token 发进聊天，不需要 Infron 模型推理 API key，也没有新购买/充值的必要前提。

公开文档描述 Recent Search 为最近7天，需要获准App和Bearer Token。计费文档为预付credits、按使用量计费，读操作按资源计费；实际费率、expansions成本和权限应在团队控制台确认。未发出带凭证请求，API请求0、付费试跑0；这不是“测试连接成功”。

一手资料：
- [Recent Search](https://docs.x.com/x-api/posts/search/quickstart/recent-search)
- [Pricing](https://docs.x.com/x-api/getting-started/pricing)
- [Timelines](https://docs.x.com/x-api/posts/timelines/integrate)
- [Expansions](https://docs.x.com/x-api/fundamentals/expansions)
- [Developer Guidelines](https://docs.x.com/developer-guidelines)

API模型对象不代表图像已识读/视频已观看。网页登录可用也不能替代有权限和预算的采集适配器。来源池里的查询是未在API验证的计划模板；不存在已运行的自动来源扫描。

可工作的降级模式：用户/agent提供原帖 → 实际深读并填写语义审核JSON → 脚本校验、状态去重、导出。未来适配器的字段、预算、分页失败恢复与游标合同见 skill 的 `references/data-access.md`；v0.1没有空函数或假discover命令。

