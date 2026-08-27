---
name: bubble-config-table-generator
description: Generate or modify Bubble project Excel configuration tables from Chinese game-design documents, with formal full-copy delivery or explicit style-preserving lightweight delta delivery, table mapping, ID allocation, tlanguage_cn references, cross-table dependencies, and runnable inferred test data. Use for Bubble 配置表、配表、测试配置、策划案转表、补测试数值 or related xlsx work under 策划/配置表.
metadata:
  author: Bubble project
  version: "1.4.0"
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
- 把 `Table` 中的源工作簿视为只读规范源；本生成工作流不覆盖源文件，应把目标 Sheet 原属的完整工作簿复制到输出目录后修改。
- 完整交付模式下，本次功能需要使用任何既有配置表时，必须把该表原属 `.xlsx` 整本复制到输出目录，在副本中配置本系统需要的测试数据；禁止直接修改 `Table` 源文件或只摘取单个 Sheet。用户明确要求“轻量、增量、快速测试”时，可切换到轻量增量模式，规则见 [references/lightweight-delta.md](references/lightweight-delta.md)。
- 保留用户已有改动。只修改本次策划案涉及的表、语言条目和必要依赖。

## 交付模式选择

生成前先根据用户意图选择模式，并在 manifest 和报告中写明：

- `full_copy`：正式交付、直接导表、需要完整运行链路时使用。既有依赖整本复制，输出可直接作为独立交付包。
- `lightweight_delta`：用户明确要求测试效率、增量配置或不复制整本依赖时使用。主功能表照常生成；既有依赖只输出本次新增/修改行，但增量工作簿必须从源工作簿派生并继承格式样式，且标记 `merge_required=true`。

不要因为“测试”自动省略依赖：只要用户未选择增量模式，仍使用 `full_copy`。不要把轻量增量包描述为完整依赖副本；它在合并回源表并重新 QA 前不能直接交给正式导表器。

## 输出路径和工作簿归属

写任何文件前先创建“工作簿归属计划”，并按照 [references/delivery-manifest-schema.md](references/delivery-manifest-schema.md) 在执行过程中维护 `generation-manifest.json`：

- `requested_output_path`：用户原始指定路径；未指定时为 `null`。
- `resolved_output_directory`：实际使用的绝对目录。
- `feature_key`：本次系统功能的稳定标识。
- `workbooks`：每个工作簿的源路径、目标路径、角色、复制动作、Sheet、测试行和归属依据。
- `delivery_mode`：`full_copy` 或 `lightweight_delta`；未明确选择时默认 `full_copy`。
- `lightweight_delta` 时必须追加 `merge_required=true`、`merge_instruction`，并在依赖工作簿条目使用 `delivery_action=delta_created`、`copy_scope=delta_rows_only`。

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
- `full_copy` 模式下，公共文本、公共条件、公共消耗、公共奖励、公共掉落等继续写入各自原属公共工作簿在输出目录中的完整副本。
- `lightweight_delta` 模式下，公共或其他系统既有表只输出源工作簿的目标 Sheet、协议头和本次新增/修改行；不能用空白新工作簿仿制格式，必须保留源工作簿的样式包和目标 Sheet 样式。详细要求见 [references/lightweight-delta.md](references/lightweight-delta.md)。
- 只有用户明确要求拆分，或现有 `Table` 已证明生命周期、负责人或导出批次确实独立，才允许多个功能工作簿，并在清单中写明证据。

一个任务可以交付“一个主功能工作簿 + 被修改的公共/引用工作簿”，但主功能自身不得碎片化。

### 既有依赖与测试数据

`full_copy` 模式只要本系统测试链路直接使用既有功能表、公共表或其他系统表，就必须执行以下规则：

1. 从 `Table` 找到目标 Sheet 的原属工作簿，把该 `.xlsx` 整本复制到用户指定输出目录；同一源工作簿只复制一次。
2. 保留源工作簿全部 Sheet、公式、样式、列宽、冻结窗格和既有数据，不只复制所需 Sheet，不把公共/引用 Sheet 并入主功能工作簿。
3. 所有新增或修改只发生在输出目录副本；禁止直接修改 `Table` 源工作簿。
4. 在副本的原属 Sheet 中新增或修改本系统需要的测试数据，保证主功能行引用的依赖 ID 在交付文件内存在；不能只复制工作簿而不配置测试行。
5. 若主功能本身已有工作簿，复制后的副本就是唯一主功能工作簿，在该副本中新增 Sheet 或测试行，不另建第二个主功能工作簿。
6. 在 `generation-manifest.json` 中为每个既有副本记录 `source_path`、`delivery_action=copied_and_modified`、`copy_scope=full_workbook`，并逐条记录测试数据的 Sheet、ID、`added/updated` 动作和用途。

具体字段和正反例见 [references/delivery-manifest-schema.md](references/delivery-manifest-schema.md)。

`lightweight_delta` 模式改用以下规则：

1. 读取源工作簿的真实 Sheet、6 行协议头、字段类型、列宽、冻结窗格、主题和样式包。
2. 从源工作簿派生增量 `.xlsx`，只保留本次涉及的目标 Sheet、协议头、新增/修改行和 `END`；保留 `styles.xml`、主题及目标 Sheet 的格式资源。
3. 增量依赖条目使用 `delivery_action=delta_created`、`copy_scope=delta_rows_only`，必须填写 `source_path`、`merge_required` 和合并规则；不能声明为 `full_workbook`。
4. 增量包只用于快速测试或交接，正式导表前按 B 列 ID 合并回源工作簿，冲突 ID 不得默认覆盖。

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

先确定用户输出路径，再展示简洁的“绝对输出路径、工作簿归属计划、既有工作簿复制清单、ID 分配台账、表映射、字段映射、依赖、ID 候选、单位、语言条目、测试值来源、待确认项”。当只有测试数值缺失时不要停下来等待确认，应继续生成。

### 3. 建立依赖和 ID

按拓扑顺序生成：语言/基础字典与资源表 → 公共条件、消耗、奖励、掉落 → 模块主表 → 明细、池、步骤 → 跳转和表现 → 反向校验。

- ID 必须符合各表 B1 规则、为正整数、非 0、表内唯一且不超过 Int32；默认只要求目标 Sheet 内唯一，除非 B1 明确共享模块或父对象命名空间。
- 按 B1 保留模块/类型段、固定宽度、父 ID 前缀和插入步长；不压缩、不重排旧 ID。不同无关 Sheet 可以复用同一数字。
- `max+1` 只在 B1 明确为连续自增且没有保留位或父子构成时使用；不能作为跨表通用算法，不虚构不存在的外键。
- 测试新增行不能随意使用 `99`、`9000`、`999999`、`9999999` 等旧表保留值，除非目标 B1 明确允许。
- 每个新增或修改 ID 都必须写入 `generation-manifest.json` 的 `id_allocations`，记录 `scope`、`kind`、`allocation_rule`、`parent_id`、`source`、`status` 和 `collision_checked`。
- 新增玩家文本先写 `tlanguage_cn.id/words`，业务表只保存语言 ID。
- 若测试依赖不存在，同时生成带测试标识的依赖行，并记录生成顺序。

### 4. 缺省测试数据设计

策划案未给数值时，自动设计测试配置，不生成空表，也不因这一点提问。至少覆盖正常值、边界值、枚举/多态分支值和必要的跨表联动值。

所有补齐值标记来源：`S` 策划案、`T` 现有表、`D` 推导、`A` AI 假设。`A` 类行的 A 列写 `测试_假设_用途`，交付状态统一为“测试假设，可运行，待策划确认”。这些值不能冒充正式平衡、经济或商业化数值。

### 5. 生成工作簿

- 若主功能已有工作簿，先整本复制到输出目录并把它作为唯一主功能工作簿；若是全新功能，才新建一个主功能工作簿。把该功能的所有新增业务表写成其中的不同 Sheet，不要按 Sheet 创建多个工作簿。
- `full_copy` 模式：对所有本次使用的既有公共/引用表，整本复制其原属规范工作簿到输出目录，并在副本中写入本系统测试数据；不把公共/引用 Sheet 复制进主功能工作簿。
- `lightweight_delta` 模式：从源工作簿派生 `*_增量.xlsx`，只保留本次涉及的目标 Sheet 和新增/修改行；必须继承源工作簿的 `styles.xml`、主题、列宽、冻结窗格、协议头、字段顺序、导出标记和目标 Sheet 样式。禁止用空白 `openpyxl.Workbook()` 重新建表后手工仿样式。
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
3. 检查直接外键、数组外键、动态参数、语言 ID 及 `words` 非空；逐条核对 `id_allocations` 的作用域、构成规则和碰撞检查。
4. 检查概率、权重、时间、金额、倍率单位及 `min <= max`。
5. 渲染或打开所有受影响 Sheet，目视确认文字、列宽、行高、边框、冻结窗格和无裁切。
6. 运行 `scripts/qa_generated_workbooks.py <xlsx...> --table-dir <Table目录>`；若当前环境没有 Python/openpyxl，执行同等检查并说明替代方式。
7. `full_copy` 模式运行 `scripts/qa_delivery_layout.py generation-manifest.json`，确认实际输出目录与用户指定路径一致、同一 `feature_key` 只有一个主功能工作簿、所有声明的 Sheet 和文件都存在；所有既有依赖均为完整工作簿副本，测试行相对源文件确实新增或修改。`lightweight_delta` 模式运行增量交付 QA：确认 `delivery_mode=lightweight_delta`、源路径有效、目标 Sheet 存在、增量 ID 相对源表新增/修改、合并规则完整，并额外比较源/增量包的样式包和目标 Sheet 样式。
8. 可用时用项目当前导表器试导出，核对客户端/服务端实际行列。

本次新增或修改范围内的错误必须修复并重新回读；源工作簿中与本次无关的历史问题应标记为“既有风险”并保留证据，不擅自扩大修改范围。警告需要解决或在交付报告中逐项说明。

## 交付合同

交付以下内容：

- 生成或修改后的 `.xlsx`；
- 每个最终文件的绝对路径，以及 `generation-manifest.json`；
- 工作簿归属计划，明确主功能工作簿和公共/引用工作簿；
- 既有工作簿复制清单：源文件、输出副本、完整复制验证，以及副本中新增/修改的测试 Sheet 和 ID；
- 轻量增量模式：源文件、增量工作簿、样式继承验证、合并规则，以及增量中新增/修改的测试 Sheet 和 ID；
- 受影响表和依赖顺序；
- 新增/复用语言 ID、中文文本、消费者字段、占位符；
- 测试数据清单：每行用途、S/T/D/A 来源、依据、触发条件、预期导出和游戏内结果；
- ID 候选与占用检查；
- QA 报告、试导出结果、剩余警告和待确认项；
- 明确状态：“测试假设，可运行，待策划确认”或“策划已确认的正式值”。

不要只交付文字分析。只要环境允许写文件，就必须交付可用工作簿和回读证据。
