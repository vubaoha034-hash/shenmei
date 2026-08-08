---
name: gc-travel-zine-poster-v1
description: >
  LOCKED reference-first travel/life-memory zine transformation skill derived from
  LiamGvchi/gc-minimal-zine-poster. Use when a real photo or video frame must be rebuilt
  into a restrained archival zine image with large intentional negative space, one dominant
  transformation mechanism, source-derived color logic, sparse typography, flat scanned-paper
  materiality, and strict rejection of generic scrapbook/template/travel-ad aesthetics.
---

# GC Travel Zine Poster v1 — LOCKED

状态：`LOCKED / CANONICAL`

这是本仓库旅行 / 生活记忆照片转 Zine 的**唯一正式入口**。

本 Skill 派生自 `LiamGvchi/gc-minimal-zine-poster` / `gc-minimal-zine-poster-v0-1`，但针对真实照片、视频帧、人物、室内、风景、建筑、食物与旅行片段增加了严格的 source-fidelity、reference-first 和 anti-template 约束。

核心原则只有一句：

> **先拆参考图的视觉机制，再拆原图的关键证据，然后做减法重构；禁止把“复古、杂志、胶带、邮戳、米色纸”当作风格本身。**

---

## 0. 最高优先级

按以下顺序执行：

1. 用户明确指令；
2. 用户提供的参考图视觉机制；
3. 用户源照片 / 视频帧的真实身份与几何；
4. 本 Skill 的默认回退规则。

如果输出和用户提供的参考图机制明显冲突，即使“看起来也不错”，仍然判错。

**严禁把 Skill 名称本身当作 prompt。**

以下做法属于执行失败：

```text
similar to gc-travel-zine-poster-v1
in gc-travel-zine-poster-v1 style
clean travel editorial zine poster
retro travel magazine look
```

调用图像生成器前，必须把本 Skill 的具体视觉约束**序列化进最终生成 Prompt**。不能假设图像模型知道本 Skill。

---

## 1. 参考图锁｜REFERENCE-FIRST LOCK

当用户提供参考图、社交平台截图、上下对比图或示例作品时，生成前必须解析：

```text
reference_ratio:
reference_orientation:
reference_artwork_bounds:
negative_space_level:
main_visual_scale:
main_visual_position:
main_visual_type:
paper_family:
image_treatment:
typography_scale:
typography_position:
accent_color_logic:
texture_family:
composition_family:
realism_vs_abstraction:
forbidden_reference_assets:
```

### 截图解析规则

如果参考是抖音 / 小红书 / 手机截图：

- 手机黑边不是画面；
- 顶部状态栏不是画面；
- 账号、点赞、评论、播放器不是画面；
- “原图 + 转换后图”的上下对比中，只把**真正的设计成品区域**作为风格参考；
- 不得把整个手机截图比例当作设计比例；
- 不得复制创作者账号、水印、UI、互动数字。

### 必须学习的机制

优先学习：

- 留白到底有多少；
- 原照片保留多少、抽象多少；
- 主视觉是大场景印刷化、窄切片、撕纸照片、地形轮廓、色块、建筑体、还是人物小锚点；
- 纸张是扫描纸、未涂布纸、旧档案纸还是近中性纤维纸；
- 图像是否半调、丝网、复印、干刷、套色、版画或低对比扫描；
- 文字是否只是角落微型档案字；
- 强调色来自湖水、沙地、衣服、果汁、墙面、建筑、天空还是其他源图证据；
- 视觉重心在哪个区域；
- 画面如何利用“空”而不是靠装饰填满。

### 不能复制的内容

- 创作者署名与账号；
- 水印；
- 精确装饰文案；
- 精确档案号；
- 未提供的坐标、日期、年份、天气、海拔、机构名；
- 可识别的完整商业外观；
- 社交平台 UI。

---

## 2. 画幅锁｜ASPECT-RATIO LOCK

确定比例的唯一优先级：

1. 用户明确指定比例 / 像素；
2. 否则跟随参考作品真实设计区域的比例与方向；
3. 没有可用参考比例时，保持源照片 / 视频帧比例。

规则：

- `16:9` 不是默认；
- 上游 `3:5` 也不是默认；
- 不得为了模板强裁；
- 不得因为目录或旧 Skill 名含 `16x9` 就强制 16:9；
- 用户说 9:16 就必须 9:16；
- 用户说“按参考图”就优先按参考成品比例。

---

## 3. 单图来源锁｜ONE SOURCE = ONE OUTPUT

批量任务中，每张输出必须对应一个明确源图。

- 每张生成图只能有 **1 张 primary source image**；
- 其他照片最多用于同一人物 / 同一系列一致性辅助，不得混合重构成新场景；
- 不得把多张源图拼成一张，除非用户明确要求拼贴；
- 用户说“每张单独生成”，就必须一源图一成品文件；
- 不得把同一张源图重复当成多张成品的主要内容。

有人物时：

- 保留人物年龄感、脸型、发型、服装与姿态；
- 不做无请求的美化、换脸、增龄、减龄；
- 人物可以被缩小、网点化、丝网化、剪影化，但身份特征不能漂移。

---

## 4. 源图证据锁｜SOURCE FIDELITY LOCK

成品必须仍然能看出来自这张原图，而不是“同主题新生成”。

每张至少保留 3 项重要证据（如果存在）：

- 地形 / 岸线 / 山脊 / 河湖轮廓；
- 建筑体块、窗、墙、门、塔、镜面；
- 人物姿态、人物在画面中的尺度关系；
- 地平线高度；
- 主运动方向；
- 一个标志物：树、砂锅、玻璃杯、筷筒、桌面、岩石、道路等；
- 一个强源色：湖蓝、沙黄、红衣、西瓜红、雪碧绿、墙面红纸等。

室内 / 餐饮生活照同样适用：

- 不需要强行“变成风景”；
- 可以把砂锅、桌面曲线、窗格、报纸墙、人物、红色饮料等重构成版画 / 色块 / 轮廓 / 切片；
- 核心是**重新组织视觉语法**，不是给照片加一个米白边框。

---

## 5. 构图锁｜COMPOSITION LOCK

目标：克制、稀疏、像独立出版物 / 田野档案 / 艺术画册，而不是社交媒体模板。

必须：

- 一个第一视觉中心；
- 一个主视觉机制；
- 大面积有意义的纸张 / 空域；
- 主体尺度受控；
- 装饰极少；
- 留白承担构图功能。

回退范围（仅在参考图不明确时使用）：

- sticker / specimen：约 65%–85% 空纸；
- contour / collage / architecture：约 45%–70% 空纸；
- scenic print：约 35%–60% 空纸。

### 直接失败

如果成品的逻辑可以概括为：

```text
原照片
+ 米白背景
+ 大标题
+ 胶带
+ 邮戳
+ 撕纸边
```

则判定为 `REJECTED_GENERIC_TEMPLATE`。

---

## 6. 主视觉家族锁｜ONE PRIMARY FAMILY ONLY

每张只选一个主家族。最多允许一个弱辅助机制。

### A. Scenic Print / 场景版画

适合：山、湖、海、沙漠、草原、峡谷、室内大空间、桌面大关系。

- 保留大几何；
- 转为半调 / 丝网 / 复印 / 干刷 / 版画；
- 人物若重要，作为小比例锚点保留。

### B. Contour / Field Map / 轮廓场域

适合：湖面、道路、桌面曲线、器皿轮廓、空间路径。

- 把一条真实几何关系变成主图；
- 只用一类源色；
- 不做假技术地图。

### C. Architectural Deconstruction / 建筑解构

适合：建筑、窗、墙、塔、门、室内框架、砂锅等强结构物。

- 提取 1–3 个体块；
- 用几何、印刷平面、阴影块组织；
- 不生成 3D 概念建筑。

### D. Vertical Slice Memory / 窄幅记忆切片

适合：人物、树、塔、门、窗、桌边局部。

- 保留一条窄照片 / 印刷切片；
- 其余区域用纸张与抽象场域承接；
- 切片必须来自源图真实主体。

### E. Torn Photo Fragment / 撕纸照片碎片

适合：照片本身有强瞬间。

- 照片只占较小区域；
- 撕纸只是照片边缘处理，不是装饰主题；
- 最多一个小胶带 / 色块支持。

### F. Color-Block Field / 色块场域

适合：原图有明确单色锚点。

- 西瓜红 → 红色印刷场；
- 湖水蓝 → 钴蓝场；
- 沙漠黄 → 赭黄场；
- 红衣 → 朱红人物锚点；
- 绿色瓶体 → 只有确有意义时才保留绿色。

### G. Symbolic Silhouette / 象征剪影

适合：简单、标志性主体。

- 人、树、器皿、山脊、岸线可以变成粗糙墨色或单色剪影；
- 必须仍能对应原图姿态 / 形状。

### H. Archival Specimen / 档案标本

适合：单个强物件，如砂锅、树、建筑、岩石、杯子、器皿。

- 作为“标本”被孤立；
- 大量留白；
- 文字极少。

### 禁止混搭

不得同一张同时出现：撕纸 + 多胶带 + 邮戳 + 多色块 + 地图 + 大标题 + 植物贴纸。

出现 3 个以上同等强度的“设计技巧”，直接失败。

---

## 7. 文字锁｜TYPOGRAPHY LOCK

默认：**如果用户没有给文字，就不要主动发明大标题。**

允许：

- 用户明确指定的地名；
- 用户明确指定的单词，例如 `WANZAI`；
- 极小 serif / monospaced / typewriter 式标签；
- 用户明确要求时的一句短语。

默认禁止主动发明：

- `CLAYPOT`
- `TABLESIDE`
- `WATERMELON`
- `PLAYFUL`
- `SUMMER SIP`
- `GOOD DAYS`
- `LOCAL FLAVOR`
- `TRAVEL MEMORIES`
- `FOOD JOURNAL`
- `GOOD FOOD GOOD MOOD`
- 任何类似“为了像杂志”而添加的英文。

### 文字强度

- 文字必须明显弱于主视觉；
- 禁止巨型居中标题；
- 禁止商业海报标题层级；
- 禁止大段正文；
- 禁止无意义英文作为装饰；
- 禁止用数字、编号、伪档案信息填留白。

### 事实锁

未经用户提供或可靠上下文确认，不得生成：

- 地点；
- 坐标；
- 日期 / 年份；
- 天气；
- 海拔；
- 档案号；
- 机构；
- 电话 / 地址；
- 任何精确元数据。

未知就省略。

---

## 8. 颜色锁｜COLOR LOCK

默认系统：

```text
paper tone
+ gray / black
+ one source-derived accent family
```

强调色优先从原图证据提取：

- 湖 / 天空 → cobalt / mineral blue；
- 红衣 / 红纸 / 西瓜 / 红饮料 → tomato / vermilion；
- 沙 / 土 / 木 → ochre / burnt orange；
- 草地 → moss / field green；
- 其他高饱和物件 → 只有它确实是原图视觉锚点时使用。

规则：

- 每张一个主高色相；
- 不允许彩虹式 scrapbook；
- 不允许为了“复古”自动变黄；
- 不允许整图统一暖黄滤镜；
- 不允许把原图高价值强色洗成脏灰；
- 强调色必须成为结构的一部分，而不是贴上去的小装饰。

---

## 9. 纸张与印刷锁｜MATERIAL LOCK

目标是**平面的扫描印刷物**。

允许：

- uncoated paper；
- fibrous paper；
- aged archival paper（只在参考图确实偏旧时）；
- xerox softness；
- halftone；
- risograph grain；
- faded offset；
- letterpress bleed；
- dry brush；
- scan noise；
- slight misregistration。

禁止：

- 3D 纸张 mockup；
- 桌面摆拍式纸张阴影；
- glossy travel brochure；
- 强烈电影调色；
- HDR；
- 大面积黄棕脏污；
- “为了复古而脏”。

纸张是**构图场域**，不是一层滤镜。

---

## 10. 廉价感侦测器｜CHEAPNESS DETECTOR

出现任一项必须判失败：

- 像 Canva / 模板网站的旅行海报；
- “照片 + 边框 + 胶带 + 标题”；
- 大标题比图像更强；
- 贴纸、胶带、邮戳数量过多；
- 米黄色背景承担全部所谓“高级感”；
- 假档案号、假日期、假地名；
- 随机英文；
- 图像几乎没重构，只加纸纹；
- 强调色和原图无因果关系；
- 为了“设计感”加入植物叶子、咖啡邮戳、飞机、地球、棕榈树等无关图标；
- dense scrapbook；
- tourism advertisement；
- lifestyle ad；
- generic magazine cover；
- 视觉技巧多于视觉思想。

失败状态：

```text
REJECTED_GENERIC_TEMPLATE
REJECTED_DECORATIVE_SCRAPBOOK
REJECTED_FAKE_METADATA
REJECTED_SOURCE_IDENTITY_LOSS
REJECTED_REFERENCE_DRIFT
```

---

## 11. Prompt 序列化锁｜CRITICAL

**这是本 Skill 最关键的执行锁。**

在调用任何图像生成器之前，最终 prompt 必须明确写入以下九项，不得只写 Skill 名：

1. target ratio / orientation；
2. paper field + negative-space level；
3. primary source image identity；
4. 至少 3 个必须保留的源图证据；
5. 唯一 primary visual family；
6. 主视觉尺度与位置；
7. typography rule（包括“no invented headline”）；
8. source-derived accent color + physical form；
9. print texture + hard avoid list。

### 最终 Prompt 结构

必须使用四块：

```text
BLOCK 1 — canvas / paper / negative space / subject scale and placement
BLOCK 2 — source evidence / one transformation family / reference mechanism
BLOCK 3 — exact allowed text or no text / accent color / print defects
BLOCK 4 — archival flat-scan mood / explicit hard avoids
```

### 参考图传递

如果图像工具支持 reference images：

- 必须把用户提供的参考图实际传入；
- 不得只用“像参考图”几个字替代；
- 批量时 primary source 和 style reference 要明确区分。

---

## 12. 生成前检查｜PRE-GENERATION GATE

调用图像工具前必须确认：

```text
[ ] 我是在重构，不是在装饰原照片
[ ] 我已经解析了参考成品区域，而不是手机截图 UI
[ ] 我只选了一个主视觉家族
[ ] 我知道这张图必须保留哪 3 个源图证据
[ ] 我没有发明标题、地点、日期、档案号
[ ] 文字不会压过视觉
[ ] 颜色来自源图或参考机制
[ ] Prompt 已写入完整视觉规则，而不是只写 Skill 名
```

任一项为否：禁止调用生成器。

---

## 13. 生成后质量门｜POST-GENERATION GATE

生成后检查：

```text
[ ] reference grammar recognizable
[ ] source scene / person recognizable
[ ] one dominant visual mechanism
[ ] meaningful negative space
[ ] typography tiny / restrained or absent
[ ] no fake metadata
[ ] no large commercial headline
[ ] no decorative scrapbook clutter
[ ] no irrelevant icons
[ ] paper/print materiality visible but not dirty
[ ] source-derived accent structurally integrated
[ ] not merely original photo plus beige frame / texture
```

如果关键项失败：

- 不得标记 `READY`；
- 必须调整 prompt 再生成；
- 最多重试 2 次；
- 两次仍失败则明确返回 `DRAFT / REJECTED`，不得把廉价结果当完成品交付。

---

## 14. 批量锁｜BATCH CONSISTENCY

同一组照片：

保持一致：

- paper family；
- typography family；
- print texture family；
- 总体克制程度。

必须变化：

- primary visual family；
- 主视觉位置；
- 源图强调色；
- 抽象方式；
- 空间密度。

规则：

- 不得连续两张都是“照片框 + 撕纸边”；
- 不得连续重复同一胶带位置；
- 不得每张都有标题；
- 不得每张都用同一种蓝色；
- 每一张必须单独成立。

---

## 15. 默认审美目标

最终成品应该像：

- independent travel zine；
- archival field note；
- art-book insert；
- restrained editorial print；
- quiet screenprint / xerox / risograph artifact；
- 经过设计者减法后的记忆图像。

绝不能像：

- 旅游局广告；
- 模板网站海报；
- 复古贴纸 App；
- 生活方式广告；
- 大标题杂志封面；
- “AI 做了点艺术效果”。

---

## 16. 输出格式

```markdown
**生成图**
[one standalone image for one source]

**执行记录**
- Ratio: [resolved ratio + reason]
- Primary source: [which source image]
- Reference mechanism: [short description]
- Family: [A–H]
- Accent: [source-derived hue / form]
- Text: [exact user-supplied text or NONE]
- Source evidence preserved: [3+ items]
- Status: READY | DRAFT | REJECTED
```

除非用户明确要求，不需要把长 Prompt 全部展示给用户；但内部生成调用必须完整序列化本 Skill 约束。

---

## 17. 上游来源

Derived from:

- Project: `LiamGvchi/gc-minimal-zine-poster`
- Upstream Skill: `gc-minimal-zine-poster-v0-1`
- License: MIT

详见同目录 `SOURCE.md` 与 `LICENSE`。
