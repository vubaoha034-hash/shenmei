---
name: gc-travel-zine-poster-v1
description: Thin travel/photo wrapper around the upstream gc-minimal-zine-poster-v0-1 skill. Preserve the upstream prompt compiler and visual grammar; only adapt aspect ratio, real-photo fidelity, factual place labels, and batch delivery when explicitly needed.
---

# GC Travel Zine Poster v1 — THIN WRAPPER

状态：`CANONICAL / UPSTREAM-FIRST`

本 Skill **不重新设计** `gc-minimal-zine-poster-v0-1`。

执行任何生成前，必须先完整读取并执行同目录：

```text
UPSTREAM_SKILL.md
```

同时必须遵守：

```text
../../rules/DIRECT_SKILL_INVOCATION_RULE.md
```

`UPSTREAM_SKILL.md` 是上游 `LiamGvchi/gc-minimal-zine-poster` 的原版 Skill 镜像。除下面列出的少量适配外，**上游 Standard Mode Prompt Compiler、Variation Engine、Color Engine、Negative Constraints、Workflow 和 Quality Gate 全部保持原样，不得二次解释、扩写、分类或重写。**

## 直接调用纪律

当用户明确说“直接用 Skill”“使用 `$zine`”或点名本 Skill 时：

- 直接执行本 Skill + `UPSTREAM_SKILL.md`；
- 不得把任务改成“助手自由写一套审美 Prompt”；
- 不得为了“更高级”补写新的视觉风格说明；
- 不得未经用户要求擅自修改本 Skill；
- 输出不满意时，先检查本 Skill 是否真的控制了最终生成链路，再讨论是否需要修改；
- 若最终 Prompt 不是由上游 Standard Mode Prompt Compiler 产生，则本次执行视为绕过 Skill。

## 唯一允许的适配

### 1. 画幅

仅替换上游的默认 `3:5` 画幅字段：

1. 用户明确指定比例 / 像素时，用用户要求；
2. 否则用户提供明确参考成品时，可沿用参考成品的画幅与方向；
3. 否则处理真实照片 / 视频帧时，可保持源图比例；
4. 其余情况仍使用上游默认 `3:5`。

**只替换 canvas ratio，不改变上游的留白、cluster、anchor、typography、color、texture、mood 和 variation 逻辑。**

### 2. 真实照片保真

当输入是一张真实照片 / 视频帧时，把它作为上游 `Image Anchor` 的素材来源。

- 保留最有识别度的主体、人物姿态、建筑、树、山脊、道路、湖岸或其他关键关系；
- 允许上游把它裁成 fragment、clipping、specimen、silhouette、illustration、texture window 等；
- 不要求固定保留百分比；
- 不增加额外的“地形版画 / 建筑解构 / 轮廓地图”等硬分类；
- 不为了保真阻止上游做大胆的最小化与抽象。

### 3. 地名与事实文字

只有用户明确提供地点或要求地名时，才可把准确的英文 / 罗马字地点作为上游的小型 typography 元素。

- 地名保持次要、小型；
- 不知道地点就不猜；
- 不自动虚构坐标、日期、天气、海拔、档案号或机构名。

### 4. 多图交付

用户给多张照片并要求“每张单独生成”时：

- 每张照片独立运行一次完整的上游 Standard Mode；
- 每张得到独立图片；
- 不把多张源照片混成一个场景，除非用户明确要求拼贴；
- variation 仍按上游规则变化，不新增本地视觉家族。

## 明确禁止的本地改写

不得再加入或执行以下本地规则：

- 固定的旅行视觉家族；
- `55%` 照片占比阈值；
- structural translation minimum；
- terrain / contour / architecture 强制分类；
- cheapness detector；
- `REJECTED_*` 审美失败码；
- reference conditioning 大型字段表；
- 为“更高级”而扩充长 Prompt；
- 把入口名、Skill 名或风格昵称当成最终视觉 Prompt。

这些规则会改变上游的生成自由度，因此全部废弃。

## Prompt 编译原则

最终图像 Prompt 必须仍然使用 `UPSTREAM_SKILL.md` 的 **四段 Standard Prompt Shape**：

1. canvas + paper + negative space + cluster size/location
2. subject metaphor + anchor type + anchor treatment
3. typography + accent strategy + print defects
4. flat scan mood + avoid-list

本 wrapper 只能在需要时替换：

- canvas ratio；
- source photo 的具体 anchor 内容；
- 用户明确提供的地点文字。

**不要把本文件全文、检查表、调用名或解释性规则塞进最终 Prompt。**

## 用户调用

推荐唯一日常入口：

```text
$zine
```

或：

```text
使用 zine 处理这张图
```

`$zine` 只是中性路由标识，视觉执行仍然是上游 `gc-minimal-zine-poster-v0-1`。

旧入口 `$tear-paper` / “撕纸效果”已废弃，因为名称本身可能污染下游图像模型，使其错误偏向 literal ripped-paper / scrapbook。旧入口不得直接触发生成，只能提示切换到 `$zine`。

## Upstream

- Project: `LiamGvchi/gc-minimal-zine-poster`
- Upstream skill: `gc-minimal-zine-poster-v0-1`
- Vendored mirror: `UPSTREAM_SKILL.md`
- Upstream blob SHA: `7b6cbbdfcd660e979ea8db6fed57816584170103`
- License: MIT
