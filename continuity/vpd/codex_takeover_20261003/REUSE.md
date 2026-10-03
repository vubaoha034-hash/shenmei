# 茶作本轮成品：读取与复用入口

这是既有主线本轮交付说明，不是新任务系统。新 ChatGPT/Codex 先核对权威仓库 `vubaoha034-hash/shenmei`、分支 `visual-program-distillation-v2-photography-design-20260814` 最新提交，再按根 `START_HERE.md` 读取 AGENTS、PROJECT_CONTROL_ADAPTER、ROADMAP、CURRENT_TASK_LOCK、LATEST_CHECKPOINT。本页中的状态描述不能覆盖最新任务锁。

本轮制作已完成三版，初版一次、修订两次，额度耗尽。三版原审均 AI_FAIL；原审正校准使用197:2母参考代理，身份限制保留。最终第三版另以真人实际认可的201:2/203:2纠正正校准后独立冷审，仍 AI_FAIL。最终设计未变。刘先生对本轮新成品的真人反馈 PENDING，未晋升母版。唯一下一动作以任务锁为准：把第三版及失败意见交刘先生验收，不自动开始第四版、第二风格、出图或定时任务。

## 直接查看及编辑

- 最终完整海报精确PNG归档：[Figma 261:2](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=261-2)，1536×1024。其上传原始字节SHA为 `078ec5aea6f9f0356a3528274588a0d75bb1533d30d9f86eedd93aaa3984f04a`。
- 可编辑源：[Figma 259:2](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=259-2)，页251:2；摄影259:3锁定，原创字标259:46有16条闭合VECTOR轮廓，文案259:65/66为TEXT。
- 字标原始SVG：`evidence/vpd/codex_takeover_20261003/chazuo-wordmark-v3.svg`；Figma实际导出SVG：同目录 `v3/FIGMA_EXPORTED_WORDMARK.svg`。字标依据、字体许可及修改记录见 `FINAL_DESIGN_RECORD.md`、`METHOD_ADOPTION.json`。
- V1源251:3／精确PNG262:2；V2源257:2／精确PNG262:3。它们全部保留为失败版本，不是备选通过方案。
- 权威作品/参考/各版/审稿定位及SHA：`evidence/vpd/codex_takeover_20261003/DELIVERY_ASSET_MANIFEST.json`。临时下载URL不能作为交付地址。

## 摄影与导出边界

原件是88-R4，Drive `195jV49c3YdrI6VtIuONJJ1d09lsRqT8D`，SHA `7d84d35523afcb2d7599c438fc946801608e85c5489a5cde08d55f13eea4c9ed`。真人正向只覆盖摄影；字标与设计否决。身份来自原生R4派发与随后真人结论的连续证据，真人反馈文本本身没有写文件ID。

原件含烘焙文字/色板和左上弧线；有界寻找未取得无字源。没有修复被旧字遮住的摄影，也没有声称删除文字后摄影不变。原件整张以1:1锁定为底层，改动仅是可逆设计层：右上[920,94,1536,409]、左上[32,28,224,142]。其余1,356,936像素与原件RGB完全相同。最终版左上遮罩成为可见空条，右上仍有硬色板，正是AI_FAIL的主要原因。

Figma直接渲染在摄影保护区存在6,601个像素的1级通道舍入。保存了原始导出；`scripts/vpd_export_photo_safe.py`只在本轮固定RGB1536×1024源、已声明遮罩范围、最大误差≤1时恢复保护区源RGB，设计区仍与Figma原始渲染完全一致。原件及最终PNG无sRGB/gAMA/iCCP标记，原始Figma导出有sRGB/gAMA；这不是任意ICC来源的通用色彩转换。详见各版 `EXPORT_FIDELITY.json` 和 `PNG_COLOR_PROFILE_AUDIT.json`。

## 在新工作区实际恢复PNG

PNG放在授权Figma文件原始image fill中，未把摄影/参考/校准私有像素提交公开Git。新工作区必须取回原始字节；只读路径或描述不能算看图。Figma需现有连接及文件读取权限；没有连接时准确记 `UNABLE_TO_RESTORE`，不得用占位图代替。

调用官方 `figma_download_assets(fileKey="uyDxOoN1iNDPpEHTKSUWg1", nodeId=...)`，**取 `rawImages` 原始PNG，不要用 `export` 重新渲染**。先把短时URL保存到gitignored的 `.liu-visual-private/asset-url.json`，内容 `{ "url": "工具实际返回的短时URL" }`；再运行：

```text
python scripts/vpd_download_bound_asset.py --url-file .liu-visual-private/asset-url.json --sha256 <清单SHA> --dest <清单private路径>
```

必需节点及落地路径：259:3→`.liu-visual-private/source-r4.png`；262:2→`versions/v1/poster.png`；262:3→`versions/v2/poster.png`；261:2→`versions/v3/poster.png`（后三项同在 `.liu-visual-private/` 下）。当前状态检查最少需要source-r4和当前v3；恢复所有三版才能对照历史。HTTP202空体表示未取得可接受PNG，可能待生成或请求形式未被服务接受；不是恢复成功。已实测默认Python UA收到202、常规UA收到200，因此脚本显式UA；仍最多四次有界请求，失败重取一次URL，200+PNG+预期SHA都符合才写文件。

校准原始字节归档：265:2→Pproxy197:2、SHA `d4f0d880656ff143a41131d2c7d0db6659de09d519e0ebc294bd86db51cc7215`；265:3→N241:2、SHA `deb1a5909bcc6ca8cb9119b3efabd5f65ccdef0dcf00f60e6b215806a44b2cf4`；265:4→Pdirect201:2、SHA `57c21466512a79cbb25c75db1d6a1748b595c3bc2d00c85ba51615557f74f925`。P只校准字标/层级/阅读关系，摄影不通过。指定参考Drive `11HpNmepnqlyZNs4uzUTjjEbP8LWwPutC`，SHA `87a28f5cd4b5d15b01e6536206127c357043a904b3c0dab3bfa0c50080782167`，只用上半横版广告。来源校验见 `REVIEW_INPUT_PROVENANCE.json`。复原审稿包时用这些实际PNG及参考原件，不把代理与直接认可样本混同。

恢复后运行既有检查：

```text
python scripts/verify_visual_memory.py --vpd-state --status-card
```

## 可运行的执行、审稿、回写

执行继续用官方 `figma-use`15.0.0核心流程和 `use_figma / upload_assets / download_assets`，先读其SKILL与API参考，使用实际发现的工具名称。没有新全局Skill安装，也不把下载源码称作启用。字标已是原生矢量，不需图像生成来替代本轮成品。后续需新的明确授权才可改作品。

审稿使用已保存的本任务载体变更 `REVIEW_CARRIER_AMENDMENT.json`。原项目外Chat协议保留历史；独立CLI尝试因TLS UnknownIssuer失败，未假称成功。实际成功载体是 `fork_turns="none"` 子代理，GPT-6.1 Sol/Max从实际turn_context核对，只有P/N/R/T四图，无创作历史或旧审稿结论。它仍在同一文件系统，不能称作项目外目录。已有通过的上下文证明不能沿用给新的审稿。

新审稿先创建新的四图包及中性提示，T真人结论隐藏。保存实际spawn，审核完成后使用 `scripts/vpd_collect_agent_review.py --help` 的显式agent/root-thread/packet/out/version/prompt/child-rollout/root-rollout参数；只读指定真实runtime文件，审核四个ImageView及tool scope、实际模型、单一turn_context，再保存PIXEL_REVIEW和证据链。提示副本SHA不是加密spawn消息的字节证明；此限制保存在 `PROOF_LIMITATIONS.json`。任何必要像素/隔离证据缺失只记无法评测，不能通过。AI审美意见与 `TECHNICAL_CHECK.json` 分开。

既有R4检验样本version0实际读取四个唯一图片，并为PNG头读取同一T一次，共5个ImageView；收集时须显式 `--holdout-target-reread --target .liu-visual-private/source-r4.png`。这是仅version0可用的读取例外，不用于正式成品审核，也不增加检验样本数。原始3版与纠正V3冷审均为4个ImageView。

执行证据先用 `scripts/vpd_record_artifact.py`生成**新的不可变**receipt；只有主执行者调用 `scripts/vpd_codex_takeover.py`，写现有任务锁/检查点/商业账本，禁止第二个状态作者。writer先核对远端=本地HEAD、历史账本前缀和本地并发差异，逐文件replace失败有回滚；这不是掉电/进程崩溃跨文件原子事务。写后跑既有状态检查，Git提交/非强推，再独立远端回读。receipt不能覆盖已引用旧版本。

## 方法、环境及真实收益

- 成熟中文品牌字标SKILL候选未证实适用，未安装或晋升；读过canvas-design、frontend-design等源码与许可并记录不适用边界。实际采用官方Figma制作技能和fontTools4.63.0几何诊断方法，后者不是Logo设计器。固定上游/许可/读过内容/实际试用见 `METHOD_ADOPTION.json`及 `skill_research/fonttools_bounded_probe_v1/RESEARCH_RESULT.json`。
- 状态检查、writer、审稿收集与下载用标准Python3.11+；字形试用需fontTools4.63.0。摄影数值补偿需实际可用bundled Python3.12.14、Pillow12.3.0、NumPy2.3.5。本机路径由 `load_workspace_dependencies`发现，不能把另一台机器固定成同一路径；系统Python图像DLL曾被拒绝，未盲目重装。
- SourceHanSerifSC-Regular 2.003试用字体24MB未提交，固定adobe-fonts提交及SHA在研究清单；按 `FONT_TRIAL_RESTORE.md`恢复并校验。最终原创字标未使用该字体轮廓；辅助文字实际Noto Serif SC Medium，Figma二进制版本不可观察，OFL来源保存，不能声称它与下载试用字体相同。
- **流程改善已验证，视觉收益未验证。** 真实制作/独立四图审稿/保护区验核/原始PNG回存/可编辑源成立。fontTools只证明轮廓诊断，未证明字标更美；时间节省未量测。检验只一个独立旧R4样本判FAIL与真人否决一致，无准确率/置信度。最终新作品真人认可仍待定；整体视觉蒸馏系统、迁移、第二风格均未完成。

对照、专业审查及新的入口恢复实测证据位于 `evidence/vpd/codex_takeover_20261003/`，以当前delivery receipt实际引用文件为准。自动学习仅指研究→试用→比较→保存，没有权重训练、后台无人触发运行或恢复定时任务。
