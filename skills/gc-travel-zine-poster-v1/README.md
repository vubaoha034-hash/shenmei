# gc-travel-zine-poster-v1

这是 `LiamGvchi/gc-minimal-zine-poster` 的**极薄旅行 / 照片适配层**。

用户日常直接写：

```text
使用撕纸效果
```

或：

```text
$tear-paper
```

## 设计原则

- 原版视觉系统不重写；
- `UPSTREAM_SKILL.md` 保存上游 Skill 镜像；
- 本地只允许少量适配：画幅、真实照片主体保真、用户明确提供的地名、多图独立交付；
- 不再增加本地“视觉家族”、照片占比阈值、结构转译检查、审美失败码或长检查表；
- 最终 Prompt 继续使用上游原版四段 Standard Prompt Shape。

详细规则见 `SKILL.md`；原版镜像见 `UPSTREAM_SKILL.md`。
