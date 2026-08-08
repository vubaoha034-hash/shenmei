---
name: zine
description: Neutral user-facing routing entry for gc-travel-zine-poster-v1. This alias only routes to the canonical upstream-first zine skill and must never contribute visual style words to the image-generation prompt.
---

# ZINE｜ROUTING ONLY

状态：`CANONICAL USER ENTRY / ROUTING ONLY`

用户日常可直接写：

```text
$zine
```

或自然语言：

```text
使用 zine 处理这张图
```

激活后唯一动作：完整读取并执行：

```text
../gc-travel-zine-poster-v1/SKILL.md
```

## 强制隔离

`zine` 只是中性的调用标识，不是最终图像 Prompt 的视觉词。

- 不得把 `$zine`、`zine style`、`travel zine` 等调用名称原样塞进最终 Prompt，除非上游 Prompt Compiler 自己明确生成这些像素级描述；
- 不得因为入口名称自行增加撕纸、胶带、邮戳、米黄色纸张、scrapbook、vintage postcard、magazine cover 等元素；
- 不得在本文件增加、总结、强化或改写上游视觉规则；
- 最终 Prompt 必须由 canonical Skill 要求的上游 `Standard Mode Prompt Compiler` 产生。

核心原则：

> **入口负责路由，视觉由上游 Skill 决定。**
