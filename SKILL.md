---
name: bubble-config-table-generator
description: Generate or modify Bubble project Excel configuration tables from Chinese game-design documents, including table mapping, ID allocation, tlanguage_cn localization references, cross-table dependencies, and runnable test data inferred when values are missing. Use for Bubble 配置表、配表、测试配置、策划案转表、补测试数值 or related xlsx work under 策划/配置表.
metadata:
  author: Bubble project
  version: "1.0.0"
---

# Bubble 配置表生成器

把策划案落实为符合 Bubble 项目既有协议的 `.xlsx` 配置，并生成可运行、可验证、可追溯的测试数据。

## 使用前必须读取

1. 完整读取 [references/bubble-config-standard.md](references/bubble-config-standard.md)。这是表结构、ID、文本、关联、数值和 QA 的项目规范。
2. 读取 [references/field-dictionary.json](references/field-dictionary.json)、[references/relation-dictionary.json](references/relation-dictionary.json) 和 [references/table-catalog.md](references/table-catalog.md)，再决定目标表和依赖关系。大文件按目标 Sheet 名检索相关段落，不要凭记忆猜字段。
3. 策划案未给出部分或全部数值，或用户要求测试数据时，完整读取 [references/test-data-design.md](references/test-data-design.md)。
4. 准备创建或修改工作簿时，读取 [references/runtime-compatibility.md](references/runtime-compatibility.md)，并遵守当前 Agent 环境的电子表格工具要求。
5. 在 Bubble 工程内操作时，同时读取目标代码仓库的 `AGENTS.md` 以及 `.agents/skills/gf-spec/reference/guides/table-design.md`（若存在）。

参考资料是快照。若 `策划/配置表/Table` 的修改时间晚于参考资料、目标表不存在于字典、或用户明确要求最新规范，先运行 `scripts/sync_project_references.py` 或直接重新审计当前源表，不能静默使用过期 Schema。

## 默认位置与写入边界

- 源表目录：`策划/配置表/Table`。
- 规范源文件：`策划/配置表/Bubble配置表_AI生成规范.md`、字段字典、关系字典和全表目录。
- 默认输出：`策划/配置表/AI生成/<功能名或日期>/`。
- 除非用户明确要求直接改正式表，否则不要覆盖 `Table` 中的源工作簿；应复制最接近的工作簿或 Sheet 到输出目录后修改。
- 保留用户已有改动。只修改本次策划案涉及的表、语言条目和必要依赖。

## 执行流程

### 1. 解析策划案

提取对象、字段、枚举、状态、条件、消耗、奖励、概率、时间、文本、资源、界面跳转和测试目标。把内容分为：策划明确值、项目现有证据、可推导值、AI 测试假设。

所有玩家可见、需要展示或可能本地化的内容归入“语言条目清单”；资源路径、程序键、SKU、策划备注等内部字符串不归入语言表。

### 2. 映射现有配置表

优先扩展现有表，谨慎新建表。对每个候选表实际读取：

- 第 1–6 行协议头和相邻正式数据；
- B1 的 ID 构成、已占用段和保留值；
- 字段类型、导出开关、单位、0/空语义和复杂字段结构；
- 关联表、数组外键及 `type + param` 分支；
- 样式、列宽、冻结窗格和 `END` 位置。

先向用户展示简洁的“表映射、字段映射、依赖、ID 候选、单位、语言条目、测试值来源、待确认项”，但当只有测试数值缺失时不要停下来等待确认，应继续生成。

### 3. 建立依赖和 ID

按拓扑顺序生成：语言/基础字典与资源表 → 公共条件、消耗、奖励、掉落 → 模块主表 → 明细、池、步骤 → 跳转和表现 → 反向校验。

- ID 必须符合各表 B1 规则、为正整数、非 0、表内唯一且不超过 Int32。
- 不把 `max+1` 当作跨表通用算法，不虚构不存在的外键。
- 新增玩家文本先写 `tlanguage_cn.id/words`，业务表只保存语言 ID。
- 若测试依赖不存在，同时生成带测试标识的依赖行，并记录生成顺序。

### 4. 缺省测试数据设计

策划案未给数值时，自动设计测试配置，不生成空表，也不因这一点提问。至少覆盖正常值、边界值、枚举/多态分支值和必要的跨表联动值。

所有补齐值标记来源：`S` 策划案、`T` 现有表、`D` 推导、`A` AI 假设。`A` 类行的 A 列写 `测试_假设_用途`，交付状态统一为“测试假设，可运行，待策划确认”。这些值不能冒充正式平衡、经济或商业化数值。

### 5. 生成工作簿

- 复制目标工作簿或同系统正式 Sheet 的真实样式，不发明全局皮肤。
- 保持 6 行表头、B 列主键、数据从第 7 行开始、列 `END` 截断。
- 只使用项目当前类型 `int/str/arr/bool`；`arr` 必须是严格 JSON。
- 导出区优先写最终静态值。必须使用公式时，在 Excel 兼容引擎中重算并确认缓存值。
- 测试行必须有至少一个实际导出的非零/非空字段。
- 非法样例只能放在 `END` 之后、A 列 `END` 下方，或不以 `t` 开头的测试 Sheet。

### 6. 回读与验证

保存后必须重新打开工作簿并验证，不得把“文件已写出”当作完成：

1. 检查表头、B3/B6、字段唯一性、ID、导出开关、类型和 `END`。
2. 解析全部 `arr` JSON，检查 `bool`、公式错误和公式缓存。
3. 检查直接外键、数组外键、动态参数、语言 ID 及 `words` 非空。
4. 检查概率、权重、时间、金额、倍率单位及 `min <= max`。
5. 渲染或打开所有受影响 Sheet，目视确认文字、列宽、行高、边框、冻结窗格和无裁切。
6. 运行 `scripts/qa_generated_workbooks.py <xlsx...> --table-dir <Table目录>`；若当前环境没有 Python/openpyxl，执行同等检查并说明替代方式。
7. 可用时用项目当前导表器试导出，核对客户端/服务端实际行列。

本次新增或修改范围内的错误必须修复并重新回读；源工作簿中与本次无关的历史问题应标记为“既有风险”并保留证据，不擅自扩大修改范围。警告需要解决或在交付报告中逐项说明。

## 交付合同

交付以下内容：

- 生成或修改后的 `.xlsx`；
- 受影响表和依赖顺序；
- 新增/复用语言 ID、中文文本、消费者字段、占位符；
- 测试数据清单：每行用途、S/T/D/A 来源、依据、触发条件、预期导出和游戏内结果；
- ID 候选与占用检查；
- QA 报告、试导出结果、剩余警告和待确认项；
- 明确状态：“测试假设，可运行，待策划确认”或“策划已确认的正式值”。

不要只交付文字分析。只要环境允许写文件，就必须交付可用工作簿和回读证据。
