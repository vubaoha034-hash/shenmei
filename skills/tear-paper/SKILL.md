---
name: tear-paper
description: >
  中文别名“撕纸效果”。当用户说“撕纸效果”“使用撕纸效果”“撕纸”“旅行撕纸”“zine撕纸”，或显式调用 $tear-paper 时使用。该名称只负责路由，不是视觉风格词；激活后必须完整执行 ../gc-travel-zine-poster-v1/SKILL.md。
---

# 撕纸效果｜短调用入口

状态：`USER-FACING ALIAS / ROUTING ONLY / LOCKED`

用户可以直接写：

```text
使用撕纸效果，把这些照片每张单独生成。
```

或：

```text
$tear-paper
```

## 最重要的规则

`撕纸效果` / `tear-paper` **只是调用名字，不是生成风格描述。**

激活后必须读取：

```text
../gc-travel-zine-poster-v1/SKILL.md
```

并完整执行。

### 严禁

最终图像生成 Prompt 中不得出现以下路由词：

```text
tear-paper
撕纸效果
gc-travel-zine-poster-v1
gc-minimal-zine-poster
```

不得因为用户说“撕纸效果”，就自动生成：

- 巨大的撕纸矩形照片；
- 米白纸背景；
- 胶带；
- 邮戳；
- vintage postcard；
- scrapbook；
- 相册模板。

只有当参考图明确使用“小型撕纸照片碎片”时，撕纸边缘才可以作为该张图的局部材料机制。

## 参考图优先

只要当前会话中存在用户用于说明目标审美的参考图，就必须把它们交给 canonical Skill 作为 `STYLE_REFERENCE_IMAGES` / `REFERENCE_STYLE_SPEC` 处理。

不得只传源照片给图像模型，再用“撕纸效果”四个字代替参考图。

## 中文触发

以下表达全部等价于 `$tear-paper`：

- `撕纸效果`
- `使用撕纸效果`
- `按撕纸效果处理`
- `用撕纸效果每张单独生成`

用户无需记住长名称。

如果 canonical Skill 无法读取，停止生成并报告，禁止自行写一套“复古拼贴”替代方案。
