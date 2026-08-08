# gc-travel-zine-poster-v1

这是 `LiamGvchi/gc-minimal-zine-poster` 的**极薄旅行 / 照片适配层**。

用户日常唯一推荐入口：

```text
$zine
```

或：

```text
使用 zine 处理这张图
```

旧入口 `$tear-paper` / “撕纸效果”已废弃，不再用于生产生成。原因不是视觉规则变化，而是入口名称本身可能在下游图像模型中触发 literal ripped-paper / scrapbook 的错误先验。

## 设计原则

- 原版视觉系统不重写；
- `UPSTREAM_SKILL.md` 保存上游 Skill 镜像；
- 本地只允许少量适配：画幅、真实照片主体保真、用户明确提供的地名、多图独立交付；
- 不再增加本地“视觉家族”、照片占比阈值、结构转译检查、审美失败码或长检查表；
- 最终 Prompt 继续使用上游原版四段 Standard Prompt Shape；
- `$zine` 只负责路由，不得作为视觉词进入最终 Prompt。

详细规则见 `SKILL.md`；原版镜像见 `UPSTREAM_SKILL.md`。
