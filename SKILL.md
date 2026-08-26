---
name: bubble-config-table-generator
description: Generate or modify Bubble project Excel configuration tables from Chinese game-design documents, including table mapping, ID allocation, tlanguage_cn localization references, cross-table dependencies, and runnable test data inferred when values are missing. Use for Bubble 配置表、配表、测试配置、策划案转表、补测试数值 or related xlsx work under 策划/配置表.
metadata:
  author: Bubble project
  version: "1.1.0"
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
- 用户指定的输出目录或完整文件路径是硬约束，优先级最高；只有用户没有指定路径时，才使用默认输出 `策划/配置表/AI生成/<功能名或日期>/`。
- 除非用户明确要求直接改正式表，否则不要覆盖 `Table` 中的源工作簿；应复制最接近的工作簿或 Sheet 到输出目录后修改。
- 保留用户已有改动。只修改本次策划案涉及的表、语言条目和必要依赖。

## 输出路径和工作簿归属

写任何文件前先创建“工作簿归属计划”，并按照 [references/delivery-manifest-schema.md](references/delivery-manifest-schema.md) 在执行过程中维护 `generation-manifest.json`：

- `requested_output_path`：用户原始指定路径；未指定时为 `null`。
- `resolved_output_directory`：实际使用的绝对目录。
- `feature_key`：本次系统功能的稳定标识。
- `workbooks`：每个工作簿的路径、角色、Sheet 和归属依据。

### 输出路径

1. 用户指定目录时，所有最终工作簿、清单和 QA 报告都必须位于该目录。
2. 用户指定完整 `.xlsx` 文件名时，主功能工作簿必须使用该文件名。
3. 指定路径不可写时报告原路径和错误；不得静默改用默认、当前、临时或工具自带输出目录。
4. 交付前把用户路径与实际绝对路径逐项比对，并检查所有文件真实存在。

### 同功能工作簿聚合

项目 59 个源工作簿中有 39 个包含多个正式导出 Sheet，单个工作簿最多 10 个导出 Sheet。以此作为硬约束：

- 同一系统功能的主表、子表、明细表、池表、阶段表和参数表必须集中在一个主功能 `.xlsx` 中，以多个 `t*` Sheet 组织。
- 现有功能新增 Sheet 时，加入该功能既有工作簿；全新功能需要多个表时，只创建一个主功能工作簿。
- 禁止把同一功能的三个新增 Sheet 生成为三个 `.xlsx`，也禁止为每个 Sheet 默认新建同名工作簿。
- 公共文本、公共条件、公共消耗、公共奖励、公共掉落等继续写入各自既有公共工作簿。
- 引用其他系统既有表并需新增行时，该行保留在目标表原属工作簿。
- 只有用户明确要求拆分，或现有 `Table` 已证明生命周期、负责人或导出批次确实独立，才允许多个功能工作簿，并在清单中写明证据。

一个任务可以交付“一个主功能工作簿 + 被修改的公共/引用工作簿”，但主功能自身不得碎片化。

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

先确定用户输出路径，再展示简洁的“绝对输出路径、工作簿归属计划、表映射、字段映射、依赖、ID 候选、单位、语言条目、测试值来源、待确认项”。当只有测试数值缺失时不要停下来等待确认，应继续生成。

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

- 先创建一个主功能工作簿，再把该功能的所有新增业务表写成其中的不同 Sheet；不要按 Sheet 创建多个工作簿。
- 公共/引用表需要修改时，复制并修改其既有规范工作簿，不把公共 Sheet 复制进主功能工作簿。
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
7. 运行 `scripts/qa_delivery_layout.py generation-manifest.json`，确认实际输出目录与用户指定路径一致、同一 `feature_key` 只有一个主功能工作簿、所有声明的 Sheet 和文件都存在。
8. 可用时用项目当前导表器试导出，核对客户端/服务端实际行列。

本次新增或修改范围内的错误必须修复并重新回读；源工作簿中与本次无关的历史问题应标记为“既有风险”并保留证据，不擅自扩大修改范围。警告需要解决或在交付报告中逐项说明。

## 交付合同

交付以下内容：

- 生成或修改后的 `.xlsx`；
- 每个最终文件的绝对路径，以及 `generation-manifest.json`；
- 工作簿归属计划，明确主功能工作簿和公共/引用工作簿；
- 受影响表和依赖顺序；
- 新增/复用语言 ID、中文文本、消费者字段、占位符；
- 测试数据清单：每行用途、S/T/D/A 来源、依据、触发条件、预期导出和游戏内结果；
- ID 候选与占用检查；
- QA 报告、试导出结果、剩余警告和待确认项；
- 明确状态：“测试假设，可运行，待策划确认”或“策划已确认的正式值”。

不要只交付文字分析。只要环境允许写文件，就必须交付可用工作簿和回读证据。
