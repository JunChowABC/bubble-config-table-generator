# Agent 运行环境兼容规则

技能主体遵循 Agent Skills 的 `SKILL.md + references + scripts` 结构。无论在哪个 Agent 中执行，项目表结构和 QA 标准都相同；工具实现可按环境替换。

## Codex

- 从 `D:\Bubble` 或其子目录工作时使用 `.agents/skills/bubble-config-table-generator`。
- 通过 `$bubble-config-table-generator` 显式调用，也允许根据描述自动触发。
- 创建或编辑 `.xlsx` 时，同时遵守当前 Codex 的电子表格技能。若其规定了专用工作簿库、渲染和导出流程，以该运行时要求为准。
- 仍必须使用本技能的 Bubble 表头、ID、语言表、关系和测试数据规则。

## Claude Code

- 项目入口位于 `.claude/skills/bubble-config-table-generator/SKILL.md`。
- 在 Claude Code 中使用 `/bubble-config-table-generator <策划案或要求>`。
- 入口要求 Claude 读取同项目 `.agents/skills` 下的唯一技能主体，避免两套规则漂移。

## 豆包工作及其他 Agent

- 若产品支持 Agent Skills 目录或技能包导入，导入 `bubble-config-table-generator.zip` 或完整技能目录。
- 若只支持上传文件/知识库，把 `SKILL.md` 设为主指令，并同时上传 `references` 与 `scripts`；要求 Agent 先完整读取 `SKILL.md`。
- 若运行环境不能直接编辑 Excel，可先生成结构化行数据和变更清单，但必须把“未生成/未回读 xlsx”标为阻塞状态，不能宣称配置表已完成。

## 通用最低能力

- 能读取和写入 `.xlsx`，保留现有样式与公式。
- 能解析 JSON、扫描 ID/外键并回读保存后的文件。
- 最好具备 Python 3 + openpyxl 以运行验证脚本；缺少时使用等价工具实现同样检查。
- 默认只写项目输出目录，不覆盖正式 `Table` 源文件。

