# 生成交付清单 Schema

每次生成配置表都要在用户指定输出目录中创建 `generation-manifest.json`。它既是交付说明，也是输出路径、工作簿聚合、既有工作簿完整复制和测试数据差异 QA 的输入。

```json
{
  "schema_version": "1.1",
  "requested_output_path": "D:/Bubble/指定输出目录",
  "resolved_output_directory": "D:/Bubble/指定输出目录",
  "feature_key": "gacha-event",
  "workbooks": [
    {
      "path": "C_抽卡表_tGachaPool.xlsx",
      "role": "feature",
      "feature_key": "gacha-event",
      "source_path": "D:/Bubble/策划/配置表/Table/C_抽卡表_tGachaPool.xlsx",
      "delivery_action": "copied_and_modified",
      "copy_scope": "full_workbook",
      "sheets": ["tGacha", "tPool", "tGuaranteed"],
      "test_data": [
        {
          "sheet": "tGacha",
          "id": 990001,
          "operation": "added",
          "purpose": "本系统正常抽卡链路"
        }
      ],
      "reason": "复用既有抽卡工作簿并补充本系统测试池"
    },
    {
      "path": "0W_文本表_tlanguage_cn.xlsx",
      "role": "shared",
      "source_path": "D:/Bubble/策划/配置表/Table/0W_文本表_tlanguage_cn.xlsx",
      "delivery_action": "copied_and_modified",
      "copy_scope": "full_workbook",
      "sheets": ["tlanguage_cn"],
      "test_data": [
        {
          "sheet": "tlanguage_cn",
          "id": 990101,
          "operation": "added",
          "purpose": "本系统测试活动名称"
        }
      ],
      "reason": "主功能测试数据新增玩家可见文本"
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
- `role=referenced`：其他系统拥有、但本次测试链路需要使用的既有工作簿。
- `sheets`：本次新增或修改的 Sheet；必须真实存在于对应 xlsx。
- `reason`：说明为何归入该工作簿，公共/引用例外尤其必须说明。

如果用户指定的是完整 `.xlsx` 路径，`role=feature` 的工作簿绝对路径必须与该路径完全一致。

## 既有工作簿副本字段

任何来自现有配置表的 `feature/shared/referenced` 工作簿都必须填写：

- `source_path`：源工作簿绝对路径，通常位于 `策划/配置表/Table`。
- `delivery_action`：必须为 `copied_and_modified`；全新创建的主功能工作簿使用 `created` 且不填写 `source_path`。
- `copy_scope`：既有工作簿必须为 `full_workbook`。
- `test_data`：非空数组，逐条记录本系统在副本中新增或修改的测试数据。
- `test_data[].sheet`：测试行所在 Sheet，必须存在于交付副本。
- `test_data[].id`：测试行 B 列主键。
- `test_data[].operation`：`added` 或 `updated`。
- `test_data[].purpose`：该行在本系统测试链路中的用途。

QA 会验证：

1. 源文件和交付副本不是同一个路径，副本位于指定输出目录。
2. 副本保留源工作簿的全部 Sheet；允许在主功能副本中额外增加新 Sheet。
3. `added` ID 在源 Sheet 中不存在、在副本中存在。
4. `updated` ID 在源 Sheet 和副本中都存在，且副本整行内容与源行不同。
5. 同一源工作簿不能在清单中复制成多个交付副本。

只复制工作簿但没有 `test_data`，或声明测试行但副本没有实际差异，都视为交付失败。
