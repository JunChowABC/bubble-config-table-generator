# Bubble 配置表全表目录

> 快照日期：2026-08-27。来源：`D:\Bubble\策划\配置表\Table`。本目录覆盖 59 个工作簿、177 个可导出的 `t*` Sheet。完整字段注释与关系证据见 `Bubble配置表_AI字段字典.json` 和 `Bubble配置表_AI关系字典.json`。

> 全局文本约束：所有玩家可见、需要展示或可能本地化的文本统一配置到 `tlanguage_cn`；其他业务表只保存并读取 `tlanguage_cn.id`，不得直接硬编码显示文案。

> 工作簿组织约束：39/59 个工作簿包含多个正式导出 Sheet。同一系统功能的新增业务表必须集中在一个 `.xlsx` 内，以多个 Sheet 组织；公共表和既有引用表保留在各自工作簿。

## 0J_机制_条件表_tCommonCondition.xlsx

### tCommonCondition

- 数据行：546；字段数：6；ID 范围：99–202100401。
- ID 说明：条件id / 2+模块序号[2]+序号[4]
- 主要关联：tlanguage_cn
- 字段：id:int、conditionType:int、find:str、conditionTypeParam:str、conditionTips:int、missionTips:int

## 0S_数值_掉落表_tCommonDrop.xlsx

### tCommonDrop

- 数据行：4440；字段数：4；ID 范围：1–4440。
- ID 说明：无实际作用
- 主要关联：tCommonReward
- 字段：id:int、dropId:int、rate:int、rewardId:int

### tCommonReward

- 数据行：4624；字段数：7；ID 范围：1–4624。
- ID 说明：无实际作用
- 主要关联：tItem
- 字段：id:int、rewardId:int、weight:int、rewardType:int、rewardTypeParam:int、numsMin:int、numsMax:int

## 0S_数值_消耗表_tCommonConsume.xlsx

### tCommonConsume

- 数据行：2958；字段数：3；ID 范围：10–55500010。
- ID 说明：消耗id
- 主要关联：tItem、tRecharge
- 字段：id:int、consumeType:int、consumeItemList:str

## 0W_文本表_tlanguage_cn.xlsx

### tlanguage_cn

- 数据行：5175；字段数：5；ID 范围：1301–830316901。
- ID 说明：7位数 / 1+序号[6] 物品名 / 8位数 / 1+序号[7] 程序文本（code码、提示） / 2+序号[7] 通用文本 / 3+模块[3]+序号[4] / 4+类型[2]+序号[5]角色 / 5家具 / 6类型[2]+序号[5]食材+菜品 / 7任务 / 8对话文本（新手、事件、xxx） / 9特殊客人+模块[2]+类型[2]+序号[4]
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、words:str、tips:str、tips:str、beizhu:str

## 0_充值表_tRecharge.xlsx

### tRecharge

- 数据行：28；字段数：7；ID 范围：1–28。
- ID 说明：无作用
- 主要关联：tCommonConsume、tGift
- 字段：id:int、rechargeId:int、channelId:int、backstageItem:str、rmb:int、rechargeSymbol:str、reissueWay:int

## 0_全局表_tGlobal.xlsx

### tGlobal

- 数据行：135；字段数：6；ID 范围：20001–42020。
- ID 说明：ID
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、tips:str、key:str、intValue:int、strValue:str、intArrValue:arr

## 0_属性表_tAttribute.xlsx

### tAttribute

- 数据行：29；字段数：8；ID 范围：1000–6005。
- ID 说明：属性id
- 主要关联：tRule、tlanguage_cn
- 字段：id:int、attrType:int、attrLimit:int、attrName:int、attrIcon:str、attrIcon2:str、attrDiscribe:int、description:int

### tFormula

- 数据行：6；字段数：3；ID 范围：10210–10300。
- ID 说明：公式id
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、formulaType:int、formulaParam:arr

## B_BUFF_tBuff.xlsx

### tBuff

- 数据行：3；字段数：6；ID 范围：1010–1030。
- ID 说明：buffid
- 主要关联：tEffectRes
- 字段：id:int、buffType:int、buffTypeParam:int、stackType:int、maxDuration:int、mutexGroup:int

## B_宝箱表_tChest.xlsx

### tChest

- 数据行：8；字段数：4；ID 范围：1010–2050。
- ID 说明：ID
- 主要关联：tCommonDrop
- 字段：id:int、drop:int、openTime:int、inBoxShow:int

## C_code码表_tCode.xlsx

### tCode

- 数据行：10；字段数：4；ID 范围：1–10。
- ID 说明：\
- 主要关联：tlanguage_cn
- 字段：id:int、type:int、code:int、textId:int

## C_场景表_tScene.xlsx

### tScene

- 数据行：4；字段数：10；ID 范围：10101–40101。
- ID 说明：101~199：餐厅场景 / 201~299：挖矿场景 / 301~399：家具场景 / 401~499：其他场景
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、sceneType:int、sceneFileName:str、defaultCamera:arr、cameraRange:arr、cameraMultiple:int、sceneBoundary:arr、customerBuildCoord:str、customerEnterCoord:str、customerQueueCoord:str

### tSceneArea

- 数据行：4；字段数：13；ID 范围：10101–10104。
- ID 说明：区域id / 场景id+区域id[2]
- 主要关联：tCommonCondition、tCommonConsume、tScene
- 字段：id:int、sceneId:int、areaRange:str、hudDisplay:int、unlockType:int、unlockTypeParam:int、条件查询:int、unlockConsume:int、limitAdd:int、unlockedSpine:str、spineCoordinate:arr、spineOffset:arr、unlockedHud:arr

### tSceneAreaDecoration

- 数据行：3；字段数：5；ID 范围：1–3。
- ID 说明：无作用
- 主要关联：tDecoration、tScene
- 字段：id:int、sceneId:int、areaId:int、decorationId:int、coordinate:arr

### tSceneUnlock

- 数据行：3；字段数：10；ID 范围：1–3。
- ID 说明：无意义
- 主要关联：tCommonCondition、tCommonConsume、tCommonDrop、tDialogueTable、tScene、tlanguage_cn
- 字段：id:int、sceneId:int、schedule:int、condition:arr、consume:int、reward:int、triggerTalkId:int、prefabNode:str、icon:str、desc:int

## C_抽卡表_tGachaPool.xlsx

### tSubGacha

- 数据行：5；字段数：18；ID 范围：3000000–3020003。
- ID 说明：ID / （30+2位数类型+3位数序号）
- 主要关联：tCommonConsume、tlanguage_cn
- 字段：id:int、consume:int、price:arr、points:arr、max:int、gachaType:int、rewards:int、randTimes:arr、randWeight:arr、freeTime:int、freeOrder:arr、freeCd:int、name:int、describe:int、bg:str、pageIcon:str、pageName:int、pageSort:int

### tGacha

- 数据行：5；字段数：10；ID 范围：3000000–3020003。
- ID 说明：ID / （30+2位数类型+3位数序号）
- 主要关联：tCommonCondition
- 字段：id:int、type:int、quaInPool:arr、quaWeight:arr、smallPity:arr、bigPity:arr、pity:arr、stepPity:arr、setID:int、unlock:int

### tPool

- 数据行：325；字段数：6；ID 范围：10–10600。
- ID 说明：ID / 物品ID+3位序号
- 主要关联：tGacha、tItem
- 字段：id:int、gachaId:int、quality:int、items:arr、weight:int、sort:int

### tGuaranteed

- 数据行：13；字段数：8；ID 范围：1010–3030。
- ID 说明：ID / 卡池+2位序号
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、guaType:int、keyQuality:arr、maxMum:int、props1:arr、props1Weight:arr、props2:arr、rangeProb:str

### tSpReward

- 数据行：6；字段数：4；ID 范围：1010–1060。
- ID 说明：ID（卡池表ID+1位序号）
- 主要关联：tItem
- 字段：id:int、id2:int、times:int、spRewardList:arr

### tGachaInfo

- 数据行：1；字段数：7；ID 范围：3000000–3000000。
- ID 说明：所属卡池
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、spRare:arr、spRarePro:int、rare:arr、rarePro:int、normal:arr、normalPro:int

## C_菜品表_tFood.xlsx

### tFoodType

- 数据行：6；字段数：2；ID 范围：1–6。
- ID 说明：ID
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、animator_id:arr

### tFoodIngredient

- 数据行：31；字段数：2；ID 范围：4011001–4014070。
- ID 说明：ID
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、name:str

### tFood

- 数据行：55；字段数：17；ID 范围：3001–3055。
- ID 说明：ID
- 主要关联：tCommonDrop、tlanguage_cn
- 字段：id:int、type:int、subtype:int、name:int、icon:str、ingredient_needs:str、food_taste:int、food_text:int、cookLimitTime:int、kitchenBonus:int、foodUnlockReward:int、unlockType:int、unlockTypeParam:arr、rubbishId:int、trendDropProb:int、trendDropCount:arr、dropCountWeight:arr

### tLvFood

- 数据行：1100；字段数：14；ID 范围：10000–20990。
- ID 说明：ID
- 主要关联：tCommonConsume、tFood
- 字段：id:int、food_id:int、food_lv:int、food_value:int、food_sell:int、food_time:int、cook_time:int、cookLessCost:int、cookSpUp:int、rearCoin:int、levelConsume:int、levelBoost:int、taste_value:int、foodEfficiency:int

### tFoodCollectReward

- 数据行：1；字段数：8；ID 范围：1–1。
- ID 说明：ID
- 主要关联：tCommonDrop、tlanguage_cn
- 字段：id:int、group:arr、sectionName:int、sectionReward:int、collectNum:int、rewardShow:str、rewardInfo:int、remind:int

### tFoodCollectGroup

- 数据行：1；字段数：3；ID 范围：1001–1001。
- ID 说明：ID
- 主要关联：tFood、tlanguage_cn
- 字段：id:int、sectionFood:arr、groupName:int

### tFoodCombo

- 数据行：36；字段数：4；ID 范围：1–36。
- ID 说明：ID
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、foodTaste1:int、foodTaste2:int、comboBonus:int

## D_动画表_tSpineAnimKey.xlsx

### tSpineAnimKey

- 数据行：62；字段数：3；ID 范围：1001–8007。
- ID 说明：1001: CommonAnimKey (通用动作) / 2001: Customer (顾客) / 3001: Employee (员工) / 4001: Miner (矿工) / 5001: Furniture (家具) / 6001: Rubbish (垃圾) / 7001：UI动效 / 8001：怪物
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、animName:str、repet:bool

## D_对话表_tDialogueTable.xlsx

### tDialogueTable

- 数据行：237；字段数：8；ID 范围：102040–1011020。
- ID 说明：对话组id / 1+5位数：剧情 / 2+5位数：其他模块 / 按模块递增 201 201..... / 7位数：新手引导
- 主要关联：tCommonDrop、tDialogContent
- 字段：id:int、dialogueIdList:arr、dialogReward:int、rewardPopup:int、rewardNode:int、isPauseGame:int、skippable:int、priority:int

### tDialogContent

- 数据行：563；字段数：18；ID 范围：2010010–30316901。
- ID 说明：内容id
- 主要关联：tlanguage_cn
- 字段：id:int、type:int、dialogBg:str、typeParam:int、tips:str、roleId:int、text:int、tips:str、textDelay:int、textSpeed:int、offsetPosition:arr、mask:int、animation:int、showPic:str、picPosition:arr、picSize:int、picAnime:str、animationName:str

### tGuideTrole

- 数据行：47；字段数：7；ID 范围：11140101–24020301。
- ID 说明：ID
- 主要关联：tlanguage_cn
- 字段：id:int、tips:str、tips:str、tips:str、expression:str、name:int、shadow:str

## G_功能表_tFunction.xlsx

### tFunction

- 数据行：53；字段数：14；ID 范围：1001–100401。
- ID 说明：ID
- 主要关联：tCommonCondition、tDialogueTable、tView、tlanguage_cn
- 字段：id:int、nameId:int、unlockType:int、unlockTypeParam:int、iconUnlock:arr、备注:int、unlockedTips:arr、showUnlockEffect:bool、icon:str、openUnlockView:int、unlockFlyShow:int、unlockIcon:str、viewId:int、uiComPath:str

## G_岗位表_tPost.xlsx

### tPost

- 数据行：18；字段数：6；ID 范围：1110101–1120106。
- ID 说明：岗位id / 不能改 / 场景[2]+岗位[3]+序号{2]
- 主要关联：tCommonCondition、tPostOrder、tTask、tlanguage_cn
- 字段：id:int、postType:int、postUnlockCondition:int、postOrderTask:arr、postClass:str、workingStateText:int

### tPostOrder

- 数据行：4；字段数：2；ID 范围：1–4。
- ID 说明：订单类型id / 订单任务类型 / 1烹饪  2点餐 3上菜 4清洁 / 研发不算
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、orderPriority:int

## G_广告_电视盒子_tAdTvBox.xlsx

### tAdTvBox

- 数据行：3；字段数：9；ID 范围：1–3。
- ID 说明：id
- 主要关联：tActivity、tBuff、tGift、tViewJump、tlanguage_cn
- 字段：id:int、tvType:int、tvTypeParam:arr、tvStyle:int、tvStyleParam:str、tvFurnitureSkin:str、tvBanner:str、tvTitle:int、tvDesc:int

### tAdTvBoxReward

- 数据行：3；字段数：3；ID 范围：1–3。
- ID 说明：id
- 主要关联：tCommonDrop
- 字段：id:int、watchTimes:int、reward:int

## G_规则表_tRule.xlsx

### tRule

- 数据行：22；字段数：6；ID 范围：1–210。
- ID 说明：无实际作用
- 主要关联：tlanguage_cn
- 字段：id:int、ruleId:int、ruleType:int、ruleTitle:int、ruleContent:int、illustration:str

## H_活动表_tActivity.xlsx

### tActivity

- 数据行：6；字段数：20；ID 范围：101010–105010。
- ID 说明：活动类型[3]+活动序号[2]+插入预留[1]
- 主要关联：tCommonCondition、tGfitLink、tGift、tGiftCheckIn、tlanguage_cn
- 字段：id:int、actType:int、actTypeParam:int、backendSwitch:int、actPlatform:arr、actOpenLimit:int、actOpenCondition:int、actOpenConditionParam:int、tips:str、actJoinCondition:int、actJoinConditionParam:int、actEndCondition:int、actEndConditionParam:int、actEntrance:int、actEntranceParam:int、subActList:arr、actNameType:int、actIcon:str、actBanner:str、actSort:int

## H_货币栏补给表_tCurrencyAdd.xlsx

### tCurrencyAdd

- 数据行：13；字段数：6；ID 范围：1–20。
- ID 说明：无作用
- 主要关联：tCommonConsume、tCurrencyAddDining
- 字段：id:int、lattice:int、nums:int、consume:int、reward:int、rewardDisplay:str

### tCurrencyAddDining

- 数据行：3；字段数：5；ID 范围：1–3。
- ID 说明：\
- 主要关联：tItem
- 字段：id:int、groupId:int、DiningLevel:arr、rewards:arr、idleRewardTime:int

## J_剧情表_tPlot.xlsx

### tPlot

- 数据行：32；字段数：16；ID 范围：101004–300104。
- ID 说明：剧情id /  / 1开头=被动触发主线剧情 / 2开头=手动触发主线任务剧情 / 3开头=顾客好感剧情
- 主要关联：tAttribute、tPlotStep、tTask
- 字段：id:int、tips1:int、tips2:int、hangPlotId:arr、hangCondition:arr、hangConditionParam:arr、needItem:str、needItemRecycle:int、extraCondition:arr、extraConditionParam:str、plotScene:int、plotStep:arr、pauseSwitch:int、closeComponent:int、openComponent:int、plotResourceDelete:arr

### tPlotStep

- 数据行：51；字段数：4；ID 范围：9999999–103018020。
- ID 说明：步骤id
- 主要关联：tCommonDrop、tDialogueTable
- 字段：id:int、stepType:int、stepTypeParam:int、blackScreen:int

### tPlotTimeLine

- 数据行：11；字段数：8；ID 范围：1000–10401。
- ID 说明：timeLineId
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、timeLinePath:str、endTime:int、createWay:int、createWayParam:arr、clickToClose:int、closeToDelete:int、blackScreen:int

## J_家具商店表_tShop.xlsx

### tShop

- 数据行：5；字段数：10；ID 范围：1–5。
- ID 说明：ID
- 主要关联：tCommonCondition、tlanguage_cn
- 字段：id:int、decoshopPosion:str、tabName:int、welcome:int、refreshBoard:int、refreshType:int、refreshParam:str、cameraMove:str、cameraIn:str、priceShow:int

### tShopCustom

- 数据行：1；字段数：3；ID 范围：1–1。
- ID 说明：ID
- 主要关联：tRole
- 字段：id:int、inShopCustom:arr、customValue:arr

### tShopPool

- 数据行：14；字段数：3；ID 范围：101–205。
- ID 说明：ID
- 主要关联：tCommonCondition、tDecoration
- 字段：id:int、poolContain:str、poolUnlock:int

### tDecoPlace

- 数据行：36；字段数：10；ID 范围：1001–9009。
- ID 说明：ID
- 主要关联：tCommonCondition、tCommonConsume、tDecoration、tShopPool、tlanguage_cn
- 字段：id:int、posionFurniType:arr、posionPic:str、posionSize:arr、posionUnlock:int、posionUnlockWord:int、firstRefreshFurni:int、decoShopPool:str、refreshTime:int、refreshNeeds:int

### tShopDecoration

- 数据行：634；字段数：7；ID 范围：1000301–1190404。
- ID 说明：ID
- 主要关联：tCommonCondition、tCommonConsume、tDecoration
- 字段：id:int、furniId:int、furniUnlock:int、consume:int、buyLimit:int、discountRate:int、discountParam:int

### tShopRefresh

- 数据行：12；字段数：4；ID 范围：10–340。
- ID 说明：ID
- 主要关联：tCommonConsume、tShop
- 字段：id:int、sub:int、refreshTimes:arr、consume:int

### tDecoShopTheme

- 数据行：5；字段数：10；ID 范围：1300010–1300050。
- ID 说明：ID
- 主要关联：tDecoration、tlanguage_cn
- 字段：id:int、name:int、designerSize:arr、designer_position:str、designerWall:arr、paperPos:str、deskPos:str、deskBackPos:str、moduleParam:str、moduleNum:int

### tDecoShopMoudel

- 数据行：5；字段数：8；ID 范围：130010–130050。
- ID 说明：ID
- 主要关联：tCommonConsume、tItem、tlanguage_cn
- 字段：id:int、name:int、smallIcon:str、banner:str、iconShow:int、designerSize:arr、designer_position:str、designerPrice:int

### tDecoShop

- 数据行：45；字段数：8；ID 范围：1305000–1314003。
- ID 说明：ID
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、name:str、icon:str、money:int、collection_point:int、collection:int、restcok_time:int、unlock_shoprank:int

## J_家具表_tDecoration.xlsx

### tDecorationType

- 数据行：8；字段数：3；ID 范围：1–8。
- ID 说明：1-厨房2-餐桌3-装饰4-绿植 / 5-墙壁6-地板7-地毯 / 8-收银台
- 主要关联：tlanguage_cn
- 字段：id:int、name:int、initialLocation:str

### tDecorationSet

- 数据行：20；字段数：4；ID 范围：130000–130019。
- ID 说明：ID
- 主要关联：tlanguage_cn
- 字段：id:int、name:int、dcset_icon:str、dcsetBanner:str

### tDecoration

- 数据行：710；字段数：27；ID 范围：1000301–1200403。
- ID 说明：ID
- 主要关联：tAttribute、tCommonCondition、tCommonConsume、tDecorationTab、tDecorationType、tlanguage_cn
- 字段：id:int、displaySwitch:int、tabType:int、decoration_id:int、dcset_id:int、styleParam:str、decoration_value:arr、furniPlaceInfo:arr、decoration_size:str、name:int、icon:str、wallInShop:str、decorationType:int、animation:str、cusani_type:int、salesType:int、salesParam:int、show:int、skeletonData:str、unlockReward:int、decoration_text:int、defaultAni:str、stoveAniAction:str、triggerAniType:int、triggerAniTypeParam:str、ableRecycle:int、showUnlockLevel:int

### tDecorationSYT

- 数据行：11；字段数：3；ID 范围：1010801–1140801。
- ID 说明：ID
- 主要关联：tDecoration
- 字段：id:int、frontFurniture:str、afterFurniture:str

### tDecorationTab

- 数据行：10；字段数：2；ID 范围：101–208。
- ID 说明：页签id
- 主要关联：tlanguage_cn
- 字段：id:int、tabName:int

### tDecorationFuncTab

- 数据行：8；字段数：4；ID 范围：1–8。
- ID 说明：无作用
- 主要关联：tViewJump
- 字段：id:int、mainTab:int、subTab:int、jumpId:int

## J_技能表_tSkill.xlsx

### tSkill

- 数据行：114；字段数：9；ID 范围：1110–91150。
- ID 说明：ID
- 主要关联：tlanguage_cn
- 字段：id:int、tips1:str、tips2:str、effect:arr、skillLevel:int、condition:int、name:int、labelTxt:int、icon:str

### tSkillEffect

- 数据行：143；字段数：19；ID 范围：10–30540。
- ID 说明：技能效果id
- 主要关联：tEffectRes
- 字段：id:int、condition:int、note:str、note2:str、conditionParam:arr、triggerChance:int、maxTriggers:int、triggerCooldown:int、targetType:int、targetParam:int、effectType:int、note2:str、param:arr、unique:int、actionType:str、effectStartTime:int、activateTime:int、effectTarget:int、skillEffect:int

### tBuff

- 数据行：22；字段数：8；ID 范围：1010–2150。
- ID 说明：buffid
- 主要关联：tEffectRes
- 字段：id:int、name:str、buffType:int、name:str、buffParam:arr、endType:int、endParam:int、skillEffect:int

## J_界面表_tView.xlsx

### tView

- 数据行：110；字段数：5；ID 范围：5–9003。
- ID 说明：界面id / 程序枚举 / 9000以上 id是虚构的
- 主要关联：tItem
- 字段：id:int、viewName:str、coin:arr、coinOffset:arr、sort:arr

### tViewJump

- 数据行：45；字段数：5；ID 范围：10101–17101。
- ID 说明：跳转id
- 主要关联：tItem、tlanguage_cn
- 字段：id:int、viewJumpType:int、viewName:str、viewJumpParam:arr、unlockedTips:int

## J_经营_派对玩法.xlsx

### tPartyRefresh

- 数据行：1；字段数：5；ID 范围：101–101。
- ID 说明：池子id
- 主要关联：tCommonCondition、tParty
- 字段：id:int、unlockCondition:int、poolWeight:int、partyId:arr、partyIdWeight:arr

### tParty

- 数据行：3；字段数：15；ID 范围：10101–10103。
- ID 说明：派对id
- 主要关联：tCommonDrop、tCustomer、tCustomerCreateTag、tEmployee、tItem、tScene、tlanguage_cn
- 字段：id:int、filter:arr、time:int、sceneId:int、ingredientNeed:int、employeeNeed:str、customerList:int、customerTime:arr、customerNums:arr、reward:str、ingredientNums:int、ingredientText:int、banner:str、partyName:int、difficulty:int

### tPartyActionParam

- 数据行：12；字段数：4；ID 范围：1–12。
- ID 说明：无作用
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、filter:int、actionType:int、actionTypeParam:int

### tPartyReward

- 数据行：15；字段数：6；ID 范围：101011–101035。
- ID 说明：奖励id
- 主要关联：tCommonDrop、tCommonReward
- 字段：id:int、integral:int、evaluate:int、integralReward:int、icon1:str、icon2:str

## J_经营_烹饪表_tManageEventFilter.xlsx

### tManageEventFilter

- 数据行：2；字段数：7；ID 范围：1–2。
- ID 说明：无作用
- 主要关联：tCommonCondition、tManage
- 字段：id:int、manageEventType:int、eventTypeParam:int、unlockCondition:int、filter:int、filterParam:int、weight:int

### tManageEventCookFail

- 数据行：5；字段数：4；ID 范围：1–5。
- ID 说明：无作用
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、filterParam:arr、failRate:int、failTimes:int

### tManageEventCookTime

- 数据行：2；字段数：3；ID 范围：1–2。
- ID 说明：无作用
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、filterParam:arr、failRate:int

## J_经营表_tManage.xlsx

### tManage

- 数据行：40；字段数：22；ID 范围：1–40。
- ID 说明：餐厅阶级
- 主要关联：tCommonCondition、tCommonConsume、tCommonDrop、tRubbish、tScene
- 字段：id:int、upCondition:arr、upReward:int、queueLength:int、queueLength2:int、dinnerRubbishTime:int、rubbishLimit:int、offlineConsume:int、charaLvLimit:int、limitType:arr、limitValue:int、lvEfficiency:int、limitEfficiency:int、rubbishTime:int、upConsume:int、addCustomerTimeLimit:int、addCustomerTime:int、cus_num:arr、popularParam:int、popularNums:int、rubbishParam:arr、cus_weight:str

### tLevelReward

- 数据行：39；字段数：6；ID 范围：1–39。
- ID 说明：ID
- 主要关联：tItem
- 字段：id:int、restuarantLv:int、rewardType:int、rewardNum:str、priority:int、rewardIcon:str

### tManageLevelCondition

- 数据行：117；字段数：6；ID 范围：2010011–2010393。
- ID 说明：ID
- 主要关联：tCommonCondition、tViewJump、tlanguage_cn
- 字段：id:int、conditionId:int、icon:str、jumpType:int、jumpTypeParam:int、jumpId:int

### tLevelNeeds

- 数据行：120；字段数：5；ID 范围：1–120。
- ID 说明：ID
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、restuarantLv:int、needsType:int、needsNum:int、needsRange:int

### tManageValue

- 数据行：50；字段数：12；ID 范围：1–50。
- ID 说明：无作用
- 主要关联：tScene
- 字段：id:int、level:int、sceneId:int、popularMin:int、popularMax:int、cleanMax:int、cleanFirst:int、cleanReduceTime:int、cleanCreateTime:int、diningCleanReduce:arr、rubbishCleanReduce:arr、foodTypeLimitNums:str

### tManageCustCreateTime

- 数据行：160；字段数：5；ID 范围：10–1600。
- ID 说明：无作用
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、level:int、popular:arr、time:int、rubbishTime:int

### tManageCustCreateNums

- 数据行：160；字段数：7；ID 范围：10–1600。
- ID 说明：无作用
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、level:int、popular:arr、nums:arr、numsWeight:arr、trendNums:arr、trendNumsWeight:arr

## J_角色_顾客表_tCustomer.xlsx

### tCustomer

- 数据行：89；字段数：15；ID 范围：22010101–230400601。
- ID 说明：id
- 主要关联：tEffectRes、tFood、tRole
- 字段：id:int、role_id:int、customerNeeds:str、needsDelic:int、customerLv:int、lvUpTimes:int、queueTime:int、waitNeedTime:int、waitDinnerTime:int、waitTime:int、needTime:int、eat_time:int、defaultSatis:int、effectId:arr、leaveSatis:int

### tCustomerSatis

- 数据行：85；字段数：9；ID 范围：1–503。
- ID 说明：id
- 主要关联：tCustomer
- 字段：id:int、customerId:int、satisParam1:arr、satisParam2:int、satisParam3:arr、satisParam4:arr、satisParam5:arr、satisParam6:int、satisParam7:arr

### tCustomerPopular

- 数据行：4；字段数：4；ID 范围：1–4。
- ID 说明：id
- 主要关联：tCustomer
- 字段：id:int、customerId:int、popularInterval:arr、popular:int

### tCustomerOrdering

- 数据行：5；字段数：6；ID 范围：1–5。
- ID 说明：id
- 主要关联：tCustomer、tRole
- 字段：id:int、foodType:int、numsTag:int、roleId:int、priority:int、weight:int

### tCustomerCreateTag

- 数据行：2；字段数：5；ID 范围：101–102。
- ID 说明：标签id
- 主要关联：tCommonCondition
- 字段：id:int、unlockCondition:int、weight:int、randomRule:int、randomParam:str

### tCustomerCreatePool

- 数据行：43；字段数：6；ID 范围：10101–101999。
- ID 说明：池子id
- 主要关联：tCustomerCreateTag、tRole
- 字段：id:int、tagId:int、filter:int、filterParam:arr、weight:int、customerList:str

### tCustomerShow

- 数据行：23；字段数：3；ID 范围：2201001–2303001。
- ID 说明：对应tRole:id
- 主要关联：tCommonCondition、tRole
- 字段：id:int、comeType:arr、eatType:arr

### tCustomerChara

- 数据行：20；字段数：2；ID 范围：1–20。
- ID 说明：特性id
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、name:int

### tCustomerStory

- 数据行：80；字段数：10；ID 范围：220100101–220200704。
- ID 说明：唯一id，无意义
- 主要关联：tCustomer、tItem、tPlot、tlanguage_cn
- 字段：id:int、cusId:int、friendshipLv:int、friendshipGift:str、ifSpecial:int、mission:int、story:int、enterBack:int、storyCharater:arr、storyId:int

## J_角色动线表_tRoleStateLine.xlsx

### tRoleStateLine

- 数据行：66；字段数：6；ID 范围：10–9021。
- ID 说明：大类[2]+序号[2]+事件变种序号[1] / 101~199：通用 / 201~299：员工 / 301~499：顾客 / 501~699：事件npc / 901~999：特殊
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、statePriority:int、stateBreakOff:int、beginEvent:int、endEvent:int、actionBreakOff:int

### tRoleLineBehavior

- 数据行：86；字段数：14；ID 范围：1001–907101。
- ID 说明：无实际作用
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、stateId:int、remark:str、behaviorOrder:arr、linePriority:int、lineWeight:int、lineLoopSwitch:int、lineBreakSwitch:int、lineEvent:arr、lineEventParams:arr、lineFilter1:int、lineFilter2:int、lineFilter3:int、lineFilter4:arr

### tRoleBehaviorAction

- 数据行：125；字段数：17；ID 范围：100101–90710101。
- ID 说明：行为id
- 主要关联：tRoleActionGroup、tRoleInteraction、tRoleStateLine
- 字段：id:int、behaviorActionTag:int、behaviorType:int、behaviorTypeParam:int、behaviorTarget:int、behaviorTargetParam:str、beginEvent:arr、endEvent:arr、actionTimeType:int、actionLoopTimes:arr、中断备注:str、actionBreakOff:arr、actionBreakOffEvent:arr、interactionId:int、bubbleType:int、bubbleEndPerform:int、bubbleBreakOff:int

### tRoleActionGroup

- 数据行：166；字段数：12；ID 范围：100100–116010。
- ID 说明：无作用
- 主要关联：tAttribute、tBuff、tRole、tScene
- 字段：id:int、tagId:int、actionGroupPriority:int、weight:int、actionList:arr、roleWalkAction:arr、roleWalkAction2:arr、roleWalkExtraAction:arr、filter1:arr、filter2:int、filter3:arr、filter3Param:arr

### tRoleAction

- 数据行：113；字段数：7；ID 范围：10101–401101031。
- ID 说明：动作大类[1]+子类[2]+数量[2] /  / 9=烹饪手部动作
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、actionName:str、actionTime:int、actionTimeExtend:int、actionEvent:arr、cookingAction:str、cookEndingAction:int

### tRoleInteraction

- 数据行：8；字段数：5；ID 范围：1011–4011。
- ID 说明：无作用 / 后面可能同个事件类型不同参数
- 主要关联：tRole、tViewJump
- 字段：id:int、eventType:int、eventTypeParam:int、eventPriority:int、eventEndCoolTime:int

## J_角色表_tRole.xlsx

### tRole

- 数据行：102；字段数：32；ID 范围：2114001–2501009。
- ID 说明：ID
- 主要关联：tCommonConsume、tCommonDrop、tItem、tRoleStateLine、tSkill、tlanguage_cn
- 字段：id:int、roleTag:arr、roleType:int、role_rank:int、roleSpeed:int、defaultStateId:int、roleClass:int、roleLevel:int、roleStar:int、roleEnergyLimit:int、roleRestParam:arr、roleFallTime:int、starNeeds:int、levelMoudel:int、starMoudel:int、skillMoudel:arr、starReward:arr、name:int、body:str、spine_skin:str、skeletonData:str、skinId:arr、starUpAni:str、show:int、unlockReward:int、icon:str、small_icon:str、collectPoints:int、role_text:int、role_bobby:int、bubbleOffsetY:int、composeConsume:arr

### tRoleStory

- 数据行：72；字段数：8；ID 范围：101–1804。
- ID 说明：ID
- 主要关联：tCommonDrop、tRole、tlanguage_cn
- 字段：id:int、roleId:int、icon:str、unlockType:int、unlockParam:int、storyPic:str、storyWord:arr、reward:int

### tSkin

- 数据行：20；字段数：5；ID 范围：2114001–2115012。
- ID 说明：ID / 同spine皮肤名
- 主要关联：tItem、tlanguage_cn
- 字段：id:int、name:int、skinIcon:str、skinRank:int、itemId:int

### tMonster

- 数据行：25；字段数：10；ID 范围：2402001–2405006。
- ID 说明：ID
- 主要关联：tCommonDrop、tMineChapter
- 字段：id:int、hp:int、atk:int、spd:int、monsDrop:int、monsFeel:int、starAtk:int、atkCd:int、lifeZone:arr、type:int

### tLevelMoudel

- 数据行：600；字段数：6；ID 范围：10–6000。
- ID 说明：ID
- 主要关联：tAttribute、tItem
- 字段：id:int、moudelId:int、roleLevel:int、levelParam:str、levelNeeds:str、boostNeeds:str

### tStarMoudel

- 数据行：15；字段数：4；ID 范围：10–150。
- ID 说明：ID
- 主要关联：tItem、tRole
- 字段：id:int、moudelId:int、starLevel:int、starNeeds:int

### tCustomerFavor

- 数据行：22；字段数：3；ID 范围：2201001–2302002。
- ID 说明：填写tRole:id
- 主要关联：tRole
- 字段：id:int、preferMenu:arr、preferTaste:arr

### tEmployee

- 数据行：18；字段数：6；ID 范围：1–18。
- ID 说明：ID
- 主要关联：tAttribute、tRole
- 字段：id:int、role_id:int、roleLevel:int、roleAttribute:str、ablity_type:arr、boba_abvolume:int

## L_垃圾表_tRubbish.xlsx

### tRubbish

- 数据行：12；字段数：4；ID 范围：1–12。
- ID 说明：ID
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、meetNeeds:int、cleanLevel:int、rubbishRate:int

### tRubbishWeight

- 数据行：40；字段数：10；ID 范围：1–2090。
- ID 说明：ID
- 主要关联：tRubbish
- 字段：id:int、rubbishType:int、rubbishTypeParam:int、rubbishStyle:str、weight:int、cleanTimeType:int、cleanTime:int、cleanSpine:str、reward:int、fallRange:int

## L_礼包_链式礼包_tGfitLink.xlsx

### tGfitLink

- 数据行：3；字段数：10；ID 范围：300101–300103。
- ID 说明：\
- 主要关联：tGift、tViewJump、tlanguage_cn
- 字段：id:int、groupId:int、giftSort:int、giftId:int、buyUnlockCondition:int、giftShowPrefab:str、giftShowStyle:int、count:int、countText:int、jumpId:int

## L_礼包_首充&签到礼包_tGiftCheckIn.xlsx

### tGiftCheckIn

- 数据行：1；字段数：5；ID 范围：1001–1001。
- ID 说明：签到礼包id
- 主要关联：tGift、tGiftCheckInGroup、tViewJump
- 字段：id:int、checkInGroupId:int、jumpView:int、receiveCondition:int、giftId:int

### tGiftCheckInGroup

- 数据行：3；字段数：4；ID 范围：101–103。
- ID 说明：无作用
- 主要关联：tGiftContents、tItem
- 字段：id:int、groupId:int、giftContentId:int、higtItems:arr

## L_礼包表_tGift.xlsx

### tGiftPool

- 数据行：12；字段数：8；ID 范围：1–12。
- ID 说明：无作用
- 主要关联：tGift、tItem
- 字段：id:int、tips:str、poolId:int、giftId:int、filterCondition:arr、filterConditionParam:str、priority:int、weight:int

### tGift

- 数据行：36；字段数：15；ID 范围：101010–305030。
- ID 说明：礼包id / 模块[3]+序号[2]+预留插入[1]
- 主要关联：tChargeRmb、tCommonCondition、tCommonConsume、tGiftContents、tlanguage_cn
- 字段：id:int、giftOpenCondition:int、giftTypeParam:arr、giftConsume:int、giftBuyLimitFresh:int、giftBuyLimit:int、giftTime:int、giftTimeRefresh:int、giftTimeRefreshParam:int、giftTag:arr、firstExtraDrop:int、giftUiPrefab:str、giftTextDict:str、giftImgDict:str、giftItemIcon:str

### tGiftContents

- 数据行：31；字段数：4；ID 范围：10101001–30503001。
- ID 说明：礼包内容id / 礼包id+序号[2]
- 主要关联：tCommonDrop、tGift、tItem
- 字段：id:int、reward:int、rewardDisplay:str、.....:int

## M_冒泡表_tTriggerTable.xlsx

### tRoleTrigger

- 数据行：27；字段数：14；ID 范围：201–112010。
- ID 说明：冒泡id
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、triggerType:int、behaviorNode:int、roleBehavior:arr、delayTime:int、priority:int、weight:int、probability:int、triggerTag:int、triggerLimitTag:int、triggerTypeId1:int、triggerParam1:arr、triggerTypeId2:int、triggerParam2:arr

### tRoleTriggerTag

- 数据行：44；字段数：6；ID 范围：1010101–909220001。
- ID 说明：id
- 主要关联：tDialogueTable、tRoleTrigger
- 字段：id:int、tag:int、roleTag:int、bornWay:int、bubbleType:int、bubbleTypeParam:int

### tTriggerContent

- 数据行：72；字段数：10；ID 范围：101010101–909220001。
- ID 说明：id
- 主要关联：tAttribute、tAudioRes、tCommonCondition、tlanguage_cn
- 字段：id:int、group_id:int、contentType:int、contentTypeParam:str、chooseType:int、chooseParam:arr、duration:int、textLanId:int、sfxId:int、weight:int

### tTriggerBubbleLimit

- 数据行：3；字段数：2；ID 范围：1001–1003。
- ID 说明：标签id
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、limit:int

## N_内购表_tChargeShop.xlsx

### tChargePage

- 数据行：4；字段数：4；ID 范围：5001–5004。
- ID 说明：ID / 等同功能ID
- 主要关联：tFunction、tView
- 字段：id:int、blockContain:arr、pageSort:int、viewId:int

### tChargeBlock

- 数据行：8；字段数：6；ID 范围：4010001–4040001。
- ID 说明：ID
- 主要关联：tActivity、tGift、tlanguage_cn
- 字段：id:int、blockType:int、blockParam:arr、name:int、unlock:int、blockSort:int

### tChargeRmb

- 数据行：6；字段数：4；ID 范围：1010101–1010601。
- ID 说明：ID
- 主要关联：tItem
- 字段：id:int、exDrop:arr、words:int、blockSort:int

### tInvestment

- 数据行：1；字段数：12；ID 范围：101–101。
- ID 说明：ID
- 主要关联：tCommonConsume、tCommonDrop、tItem、tlanguage_cn
- 字段：id:int、goodsSales:int、gainType:int、gainParam:arr、investGainArrange:arr、investGain:str、groupPool:arr、firstPool:int、icon:str、beforeBuyWords:arr、waitingWords:arr、itemId:int

## R_主线任务表_tMainTask.xlsx

### tTaskMain

- 数据行：29；字段数：9；ID 范围：101–130。
- ID 说明：阶段id / 任务类型[2]+任务分段序号[5]
- 主要关联：tCommonDrop、tlanguage_cn
- 字段：id:int、nextStageId:int、manageTask:arr、rewardId:int、wordId:int、nameId:int、descId:int、banner:str、bannerFinish:str

### tTaskPlot

- 数据行：8；字段数：15；ID 范围：1010101–1010303。
- ID 说明：唯一id，无意义
- 主要关联：tCommonCondition、tCommonDrop、tPlot、tTask、tViewJump、tlanguage_cn
- 字段：id:int、groupId:int、taskList:arr、displayCondition:int、plotGroupReward:int、plotGroupEndJudge:int、plotGroupEndParam:arr、endButtonEffect:int、endButtonEffectParam:int、endButtonText:int、story:int、title:int、banner:str、wordId:int、nameId:int

## R_活跃任务表.xlsx

### tActiveTask

- 数据行：15；字段数：5；ID 范围：101000–201060。
- ID 说明：无作用
- 主要关联：tTask
- 字段：id:int、useLv:arr、order:int、taskId:int、taskType:int

### tProgressTask

- 数据行：10；字段数：4；ID 范围：1010–2050。
- ID 说明：唯一id，无意义
- 主要关联：tCommonDrop
- 字段：id:int、useLv:arr、point:int、reward:int

## R_通用任务表_tTask.xlsx

### tTask

- 数据行：784；字段数：16；ID 范围：1001010–3206302。
- ID 说明：任务ID / 10+阶段[2位]+任务序号[2位]+插入任务用序号 / 主线 10 / 支线 20 / 日常 30 / 活动 40
- 主要关联：tCommonCondition、tCommonDrop、tFunction、tView、tViewJump、tlanguage_cn
- 字段：id:int、note:str、triggerCondition:int、parameter:int、showCondition:int、showParam:arr、type:int、taskType:int、taskTypeParam:arr、droppedId:int、nameId:int、wordId:int、jumpType:int、jump:int、conditionType:int、countingType:int

## S_事件_团餐事件表_tGroupMeal.xlsx

### tGroupMeal

- 数据行：52；字段数：16；ID 范围：102010101–102020403。
- ID 说明：ID
- 主要关联：tCommonDrop、tCustomer、tFood、tGroupMealFoodFilter、tItem、tRole、tlanguage_cn
- 字段：id:int、roleAvatar:int、orderText:int、food1ChoiceWay:int、food1List:int、food1Nums:str、food2ChoiceWay:int、food2List:int、food2Nums:str、rewardContent:arr、cookTime:int、cookAnime:int、refreshRule:int、refreshParam:int、requireFood:str、thanksId:int

### tGroupMealFood

- 数据行：40；字段数：2；ID 范围：3003–3047。
- ID 说明：ID
- 主要关联：tFood
- 字段：id:int、level:int

### tGroupMealDining

- 数据行：50；字段数：2；ID 范围：1–50。
- ID 说明：ID
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、rewardMultiple:int

### tGroupMealFoodFilter

- 数据行：95；字段数：4；ID 范围：1–95。
- ID 说明：无用
- 主要关联：tFood
- 字段：id:int、tagId:int、foodId:int、weight:int

## S_事件_流行菜事件表_tTrendContent.xlsx

### tTrendContent

- 数据行：6；字段数：13；ID 范围：101010101–101020501。
- ID 说明：id
- 主要关联：tCommonDrop、tItem、tlanguage_cn
- 字段：id:int、eventType:int、trendType:int、trendValue:arr、duration:int、effectiveFloor:int、trendEntrance:str、trendEntranceType:str、posterIcon:str、posterTitle:int、posterContent:int、rewardTier:arr、rewardtGroup:arr

### tTrendCustomerIncrease

- 数据行：3；字段数：3；ID 范围：30101–30103。
- ID 说明：ID
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、dishCountRange:arr、passengerFlowRate:int

## S_事件_特殊顾客表_tEventCuster.xlsx

### tEventCuster

- 数据行：83；字段数：9；ID 范围：105010101–107012102。
- ID 说明：ID / 对应事件ID
- 主要关联：tCommonDrop、tCustomer、tItem、tRole
- 字段：id:int、roleAvatar:int、roleType:int、roleParam:arr、thiefExdrop:arr、eventResolut:arr、rewardContent:arr、refreshRule:int、refreshParam:int

### tEventCusterResolut

- 数据行：98；字段数：9；ID 范围：100–1640。
- ID 说明：ID
- 主要关联：tAttribute、tCommonConsume、tCommonDrop、tlanguage_cn
- 字段：id:int、resolutRewardType:arr、resolutRewardParam:arr、templateStyle:int、consumeType:int、consumeParam:arr、messageHeadIcon:str、messageShown:arr、tweet:str

## S_事件_通用对象交互事件_tEventGeneralProgress.xlsx

### tEventGeneralProgress

- 数据行：13；字段数：9；ID 范围：301010101–301011301。
- ID 说明：事件id
- 主要关联：tDialogueTable、tRole
- 字段：id:int、tips:int、projectType:int、projectTypeParam:int、createWay:int、createWayParam:arr、eventType:int、eventTypeParam:arr、eventEndWay:int

## S_事件表_tEventTable.xlsx

### tEventTrigger

- 数据行：38；字段数：11；ID 范围：101–3113。
- ID 说明：事件类ID
- 主要关联：tCommonCondition、tTagLimit、tTask
- 字段：id:int、eventPoolId:arr、conditionId:int、eventTriggerType:int、eventTriggerParam:arr、logInTrigger:int、eventTriggerMax:int、limitResetType:int、limitResetParam:arr、eventTag:int、eventPoolWeight:arr

### tEventPool

- 数据行：111；字段数：8；ID 范围：10101–31113。
- ID 说明：唯一id，无意义
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、eventType:int、resLv:arr、filterType:int、filter:arr、eventTypeId:arr、randomRule:int、eventTypeWeight:arr

### tEventGroup

- 数据行：170；字段数：9；ID 范围：1001–301011301。
- ID 说明：事件id（唯一）
- 主要关联：tAttribute、tItem
- 字段：id:int、eventType:int、groupId:int、filter:int、filterParam:arr、Weight:int、endCondition:int、endParam:arr、eventEndRoleState:int

### tTagLimit

- 数据行：8；字段数：3；ID 范围：102–3001。
- ID 说明：标签id
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、eventMaxCount:int、limitHandle:int

## S_商店表.xlsx

### tMainEntrance

- 数据行：5；字段数：6；ID 范围：1–6。
- ID 说明：总入口id / 1=鼹鼠商店 / 2=矿下商店 / 3=食材商人 / 4 = 设计师 / 5 = 地毯商人 / 6=自动补货
- 主要关联：tFunction、tItem
- 字段：id:int、openType:int、containShop:arr、freeGift:arr、openTime:int、carpetLimit:int

### tMainShop

- 数据行：21；字段数：9；ID 范围：101–901。
- ID 说明：商店id
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、name:str、autorefreshRule:int、autorefreshParam:str、ifShowTime:int、maxRefresh:int、refreshPrice:arr、showCoin:arr、order:int

### tgoodsBlock

- 数据行：134；字段数：12；ID 范围：101001–901004。
- ID 说明：id
- 主要关联：tMainShop、tgoods
- 字段：id:int、shopId:int、bolckId:int、goodsPool:arr、poolWeight:arr、showType:int、showParam:arr、openType:int、openParam:arr、order:int、firstGoods:int、guaraPool:arr

### tMainShopPool

- 数据行：61；字段数：4；ID 范围：1000–9014。
- ID 说明：池id
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、unlockType:int、unlockParam:arr、sure:arr

### tgoods

- 数据行：345；字段数：18；ID 范围：30010–9014001。
- ID 说明：商品id
- 主要关联：tCommonConsume、tDecoration、tItem、tShop
- 字段：id:int、poolid:int、showType:int、showParam:arr、weight:int、goods:arr、priceType:int、truePrice:arr、fakePrice:int、discountProper:arr、discount:arr、freeLimit:int、advLimit:int、consume:int、buyLimit:int、highLight:int、limitRefresh:int、order:int

### tSonEntrance

- 数据行：3；字段数：7；ID 范围：10101–30101。
- ID 说明：子入口管理id
- 主要关联：tMainShop
- 字段：id:int、entranceId:int、shopId:int、showType:int、showParam:arr、openType:int、openParam:arr

### tShopSpeach

- 数据行：1；字段数：7；ID 范围：1–1。
- ID 说明：发言id
- 主要关联：tTask、tlanguage_cn
- 字段：id:int、speachType:int、speachTrigger:int、speachParam:arr、abandonTrigger:int、abandonParam:arr、speachText:int

### tCarpetShop

- 数据行：3；字段数：4；ID 范围：1001–1003。
- ID 说明：id / 无意义
- 主要关联：tCommonConsume、tlanguage_cn
- 字段：id:int、buyTime:int、buyParam:int、dealerWords:int

## T_事件_天坑事件表tMineEvent.xlsx

### tMineEvent

- 数据行：20；字段数：11；ID 范围：1001–1302。
- ID 说明：事件id
- 主要关联：tCommonCondition、tMineTile
- 字段：id:int、eventType:int、eventLevel:arr、startType:int、startParam:arr、showBubble:int、showBubbleType:int、bubbletTps:arr、wayTps:int、endType:int、endTypeParam:int

### tMineTalkEvent

- 数据行：23；字段数：17；ID 范围：1001–1302。
- ID 说明：唯一id
- 主要关联：tDialogueTable、tMineRoleState、tMineTile、tRole
- 字段：id:int、tips:int、eventId:int、talkType:int、talkParam:arr、talkWay:int、wayParam:arr、projectType:int、roleId:int、prefabPath:str、roleCreateWay:int、roleCreateWayParam:arr、standby:int、endRoleState:int、endProjectRecycle:int、endClickEvent:int、endClickEventParam:arr

## T_图鉴表_tBestiary.xlsx

### tBestiaryReward

- 数据行：61；字段数：9；ID 范围：1010–4180。
- ID 说明：ID
- 主要关联：tAttribute、tCommonDrop、tItem、tlanguage_cn
- 字段：id:int、name:int、collectNum:int、rewardType:int、rewardParam:arr、rewardShow:int、rewardInfo:int、remind:int、wayToGet:int

## T_天坑_关卡表_tMine.xlsx

### tMine

- 数据行：104；字段数：34；ID 范围：100010–106200。
- ID 说明：关卡ID / 1+关卡类型[2] + 序号[4]
- 主要关联：tCommonCondition、tCommonDrop、tItem、tMineMechanics、tMineModule、tMineTile、tlanguage_cn
- 字段：id:int、mineType:int、blockType:int、mineDepth:arr、refreshWay:arr、spawnPoint:int、nextLevel:int、mineWidth:int、firstReward:int、enterLevelTemplate:str、templayteType:int、autoSpawn:arr、mineGround:str、templayteBg:arr、randomTemplate:arr、randomTemplateWeight:arr、bgDecoTypeParm:str、envDecoDistributed:str、envDecoPool:arr、levelAtkDisplay:int、levelName:arr、aniOutTime:int、mineReward:arr、showType:int、showParam:arr、mechanics:arr、mechanicsWeight:arr、npcMark:str、addTileNums:int、addTileWay:arr、DownSwitch:int、unlockCondition:int、passRewards:str、specialDrop:arr

### tMineModule

- 数据行：38；字段数：2；ID 范围：1003–9999999。
- ID 说明：模板id
- 主要关联：tMineModulePool
- 字段：id:int、modulePool:str

### tMineModulePool

- 数据行：38；字段数：2；ID 范围：10001–9000002。
- ID 说明：池子id
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、size:str

### tMineAuto

- 数据行：6；字段数：7；ID 范围：1–6。
- ID 说明：序号
- 主要关联：tCommonDrop、tMineTile
- 字段：id:int、autoId:int、tileID:int、tilePer:int、maxNum:int、tileFloor:arr、floorMaxNum:int

### tMineEnvPool

- 数据行：6；字段数：2；ID 范围：10101–10601。
- ID 说明：池子id
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、mineList:arr

### tMinePackage

- 数据行：3；字段数：7；ID 范围：1–3。
- ID 说明：ID
- 主要关联：tCommonConsume、tCommonDrop、tItem
- 字段：id:int、itemType:int、packageDrop:int、buyTimes:arr、packageType:int、packageParam:int、packagePic:arr

### tMineStaminaConsume

- 数据行：5；字段数：5；ID 范围：101–202。
- ID 说明：ID
- 主要关联：tCommonConsume、tItem
- 字段：id:int、group:int、buyTimesInterval:arr、consumeId:int、reward:arr

### tMineChapter

- 数据行：25；字段数：8；ID 范围：1–25。
- ID 说明：占位
- 主要关联：tMineSuit
- 字段：id:int、name:int、containMine:arr、showType:int、showParam:arr、enterPic:int、startHall:int、tips:arr

### tMineSuit

- 数据行：6；字段数：4；ID 范围：101–106。
- ID 说明：标识归属哪套资源
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、bannerPic:str、bottonPic:str、textOutlinePrese:int

### tMineMechanics

- 数据行：1；字段数：5；ID 范围：1–1。
- ID 说明：机制id
- 主要关联：tlanguage_cn
- 字段：id:int、mechanicType:int、mechanicTypeParam:arr、mechanicName:int、screenEffect:str

## T_天坑_地块表_tMineTile.xlsx

### tMineTile

- 数据行：383；字段数：10；ID 范围：10000010–19106030。
- ID 说明：ID / 1+地块类型[2]+序号[4]
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、tips:str、tileType:int、tagType:int、tileDurability:int、effect_id:str、land:int、occupyGrid:arr、extraLoadTile:int、tileTag:int

### tMineTileStyle

- 数据行：424；字段数：6；ID 范围：100000101–201000301。
- ID 说明：无作用
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、prefabName:str、monsId:int、spinePrefab:str、skin:str、idleName:str

### tMineTileParam

- 数据行：1666；字段数：11；ID 范围：1–1666。
- ID 说明：无实际作用
- 主要关联：tCommonConsume、tCommonDrop、tMine、tMineTile、tSkill
- 字段：id:int、mineTileId:int、levelId:int、breakableTimes:int、tilePoint:str、tileHp:int、tileStyleParam:str、tips:str、tips:str、tileTypeParam:str、tileTypeCost:arr

### tMineTileSkill

- 数据行：9；字段数：6；ID 范围：1001–1009。
- ID 说明：技能id
- 主要关联：tMineTileStyle、tSkill
- 字段：id:int、skillType:int、skillTypeParam:str、skillAttack:int、skillEffectID:str、skillEffectBullet:int

### tMineItem

- 数据行：2；字段数：4；ID 范围：5001001–5001002。
- ID 说明：道具ID / 50开头+类型2位数+序号3位数
- 主要关联：tAttribute、tItem、tSkill
- 字段：id:int、mineItemType:int、mineItemParam:arr、maxBring:int

## T_天坑_角色状态表_tMineRoleState.xlsx

### tMineRoleState

- 数据行：18；字段数：7；ID 范围：1010–5060。
- ID 说明：状态id
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、priority:int、isLoop:int、canBreakOff:int、nextStateId:int、defaultAction:str、prefabNodeSwitch:str

## T_推送表_tPush.xlsx

### tPush

- 数据行：5；字段数：7；ID 范围：401010–401050。
- ID 说明：推送id /  / id规则=推送内容[1]+模块[2]+序[2]+插入预留[1]
- 主要关联：tActivity、tGift、tGiftPool、tScene、tView
- 字段：id:int、pushScene:arr、pushCool:int、triggerGroup:arr、pushContent:int、pushContentParam:int、pushLimit:int

### tPushCondition

- 数据行：6；字段数：4；ID 范围：1–6。
- ID 说明：无
- 主要关联：tAttribute、tCommonCondition、tItem、tUserTag、tView
- 字段：id:int、pushGroupId:int、pushCondition:int、pushConditionParam:arr

### tUserTag

- 数据行：8；字段数：6；ID 范围：101010–102040。
- ID 说明：用户标签id
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、tagType:int、statCycle:int、statCycleParam:int、minValue:int、maxValue:int

## T_特效表_tEffectRes.xlsx

### tEffectRes

- 数据行：48；字段数：4；ID 范围：1–2030。
- ID 说明：特效ID
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、path:str、repet:str、type:int

## T_特权卡配置表_tPrivilegeCard.xlsx

### tPrivilegeCard

- 数据行：3；字段数：4；ID 范围：2600001–2700001。
- ID 说明：特权卡是一种道具 / 此处填写道具id
- 主要关联：tItem、tPrivilegeParam
- 字段：id:int、privilegeSet:int、giftPerday:str、time:int

### tPrivilegeParam

- 数据行：4；字段数：4；ID 范围：10001–10004。
- ID 说明：唯一id
- 主要关联：tItem
- 字段：id:int、groupId:int、type:int、Param:arr

### tAutoRestock

- 数据行：1；字段数：7；ID 范围：10002–10002。
- ID 说明：唯一id
- 主要关联：tViewJump
- 字段：id:int、order:int、openIngredients:int、chooseTimes:int、replaceCd:int、restockNum:str、linkid:int

## W_物品表_tItem.xlsx

### tItem

- 数据行：976；字段数：14；ID 范围：1–21140011。
- ID 说明：ID / 七位数： / 家具：1+序号[6] / 角色：2+序号[6] / 菜品：301+珍稀度+序号[3] / 食材：401+珍稀度+序号[3]
- 主要关联：tCommonDrop、tCommonReward、tItemWay、tRandomRuleReward、tlanguage_cn
- 字段：id:int、tips:str、itemType:int、itemTag:int、itemTypeParam:str、itemStyle:int、itemQuality:int、name:int、desc:int、tipsStyle:int、itemWay:arr、icon:str、big_icon:str、change:int

### tItemWay

- 数据行：58；字段数：4；ID 范围：1001–1560。
- ID 说明：途径id
- 主要关联：tViewJump、tlanguage_cn
- 字段：id:int、text:int、icon:str、jumpId:int

### tRandomRuleReward

- 数据行：2；字段数：6；ID 范围：1010–1020。
- ID 说明：随机规则id
- 主要关联：tCommonDrop、tItem、tRule
- 字段：id:int、basicRate:int、upRate:int、commonDrop:int、guaranteedDrop:int、displayReward:str

## Y_引导表_tGuideGroup.xlsx

### tGuideGroup

- 数据行：83；字段数：29；ID 范围：10000–9029050。
- ID 说明：引导组ID
- 主要关联：tCommonCondition、tFunction、tGuideGroup、tMine、tRole、tScene、tShop、tTask、tView
- 字段：id:int、nextId:int、reGuideIdOnBreak:int、withoutSaving:int、keepEvent:int、viewId:int、guideViewId:int、界面id备注:str、sceneEventType:int、keepUINode:str、roomId:int、formLevel:int、formBuilding:int、hideModule:arr、hideModuleOnComplete:arr、alone:bool、conditionViewId:arr、delayShow:bool、itemLimit:arr、delay:int、allowSkip:bool、completedIdOnStart:arr、completedIdOnFinish:arr、addGuideOnBreak:int、finishGuideOnBreak:arr、breakRestartType:int、guides:arr、lockOnFinish:bool、unlockFuncId:arr

### tGuideLogic

- 数据行：136；字段数：48；ID 范围：100–9120035。
- ID 说明：引导逻辑ID
- 主要关联：tCustomer、tDecoration、tDialogueTable、tEffectRes、tFunction、tRole、tlanguage_cn
- 字段：id:int、description:str、description:str、pauseGame:bool、funcType:int、endEvent:int、maskStatus:int、avoidFalseClickTime:int、funcParam:int、mainUi:str、dialogueGroupId:int、effectIdArray:arr、effectPosType:arr、effectPosArray:arr、followTarget:bool、uiComPath:str、uiClikCondition:int、maskType:int、maskImg:str、maskAutoSize:int、maskSizeW:int、maskSizeH:int、maskRadius:int、offect:arr、specialIndexSmoke:arr、maskCellType:int、maskCellPos:arr、secondMaskPos:str、accelerate:int、cgPath:str、cgAniName:str、cgTime:arr、blackScreen:int、clickTimes:int、uiDragEffectIndex:int、uiDragTargetPoint:arr、uiDragTargetPosType:int、uiDragDuration:int、uiDragTargetRect:int、uiDragCondition:int、sceneClickObjType:int、clickParam:int、startStateLine:str、stopCondition:str、endStateLine:str、mainCameraPosition:arr、mainCameraSize:int、mainCameraTime:int

## Y_研发表_tResearchSlotUnlock.xlsx

### tResearchSlotUnlock

- 数据行：6；字段数：8；ID 范围：1–6。
- ID 说明：研发位置id
- 主要关联：tCommonCondition、tCommonConsume、tlanguage_cn
- 字段：id:int、deskType:int、condition:int、conditionParam:int、conditionParam2:int、consumeType:int、consumeParam:int、unlockWords:int

## Y_音效表_tAudioRes.xlsx

### tAudioRes

- 数据行：64；字段数：4；ID 范围：1–80。
- ID 说明：ID
- 主要关联：未从表头或字段值确认到稳定外键；仍需按type+param语义检查。
- 字段：id:int、path:str、repet:bool、audio3D:bool
