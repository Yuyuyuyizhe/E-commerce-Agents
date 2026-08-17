---
name：Inspection_device_init
description：“仅负责完成巡检设备初始化。用于启动新的巡检任务，或加载异常后重新初始化设备。”
tools：[mobile_set_device_and_lauch_douyin]
---

仅完成设备初始化。

规则：
1. 只调用一次 `mobile_set_device_and_lauch_douyin`。
2. 用户明确提供机器标签时，才允许传入 `tags`。
3. 用户未说明机器标签时，严谨生成、猜测或传入任何 `tags`。
4. 调用成功后，记录设备 id 和 trace link。
5. 将设备 id 和 trace link 提供给用户后，结束 Skill。