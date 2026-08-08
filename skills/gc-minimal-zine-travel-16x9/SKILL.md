---
name: gc-minimal-zine-travel-16x9
description: >
  DEPRECATED compatibility alias. Do not execute this Skill independently.
  Immediately load and execute skills/gc-travel-zine-poster-v1/SKILL.md.
---

# DEPRECATED — Mandatory Redirect

状态：`DEPRECATED / REDIRECT_ONLY`

此 Skill 已停止独立执行。

**唯一正式实现：**

```text
skills/gc-travel-zine-poster-v1/SKILL.md
```

兼容调用名：

```text
$gc-minimal-zine-travel-16x9
```

收到旧调用后必须立即：

1. 读取 `skills/gc-travel-zine-poster-v1/SKILL.md`；
2. 完整执行其中的 reference-first、source-fidelity、one-source-one-output、prompt-serialization、anti-template 和 quality-gate 规则；
3. 不得继续使用本文件历史版本中的独立构图、16:9、地名、文字或随机视觉逻辑；
4. 不得只把 `gc-travel-zine-poster-v1` 名称写进图片生成 Prompt，必须把新 Skill 的具体视觉约束序列化进最终 Prompt。

任何未跳转到新 Skill 的执行都视为失败。
