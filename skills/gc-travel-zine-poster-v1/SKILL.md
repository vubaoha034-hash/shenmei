---
name: gc-travel-zine-poster-v1
description: >
  LOCKED reference-first travel/life-memory zine transformation skill derived from
  LiamGvchi/gc-minimal-zine-poster. Rebuild real photos or video frames into restrained
  archival zine artwork through structural image translation, not literal torn-paper framing.
---

# GC Travel Zine Poster v1 — LOCKED / REFERENCE-CONDITIONED

状态：`LOCKED / CANONICAL / V1.2`

这是本仓库旅行 / 生活记忆照片转 Zine 的唯一权威实现。

核心目标不是“撕纸”，而是：

> **把真实照片的视觉证据重新翻译成独立出版物 / 田野档案 / 版画式图像语言。**

用户说“撕纸效果”只是调用别名，不代表成品必须出现撕纸边框。

---

## 0. 最高优先级

执行优先级：

1. 用户明确指令；
2. 用户提供的参考图真实视觉机制；
3. 用户源照片 / 视频帧的真实身份、几何和关键色彩；
4. 本 Skill 的回退规则。

如果结果只是“看起来复古”但参考图机制没有被执行，判错。

---

## 1. 路由名隔离锁｜ROUTING TOKEN IS NOT A STYLE TOKEN

以下词只用于路由，不得原样传给图像生成器：

- `tear-paper`
- `撕纸效果`
- `gc-travel-zine-poster-v1`
- `gc-minimal-zine-poster`

最终生成 Prompt 中默认禁止出现：

```text
tear paper style
scrapbook
vintage postcard
retro magazine
photo pasted on beige paper
similar to gc-travel-zine-poster-v1
```

除非参考图本身明确以“小型撕纸照片碎片”为核心，否则不得主动要求 literal torn-paper frame。

---

## 2. 参考图必须真实参与生成｜REFERENCE CONDITIONING LOCK

只要用户在当前会话、当前任务或紧邻上下文中提供过目标参考图，就必须把它们视为真实 style reference，而不是靠文字记忆概括。

生成前必须区分：

```text
STYLE_REFERENCE_IMAGES = 用户用来说明审美 / 转换机制的图
SOURCE_IMAGE = 当前这一张要被处理的原图
```

硬规则：

- 参考图存在时，不得声称“没有明确参考图”；
- 不得只把 SOURCE_IMAGE 交给图像模型，再用一句“zine style”代替参考图；
- 如果工具支持同时提供参考图和源图，必须同时提供，并在 Prompt 中明确角色；
- 如果工具无法可靠地区分多张参考图与源图，则先独立解析参考图，形成 `REFERENCE_STYLE_SPEC`，再逐张生成；
- 批量任务中，每次生成仍然只能有 1 张 primary source；参考图只能承担审美机制，不得混入场景内容；
- 参考截图中的手机 UI、黑边、账号、点赞评论、播放器、上方原图区域都不是最终成品内容。

### 参考图解析字段

生成前必须解析：

```text
reference_artwork_bounds:
reference_ratio:
negative_space_level:
photo_preservation_ratio:
abstraction_strength:
main_visual_scale:
main_visual_position:
composition_family:
print_process:
paper_family:
typography_scale:
accent_color_logic:
structural_translation:
```

没有完成上述解析，不得生成。

---

## 3. 参考样例真正的视觉机制｜TARGET GRAMMAR

当前目标参考体系的重点不是“撕纸边缘”，而是以下机制：

### A. Memory Fragment / 记忆碎片

- 大面积纸张留白；
- 原照片只保留成一个很小的不规则碎片；
- 照片一般不超过画布约 10%–25%；
- 可有一个很小的色块 / 墨迹支持；
- 绝不允许把 70%–90% 的原照片包一圈撕纸边当成此模式。

### B. Terrain / Scene Print / 地形版画

- 把山脊、峡谷、田野、道路、云层等主几何重新制版；
- 用半调、丝网、复印、干刷、木刻感、粗网点把场景变成印刷图像；
- 原照片不是“被贴上去”，而是被重新画成版画系统。

### C. Layered Terrain Bands / 分层地貌

- 将峡谷、山体、沙丘、田野等拆成 2–5 层地形带；
- 保留原场景轮廓关系；
- 大量纸张露出；
- 人物可以成为极小色彩锚点。

### D. Architectural Specimen / 建筑或物件标本

- 从原图提取 1 个最强结构：建筑、塔、树、路灯、锅、窗、桥等；
- 将其孤立、缩小或几何化；
- 周围用纸张、印刷云层、地形带承接；
- 像档案研究图，而不是旅游海报。

### E. Vertical Slice / 窄幅记忆切片

- 只保留一条窄照片切片；
- 切片里保留人物 / 树 / 建筑等真实证据；
- 其余画面用抽象场域、版画天空、地形带重新组织；
- 切片是“证据”，不是整张照片主体。

### F. Contour / Field Map / 轮廓场域

- 把湖泊、道路、田埂、桥、山谷等真实形状转为简化轮廓 / 等高线 / 色块场；
- 只保留必要线条；
- 一种饱和源色承担主要视觉锚点；
- 禁止假技术地图和复杂伪数据。

### G. Full-field Screenprint / 全场丝网转译

- 可以让最终图像占较大面积，但必须明显被重新制版；
- 人、岩石、天空、地形整体进入半调 / 丝网 / 粗网点系统；
- 不允许保留“高保真原照片 + 纸张边框”的状态。

### H. Brush / Ink Silhouette / 粗笔剪影

- 将沙丘、山脊、人物、树等压缩成一个强轮廓；
- 用干刷、墨迹、粗糙边缘和单一色场重构；
- 保留姿态或地形证据。

---

## 4. 源图证据锁｜SOURCE FIDELITY

每张最终图必须仍然能证明来自 SOURCE_IMAGE。

至少保留 3 项重要证据（存在时）：

- 山脊 / 岸线 / 云层 / 田野 / 道路 / 河湖的主几何；
- 建筑体块、塔、窗、桥、路灯、树等标志物；
- 人物姿态、位置和尺度关系；
- 地平线高度或透视方向；
- 一个关键源色；
- 一种最有识别度的结构关系。

禁止为了风格把真实场景换成“同主题的新景色”。

---

## 5. 结构转译最低要求｜STRUCTURAL TRANSLATION MINIMUM

每张必须至少完成：

1. **一种结构转译**：
   - 地形分层；
   - 轮廓地图；
   - 建筑解构；
   - 窄切片；
   - 剪影；
   - 场景版画；
   - 标本孤立；
   - 小型记忆碎片。

2. **一种材料转译**：
   - halftone；
   - risograph；
   - xerox；
   - faded offset；
   - dry brush；
   - coarse screenprint；
   - ink bleed / misregistration。

只有“旧纸 + 撕边 + 降饱和”不满足最低要求。

---

## 6. 原照片占比硬锁｜PHOTO DOMINANCE CAP

这是防止再次生成廉价模板的关键规则。

### 默认禁止

如果画面中出现一个占画布 **55% 以上**、基本保持原摄影结构和原色彩的完整照片区域，并且只是被撕纸边框围住，则直接判：

`REJECTED_PHOTO_IN_FRAME`

### 各模式约束

- Memory Fragment：原照片区域默认 ≤ 25%；
- Vertical Slice：原照片切片宽度默认 ≤ 25%；
- Terrain / Contour / Specimen / Brush / Screenprint：最终主体区域可以大，但必须经过明显结构 / 印刷转译，不再读作原照片；
- Full-field Screenprint：允许 60%–90% 画面占比，但不得读作普通照片。

### 撕纸边缘占比

除非参考图明确如此：

- 不得用一个巨大完整撕纸矩形包住整张照片；
- 撕纸只允许成为局部材料语法；
- “纸边框”不能成为第一视觉中心。

---

## 7. 留白锁｜NEGATIVE SPACE

参考图优先。

参考不明确时：

- Memory Fragment / Specimen：60%–85% 留白；
- Contour / Architecture / Vertical Slice：40%–70% 留白；
- Terrain Bands：35%–65% 留白；
- Full-field Screenprint：可降低留白，但必须有平面印刷感。

留白必须是真正的构图空间，不是给完整照片加一圈米色边。

---

## 8. 色彩锁｜SOURCE-DERIVED COLOR

使用：纸张 + 黑 / 灰 + 1 个主要源色。

例如：

- 湖水 / 天空 → 钴蓝、矿物蓝、青蓝；
- 稻田 / 草地 → 稻绿、苔绿、田野绿；
- 红衣人物 → 番茄红 / 朱红；
- 沙漠 / 土地 → 赭黄 / 烧橙；
- 建筑白 → 中性白作为主体，蓝 / 黄作支持。

禁止自动固定成“米黄纸 + 复古棕 + 蓝点”。

---

## 9. 文字锁｜TYPOGRAPHY

默认少字甚至无字。

允许：

- 用户明确给出的地名；
- 用户明确给出的单词；
- 极小 serif / monospaced / typewriter 标签；
- 参考图明确存在的小型 field-note 行为。

禁止主动发明：

- 大标题；
- 文艺英文；
- `CLAYPOT` / `SUMMER SIP` / `TABLESIDE` 等自动标题；
- 坐标、日期、档案号、天气、海拔、机构、年份；
- 无意义英文。

文字永远不能比主视觉更响。

---

## 10. Prompt 编译硬锁｜PROMPT SERIALIZATION

调用图像生成器前，最终 Prompt 必须显式写入：

```text
SOURCE_IMAGE role
STYLE_REFERENCE_IMAGES role or REFERENCE_STYLE_SPEC
resolved aspect ratio
reference-derived composition mechanism
source evidence to preserve
selected ONE primary transformation family
structural translation action
material / print translation
negative-space geometry
source-derived accent color
text policy
hard avoids
```

### 严禁出现的偷懒 Prompt

```text
make it artistic
minimal travel editorial
retro zine
tear-paper style
scrapbook style
similar to gc-travel-zine-poster-v1
```

这些只能算风格词，不算执行。

---

## 11. 生成前闸门｜PRE-GENERATION GATE

必须全部通过：

```text
[ ] 已识别 SOURCE_IMAGE
[ ] 已识别 STYLE_REFERENCE_IMAGES 或明确无参考图
[ ] 若参考图存在，已真实参与解析 / 条件输入
[ ] 已剥离 UI / 手机黑边 / 上下对比壳
[ ] 已选 1 个主视觉家族
[ ] 已定义结构转译，不是装饰叠加
[ ] 已定义材料转译
[ ] 已定义原照片占比上限
[ ] 已定义留白
[ ] 已定义一个源色锚点
[ ] 没有虚构文字 / 元数据
[ ] 路由词“撕纸效果 / tear-paper”不会进入图像 Prompt
```

任一失败：不得生成。

---

## 12. 出图后廉价感侦测｜POST-GENERATION CHEAPNESS GATE

生成后必须用视觉检查回答：

- 是否像“照片套撕纸边框”？
- 是否像 scrapbook / vintage postcard / Canva 模板？
- 是否只是降低饱和度并加纸张纹理？
- 是否仍然有一个大面积、几乎未转译的完整照片？
- 是否装饰比结构更突出？
- 是否参考图最关键的重构机制没有出现？
- 是否所有批量图片都变成同一种撕纸矩形？

如果任一为“是”，标记 `REJECTED_CHEAP_TEMPLATE`，必须重做，不能交付。

### 特别失败码

```text
REJECTED_PHOTO_IN_FRAME
REJECTED_SCRAPBOOK
REJECTED_GENERIC_POSTCARD
REJECTED_DECORATION_OVER_STRUCTURE
REJECTED_REFERENCE_NOT_USED
REJECTED_TEMPLATE_REPETITION
```

---

## 13. 批量序列锁｜BATCH MODE

用户说“每张单独生成”时：

- 1 张源图 = 1 张最终图；
- 不得混合多张源图场景；
- 参考图可以共享；
- 保持纸张 / 字体 / 印刷系统一致；
- 连续输出不得重复同一个构图骨架；
- 在参考图允许的机制内轮换：Terrain Print / Memory Fragment / Contour / Specimen / Vertical Slice / Screenprint / Brush Silhouette；
- 不得通过“每张换一个撕纸边形状”冒充变化。

---

## 14. 参考截图使用方式

如果用户给的是“上面原图 + 下面转换图”的截图：

- 上半部分只帮助理解源图与转换后的对应关系；
- 真正的 STYLE_REFERENCE 是下半部分成品；
- 最终输出不要自动生成上下 before/after 对比；
- 学习的是：怎么把原图几何压缩、抽象、版画化、切片化、地图化；
- 不复制创作者账号、水印、原始装饰文案或完整专有布局。

---

## 15. 最终审美目标

应该像：

- 独立旅行 Zine；
- 艺术家书 / field notes；
- 小批量丝网 / Risograph 印刷；
- 建筑 / 地貌档案图；
- 克制、有余味、有明确图像编辑观点。

绝不能像：

- 相册模板；
- 旅游明信片；
- 复古 scrapbook；
- 米白底贴照片；
- Canva 模板；
- AI 自动“文艺化”。

---

## 16. Workflow

1. 识别参考图和源图角色；
2. 解析参考图真正成品区域；
3. 提取参考机制；
4. 提取源图 3–5 个关键证据；
5. 选择 1 个主视觉家族；
6. 定义结构转译；
7. 定义材料转译；
8. 定义留白与原照片占比；
9. 定义一个源色锚点；
10. 编译完整生成 Prompt，剥离所有路由名；
11. 一源图一生成；
12. 运行廉价感闸门；
13. 失败则换结构机制重做，不得只调滤镜；
14. 通过后才能交付。

---

## Upstream attribution

Derived from `LiamGvchi/gc-minimal-zine-poster` (`gc-minimal-zine-poster-v0-1`), MIT License.
See `SOURCE.md` and `LICENSE` in this directory.
