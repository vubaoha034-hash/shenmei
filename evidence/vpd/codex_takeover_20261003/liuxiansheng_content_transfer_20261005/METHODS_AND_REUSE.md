# 刘先生：实际 image → Figma 文字迁移试验

唯一业务状态从 `START_HERE.md` → 当前任务锁恢复，不以本文或历史聊天的下一动作代替锁。当前成品是文字迁移试验，摄影由刘先生要求暂停；茶作29版/28修订、摄影7fd7777f及原山野集研究S2(416:2)均保留。

## 真实交付

| 版本 | Figma 节点 | PNG Drive 原件 | 独立像素结论 |
|---|---|---|---|
| S1 手绘曲线 | 424:2 | 1tWwbwKxIbD2JAh0_DbX_u8xxH4Yj2R1B | CONTENT_TRANSFER_FAIL |
| S2 块面曲线 | 429:2 | 1D7ALZZ9IFh_ZT427H37YNh9r54oKBrBC | CONTENT_TRANSFER_FAIL |
| S3 image 图稿重建 | 435:2 | 19HJIyPjjzNV_4yBzGN4zbngjp6Xx4T7P | CONTENT_TRANSFER_FAIL |

Figma 文件 `uyDxOoN1iNDPpEHTKSUWg1`，页 `412:2`；[S3源文件](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=435-2)。[S3完整PNG](https://drive.google.com/file/d/19HJIyPjjzNV_4yBzGN4zbngjp6Xx4T7P/view)、[image原图稿](https://drive.google.com/file/d/1mZn0nQeclp1ty75-4z2QloLO_tyfxDxC/view)、[字标SVG](https://drive.google.com/file/d/1l5eS4O8-KWVA1uVTT4RZpJis3603AHYl/view)。三份实际原字节回读已逐字节匹配；Drive继承既有私有目录权限，没有改成匿名公开。

S3 PNG 960×1280 / SHA65450794a8e6f8459a8672c942ac8f5f47760c03f9b371b7b32fbb0a3218008d。图稿1086×1448 RGBA / SHAe4c9ba5f928cd63e8c7feb8ff0480ff142e0953e02ca7e8b5c8acf1a6f763f6f。SVG32913 bytes / SHAb9dfbbc199666a5b2e1a46066e1b7d73e59b73dcaa0ef6cb814627779444976c。文件身份以DELIVERY_MANIFEST及对应回读证据为准。

## 制作与可编辑范围

实际顺序：读取山野集原件9a29fbdc并提取文案/层级 → 用冻结COPY_MANIFEST和IMAGE_GUIDE_PROMPT调用一次内置 `image_gen.imagegen` → 保存透明图稿 → VTracer恢复主字标奶油形状和可见橙线 → Figma建立原生矢量与辅助TEXT → 导出 → 新隔离两图审稿 → Drive回读。

S3字标节点435:8含20个原生VECTOR；十二个辅助TEXT全部可见、未锁、无缺字字体且准确匹配冻结文案；画框无IMAGE paint。主字标是从生成图稿恢复的曲线，不是可直接输入替换的字体。辅助文案可以直接改字，主标换成其他三字需新的图稿/字形制作及重新审核。不能承诺任意字数自动保持相同风格。

普通文字使用实际可用 Inter Bold/Regular、Noto Serif SC Bold、Noto Sans SC Bold/Regular、Ma Shan Zheng Regular。它们让普通文字可编辑，但与图稿中生成的字形、纹理、字势有近似差异；椭圆侧章亦为原生近似重建。当前不能称整套一模一样。

ChatGPT读取成果时：先读入口/锁/manifest，再实际fetch上列Drive PNG查看，不从描述判审美；用Figma插件只读435:2定位TEXT。改字必须遵循 `figma-use`：读取现有fontName → await loadFontAsync → 改characters → 返回全部受影响节点ID → 重新导出并审核。当前额度以原生锁为准，不自动重放写入脚本。

## 成熟上游与实际调用

* 官方Figma插件技能 `figma-use` 实际读取并每次传 `skillNames:figma-use`。它提供真实可编辑节点操作，不能自动提供中文字标品味。
* Codex内置 `imagegen` 技能实际使用默认工具路径。图稿返回工具名明确，底层生图模型未公开，记 `NOT_EXPOSED_BY_BUILTIN_TOOL`；没有付费CLI/API。Root实际Sol/xhigh，审稿实际Sol/Max，以runtime审计为准。
* [VTracer上游](https://github.com/visioncortex/vtracer) 0.6.15，MIT；固定cp312/win_amd64包身份和恢复步骤沿用当前入口的vectorization证据。实际import并执行未修改上游；本目录guide-adapter是本轮实际执行的薄适配源码副本，不是新安装技能。
* [官方design-critique](https://github.com/anthropics/knowledge-work-plugins/blob/d3ee81913e5e179273313345847a2a4f42449bd2/design/skills/design-critique/SKILL.md)，固定d3ee819…，Apache-2.0，既有安装/发现/实际读取证据在skill_review_20261003/SKILL_RESEARCH.json。采用可见区域证据和优先问题审稿顺序；它是通用批评流程，没有证实中文字标专家能力。S1实际读skill；S2/S3使用相同有界要求，不能宣称每人读过skill。

实际薄适配：alpha/颜色/连通区域筛除小噪点，再VTracer spline；filter_speckle12、length_threshold4、path_precision2。两个颜色分别用样本中值平色。只恢复可见线段，不编造遮挡后的隐藏路径；原图稿未修改。guide-adapter/PROVENANCE.json记录依赖、参数、路径与局限，LICENSE保存原MIT声明。

复制源码回私有image-guide-reconstruction目录、按入口获取原图稿及固定依赖后，原执行顺序为Node prepare-trace-inputs.cjs → Python trace-guide.py → Node render-trace-and-check.cjs。源码保留真实本机依赖定位和本例SHA/ROI；直接在evidence目录运行会找不到私有输入。跨机路径与新输入必须做有界适配、重新绑定，不冒称通用自动字体生成器。Node24.19/sharp0.35.4，Python3.12.14/Pillow12.3/NumPy2.3.5。本例无需训练、付费依赖或定时运行。

## 审核、收益和失败

S3独立审稿为新fork-none/Sol-Max子代理，仅收到R/T和本轮必要标准；实际两次原图ImageView及全部调用已绑定，见s3_verified_review/PIXEL_REVIEW.json和ISOLATION_AUDIT.json。共享文件系统不是OS沙箱；provider内部完整prompt不可逐token证明。此有界迁移载体没有替换茶作原项目外五图冷审。

审稿具体确认：橙线与三字可见共构、内容和层级框架成立；失败是主字圆胀、切面及颗粒不足，英文/侧章/金色说明偏重，手写句过规整。技术可运行不等于审美通过。

保留S1/S2失败，可观察到S3橙线共构比失败记录改善，但整体视觉收益尚未验证，真人仍PENDING。流程改善与可编辑性已验证，节省时间未验证；不能因一张图或测试数量宣称蒸馏/迁移能力完成。实际耗时诊断：现有全量validator每次重验29版，重复PNG解码及多遍476MB历史日志；这解释部分开销，但不能为设计质量不足开脱。

本轮同方向S1/S2/S3及一次图稿调用如实累计，不隐藏失败、不扩第二风格。下一动作只读原生锁；当前失败成品不晋升为茶作合格基准。AI结果及真人反馈分别保存，不能以AI通过代替刘先生认可。
