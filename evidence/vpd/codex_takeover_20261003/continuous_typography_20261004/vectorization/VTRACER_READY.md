# VTracer 有界工程试用

2026-10-04。可用，目的仅为 raster → SVG editable paths；不设计字形、不证明审美收益。没有读取冷审、生成字标候选、改摄影或写业务状态。

## 官方来源与固定版本

[官方仓库](https://github.com/visioncortex/vtracer)、[官方包/示例](https://pypi.org/project/vtracer/0.6.15/)。固定 Python package **0.6.15**，发布于2026-03-23；没有采用1.0 alpha。源包 pyproject 0.6.15 / MIT，cmdapp Cargo 0.6.12；真实 SVG generator 标记 **0.6.12**，两者不混称。

wheel：`vtracer-0.6.15-cp312-cp312-win_amd64.whl`，SHA256 `b0f08b66734e41872d4ac343ed6d08870b3235346def3e112e10b3b2443e619e`；sdist SHA256 `f7f39943d1fc8e9dc82f5360a40e941aaf4c9166d8df30c3f6a2da8cc21dfc52`。下载字节均匹配官方 PyPI checksum。源码固定到此源包/hash，未推定 Git SHA，也未重建 native wheel。

已实际读取源 LICENSE、Python README 的 binary 示例、pyproject、root/cmdapp Cargo。**本固定包 MIT**（当前 master 的 MIT OR Apache-2.0 不用于替代它）；许可要求保留版权/许可声明。许可证与源包保存在私有依赖目录；完整下载 URL/成员 SHA 在 `UPSTREAM_MANIFEST.json`。Rust依赖声明包括 visioncortex 0.8.8、image 0.23.10、pyo3 0.19.0；没有运行编译/源码安装。

## 环境与调用

初始 PATH 无 vtracer/potrace；两个 Python 环境均未装 vtracer。采用既有 bundled Python **3.12.14 / Windows x64**、Pillow **12.3.0**；`pip --no-index --no-deps --target` 只安装核验 wheel 到 `.liu-visual-private/dependencies/vtracer_0_6_15_cp312/site-packages/`，不改全局，不需要 Rust 编译器。

在仓库工作目录运行（两个目标文件都须为新路径）：

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 'evidence/vpd/codex_takeover_20261003/continuous_typography_20261004/vectorization/vectorize_mask.py' '<黑字白底PNG>' '.liu-visual-private/continuous_typography_20261004/new-paths.svg'
```

薄 wrapper 只调用官方 `convert_raw_image_to_svg(..., img_format='png', colormode='binary', mode='spline')`，固定其余参数见脚本/试用 JSON。自动定位私有包；不覆盖输入/已存在输出。

附有 `--alpha-mask`：仅有真实透明通道时将 alpha≥128 映为黑、其余白，保持尺寸；输出黑色路径，可在Figma设统一颜色。**该 alpha 选项未在本次试用运行**，不要据此宣称透明生产字形已验证；图像全不透明时会拒绝该模式。

## 真实一次试用与限制

仅一个96×64非作品 fixture：带孔矩形环+三角。2026-10-03T22:34:41Z 实际 conversion 用时 **0.0043204s**，输出 **820 bytes / 2 paths / M数2与1 / 有C曲线 / 无image与text**。源PNG已 view_image(original)，SVG已读取/XML解析；未对SVG回栅格测像素误差。孔由同一路径中方向相反的两个轮廓表示。细节见 `TRIAL_RESULT.json` 与 synthetic 文件，输入/输出 SHA 可重验。

实际执行 chunk：环境84611a、官方下载58a3d9、安装09075f、试用85c2d1、SVG源码读取e02f1b。`CODEX_THREAD_ID=01a0ffad-8b0c-71d0-9b4d-2dc355ab25af` 为实际单变量读取及进程记录；服务端模型/effort字段不可见。chunk是工具执行输出标识，不代替服务端模型身份。

未验证：生产中文字形保真、半透明细笔画、Figma实际导入/节点编辑、孔洞的Figma显示、审美改善。曲线拟合会近似边界；二值化会改半透明边缘，filter_speckle=0保留小点也会保留噪声。它生成几何路径，不能恢复字体结构或纠正字形；Figma接受SVG路径的预期须由Root真实导入确认。
