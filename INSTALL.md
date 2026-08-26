# 安装与调用

## Codex

项目技能已位于 `.agents/skills/bubble-config-table-generator`。从 `D:\Bubble` 项目中调用：

```text
$bubble-config-table-generator 根据这份策划案生成配置表，并自动补齐可运行测试数据。
```

## Claude Code

项目兼容入口位于 `.claude/skills/bubble-config-table-generator/SKILL.md`。调用：

```text
/bubble-config-table-generator 根据这份策划案生成配置表，并自动补齐可运行测试数据。
```

首次在已打开的 Claude Code 会话中新增顶层 `.claude/skills` 时，若没有立即发现技能，重新启动一次 Claude Code。

## 豆包工作或其他 Agent

导入项目输出的 `bubble-config-table-generator.zip`。若当前产品没有 Agent Skills 导入入口，则上传解压后的 `SKILL.md`、`references` 和 `scripts`，并把 `SKILL.md` 设为该任务的主指令。

技能包不包含 `Table` 下的全部原始工作簿；执行时仍需让 Agent 访问 Bubble 项目的 `策划/配置表/Table`，或把本次涉及的源工作簿一并提供。

