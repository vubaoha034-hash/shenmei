# R25｜真实原创笔画 + Figma原生修改（2026-10-28）

**当前评级：矢量路径创作与Figma操作链PASS，商业/审美设计HOLD，蒸馏规则未通过。**

## 原因
R24的两个“溪桥听雨”均为ChatGPT生成PNG，**没有任何Figma逐笔设计**。用户指出“这不就是用了一个字体，没有设计感”，必须纠正把“看起来像书法”当设计能力的错误。

## 本轮实际作品
研究词“山月”，使用两种完全不同的汉字结构建立一个极小原创编辑样本。不是直接套字体，不是从图片提取轮廓，也没有复制设计师的SVG或笔画。
- [R25 独立Figma设计文件](https://www.figma.com/design/RpcWXDRNyN3y4KEmCspgfZ)
- [C3 原始9条向量](https://www.figma.com/design/RpcWXDRNyN3y4KEmCspgfZ?node-id=1-2)
- [C4 在Figma内真改过2条向量](https://www.figma.com/design/RpcWXDRNyN3y4KEmCspgfZ?node-id=2-2)
- [C3从Figma读取出的SVG](R25_C3_山月_真实Figma原稿.svg)
- [C4从Figma读取出的SVG](R25_C4_山月_真实Figma路径导出.svg)
- [R25原生验证与失败账本](R25_ACTUAL_FIGMA_NATIVE_VECTOR_AND_AESTHETIC_HOLD.json)

## 验证
Figma真实读回两个画框各9个 `VECTOR` 节点，用户能逐个选择修改，没有 `TEXT`、没有任何 `IMAGE` 填充。C4对C3只修改了「山/承重底横」和「月/内横下」的真实 `vectorPaths`，其他7个节点路径保持不变。C4 SVG经本地直接按Figma源导出，Git Blob SHA1＝`72e3d9fcc4c4f9a7eda26d193b5fac3414c73c94`，已与GitHub远程哈希比对一致。C3与C4渲染后RGBA差异像素 8537，主要在下部两条笔画所在垂直区。

**必须如实表述：最初9条贝塞尔轮廓由人工在本地Python/SVG源码中设计，再导入Figma；不是在Figma里从第一条鼠标笔画绘起。C4两条轮廓确实在Figma里用矢量路径属性编辑。**

C1、C2初稿都过于几何，负面试验继续保留。C3/C4比它们有更明确的曲线意图，但仍偏简练、没有强烈独特的设计身份。没有真人盲评、第三字组迁移或已商业化验收。故严禁写入“专业字体设计已蒸馏成功”。

## 血统保存方式
- 冻结原任务：[R25_FROZEN_AUTHOR_CONTOUR_DECISIONS.json](R25_FROZEN_AUTHOR_CONTOUR_DECISIONS.json)
- 实际路径与结果：[R25_ACTUAL_FIGMA_NATIVE_VECTOR_AND_AESTHETIC_HOLD.json](R25_ACTUAL_FIGMA_NATIVE_VECTOR_AND_AESTHETIC_HOLD.json)
- 下载包 `R25_山月_Figma原生矢量与失败血统包.zip`，本聊天中已有真实容器文件，SHA256=`2cfc655628379b03c875a1fb13ed010c5e01462d90987dae989754b531111d98`，共26件，包括C1/C2/C3/C4全部SVG/PNG原件、生成/验证代码、两幅对照图和审计数据。
- 不把第三方设计师原作品复制到公开仓库；来源研究为梁志坚字体设计过程 [原文](https://www.uisdc.com/11-font-design-case)。

## 唯一后续检验
先看本次真正两字SVG的字形识别与审美：若明显仍“普通字体/没有设计感”，就**停止围绕这几条笔画无限微调**。下一阶段只选一项作者真实的“草稿→整字拓扑调整→定稿”过程，拆出明确的创作目的、正反例和回退条件，再做真正不同结构字的原生路径迁移。必须独立认字和人工盲评验证，而不是靠生成张数或软件节点数累积。

正式视觉生产主线 `visual-program-distillation-v2-photography-design-20260814`、唯一任务锁Revision355、Checkpoint377均不变。S7人工审美结论仍PENDING。
