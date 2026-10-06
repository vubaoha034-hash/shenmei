# 刘先生 S4：真实文字成品与复用

先固定权威分支最新提交，按 START_HERE.md 读取原生锁、检查点与 WORKER_CURRENT_REUSE.md。本文说明成果，不代替任务锁。当前范围是山野集文字气质的“刘先生”内容迁移实验；摄影暂停。S4内部审稿通过但真人仍 PENDING，下一动作只应是 LIU_REVIEW_LIUXIANSHENG_CONTENT_TRANSFER。不得据此恢复茶作、改主线或开启第二风格。

## 成品与身份

[Figma完整源442:2](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=442-2)，文件 uyDxOoN1iNDPpEHTKSUWg1，页412:2，主字标442:8。[完整PNG原件](https://drive.google.com/file/d/1V_7Vlv4wJj_LZz6nGXlMxZ2hCxhXX5kD/view?usp=drivesdk)、[字标SVG](https://drive.google.com/file/d/162fcRt3WK_NvnDXjaxBECeDg_KE0xLtG/view?usp=drivesdk)、[第2张真实生成图稿](https://drive.google.com/file/d/1pzmY7I7BtEQ7kkOJ8B5EIMd5O-Lk0aTS/view?usp=drivesdk)。均继承原私有目录权限；认证读取与原字节恢复已验证，未验证匿名访问，未改共享权限。

PNG960×1280、62055B、SHA256 ddb621ebf7e230279a1358b1b93ab9fcd55705b7e6ca99af8649aa3295ab1ca4。SVG26910B、SHA256 0f0a43f7547ded5afa46f36de391dd4ac536c1d7018facabad988248da78d2b9。文件、出处、各版对应及审稿绑定以 DELIVERY_MANIFEST_S4.json 为准；不能只凭文件名或描述判断画面。

| 正式试验版 | Figma画框 | PNG Drive ID | 实际独立像素判断 |
|---|---|---|---|
| S1 手绘曲线 | 424:2 | 1tWwbwKxIbD2JAh0_DbX_u8xxH4Yj2R1B | FAIL：圆滑笔势、橙线脱离 |
| S2 块面修订 | 429:2 | 1D7ALZZ9IFh_ZT427H37YNh9r54oKBrBC | FAIL：笔画碎裂 |
| S3 首次image图稿重建 | 435:2 | 19HJIyPjjzNV_4yBzGN4zbngjp6Xx4T7P | FAIL：圆胀主字、切面颗粒不足、附文偏重 |
| S4 同方向切面与层级修订 | 442:2 | 1V_7Vlv4wJj_LZz6nGXlMxZ2hCxhXX5kD | PASS_WITH_LIMITATIONS：允许交刘先生审核 |

共4个正式迁移版本、2次真实图稿工具调用。S4内部遮线预览、480px预览、两次补白接缝失败是同一字标的技术诊断，未作为备选海报挑图。TECHNICAL_ATTEMPTS.json保留失败身份；4次VTracer调用不等于4张生成作品。旧S3 DELIVERY_MANIFEST.json与METHODS_AND_REUSE.md保持失败基线。

## 实际制作依据与可编辑范围

实际步骤：查看正确山野集原件9a29fbdc…并提取层级与文案 → 冻结COPY_MANIFEST → 内置image_gen.imagegen生成第2张透明文字图稿9ef09dd1… → 独立专业字形诊断 → 未修改VTracer0.6.15提取图稿真实奶油轮廓及孔位 → skia-pathops0.9.2实施明确局部切面、橙线遮挡补白与中心线扩展 → Figma原生矢量、侧章和12个TEXT排版 → 960×1280真实导出 → 新隔离参考/成品两图审稿 → Drive原字节回读。

主字标保留图稿可见骨架；切面、刘短竖、7个局部补白窗及生底横交点修补是专家推断，见guide-adapter-s4/PROVENANCE.json，不能称原始字体或原白像素。橙线为明确重建的2.8px曲线，分前后层穿插字形。图稿奶油盒[246,478,963,747]映射至[224,431,791,601]；不重排另一风格。

实际61孔/464px是源mask记录。样条和缩放会遗漏部分微孔，不能宣称所有颗粒均保留。两次局部技术失败来自颜色门限漏掉橙白混色边缘及生底横旧交点缺口；修补限制到真实混色/橙线支持窗，并排除真实源颗粒，没有用随机噪声掩盖问题。

Figma有28节点、12个可见未锁TEXT、6个VECTOR（主标5+侧章1）、0个IMAGE paint。辅助文字实际字体为Inter Bold/Regular、Noto Serif SC Bold、Noto Sans SC Bold/Regular、Ma Shan Zheng Regular；所有字体加载后写入。准确文字绑定COPY_MANIFEST，口号两半恰为两个空格，橙字44–50px原生范围样式。辅助文案可直接改字；刘先生主标是曲线，换名字必须重新制作与审稿，不能承诺自动生成任意中文字。

顶端四英文组25px；主标下金色短句30px；橙色情绪句基准47px；底部署名46px、小字18px、两角14px。相关文字堆栈使用原生auto-layout。前后指纹证明原研究S2、S1–S3与茶作402:2/摄影402:3读取属性一致。该指纹是有限属性FNV检查；摄影原文件SHA与原生严格回放另行保留，不能把FNV称密码学像素证明。茶作29版/28修订、V29文字真人REJECTED、摄影7fd7777f认可冻结不变。

## 上游、真实调用与运行

[官方design-critique SKILL](https://github.com/anthropics/knowledge-work-plugins/blob/d3ee81913e5e179273313345847a2a4f42449bd2/design/skills/design-critique/SKILL.md)，固定d3ee81913e5e179273313345847a2a4f42449bd2，Apache-2.0。本机安装发现记录在既有skill_review_20261003/SKILL_RESEARCH.json；S4冷审实际读取安装SKILL，采用第一印象、层级、一致性与画面证据，不套UI导航/触控。它提供批评框架，不构成中文字标专家认证。

[VTracer](https://github.com/visioncortex/vtracer)0.6.15/MIT、[skia-pathops](https://github.com/fonttools/skia-pathops)0.9.2/BSD-3-Clause实际导入并调用，核心上游未修改，许可证与实际源码指纹在guide-adapter-s4。它们是制作库，不伪称成熟中文品牌创作skill。Figma官方figma-use与Codex imagegen技能实际调用；figma-generate-design的UI模板流程不适用于本品牌字标。未找到并验证可直接包办本任务的成熟中文字标创作SKILL，采用可追溯图像分析及字形制作。

Python3.12.14/Pillow12.3/NumPy2.3.5，Node24.19/sharp0.35.4；固定Win_amd64 VTracer cp312与Pathops abi3 wheel。依赖恢复参照S4_SEALED_RECOVERY_INDEPENDENT.json、S4_VTRACER_LOCATION_INDEPENDENT.json及NATIVE_DEPENDENCY_RECOVERY_S4.json；固定wheel SHA和原路径不能随意替换。Node脚本的sharp使用当前已发现runtime绝对路径，跨机须有界适配，尚非跨平台安装包。

恢复图稿到 .liu-visual-private/liuxiansheng_transfer_20261005/IMAGE_GUIDE_S4.png，正确参考到 .liu-visual-private/product-type-integration-20261004/SHANYEJI-canonical-readback-20261005.jpg；先核对精确SHA。复制FROZEN_SPEC.json到新的私有输出目录。实际生产代码入口：
```text
node guide-adapter-s4/prepare-inputs.cjs --root <checkout> --output-dir <new-private-directory>
python -B -s guide-adapter-s4/build-wordmark.py --root <checkout> --output-dir <new-private-directory>
node guide-adapter-s4/render-preview.cjs --root <checkout> --output-dir <new-private-directory>
```
上述guide-adapter-s4是本文所在证据目录的子目录；完整路径见manifest。重建须读当前授权，不自动执行FIGMA_ASSEMBLY_S4.js；该脚本保留真实制作源码与SVG，重复执行会新建节点。改普通TEXT遵循figma-use：读取fontName → await loadFontAsync → 改characters → 返回所有受影响ID → 重新导出与审稿。

Root实际gpt-6.1-sol/xhigh，未切到Max；独立冷审实际Sol/Max，字形专家Astra/xhigh。内置生图工具底层模型未公开，记NOT_EXPOSED；没有付费CLI/API、训练或自动任务。

## 独立审核、收益与边界

s4_verified_review/PIXEL_REVIEW.json及ISOLATION_AUDIT.json绑定960×1280成品SHA、9a29参考、时间、审稿线程和实际Sol/Max。新fork-none审稿只实际读安装skill及两张原件，无创作历史、自评或旧审稿。共享文件系统不等于OS沙箱，provider内部完整prompt不能逐token证明；本文字实验载体未替换原茶作项目外五图冷审。

结论CONTENT_TRANSFER_PASS_WITH_LIMITATIONS，仅进入真人审核。具体限制：刘刂/先脚/生底横塑形节奏尚不统一；颗粒密度低于参考；右橙环仍较规整；金色短句偏轻、底部署名专属性弱。没有分数或虚构准确率，旧AI放行真人否决记录不撤销。专业制作审查见PROFESSIONAL_IMPLEMENTATION_REVIEW_S4.json；其实际独立运行结果与局限独立于审美结论。

流程改善、源编辑性及Drive恢复已验证。本例文字层级和橙线穿插通过内部审查，成熟品牌质量、整体图文融合、迁移泛化、第二风格、节省时间及真人认可未验证。大量时间的实际原因包括字形方法不充分、错误的来源绑定历史、技术接缝修复以及每次原生状态写入全量回放29版；工程通过和文档数量不能抵消审美差距。

新上下文入口验证结果以s4_fresh_entry/FRESH_ENTRY_REPORT.json实际报告为准；缺文件时不得声称完成。该报告绑定读到的原生状态、实际源读取和原图恢复，不是第二状态系统。发布版本由Git提交与独立远端回读确定。

唯一下一动作：刘先生审核S4这张文字成品。真人未认可前不晋升模板，不恢复茶作或继续下一风格。

