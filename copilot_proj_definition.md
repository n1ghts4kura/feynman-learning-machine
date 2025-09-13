# Feynman Learning Machine 项目定义（对齐当前实现）

## 1. 方法论与目标

Feynman 学习法强调“用容易理解的语言进行具体详细的描述”，通过反复讲解—反馈—修订来实现“理解深度”和“知识完整性”的双提升。本项目以此为目标，通过多智能体编排实现学习闭环。评分维度采用 0–10 分制，关注可理解性与完整性两个核心指标。

## 2. 阶段化流程（Stage 机制）

- Stage 1：知识大纲构建（Outline）
  - 用户输入学科/领域或概述
  - OutlineAgent 生成树状结构的完整知识大纲（root_levels/Level）
  - 运行完毕应调用 set_current_stage(2)

- Stage 2：用户自述与系统评分（Evaluate）
  - 用户依据大纲进行自述
  - EvaluatorAgent 必须获取历史评分、当前复述轮次、知识大纲后进行评分与反馈，并在结束时自增复述轮次
  - 当达到高水平时应调用 set_current_stage(3)

- Stage 3：学习总结（Conclusion）
  - ConclusionAgent 汇总所有评分结果、复述轮次、知识大纲，生成总结与建议

GeneralAgent 作为总控，接收原始用户输入，根据 get_current_stage 决策 handoff 到对应子 Agent；Runner.run 的输出即为被 handoff 的子 Agent 的执行结果。

## 3. Agent 体系与职责

- GeneralAgent（总控/调度）
  - 输入：用户文本、会话状态
  - 决策：基于 get_current_stage handoff 到 Outline/Evaluator/Conclusion
  - 约束：使用 handoffs 声明可交接的目标 Agent

- OutlineAgent（知识大纲）
  - 目标：生成完整树状大纲（typedef.OutlineAgentOutput）
  - 工具：set_current_stage（成功后置 2）
  - Prompt：采用 `handoff_instructions`、`global_context`、`prompt` 分区，提供输入/输出 JSON 示例，明确严格 JSON 输出要求

- EvaluatorAgent（评分与反馈）
  - 目标：对用户自述进行 0–10 分制评分（可理解性/完整性），列出遗漏点与评语
  - 工具：get_evaluating_rounds、get_knowledge_outline、get_current_retell_count、increase_current_retell_count、set_current_stage
  - 规则：先取依赖数据再评分；结束后自增复述轮次；高水平时置 stage=3

- ConclusionAgent（学习总结）
  - 目标：生成学习过程总结（依据评分历史、知识大纲、复述轮次）
  - 输出：严格 JSON，总结具体、基于事实

## 4. 工具调用与强制约束

- 必须工具：在 Prompt 中用“必须调用”明确要求，同时在代码层声明 tools 列表，GeneralAgent 通过 handoff 管理子 Agent 调用
- 强制调用策略：
  - Prompt 层：使用“必须”“自行调用”等措辞，列出执行步骤
  - 代码层：将所需函数注册为 tools；必要时用过滤器拦截未调用工具的输出（后续可扩展）

## 5. 评分与判定标准（当前实现）

- 可理解性（0–10）：语言清晰度、逻辑性、具体细节、面向非专家的可读性
- 完整性（0–10）：覆盖知识大纲的比例与深度；允许随复述轮次动态调权
- 达标条件：当综合表现高（由 EvaluatorAgent 判断）→ set_current_stage(3)

## 6. 数据结构要点

- OutlineAgentOutput：root_levels -> Level(name, description, sub_levels)
- EvaluatorAgentOutput：understandability_score, completeness_score, missing_points, evaluating_comments
- Conclusion 输出：summary（string, JSON 包装）

## 7. 运行路径与交互

1) 用户首次输入 → GeneralAgent → OutlineAgent → set_current_stage(2)
2) 用户自述 → GeneralAgent → EvaluatorAgent（工具链：获取历史/大纲/轮次 → 评分 → 自增轮次 → 可能置 stage=3）
3) Stage=3 → GeneralAgent → ConclusionAgent → 返回学习总结

## 8. 设计原则与一致性

- 以“容易理解且具体详细”+“完整性”双标准为核心
- Prompt 分区一致化：`handoff_instructions`、`global_context`、`prompt`
- 输出严格 JSON，附示例，便于解析与校验
- 状态与工具使用显式化、可追踪

---
本文件已对齐当前 agent.py 的实现约束与流程，作为后续开发与重构的参考标准。
