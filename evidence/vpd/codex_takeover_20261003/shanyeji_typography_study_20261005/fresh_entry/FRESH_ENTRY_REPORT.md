# 山野集当前入口：一次新读取上下文复用测试

当前**工作树入口可恢复，已有资产只读复用可执行，保留限制**。本测试从 START_HERE.md 开始，读取 adapter、roadmap、唯一任务锁、checkpoint、WORKER_CURRENT_REUSE.md 及其研究证据；业务结论来自文件。没有进行独立审美审核，也没有给出审美 PASS。

## 当前状态与固定提交的差异

本地 HEAD 与 origin 跟踪均为 `65e51a7f6008c59cd9702a26526a9d5888557f66`。固定提交保存 revision333/checkpoint355：V29 已交付且 AI_PASS，下一动作是刘先生审完整海报，没有本轮研究字段或 inspect 脚本。

实际工作树是 revision336/checkpoint358：`SHANYEJI_WHOLE_TYPOGRAPHY_REFERENCE_STUDY`，状态 `VPD_CODEX_CHAZUO_CORRECT_SOURCE_REFERENCE_STUDY_ARCHIVE_BLOCKED`。研究文件初读未提交，后续观察为另一执行者已暂存；仍不属于固定 HEAD。**只克隆该固定提交，不能恢复当前研究入口。** 两次只读远端核验分别因 schannel 凭据错误与 OpenSSL TLS EOF 失败，因此不宣称已实际确认实时远端。

adapter 任务锁、WORKER 入口及研究引用共23项 SHA 均匹配。roadmap 原始 CRLF 字节 SHA 为 f4da36a3…，转为 LF 后为 adapter 绑定的 2abced16…；这是换行差异，不报告成业务状态失败。本测试没有重复全量历史原生校验，也不借父执行者的校验消息宣称自己执行了全状态 PASS。

## 恢复出的范围与唯一动作

同一任务 `VPD-CHAZUO-CODEX-COMPLETE-POSTER-20261003-01`、unit `CHAZUO_APPROVED_SOURCE_TYPOGRAPHY_20261003_R1`。用户要求暂不管底图/茶作新海报，只研究山野集**整个文字系统**并在 Figma 临摹。原授权文件逐字保存该要求。当前29个正式海报版本与旧 AI 结论保留；V29文字真人 REJECTED，完整海报真人 PENDING，研究真人 PENDING。摄影7fd7777f仍认可且冻结；没有V30，render_allowed 与 p6_allowed 都为 false。

唯一下一动作是 `AUTHORIZE_SHANYEJI_STUDY_DRIVE_DESTINATION`。Drive归档两次自动审批拒绝，目录归属/可见性证据不足，具体目录授权 PENDING，文件ID为空。归档完成后才交刘先生审研究，不能据等待时间批准。START_HERE/WORKER首段及adapter明确只用原生锁调度；V29等待验收、旧V24–V28继续修复、三版停止与H1–H4旧动作都是历史，不能覆盖当前范围。

## 真实作品、源结构与像素读取

实际查看原参考JPEG、S1完整PNG及S2完整PNG，均用 view_image 原始细节读取。对应SHA分别为9a29fbdc…、6f23f8fb…、200619e4…，完整字节复核与manifest一致；研究画幅为960×1280。参考为山野集，不是旧山葵炙。S1/S2完整图呈现全套文字研究与暗色平底，原参考包含摄影树叶；这里只核验作品身份与像素可读，不另作审美通过判断。

- [S1纯矢量412:5](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=412-5)
- [S2显示研究416:2](https://www.figma.com/design/uyDxOoN1iNDPpEHTKSUWg1/?node-id=416-2)
- 本地S2：`.liu-visual-private/shanyeji_typography_study_20261005/FIGMA_TYPE_STUDY_S2.png`
- clean SVG：`reconstruction/02_full_final_vector_detail/SHANYEJI_typography_contours_clean.svg`（SHA59376f5d…）
- 显示墨层：`reconstruction/03_soft_foreground_trial/SHANYEJI_soft_foreground_all.png`（SHA0c4fb7f9…）

先读取官方 figma-use 后，实际执行仓库 FIGMA_READONLY_REUSE.js。416:2与页412:2可访问；241个VECTOR在隐藏组416:3，有效可见VECTOR为0，416:271的一层IMAGE可见，imageHash189ae792…与原上传记录一致。脚本writes=0，没有切换可见性、创建/编辑节点、修改摄影或导出新作品。曲线具备结构上的编辑入口，但本次没有实际编辑，因此也不证明另一账号写权限。修改曲线不会自动重建显示墨层；它不是原字体、原透明层或完全纯矢量显示。当前连通账号读取成功不证明公开或新机访问。

## 实际可执行调用与失败边界

裸命令 `python -B scripts/vpd_shanyeji_typography_study.py inspect` **实际失败**：shell选中hermes Python3.11 / NumPy2.4.6，NumPy C扩展DLL无法加载。随后通过load_workspace_dependencies发现并使用现有runtime，实测Python3.12.14 / Pillow12.3.0 / NumPy2.3.5。

可复用的PowerShell调用是：

```powershell
& 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B scripts/vpd_shanyeji_typography_study.py inspect
```

该调用exit0，`STRUCTURAL_INTEGRITY_PASS_ONLY`，production_run=false。clean SVG有241个非空path；文字支持外alpha非零像素0，非零alpha95775，中间alpha51790，三处空白/字腔探针全0。它只证明当前资产结构与身份，不重评保真、审美或真人接受。

另用不存在的repo-root执行只读inspect，实际返回`PRIVATE_MATERIAL_MISSING`，没有下载、替换或生产。源码确认SHA不符/私有材料缺失即拒绝；生产输出须是Git忽略树中的新目录，不能覆盖已有目录。没有运行trace或soft-ink成功生产分支，没有安装依赖。公开保存的producer代码可恢复代码字节，参考JPEG、mask与SVG/PNG必须另从获授权的私有存储恢复。

## 新上下文与新机器、技术与审美

本测试验证**现有机器的新读取上下文**，不是新机器完整制作。Git忽略像素、中间mask、私有VTracer与运行时、Figma账号能力和待归档素材都是新机边界。初始导入SVG的257854…原字节本地丢失，clean SVG是不同SHA，原导入在Figma413:3的说法来自已绑定记录；本次没有恢复那份原字节。原字体、原alpha、原SVG与高分辨率设计源未知，不能承诺一模一样。

已保存S1审稿为REFERENCE_FIDELITY_FAIL，S2为REFERENCE_FIDELITY_PASS_WITH_LIMITATIONS；本测试只读取并核对引用，没有重做审美结论。它们属于两图参考形态复建，不是茶作新AI_PASS或正式五图冷审，也没有解决历史AI通过而真人否决的误放行问题。完整迁移、原创茶作设计质量、节时、新机制作与真人认可未验证。

本报告仅写指定fresh-entry目录；未更新业务状态、未改Figma/图片、未上传、未联系用户、未执行Git写操作、未新建子任务。原始工具结果、完整SHA、已测/未测项保存在同名JSON。报告本身当前位于Git忽略私有目录，不等于已发布保存。

## 测试期间发布后的固定回读补充

开始时HEAD65/未提交是当时真实事实。父执行者随后发布同树提交93451aa42aca6e3198aee83d6a06c11854dc85e2；本测试再实际读取本地HEAD与树82becf375c74bdf9bf31315a44fd8aa2df334bb9，并用GitHub fetch连接器对固定934提交的CURRENT_TASK_LOCK、WORKER_CURRENT_REUSE、DELIVERY_MANIFEST进行独立回读。三个UTF-8内容SHA均与已经测过的本地原字节一致，恢复revision336及唯一动作AUTHORIZE_SHANYEJI_STUDY_DRIVE_DESTINATION。因此**当前研究入口与元数据已在该固定提交保存**；开头的未提交观察属于时间线，不是最终发布状态。shell两次远端失败原样保留；另未核验实时分支tip。

固定提交保存代码和证据，Git忽略像素/私有中间资产以及Drive归档缺口未因此解决；新机制作与审美/真人接受仍未验证。此次补充未修改业务状态或Figma。
