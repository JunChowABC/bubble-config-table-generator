# Bubble 配置表生成器

这是一个面向 Bubble 项目的 Agent Skill：把中文游戏策划案转换为符合项目现有规范的 Excel 配置表，并自动补齐可运行的测试数据、文本配置、ID 和跨表依赖。

## 适用场景

- 根据系统策划案新建或扩展配置表
- 为已有系统补充测试配置
- 检查配置表的表头、字段类型、ID、文本引用、数组 JSON 和跨表关系
- 在策划案缺少数值时，按项目现有分布和字段约束设计测试值

Skill 会读取 Bubble 项目的 `策划/配置表/Table` 及随附规范快照。当前快照覆盖 59 个工作簿、213 个 Sheet、177 个可导出 `t*` Sheet 和 1431 个字段。

## 核心规则

### 输出路径

用户指定的输出目录或完整 `.xlsx` 路径是硬约束。所有最终工作簿、`generation-manifest.json` 和 QA 报告都必须写入该路径，并在交付前按绝对路径检查文件存在。

### 一个功能一个主工作簿

同一系统功能的主表、子表、明细表、池表、阶段表和参数表集中在一个主 `.xlsx` 中，用多个 Sheet 组织。不会因为新增了多个 Sheet 就拆成多个主工作簿。

公共表和其他系统引用表可以作为独立工作簿交付，但必须有清单中的归属依据。

### 既有配置表依赖

如果本系统需要使用 `Table` 中已有的配置表：

1. 将该 Sheet 原属的 `.xlsx` 整本复制到指定输出目录。
2. 保留源工作簿的全部 Sheet、样式、公式、列宽、冻结窗格和既有数据。
3. 只修改输出目录中的副本，不修改 `Table` 源文件。
4. 在副本的原属 Sheet 中配置本系统需要的测试数据，不能只复制空依赖。
5. 同一个源工作簿只复制一次；如果它是已有主功能工作簿，副本就是该功能唯一的主工作簿。

这些信息通过 `generation-manifest.json` 记录，包括 `source_path`、`delivery_action`、`copy_scope`、测试 Sheet、测试 ID 和用途。

### 文本与测试数据

- 所有玩家可见文本统一写入 `tlanguage_cn`，业务表只引用文本 ID。
- ID 遵守目标表 B1 的分段规则，正整数、非 0、表内唯一且不超过 Int32。
- 策划案没有给出的数值会自动设计正常值、边界值、枚举/多态分支值和跨表联动值。
- 测试值标记为 `S/T/D/A`：策划明确值、现有表证据、推导值、AI 假设。AI 假设的交付状态为“测试假设，可运行，待策划确认”，不代表正式平衡数值。

## 快速使用

### Codex

将此目录放在项目的 `.agents/skills/bubble-config-table-generator`，然后调用：

```text
$bubble-config-table-generator 根据这份策划案生成配置表，并自动补齐可运行测试数据。
```

### Claude Code

将 `SKILL.md` 放在 `.claude/skills/bubble-config-table-generator/SKILL.md`，然后调用：

```text
/bubble-config-table-generator 根据这份策划案生成配置表，并自动补齐可运行测试数据。
```

### 豆包工作或其他 Agent

导入仓库中的 `bubble-config-table-generator.zip`。如果产品没有 Agent Skill 导入入口，上传解压后的 `SKILL.md`、`references/` 和 `scripts/`，并把 `SKILL.md` 设为任务主指令。

执行时必须让 Agent 能访问 Bubble 项目的 `策划/配置表/Table`，或者同时提供本次涉及的源工作簿。

## 交付内容

一次完整生成应包含：

- 一个主功能工作簿，以及必要的公共/引用工作簿副本
- `generation-manifest.json`
- 受影响表、字段、ID 和跨表依赖说明
- 文本 ID 与中文文本清单
- 测试数据用途、来源、预期结果和待确认项
- 回读 QA 结果及剩余警告

详细清单格式见 [`references/delivery-manifest-schema.md`](references/delivery-manifest-schema.md)。

## 本地校验

在已生成输出目录中运行：

```powershell
python scripts/qa_delivery_layout.py <输出目录>\generation-manifest.json
python scripts/qa_generated_workbooks.py <工作簿路径...> --table-dir <Bubble项目>\策划\配置表\Table
```

`qa_delivery_layout.py` 会检查输出路径、主工作簿聚合、既有工作簿是否整本复制、源 Sheet 是否完整保留，以及测试行相对源文件是否实际新增或修改。

## 目录说明

| 路径 | 作用 |
| --- | --- |
| `SKILL.md` | Agent 主指令 |
| `references/bubble-config-standard.md` | 项目配置表规范快照 |
| `references/field-dictionary.json` | 字段、类型和表头字典 |
| `references/relation-dictionary.json` | 跨表关系字典 |
| `references/table-catalog.md` | 工作簿和 Sheet 目录 |
| `references/delivery-manifest-schema.md` | 输出清单和依赖副本 Schema |
| `scripts/qa_delivery_layout.py` | 输出路径、工作簿聚合和副本差异 QA |
| `scripts/qa_generated_workbooks.py` | 工作簿结构和关系 QA |
| `scripts/sync_project_references.py` | 从 Bubble 项目重新同步规范快照 |
| `INSTALL.md` | Codex、Claude Code 和其他 Agent 的安装说明 |

## 重要边界

本 Skill 生成的是可运行的测试配置。除非策划明确确认，否则 AI 补齐的数值不能直接视为正式经济、难度、概率或商业化配置；正式上线前仍需经过策划和程序审核。

