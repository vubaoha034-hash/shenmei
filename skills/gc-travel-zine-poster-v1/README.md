# gc-travel-zine-poster-v1

本仓库旅行 / 生活记忆照片转 Zine 的**唯一正式入口**。

调用名：

```text
$gc-travel-zine-poster-v1
```

核心规则：

- 参考图优先，不是模板优先；
- 用户指定比例优先，其次参考成品比例，再其次源图比例；
- 一张源图对应一张独立成品；
- 必须做减法重构，禁止“照片 + 米白底 + 大标题 + 胶带 + 邮戳”；
- 每张只允许一个主视觉家族；
- 没有用户提供文字时，不主动发明大标题、地名、日期、档案号或装饰英文；
- 强调色必须来自源图或参考机制；
- 图像生成 prompt 必须显式写入完整视觉规则，不能只写 Skill 名称；
- 任何 Canva / scrapbook / 旅游广告 / 通用杂志模板感直接判失败。

旧调用：

```text
$gc-minimal-zine-travel-16x9
$gc-minimal-zine-travel-poster-v1
```

仅作为兼容入口，必须跳转到本 Skill，不得继续独立执行。

详细规则见 `SKILL.md`。
