# 私有文字方法 CLI 收尾回执

本次只新增公开脚本 `scripts/vpd_shanyeji_typography_study.py`（13,960 字节，SHA256 `aa417dce468db08904efd266c9a5e383adcc8c55de77885862295a5c89e1a27a`）和此私有回执。没有新增公开辅助脚本、复制私人图像/资产到公开路径、生成新素材、改变 S1/S2 或业务状态、修改入口或其他作者文件。

该脚本是薄适配器，固定调用现有私人 producer，既有算法没有被复制重写：

- `inspect` 只读取成果。实际核对 canonical JPEG SHA 和 960×1280，clean SVG SHA、241 个非空 path、viewBox 与无 image/text/foreignObject，S2 三个 PNG 的真实 SHA/RGBA/尺寸，并用原 soft producer 的几何 helper 重算文字支持域，检测既有 PNG alpha。它没有调用 producer.main() 或保存任何新图像。
- `trace --output ...` 固定调用现有 VTracer producer，参数 full/correction2/aux-vector-scale4。默认上游依赖保持 MIT VTracer 0.6.15 未修改版本，并使用已捆绑 Node sharp；可显式覆盖 Node 与 sharp 路径。只接受仓库 `.liu-visual-private` 内尚不存在的新输出目录，原资产目录会在加载制作 producer 之前拒绝。
- `soft-ink --output ...` 固定调用现有软色/软 alpha producer，把输出重定向到尚不存在的新私有目录；输入继续使用固定 canonical 与已存 S1/baseline 遮罩。没有替换字形、生成摄影或宣称真实原 alpha。

调用前拒绝缺失私有素材与 producer fingerprint 不符，不下载、不安装依赖、不生成替代来源。公开仓库单独 clone 不包含原件、遮罩或私人 producer；恢复这些获授权材料之前拒绝执行是预期行为。只检查当前私有输入，不擅自扩大为通用新案例生成器。

真实依赖：Python、Pillow、NumPy 用于 inspect/soft-ink；trace 还需要 cp312 本地 VTracer 0.6.15 及 Node sharp。当前私人 trace producer 仍包含本机 bundled Windows 默认 runtime 路径。fresh 机器从未验证；本适配器的 trace 和 soft-ink 成功制作分支本次也未执行，不将之前直接运行私人 producer 的成功冒称为新 CLI 已完整生产验证。

实际执行（Python 为 `C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 -B`）：

1. `scripts/vpd_shanyeji_typography_study.py --help`：实际 PowerShell 工具 exit0；显示 inspect/trace/soft-ink、私有素材缺失拒绝、真实依赖、只用新私有输出目录、fresh machine 未验证等说明。
2. `scripts/vpd_shanyeji_typography_study.py inspect`：最终文件实际运行 exit0，`STRUCTURAL_INTEGRITY_PASS_ONLY`，production_run=false。原件 SHA=`9a29fbdc…414`，clean SHA=`59376f5d…6b`，241 非空 path；S2 all SHA=`0c4fb7f9…5337`、typography SHA=`6915bd41…1cb3`、tiny SHA=`50f385f7…5dcd`；RGBA 尺寸分别 960×1280、960×1280、50×31；文字支持域外非零 alpha=0，中间 alpha=51,790，非零 alpha=95,775，空白/山内白/Λ 开口三个探针全0。
3. 防覆盖负例 `trace --output .liu-visual-private/shanyeji_typography_study_20261005/reconstruction/02_full_final_vector_detail`：实际 PowerShell 工具非零 exit1，输出 `REFUSED_OR_FAILED / OUTPUT_ALREADY_EXISTS`，production_success_claimed=false。Python handler 对拒绝返回2；PowerShell 工具报告非零为1。没有进入 producer.main()、没有生成或覆盖图像。

producer 固定 SHA：trace `badccb256bb95a95e25106d8d70d3058d9ddc4f9be49fb9892776d6b6dc3d55b`；soft `55a0c90d24b24827fe8afdf104396f55b55f8ce2baa474339284debc4eb8baa8`。真实 inspect 核对了这两个指纹。

完整 source/asset SHA 都在 CLI stdout 的实际 inspect 结果以及此前私有成果回执中。这里不重新判 S1/S2 保真，不改变真人验收状态，不声称找回 257 上传字节或原始 alpha。Root 负责 Git、公共证据、状态和外部归档；本 worker 制作到此结束。
