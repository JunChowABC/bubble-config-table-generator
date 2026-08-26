# 生成交付清单 Schema

每次生成配置表都要在用户指定输出目录中创建 `generation-manifest.json`。它既是交付说明，也是输出路径和工作簿聚合 QA 的输入。

```json
{
  "schema_version": "1.0",
  "requested_output_path": "D:/Bubble/指定输出目录",
  "resolved_output_directory": "D:/Bubble/指定输出目录",
  "feature_key": "gacha-event",
  "workbooks": [
    {
      "path": "C_抽卡活动表_tGachaEvent.xlsx",
      "role": "feature",
      "feature_key": "gacha-event",
      "sheets": ["tGachaEvent", "tGachaEventPool", "tGachaEventStage"],
      "reason": "同一抽卡活动功能的主表、池表和阶段表"
    },
    {
      "path": "0W_文本表_tlanguage_cn.xlsx",
      "role": "shared",
      "sheets": ["tlanguage_cn"],
      "reason": "新增玩家可见文本"
    }
  ]
}
```

## 字段规则

- `requested_output_path`：用户原始指定值；未指定时为 `null`。
- `resolved_output_directory`：实际写入目录的绝对路径。
- `feature_key`：同一系统功能使用同一个稳定键。
- `workbooks[].path`：相对 `resolved_output_directory` 的文件名，或该目录内的绝对路径。
- `role=feature`：本功能业务表所在的主功能工作簿。同一个 `feature_key` 必须且只能有一个。
- `role=shared`：语言、公共条件、公共消耗、公共奖励、公共掉落等既有公共工作簿。
- `role=referenced`：其他系统拥有、但本次需要新增引用行的既有工作簿。
- `sheets`：本次新增或修改的 Sheet；必须真实存在于对应 xlsx。
- `reason`：说明为何归入该工作簿，公共/引用例外尤其必须说明。

如果用户指定的是完整 `.xlsx` 路径，`role=feature` 的工作簿绝对路径必须与该路径完全一致。
