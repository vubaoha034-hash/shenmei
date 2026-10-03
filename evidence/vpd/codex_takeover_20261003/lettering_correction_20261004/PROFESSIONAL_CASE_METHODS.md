# 两个官方品牌字体案例：像素方法证据

2026-10-04；有界研究反馈，非冷审、真人评审或视觉改善证明。Root随后从worker真实turn_context核验gpt-6.1-sol / max；三次看图工具结果返回14个图像块（含三个项目图），见RESEARCH_WORKER_EXECUTION.json。没有生成候选、改摄影、下载字体、安装软件或改业务状态。

## 方正：喜茶灵感体

[官方正文](https://www.foundertype.com/index.php/FontofMade/caseDetail/id/16.html)。实际读 HTML、六张正文/应用 JPEG 和两 GIF 工具首帧。可见粗直略窄高骨架、平切端点、圆转内弧；应用标题粗细共享骨架。官方将高重心/开空间关联轻盈，将直切与曲线组合关联适度甜感。这里只验证形状，未验证观众感知。

茶作可借“一个品牌理由对应具体端点或空间变化、在两字重复”的步骤。暖茶汤和陶碗支持克制圆转；不搬其比例、几何点、粗字重或冰饮装饰。

## 汉仪：大白兔

[官方正文](https://hanyi.com.cn/custom-font-case?id=15)；网页工具未取到正文，实际 Python GET [官方案例 API](https://hanyi.com.cn/api/custom-font/case/get?id=15) 成功。原 LOGO/字体对照保留右倾与圆点；“小”可见圆弧起笔、切角收笔，另一图可见连笔和局部开口。官方解释为继承标志身份和奶糖软硬材质；这不是观众反应验证。

茶作可借材料感统一起收笔、开口组织内白；不搬兔字圆点、糖果膨胀感、右倾或其轮廓。

## 适用边界

已用 view_image 原分辨率看冻结摄影、V3、reference.jpg 上半广告：摄影是暗绿植物、暖茶汤、陶碗和木桌；V3为规则宋体；参考白字有伸缩、倾斜、字间节奏。下半参考不作依据。文件为：

- .liu-visual-private/source_recovery_20261003/photography-local-reconstruction-final.png
- .liu-visual-private/correct_source_typography/v3/poster.png
- .liu-visual-private/reference.jpg

字体库要让大量字符/字重共享规则；两字字标可专门设计轴线、尺寸、负空间和字间关系。普通输入转轮廓不能证明完成字标。没有找到合适的中文品牌字标 production Skill；工程字体诊断不能补足作者能力。

最可复用步骤：固定摄影，选一个慢茶/手作理由，每次只改变一类起收笔或接点行为，在“茶”“作”共同体现；先验证黑白整体，再放回摄影评测。此适用性是研究推断，尚未证明审美收益。

## 缓存及实际工具证据

全文已移入私有 .liu-visual-private/lettering_correction_20261004/worker_cases/，移动前验证全部绝对路径在 workspace 内；单一 PowerShell Move-Item，移动后 SHA256 一致：

| 私有缓存文件 | SHA256 |
|---|---|
| founder_heytea_case16.html | 71469beac46f58ccf48da268d0e5fd21bc236e4967076cce6f6e167a0f1ef0ae |
| hanyi_custom_font.html | a0f7c726200fbb7b171592572ab38c99bc363e118d4e98cbe5457e64efee0dc5 |
| hanyi_white_rabbit_case15.json | 3f25951ed36460605b7fe6d474de4d8c8951185711f68c3e5643b8044ffefa91 |

案例列表、两 HTML manifest、HTML读取脚本也在上述私有目录。官方入口为 [方正](https://www.foundertype.com/index.php/FontofMade/customFont.html)、[汉仪](https://www.hanyi.com.cn/orderfont)。

作品像素仅在私有 .liu-visual-private/lettering_case_sources_20261004/。完整原图 URL/尺寸/SHA256 在公共 CASE_IMAGE_TOOL_EVIDENCE.json、CASE_IMAGE_TOOL_EVIDENCE_02.json。实际执行 GET、Pillow元数据、view_image(detail=original)：

| 已看作品文件 | 观察位置 / SHA前缀 |
|---|---|
| heytea_01_introduction.jpeg | 下方喜茶轮廓 / dc595fb0 |
| heytea_03/05/07/09_mechanism.jpeg | 正文说明，不独立作轮廓证据 |
| heytea_02_structure.gif | 首帧心部 / d9e427a7；92帧未遍历 |
| heytea_06_terminals.gif | 首帧波字 / 9b8167d0；126帧未遍历 |
| heytea_application.jpg | 上部粗细标题 / d53b2c83 |
| hanyi_white_rabbit_specimen.png | 上LOGO/下字体 / 29916dcb |
| hanyi_white_rabbit_start.png | 中央小字 / d32fe2ba |
| hanyi_white_rabbit_openings.png | 上兔/左四字 / c13fea3e |

汉仪 end/start 两URL返回相同字节，只算一份像素证据。GIF仅工具首帧。未编造不可见的调用ID。没有追摹、生成或生产接入。公开展示不等于开放授权，未找到复制轮廓/标志/作品图许可；[汉仪许可页](https://hanyi.com.cn/license)明确区分LOGO用途。本次只提炼方法。

