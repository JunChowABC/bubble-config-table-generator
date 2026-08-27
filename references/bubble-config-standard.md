# Bubble 项目配置表 AI 生成规范

> 版本：1.4（2026-08-27）
> 适用目录：`D:\Bubble\策划\配置表\Table`  
> 审计覆盖：59 个 `.xlsx`、213 个 Sheet、177 个可导出的 `t*` Sheet、1431 个字段。  
> 状态：**可作为 AI 生成和自检的项目级约束；不替代策划对业务语义、程序对新增表类/枚举的正式确认。**

## 1. 规则分级

- **硬约束**：来自当前导表器代码，违反后会漏字段、漏行、覆盖数据或导出失败。
- **项目惯例**：由 177 个正式 Sheet 的共同结构和高频写法归纳；新增内容应遵守。
- **推荐约束**：用于降低联表、测试和维护风险；遇到旧表反例时，以“新数据更严格”为原则，不复制历史问题。

## 2. 文件、工作簿与 Sheet

1. **硬约束**：只有名称以小写 `t` 开头的 Sheet 才是有效导出候选，如 `tItem`、`tCommonReward`、`tlanguage_cn`。
2. **硬约束**：正式 Sheet 名在整个 `Table` 目录内必须唯一。导出文件按 Sheet 名命名，同名 Sheet 同时导出时可能互相覆盖。
3. 一个工作簿可以含多个正式 `t*` Sheet，也可以含“备注、公式计算、临时、枚举代码”等非导出 Sheet。
4. 运行时资源名来自 **Sheet 名**，不是工作簿名。工作簿名主要用于策划归档和排序。
5. 工作簿名高频采用 `分类前缀_中文主题_t主表名.xlsx`，如 `W_物品表_tItem.xlsx`；但存在无 `t` 后缀或一表多 Sheet 的历史例外，因此文件名不能作为导出判断依据。
6. 分类前缀是目录惯例：`0/0J/0S/0W` 为公共、机制、数值、文本；`B/C/D/G/H/J/L/M/N/R/S/T/W/Y` 按中文主题首字母或历史模块排序。新增文件应沿用所属系统最近的前缀。

### 2.1 输出路径是硬约束

1. 用户指定的输出目录或完整文件路径优先级最高，必须原样解析并使用；不能擅自改到默认目录、当前目录、临时目录或工具自己的 `outputs` 目录。
2. 用户指定目录时，本次交付的所有工作簿、清单和 QA 报告都保存到该目录。用户指定完整 `.xlsx` 文件名时，主功能工作簿必须使用该文件名。
3. 只有用户没有指定路径时，才使用 `策划/配置表/AI生成/<功能名或日期>/`。
4. 写入前先输出解析后的绝对目标路径；写入后逐个按绝对路径检查文件存在，并确认没有把最终文件误写到默认目录或其他临时目录。
5. 若用户指定路径不可写，必须报告该路径和实际错误；不得静默换路径后宣称完成。

### 2.2 同一功能使用一个工作簿、多个 Sheet

当前 59 个工作簿中，39 个包含多个正式导出 Sheet，只有 20 个是单导出 Sheet；单个工作簿最多包含 10 个导出 Sheet。项目稳定做法是：**同一系统功能的主表、子表、明细表、池表、阶段表和参数表集中在一个 `.xlsx` 中，以不同 `t*` Sheet 组织。禁止默认“一个 Sheet 一个 xlsx”。**

代表性证据：

- `C_菜品表_tFood.xlsx` 集中 `tFoodType/tFoodIngredient/tFood/tLvFood/tFoodCollectReward/tFoodCollectGroup/tFoodCombo`。
- `C_抽卡表_tGachaPool.xlsx` 集中 `tSubGacha/tGacha/tPool/tGuaranteed/tSpReward/tGachaInfo`。
- `J_家具商店表_tShop.xlsx` 集中 9 个商店相关正式 Sheet。
- 场景、顾客、经营、礼包、剧情、角色动线等也采用相同组织方式。

生成前必须先给出“工作簿归属计划”：`功能 → 源xlsx → 目标xlsx → Sheet → 角色(feature/shared/referenced) → 动作(created/copied_and_modified) → 测试行 → 归属依据`。归属规则：

1. 现有功能新增 Sheet：把该功能既有工作簿整本复制到指定输出目录，在副本中加入新 Sheet 或测试行。
2. 全新功能需要多个业务表：创建一个主功能工作簿，并在其中创建多个 Sheet。
3. 公共文本、公共条件、公共消耗、公共奖励、公共掉落等：把各自既有公共工作簿整本复制到指定输出目录，在副本的原属 Sheet 中写入本系统测试数据；不复制进功能工作簿。
4. 引用其他系统既有表：把该表原属工作簿整本复制到指定输出目录，在副本的原属 Sheet 中写入本系统需要的测试数据。
5. 只有用户明确要求拆分，或当前 `Table` 已存在独立工作簿边界且生命周期、负责人或导出批次确实不同，才允许拆成多个功能工作簿，并必须说明证据。

因此一个任务可以交付“一个主功能工作簿 + 若干被修改的公共/引用工作簿”，但不能把同一功能的三个新 Sheet 拆成三个新 `.xlsx`。

### 2.3 既有依赖工作簿必须整本复制并配置测试数据

如果本系统的主功能配置、公共配置或跨系统引用需要使用 `Table` 中任何既有配置表，必须把该 Sheet 原属的 `.xlsx` **整本复制**到用户指定输出目录，再只修改交付副本：

1. 不得直接修改 `策划/配置表/Table` 中的源工作簿。
2. 不得只摘取所需 Sheet，也不得把既有公共/引用 Sheet 并入主功能工作簿；必须保留源工作簿的全部 Sheet、公式、样式、列宽、冻结窗格和既有数据。
3. 同一源工作簿被多个字段或 Sheet 引用时只复制一次，所有本次测试数据集中写入这一副本。
4. 在副本的原属 Sheet 中新增或修改本系统测试行，使主功能测试链路引用的 ID 在交付文件内真实存在且可运行；不能只复制空依赖而不配数据。
5. `generation-manifest.json` 对每个既有副本记录 `source_path`、`delivery_action=copied_and_modified`、`copy_scope=full_workbook`，并逐条记录 `test_data` 的 Sheet、ID、`added/updated` 动作和用途。
6. 交付 QA 必须比较源文件与副本：源 Sheet 集合完整保留；`added` 行只在副本中存在；`updated` 行在副本中与源行确实不同。

若主功能本身已有工作簿，复制后的该工作簿就是唯一主功能工作簿，不得再额外创建第二个主功能 xlsx。

## 3. 固定表结构

正式 Sheet 的前 6 行是协议头，数据从第 7 行开始：

| 行 | A列固定文字 | B列至END前的内容 | 导表作用 |
|---|---|---|---|
| 1 | 表中文名/用途 | 每个字段的说明、枚举、单位、公式、引用表 | 读取为字段注释；也是 AI 判断语义的首要依据 |
| 2 | `中文字段名` | 中文字段名 | 工具不写入 JSON，但表头不得空 |
| 3 | `英文字段名` | 程序字段名 | JSON/BSON 键名 |
| 4 | `客户端数据` | `0` 或 `1` | 是否写入客户端 |
| 5 | `服务端数据` | `0` 或 `1` | 是否写入服务端 |
| 6 | `数据类型` | `int/str/arr/bool` | 控制解析方式 |
| 7+ | 策划备注 | 实际数据 | 数据区 |

### 3.1 A列与B列

- **A列是策划备注列，不导出。** 数据行可写可读中文名、分组、测试说明。
- **B列是主键列。** B3 必须为 `id`，B6 必须为 `int`；数据行 B 列必须是正整数且非 0。
- 主键由导表器用 `int.Parse` 读取，因此必须小于等于 `2,147,483,647`。项目代码基类按无符号 ID 使用，新数据禁止负数。
- 同表 ID 必须唯一。重复 ID 虽会记录错误，但客户端 JSON 的后行可能覆盖前行。
- 空 ID 或 ID=0 的行会被跳过。

### 3.2 END 截断

- 推荐每个新正式 Sheet 都在最后一个导出字段右侧的第 1 行写 `END`。工具不区分大小写。
- `END` 所在列及右侧全部不导出，适合放查询公式、校验、备注或临时计算。
- 若在某一行 A 列写 `END`，该行及下方全部不导出。
- 当前 177 个正式 Sheet 中有 39 个未放列 `END`，它们依赖“右侧没有辅助列”仍能导出；这是历史兼容，不是新表模板。
- B列至 `END` 前，每个字段的 1–6 行必须全部非空。

## 4. 表头与数据区样式

样式不是导表硬约束，而且各工作簿存在历史差异。AI 生成时的优先级是：**复制目标工作簿相邻正式 Sheet > 复制同系统最近表 > 使用下列基线。**

- 字体以微软雅黑 10–11 pt 为主。
- A1 通常为深蓝/主题色底、白字、左对齐；B1 以后为字段说明，自动换行，按内容左对齐或居中。
- A2、A3 通常加粗且左对齐；B2 以后居中。
- 第 3 行英文字段通常加粗、浅蓝底、细边框；主键 `id` 可用更深底色强调。
- 第 4–6 行通常居中并加细边框；A4:A6 左对齐。
- 数据区 A 列左对齐；ID、枚举、数量通常居中；长文本、路径、JSON 数组左对齐并按需换行。
- 第 1 行高度随注释自动增加。冻结窗格常见于 `A7/C7/D7`，但大型旧表也会冻结到当前编辑位置；新表应冻结在第 7 行上方，不复制异常编辑位置。
- 导出区不要合并单元格。列宽以完整显示表头和常用值为准，超长说明放第 1 行换行，不靠极宽列解决。

## 5. 字段命名和类型

### 5.1 命名

- Sheet：`t` + PascalCase，名词单数，如 `tGift`、`tMineTile`。
- 英文字段：新增字段统一 lowerCamelCase，如 `rewardId`、`openTime`、`conditionParam`。
- B3 固定为 `id`。
- 字段名在同一 Sheet 内必须唯一。当前旧表中存在 `tips/description/name` 等重复字段名，属于历史风险，禁止复用。
- 第 1 行必须写清：取值范围、单位、默认值、0/空含义、目标表名、数组元素结构、type+param 对应关系。

### 5.2 导表类型

当前 1,431 个字段只使用以下四类：

| 类型 | 当前字段数 | 写法 |
|---|---:|---|
| `int` | 957 | 数值型。项目导表器也接受小数，因此它实际承担“通用 number”角色 |
| `str` | 208 | 文本、资源路径、复杂 JSON 字符串或字典文本 |
| `arr` | 256 | 严格 JSON 数组 |
| `bool` | 10 | `True/False`，工具兼容 `0/1` |

导表器代码还支持 `long`，但当前正式表未使用。AI 不应自行引入 `long`；新增类型需要程序确认。

### 5.3 `int` 中的小数

当前至少 18 个声明为 `int` 的字段包含小数，例如镜头倍数、菜品售价、文本速度、动作时长、奖励倍率。这是导表器允许 `double` 回退解析造成的项目现实。因此：

- 不要仅因第 6 行写 `int` 就把现有小数取整。
- 是否允许小数以字段第 1 行说明、现有相邻数据和对应 C# 字段为准。
- 新增全新字段若需要小数，先让程序确认字段类型；Excel 第 6 行仍只能用导表器支持的标签。

## 6. 复杂字段语法

1. `arr` 必须使用严格 JSON：半角 `[]`、半角逗号、字符串用双引号。例如 `[1001,1002]`、`[[1,10],[2,5]]`、`[{"type":1,"value":100}]`。
2. 不要用中文逗号、中文引号、尾随逗号或 Excel 展示文本代替 JSON。
3. 空数组明确需要导出时写 `[]`；留空表示字段不存在。
4. 二维数组要在第 1 行写明每个位置的意义，如 `[[物品id,数量], ...]`。
5. `str` 中若承载字典/嵌套 JSON，也必须保持可解析，但导表器不会替你校验 `str` 内部结构。
6. `type + param` 是项目高频多态模式。AI 必须先根据 `type` 选分支，再按该分支生成 `param`；不能把所有参数一律当成同一外键。

## 7. 文本与本地化规范

这是项目级硬约束：**所有面向玩家、需要显示或可能本地化的文本，必须集中配置在 `tlanguage_cn`；其他业务表只保存并读取语言 ID，不得直接硬编码中文或其他显示文案。**

### 7.1 必须进入文本表的内容

- 名称、标题、描述、提示、按钮、弹窗、规则说明、状态说明。
- 任务、对话、剧情、邮件、活动、商品展示等玩家可见文案。
- 富文本、带图标标记的文案，以及包含 `{0}` 等格式化占位符的文案。

`tlanguage_cn` 以 `id:int` 为主键，以 `words:str` 保存简体中文内容。其他表的 `name/nameId/desc/descId/textId/words/wordId/tips/title` 等字段是否是语言 ID，以该表第 1 行说明和现有数据为准；沿用当前 Schema，不为统一命名擅自重命名旧字段。代表性现状包括 `tItem.name/desc`、`tAttribute.attrName/attrDescription`、`tCode.textId` 引用文本表。

### 7.2 不进入文本表的内部字符串

以下内容不是玩家显示文案，可以继续保留在原表：

- A 列策划备注、第 1 行字段说明、枚举和单位说明。
- 资源路径、Prefab/Spine/音频/特效路径、Unity 节点或组件路径。
- 程序键、枚举键、调试过滤串、内部脚本参数。
- 后台商品名、SKU、渠道标识等明确不展示给玩家的内部字符串。
- 结构化 JSON 本身；但 JSON 中若包含玩家可见文本，该文本仍应拆成语言 ID。

判断原则不是“单元格类型是否为 `str`”，而是“内容是否会展示给玩家或需要本地化”。边界不清时，默认按玩家文本处理并标为待确认。

### 7.3 语言 ID 与引用完整性

1. 先读取 `tlanguage_cn` 的 B1 分段规则和目标模块现有 ID，再分配未占用语言 ID；不能只做 `max+1`。
2. 业务表语言字段保存 `tlanguage_cn.id`，通常为 `int`；每个非 0 引用都必须存在，且对应 `words` 非空。
3. 只有字段说明明确允许“无文本”时，语言 ID 才能填 0 或留空；同时遵守客户端对数值 0 的省略语义。
4. 只有语义、语境和未来本地化需求都相同的文本才复用同一 ID。仅当前中文恰好相同，但所属按钮、角色语气、单复数或上下文不同，应分配不同 ID。
5. 修改展示文案时优先修改 `tlanguage_cn.words`；若改变语义或会影响其他消费者，应新建语言 ID，不能误改共用文本。
6. `{0}` 等占位符、富文本标签和图标标记写在 `words` 中；业务表提供参数。必须校验占位符数量、顺序、参数类型和标签闭合。

### 7.4 生成与交付顺序

先从策划案抽取“语言条目清单”，按模块分配 `tlanguage_cn.id` 并填写 `words`，再生成引用这些 ID 的业务表，最后检查：引用存在、文本非空、无业务表硬编码显示文案、占位符替换正确。AI 交付时必须单列“新增/复用语言 ID、中文文本、消费者表.字段、占位符说明”。

## 8. 导出开关与“0/空”语义

当前字段开关分布：1,387 个 `客户端=1/服务端=0`，43 个 `0/0` 辅助字段，仅 `tGuideLogic.dialogueGroupId` 为 `1/1`。

- 空单元格：客户端、服务端都不写出该字段。
- 客户端 `int/long` 值为文本 `0`：不写出该字段。
- 客户端 `bool=False`：不写出该字段。
- 服务端字段若开关为 1，`0/False` 会保留。
- 一行若最终只有 ID、没有任何其他导出字段，该行不会写入输出。
- 因此测试数据不能全填 0；每个测试分支至少要有一个会实际写出的非零/非空字段。
- `0`、空、`[]` 不是等价值。必须按字段第 1 行注释选择。

## 9. ID 设计

### 9.1 通用规则

项目没有一条适用于所有表的全局 ID 公式。ID 由各表 B1 注释定义，常见形式是“模块段 + 类型段 + 序号段 + 插入预留位”或“父 ID + 子序号”。AI 必须：

1. 读取目标 Sheet 的 B1 ID 说明。
2. 统计当前 ID 位数、前缀和已占用值。
3. 识别容错 ID、测试 ID、虚构 ID、保底 ID 等保留值。
4. 在相同模块段内选未占用 ID，并保留固定宽度与插入位。
5. 若 B1 没有正式构成规则，不把 `max+1` 当作默认；先向策划确认模块段，或把候选 ID 标为“待确认”。

### 9.2 已确认的代表性规则

- `tlanguage_cn`：按首位/模块分段；1 为物品名或程序文本，2 为通用文本，3 为模块文本，4 为角色，5 为家具，6 为食材/菜品，7 为任务，8 为对话，9 为特殊客人。旧数据存在 4–9 位混用，新增必须进入目标模块当前有效段。
- `tItem`：家具 `1 + 序号[6]`，角色 `2 + 序号[6]`，菜品 `301 + 珍稀度 + 序号[3]`，食材 `401 + 珍稀度 + 序号[3]`；货币等基础物品保留短 ID。
- `tCommonCondition`：说明为 `2 + 模块序号[2] + 序号[4]`，但存在 `99/1001...` 等公共兼容段；新增业务条件使用所属模块的 7 位段。
- `tGift`：`模块[3] + 序号[2] + 插入预留[1]`；`tGiftContents` 为 `礼包ID + 序号[2]`。
- `tTask`：任务类型段 + 阶段 + 任务序号 + 插入位；主线/支线/日常/活动分别使用既有类型段。
- `tMine`：`1 + 关卡类型[2] + 序号[4]`；`tMineTile`：`1 + 地块类型[2] + 序号[4]`。
- `tSceneArea`：场景 ID + 区域序号；`tPlotStep`、礼包内容、部分池表也采用父 ID 派生子 ID。
- `tView` 的 9000 以上为虚构 ID；不能把该规则迁移到其他表。

完整 177 表的 B1 说明、实际范围、位数和样本在 `Bubble配置表_AI字段字典.json` 中。

### 9.3 分层 ID 分配流程

项目当前不能采用“全项目 ID 唯一”：不同无关 Sheet 会复用小整数 ID，外键也按目标 Sheet 解释。因此新增 ID 按以下层级判断：

1. **表内层**：同一 Sheet 的正式数据 ID 必须唯一，这是所有表的硬约束。
2. **模块层**：只有 B1 明确共享模块段时，才在同一模块内检查冲突；不能把文件名前缀或 Sheet 名猜成模块段。
3. **父对象层**：明细、步骤、内容、池项等若 B1 使用父 ID 派生，子 ID 必须保留父 ID 前缀、序号位宽和插入步长。
4. **关系层**：外键只需在声明的目标 Sheet 中存在；无关 Sheet 可以复用相同数字，不能因为跨表数值相同就强行改号。

新增或修改 ID 的决策优先级是：用户/策划明确值 → B1 正式构成 → 同 Sheet/模块已占用值与保留间隔 → 父 ID 和外键关系 → 候选并待确认。每一步都要把占用集合扩展为“源工作簿 + 输出副本 + 本次新行”，避免复制既有表后与测试行碰撞。

`max+1` 只在 B1 明确为连续自增、没有模块段/插入位/保留值/父子构成时，才允许在该 Sheet 内使用。对于常见的 `+10`、`+100` 插入预留、模块段、类型段和父 ID 派生，必须按模板找最小可用候选，保留旧 ID 空洞，不重排旧数据。

测试新增行不能随意使用 `99`、`9000`、`999999`、`9999999` 或时间戳式 ID；这些在部分旧表中只是容错、虚构或上限值。目标 B1 没有明确测试段时，仍使用正式构成内的未占用候选，并把状态标为 `candidate`。更新既有行沿用原 ID，不为“看起来更整齐”而重编号。

每个新增或修改 ID 都要写入 `generation-manifest.json` 的 `id_allocations`，至少记录：`sheet`、`id`、`scope`（`sheet/module/parent`）、`kind`、`allocation_rule`、`parent_id`、`source`（`S/T/D/A`）、`status`（`reused/candidate/confirmed`）和 `collision_checked=true`。没有 ID 台账或无法说明构成规则的 ID，不得宣称为正式 ID。

## 10. 跨表关系

关系证据分三级：

- **明确**：第 1 行直接写目标 `tXxx` 或公式直接引用目标 Sheet。
- **高**：字段语义与实际 ID 覆盖同时指向同一目标表。
- **中**：只有字段名/部分数值吻合，必须人工确认，尤其是 `type+param`、小整数枚举和复用 ID 段。

### 10.1 核心枢纽

| 目标表 | 高置信消费者表数 | 代表消费者 |
|---|---:|---|
| `tlanguage_cn` | 51 | tActivity、tAdTvBox、tAttribute、tBestiaryReward、tCarpetShop、tChargeBlock、tCode、tCommonCondition、tCustomerStory、tDecoPlace、tDecoShopMoudel、tDecoShopTheme、tDecoration、tDecorationSet、tDecorationTab、tDecorationType、tDialogContent、tEventCusterResolut、tFood、tFoodColl… |
| `tItem` | 35 | tBestiaryReward、tChargeRmb、tCommonConsume、tCommonReward、tCurrencyAddDining、tCustomerStory、tDecoShopMoudel、tEventCuster、tEventGroup、tGiftCheckInGroup、tGiftContents、tGiftPool、tGroupMeal、tInvestment、tLevelMoudel、tLevelReward、tMainEntrance、tMine、tMineItem、tMinePa… |
| `tCommonDrop` | 30 | tAdTvBoxReward、tBestiaryReward、tChest、tDialogueTable、tEventCuster、tEventCusterResolut、tFood、tFoodCollectReward、tGiftContents、tGroupMeal、tInvestment、tItem、tManage、tMine、tMineAuto、tMinePackage、tMineTileParam、tMonster、tParty、tPartyReward、tPlotStep、tProgressTask、… |
| `tCommonCondition` | 27 | tActivity、tCustomerCreateTag、tCustomerShow、tDecoPlace、tDecoration、tEventTrigger、tFunction、tGacha、tGift、tGuideGroup、tManage、tManageEventFilter、tManageLevelCondition、tMine、tMineEvent、tPartyRefresh、tPost、tPushCondition、tResearchSlotUnlock、tSceneArea、tSceneUnlock… |
| `tCommonConsume` | 22 | tCarpetShop、tCurrencyAdd、tDecoPlace、tDecoShopMoudel、tDecoration、tEventCusterResolut、tGift、tInvestment、tLvFood、tManage、tMinePackage、tMineStaminaConsume、tMineTileParam、tRecharge、tResearchSlotUnlock、tRole、tSceneArea、tSceneUnlock、tShopDecoration、tShopRefresh、tSub… |
| `tRole` | 17 | tCustomer、tCustomerCreatePool、tCustomerFavor、tCustomerOrdering、tCustomerShow、tEmployee、tEventCuster、tEventGeneralProgress、tGroupMeal、tGuideGroup、tGuideLogic、tMineTalkEvent、tRoleActionGroup、tRoleInteraction、tRoleStory、tShopCustom、tStarMoudel |
| `tAttribute` | 11 | tBestiaryReward、tDecoration、tEmployee、tEventCusterResolut、tEventGroup、tLevelMoudel、tMineItem、tPlot、tPushCondition、tRoleActionGroup、tTriggerContent |
| `tViewJump` | 10 | tAdTvBox、tAutoRestock、tDecorationFuncTab、tGfitLink、tGiftCheckIn、tItemWay、tManageLevelCondition、tRoleInteraction、tTask、tTaskPlot |
| `tGift` | 9 | tActivity、tAdTvBox、tChargeBlock、tGfitLink、tGiftCheckIn、tGiftContents、tGiftPool、tPush、tRecharge |
| `tScene` | 9 | tGuideGroup、tManage、tManageValue、tParty、tPush、tRoleActionGroup、tSceneArea、tSceneAreaDecoration、tSceneUnlock |
| `tDecoration` | 8 | tDecoPlace、tDecoShopTheme、tDecorationSYT、tGuideLogic、tSceneAreaDecoration、tShopDecoration、tShopPool、tgoods |
| `tCustomer` | 8 | tCustomerOrdering、tCustomerPopular、tCustomerSatis、tCustomerStory、tEventCuster、tGroupMeal、tGuideLogic、tParty |
| `tDialogueTable` | 7 | tEventGeneralProgress、tFunction、tGuideLogic、tMineTalkEvent、tPlotStep、tRoleTriggerTag、tSceneUnlock |
| `tTask` | 7 | tActiveTask、tEventTrigger、tGuideGroup、tPlot、tPost、tShopSpeach、tTaskPlot |
| `tFood` | 6 | tCustomer、tFoodCollectGroup、tGroupMeal、tGroupMealFood、tGroupMealFoodFilter、tLvFood |

### 10.2 典型依赖链

```text
业务表
├─ 条件 → tCommonCondition
├─ 消耗 → tCommonConsume → tItem / tRecharge / 广告配置
├─ 掉落 → tCommonDrop → tCommonReward → tItem
├─ 文本 → tlanguage_cn
├─ 界面跳转 → tViewJump → tView / 功能表
├─ 礼包/内购 → tGift / tGiftContents / tChargeRmb / tRecharge
├─ 角色与表现 → tRole / tRoleStateLine / tRoleAction* / tDialogueTable / tEffectRes / tAudioRes
└─ 具体系统子表 → 场景、经营、事件、任务、天坑、商店等模块表
```

生成多表配置时按依赖顺序：**文本/基础字典与资源表 → 公共条件/消耗/奖励/掉落 → 模块主表 → 模块明细/池/步骤表 → 跳转和表现补齐 → 反向引用与文本显示校验。**

完整 490 条候选关系及证据、覆盖率在 `Bubble配置表_AI关系字典.json` 中；其中“中”级不可直接当作正式外键。

## 11. 数值规范

### 11.1 不允许按字段名猜单位

项目内同叫“概率/倍率/时间”的字段并不统一：

- 万分比：通常 `10000 = 100%`，如掉落率、触发率、部分加成。
- 百分数：部分字段用 `100 = 100%`，如直接写“百分比”的经营或客流参数。
- 小数系数：部分字段直接用 `0.5/1.2/1.5`。
- 时间同时存在秒、毫秒、分钟、小时、自然日和时间点数组。
- 充值金额 `tRecharge.rmb` 的单位是“分”。
- 权重通常是相对权重，不要求总和为 10000；只有字段说明明确为概率时才检查总和/上限。

AI 必须把**单位和换算写入第 1 行**，并从同字段相邻数据确定量纲。禁止把所有 `rate` 自动除以 10000，或把所有 `time` 自动当秒。

### 11.2 边界与哨兵

当前高频值包括 `0/1/100/1000/10000/99999/999999/-1`。这些值可能分别表示关闭、默认、百分比、万分比上限、无限、容错或特殊分支，不能跨字段复用含义。

- `999999/99999999` 常用于“近似无限时长/上限”，但必须由字段注释确认。
- `99` 常见为容错/默认 ID，但不是全项目统一规则。
- 最小值/最大值成对字段必须满足 `min <= max`。
- 权重不得为负；数量、等级、ID 默认不得为负。
- 价格、消耗、奖励和产出应同时做数量级检查，防止把“分、金币、万分比”混填。

## 12. 测试数值生成规范

### 12.1 策划案未提供配置数值时

若策划案只描述功能、流程或规则，没有给出具体配置数值，**AI 默认获得设计测试配置的授权，不得仅因缺少数值而停止生成或把整张表留空。** AI 应根据本规范、目标表表头、同系统现有数据和关联约束，生成一套可导出、可验证、可追溯的测试值。

这些值的交付状态必须写成“**测试假设，可运行，待策划确认**”，不能冒充正式平衡、经济、商业化或活动投放数值。数值来源按以下优先级选择并标记：

| 标记 | 来源 | 使用方式 |
|---|---|---|
| `S` | 策划案明确值 | 原样采用；若与表结构冲突则报告 |
| `T` | 当前配置表证据 | 参考目标列、同模块相邻正式行的中位量级、众数、常见区间或代表组合 |
| `D` | 推导值 | 根据公式、上下限、单位、依赖关系、`min<=max`、概率总量等不变量计算 |
| `A` | AI 测试假设 | 仅在 S/T/D 不足时使用最小可行值，必须说明理由、预期结果和待确认风险 |

自动设计顺序：

1. 明确字段单位、类型、合法范围、0/空语义、枚举分支和导出省略规则。
2. 读取同列及同系统现有分布；正常值优先取中位量级、众数或代表组合，不直接复制极端值。
3. 生成正常、边界、分支和必要的跨表联动数据；外键和语言 ID 同步补齐。
4. 在 A 列以 `测试_假设_用途` 标记 AI 设计行，并在交付报告逐字段记录 S/T/D/A 来源。
5. 给出每行预期触发条件、导出结果和游戏内可观察结果，便于程序和策划验收。

若连字段单位或合法分支也无法从表头、相邻数据及代码中判断，AI 应在非导出测试 Sheet 给出候选组合并列出待确认项，不得用未经说明的猜测污染正式导出区。

### 12.2 有效测试行

每个新增功能至少生成以下三类**可导出的有效行**：

| 类别 | 目的 | 生成要求 |
|---|---|---|
| 正常值 | 验证主流程 | 使用项目中位量级、真实存在的外键、非零导出字段 |
| 边界值 | 验证上下限 | 0/空语义、最小正数、字段允许的最大值、`min=max` 等，按注释选择 |
| 分支值 | 验证枚举/多态 | 每个 `type` 至少一条，并生成对应结构的 `param` |

概率字段若为万分比，常用测试点为 `1 / 5000 / 10000`；若为百分数则用 `1 / 50 / 100`；若为小数系数则用字段已有量级。权重测试用不相等的相对值并记录预期分布。

### 12.3 ID 与外键

- 测试 ID 也必须是合法、未占用、符合目标表分段的正式整数，A 列备注以 `测试_` 开头。
- 不能虚构不存在的外键。优先引用现有稳定测试对象；若依赖也新增，必须同时生成依赖行并给出拓扑顺序。
- 删除测试数据前要做反向引用检查。
- 未获得测试专用 ID 段时，AI 应把 ID 标为“候选，待策划确认”，不得宣称已正式占号。
- 测试行使用的语言 ID 必须真实存在且 `words` 非空；新增语言条目需同时交付。至少验证一条普通文本、一条带占位符/富文本的文本（若本功能存在），以及显示结果符合预期。

### 12.4 非法测试

重复 ID、缺失外键、错误 JSON、越界概率等负向样例不得放在正式导出区。应放在：

1. `END` 右侧；或
2. A列 `END` 下方；或
3. 名称不以 `t` 开头的独立测试 Sheet。

## 13. AI 生成工作流

1. 解析用户指定输出路径；若已指定，锁定为硬约束并记录绝对路径。读取策划案，拆出对象、字段、枚举、状态、数值、玩家可见文本、内部字符串、资源、条件、消耗、奖励和跳转。
   若策划案没有给出数值，直接启用 12.1 的缺省测试数据设计流程，不把“缺少数值”视为阻塞。
2. 在 `Bubble配置表_AI字段字典.json` 中查找最接近的现有 Sheet；优先扩展旧表，谨慎新建表。
3. 生成“工作簿归属计划”；同一功能的新增业务 Sheet 必须归入一个主功能 xlsx。凡本次使用既有功能/公共/引用表，先把原属工作簿整本复制到指定输出目录，同一源工作簿只复制一次；计划确定后才能写文件。
4. 读取目标工作簿的实际 1–6 行和相邻数据，确认样式、ID 段、单位、默认值、空值语义；所有新增或修改只写入输出目录副本，不修改 `Table` 源文件。
5. 生成“字段映射与依赖清单”，区分直接外键、数组外键、动态 `type+param` 和纯枚举。
6. 先生成“语言条目清单”，分配/复用 `tlanguage_cn.id` 并填写 `words`；再分配其他依赖表 ID 和业务表 ID。
7. 按 ID 分层规则生成正式数据和正常/边界/分支/联动测试值；为每个新增或修改 ID 建立 `id_allocations` 台账，标明作用域、构成规则、父ID、来源、状态和碰撞检查结果。AI 补齐值逐字段标记 S/T/D/A。业务表玩家文本字段只写语言 ID，公式仅用于策划辅助，导出区优先写最终值。
8. QA：输出路径、工作簿聚合、结构、类型、JSON、ID、外键、文本硬编码、语言 ID/文本/占位符、数值、公式缓存、重复字段名、END、样式、导出开关。
9. 用当前导表器做试导出或等价模拟，确认客户端/服务端 JSON/BSON 中的行和字段符合预期。
10. 在指定路径交付 Excel、工作簿归属计划、受影响表清单、语言条目清单、测试值说明（含 S/T/D/A、依据与预期结果）、依赖新增清单和 QA 报告；逐个回查绝对文件路径。

## 14. AI 交付检查清单

- [ ] 已解析用户指定输出路径，所有最终文件均实际存在于该路径；未擅自写入默认或临时目录。
- [ ] 已输出工作簿归属计划；同一功能的主表/子表/明细表集中在一个 xlsx 的多个 Sheet 中。
- [ ] 没有出现多个只含单个同功能新 Sheet 的碎片化 xlsx；公共表和引用表例外均有归属证据。
- [ ] 本次使用的每个既有功能/公共/引用工作簿均已整本复制到指定输出目录；未直接修改 `Table` 源文件，未只复制单个 Sheet。
- [ ] 每个既有副本均已配置本系统需要的测试数据；清单记录源路径、复制动作、测试 Sheet、ID、added/updated 和用途，并通过源副本差异校验。
- [ ] 正式 Sheet 名以 `t` 开头；备注 Sheet 不以 `t` 开头。
- [ ] 前 6 行完整，A2:A6 固定文字正确。
- [ ] B3=`id`、B6=`int`；所有 ID 正整数、非0、唯一、未越 Int32。
- [ ] 每个新增/修改 ID 都有 `id_allocations` 台账；作用域、B1构成、父ID、来源、状态和碰撞检查已填写，未把无依据的max+1或保留值当正式ID。
- [ ] 每个字段第 1–6 行非空；字段名 lowerCamelCase 且不重复。
- [ ] 只使用当前类型 `int/str/arr/bool`，未擅自引入新类型。
- [ ] `arr` 能被严格 JSON 解析；`bool` 使用 `True/False`。
- [ ] `END` 列存在，辅助公式和备注均位于其右侧。
- [ ] 0、空、`[]` 的选择符合字段说明，并验证客户端省略语义。
- [ ] 所有直接外键存在；数组内 ID 全部存在；动态参数逐分支验证。
- [ ] 所有玩家可见文本均进入 `tlanguage_cn`，业务表没有硬编码显示文案。
- [ ] 所有非 0 语言 ID 均存在且 `words` 非空；复用 ID 的语义和语境一致。
- [ ] 占位符、富文本标签、图标标记与业务参数数量、顺序和类型匹配。
- [ ] 概率、权重、时间、金额、倍率单位明确且与同列一致。
- [ ] `min <= max`，数量/权重/ID 无意外负数，哨兵有注释。
- [ ] 测试行覆盖正常、边界、分支，且至少有一个非零导出字段。
- [ ] 策划案缺少数值时已自动生成测试配置，没有无故留空；AI 补齐字段均标记 S/T/D/A、依据和预期结果。
- [ ] AI 假设值明确标为“测试假设，可运行，待策划确认”，未冒充正式平衡或商业化数值。
- [ ] 测试组合覆盖必要的跨表联动；测试依赖 ID 和语言 ID 均已实际生成或引用现有值。
- [ ] 导出区公式有缓存值且无 `#REF!/#VALUE!/#N/A`；最好改为最终静态值。
- [ ] 试导出后行数、主键和关键字段与预期一致。

## 15. 可直接复用的 AI 指令

```text
请先读取：
1. Bubble配置表_AI生成规范.md
2. Bubble配置表_AI字段字典.json
3. Bubble配置表_AI关系字典.json
4. 本次涉及的原始xlsx及其相邻正式Sheet

根据我提供的策划案生成/修改配置表。必须遵守6行表头、B列主键、END截断、现有ID分段、字段类型、客户端/服务端开关、严格JSON数组和跨表引用规则。所有玩家可见、需要展示或可能本地化的文本必须先配置到tlanguage_cn，其他业务表只能保存tlanguage_cn.id，禁止直接硬编码显示文案。

用户指定的输出路径是硬约束：所有最终文件必须保存到该路径并按绝对路径回查。若未指定路径，才能使用默认目录。同一系统功能的主表、子表、明细表、池表、阶段表和参数表必须集中在一个xlsx中并分成不同Sheet，禁止把同一功能的多个新Sheet拆成多个xlsx。凡本系统需要使用既有功能表、公共表或其他系统引用表，必须把该表原属xlsx整本复制到指定输出目录，在副本的原属Sheet中配置本系统需要的测试数据；禁止修改Table源表、只复制单个Sheet或只复制依赖而不配测试行。

如果策划案未提供部分或全部配置数值，不要停在提问或空表：按规范第12.1节自动参考现有表分布、字段单位、边界、公式和关联关系，设计可运行的正常值、边界值、分支值和联动值。把每个补齐值标记为S/T/D/A并说明依据与预期；AI假设统一标为“测试假设，可运行，待策划确认”，不得冒充正式平衡数值。

先输出“绝对输出路径 + 工作簿归属计划（功能、源xlsx、目标xlsx、Sheet、角色、created/copied_and_modified、测试行、依据）+ ID 分配台账（Sheet、ID、scope、kind、构成规则、parent_id、S/T/D/A、status、碰撞检查）+ 表映射 + 字段映射 + 语言条目清单（新增/复用ID、中文文本、消费者字段、占位符）+ 其他ID候选 + 依赖关系 + 数值单位 + 测试值来源 + 待确认项”，再生成xlsx。先复制全部既有依赖工作簿，再在副本中生成tlanguage_cn和其他依赖测试行，最后生成业务表引用。为每个业务分支配置正常值、边界值、分支值和必要的联动值；非法样例只能放在非导出区。不要虚构目标表不存在的外键，不要把所有概率都当万分比，不要把声明为int的现有小数取整。

交付前必须回读并检查：输出路径正确、同功能工作簿没有碎片化、177表规范兼容、ID唯一、字段名唯一、JSON可解析、外键存在、无业务表硬编码显示文案、语言ID存在且文本非空、占位符替换正确、min<=max、公式缓存有效、无公式错误、试导出行列符合预期。最后附绝对文件路径、工作簿归属计划、语言条目清单、测试值预期结果和未确认项。
```

## 16. 当前源表的已知历史风险

这些是审计发现，**不是可复制的规范**：

- 7 个 Sheet 存在重复英文字段名（如 `tips/description/name`）；新表必须消除。
- `tBuff` 同名正式 Sheet 同时存在于 `B_BUFF_tBuff.xlsx` 与 `J_技能表_tSkill.xlsx`；在确认哪一张有效前，不应自动修改或同时导出两张。
- 导出区识别到 23,101 个公式单元格，其中 5 个 Sheet 共 289 个公式在当前文件缓存中无值。公式若未被 Excel 重算，导表器可能读到空文本。
- 部分 `0/0` 辅助字段仍位于 `END` 左侧；新表应把纯辅助列放到 `END` 右侧。
- 39 个正式 Sheet 没有列 `END`；仅因右侧无辅助列而兼容。
- 样式、冻结位置、命名大小写和拼写存在历史差异；新增内容应遵循本规范的收敛规则，而不是复制异常。
- 当前字段字典和关系图是 2026-08-27 快照。源表更新后应重新扫描，不能视为永久不变的数据库 Schema。

## 17. 配套文件

- `Bubble配置表_全表目录.md`：59 个工作簿、177 个导出 Sheet 的人类可读目录。
- `Bubble配置表_AI字段字典.json`：完整字段、注释、类型、开关、ID 范围与公式风险，适合 AI/脚本读取。
- `Bubble配置表_AI关系字典.json`：明确/高/中三级关系、ID 覆盖率和核心枢纽。
