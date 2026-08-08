---
name: tear-paper
description: DEPRECATED compatibility alias. Do not use this name for production image generation because the wording itself can bias downstream image models toward literal ripped-paper / scrapbook imagery. Redirect users to $zine.
---

# DEPRECATED — DO NOT GENERATE FROM THIS ENTRY

状态：`DEPRECATED / REDIRECT ONLY`

`$tear-paper` 和中文“撕纸效果”已废弃为生产入口。

原因：该名称本身包含强视觉语义，可能在下游图像生成链中诱发 literal ripped-paper、胶带、手账、scrapbook、vintage postcard 等错误先验，即使 canonical Skill 本身并没有要求这些元素。

收到旧调用时：

1. 不得直接开始图片生成；
2. 不得把 `tear-paper`、`撕纸效果` 或任何对应翻译放进图像 Prompt；
3. 告知并切换到中性入口：

```text
$zine
```

4. 实际视觉执行仍由：

```text
../gc-travel-zine-poster-v1/SKILL.md
```

决定。

本文件只承担旧调用兼容和弃用提示，不定义任何视觉行为。
