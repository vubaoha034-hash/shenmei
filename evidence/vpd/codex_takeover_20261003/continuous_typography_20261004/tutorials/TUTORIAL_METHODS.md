# 两个可核查教程入口

2026-10-04，有界教程调查；没有制作字标候选或读取独立冷审。以下因官方出处、明确制作步骤和可查看示范选择，不用星标、播放量或“顶级”自称作质量证明。

## 1. Glyphs：Drawing good paths

[实际正文](https://glyphsapp.com/learn/drawing-good-paths)，署名 Rainer Erich Scheichelbauer，首次2013-01-06，页内更新2026-08-28。实际读到曲线段/控制柄、极值节点、去多余点、内外曲线匹配、闭合与轮廓方向章节。这是专业字体轮廓教程，非中文品牌概念课程。

实际看两幅像素示范：317×284图的节点与控制柄处于三角区域内；1330×721的两个O，右侧内外曲线不匹配，斜向笔画明显更鼓。它说明局部笔画重量需同时看内外边界，而不是给整字套圆角。Glyphs专用快捷键和自动G2功能不直接套用Figma；Figma可手动实现相同几何调整。故意的尖角不应一律抹平。

## 2. Figma 官方钢笔/矢量编辑教学

[官方YouTube：Pen Tool Basics & Vector Networks](https://www.youtube.com/watch?v=5x2uHUB_pzw)（2020-05-29）：实际读到Figma频道、题目和描述，视频正文抓取失败；**没有取得字幕，没有看完整视频**。官方帮助页提示嵌入视频用旧界面，因此本次操作依据是实际读取的 [Vector networks](https://help.figma.com/hc/en-us/articles/360040450213-Vector-networks) 与 [Edit vector layers](https://help.figma.com/hc/en-us/articles/360039957634-Edit-vector-layers)，作为同一官方工具教程入口。

确实读到：P放节点/拖拽建立曲线、Enter进路径编辑、Bend生成控制柄、Mirror angle只联动方向、选局部节点后移动/缩放、闭合区域填充。实际下载其Bend官方GIF，查看112帧中的0/56/111三帧：直线→出现控制柄的弧线→端点柄位置改变、弧度继续变化。不是YouTube观看记录，也不是中文字标课程。

## 本版最多三项操作

1. 保留原矢量备份，进入节点编辑；对已选定的起收笔/接点手动移动节点和控制柄，形成具体轮廓变化，在两字中重复同类处理。教程支持操作，品牌含义与选择由本版设计决定。
2. 描摹曲线只保留形状需要的节点；在合适的极值处分段，连续曲线调柄方向/长度，并一起检查内外边界，避免鼓包；保留设计需要的尖角。
3. 检查闭合、孔洞与交叉，再看实际成品尺寸。局部节点可单独移动，但不能只靠整体拉伸或缩小替代两字关系设计。

自动描摹只是估计已有像素的边界；字形创作包含主动决定骨架、端点、负空间和字间关系。这两入口可帮助执行局部轮廓工作，不能证明获得中文品牌字标创作能力、自动补出品牌风格或保证审美通过。本次没有找到已实际读到完整中文品牌字标制作步骤的公开视频；中文justfont搜索结果只有课程大纲，未以它冒充已学习课程。

## 缓存、工具与许可边界

公开仅此短MD、缓存脚本与 `TUTORIAL_IMAGE_METADATA.json`。正文/像素仅私有 `.liu-visual-private/continuous_typography_20261004/tutorials/`：HTML SHA256 `bc47e3b4d0285ffac49b4ccf8f343ef297c7c01ccaf4149c837de848805049d6`；Glyphs两图SHA前缀8d22f08a / 9e666936；Figma GIF 057a3d0d。完整源URL、尺寸、帧编号与SHA见JSON。GIF帧是原动画忠实解码用于观察，没有生成设计。

实际执行：web读取正文/官方描述；Python GET缓存（chunk f549e6）；view_image(detail=original)查看两图与三帧。`CODEX_THREAD_ID=01a0ffad-8b0c-71d0-9b4d-2dc355ab25af` 为进程读取值，模型/effort字段不可见。未发现允许生产复用教程作品图或字形的开放许可；不复制图示轮廓、不将完整正文或像素提交公开仓库。
