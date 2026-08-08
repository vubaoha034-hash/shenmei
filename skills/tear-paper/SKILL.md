---
name: tear-paper
description: >
  中文别名“撕纸效果”。当用户说“撕纸效果”“使用撕纸效果”“撕纸”“旅行撕纸”“zine撕纸”，或显式调用 $tear-paper 时使用。这个 Skill 是旅行/生活记忆 Zine 锁死版的短调用入口；激活后必须读取并完整执行 ../gc-travel-zine-poster-v1/SKILL.md，不得简化成照片加米白底、胶带、邮戳、大标题或通用杂志模板。
---

# 撕纸效果｜短调用入口

状态：`USER-FACING ALIAS / LOCKED`

这是 `$gc-travel-zine-poster-v1` 的**短调用入口**，方便用户直接写：

```text
使用撕纸效果，把这些照片每张单独生成。
```

或：

```text
$tear-paper
```

## 强制跳转

一旦本 Skill 被激活，必须立即读取并完整执行：

```text
../gc-travel-zine-poster-v1/SKILL.md
```

该文件是唯一权威实现。不得把本文件当作缩略版视觉提示词，也不得自行总结后省略其中任何以下硬锁：

- reference-first；
- one source = one output；
- source fidelity；
- 画幅优先级；
- 单一主视觉家族；
- 文字与事实锁；
- prompt 序列化；
- 廉价模板 / scrapbook / 旅游广告一票否决；
- 出图前、出图后的质量闸门。

## 中文别名行为

以下表达全部等价于显式调用 `$tear-paper`：

- `撕纸效果`
- `使用撕纸效果`
- `按撕纸效果处理`
- `用撕纸效果每张单独生成`

用户无需记住旧的长调用名。

## 禁止降级

不得因为用户只写了“撕纸效果”四个字，就把任务解释为普通 Photoshop 撕纸边缘、相册拼贴、胶带贴纸或复古滤镜。

这里的“撕纸效果”专指本仓库已经锁死的旅行 / 生活记忆 Zine 转换系统。

如果无法读取权威实现文件，则停止生成并明确报告，禁止自行补写一套替代风格。
