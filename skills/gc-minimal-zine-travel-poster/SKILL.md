---
name: gc-minimal-zine-travel-poster-v1
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
$gc-minimal-zine-travel-poster-v1
```

收到旧调用后必须立即：

1. 读取 `skills/gc-travel-zine-poster-v1/SKILL.md`；
2. 完整执行其中的 reference-first、source-fidelity、one-source-one-output、prompt-serialization、anti-template 和 quality-gate 规则；
3. 不得继续使用本文件历史版本中的默认 16:9、随机大标题、贴纸、地名或其他独立视觉逻辑；
4. 不得只把新 Skill 名称作为风格词传给图像模型，必须把具体视觉约束完整写进最终生成 Prompt。

任何未跳转到新 Skill 的执行都视为失败。
