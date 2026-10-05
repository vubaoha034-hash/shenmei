# 山野集整体文字临摹：实际方法与复用

这是用户明确要求的原参考文字研究，不是茶作新成品，不是新风格验证。业务状态只读 CURRENT_TASK_LOCK；此目录没有第二套任务系统。

## 实际完成及差距

同一个960×1280参考，Figma文件uyDxOoN1iNDPpEHTKSUWg1，新页412:2。参考412:3；S1纯矢量412:5；对位诊断412:6；S2软墨层416:2。S1独立实际像素审核FAIL：硬孔洞、锯齿、小字断笔、色差。S2使用同样轮廓和坐标，只改变前景细纹理/颜色表示，新的隔离审稿为REFERENCE_FIDELITY_PASS_WITH_LIMITATIONS；不是完全像素一致。两版和原FAIL保留。

S2显示一层来源JPEG估计的RGBA墨层416:271；241个曲线保留在隐藏组416:3。打开该组并隐藏墨层可编辑纯矢量形状，但不能宣称改曲线后纹理会自动更新。这里没有可直接输入替换的原生字体。原字体、原alpha、原SVG和JPEG压缩前色值未知。若要求精确复原，应取得原设计源文件、透明字标/纹理及字体依据；仅截图无法证明一模一样。

## 设计依据与实际制作

不是将普通字体放大。原图主标以山形峰顶、块状笔画、内部三角/不规则负形构造“山野集”，橙色回环在不同位置前后穿插；顶部四组英文、山形下两行Mountain/market、中文副行、橙色手写整行和底部署名共同形成完整系统。字形身份和不规则纹理比单个字号更关键。

实际从固定JPEG分区域读取颜色与字形支持，调用未改的VTracer0.6.15提取曲线，保留七类文字资产、遮挡可见形态及同坐标布局。细小英文和笔画采用放大描摹；纯矢量无法准确表示JPEG中的颗粒和软边，第一版被否决。第二版用同样支持范围，估计软alpha并保留高置信墨芯的来源RGB，边缘仍存在灰褐/暗色光晕。它是图像分离近似，不是恢复了原透明层。摄影像素没有移入研究文字作品作为底图，也没有改变茶作摄影。

上游官方资料实际读了三篇正文：[Vector networks](https://help.figma.com/hc/en-us/articles/360040450213-Vector-networks)、[Edit vector layers](https://help.figma.com/hc/en-us/articles/360039957634-Edit-vector-layers)、[Boolean operations](https://help.figma.com/hc/en-us/articles/360039957534-Boolean-operations)。阅读范围和局限在TUTORIAL_SOURCES.json，视频实际观看数0。闭合轮廓、曲线控制、负形和分层是适用方法；本轮实际通过描摹和SVG导入建曲线，没有逐点操作Figma钢笔或原生布尔组，不将教程提议写成操作证据。官方操作教程也不等于中文字标设计教学。

## 依赖与调用

未新增、安装或宣称发现一种能直接做中文品牌字标的成熟skill。复用已核实的Figma官方figma-use制作接口、原生独立审核机制和VTracer。VTracer0.6.15 MIT，上游核心未改；版本、wheel/sdist SHA、许可证及私有安装恢复见continuous_typography_20261004/vectorization/VTRACER_READY.md及LICENSE-VTRACER-MIT.txt。既有Anthropic官方design-critique固定提交d3ee81913e5e179273313345847a2a4f42449bd2、Apache-2.0提供分区证据审稿框架，不是字形创作工具。本轮简化为独立两图复原对照；不替代茶作正式五图项目外冷审。

实际环境Python3.12.14、Pillow12.3.0、NumPy2.3.5、Node24.19.0、sharp0.35.4；VTracer私有目录依赖cp312/win_amd64。新机先用load_workspace_dependencies发现真实runtime，再按固定包恢复。现有Figma曲线复用无需重新运行描摹。制作入口scripts/vpd_shanyeji_typography_study.py的inspect只读核验；重新制作须私有参考及所需中间资产，新输出目录禁止覆盖。跨机完整制作尚未验证。

独立像素审稿：fork_turns=none、只有本轮两张指定图片和必要要求、一次上下文，实际gpt-6.1-sol/max；s1_pixel_review和s2_pixel_review内的原始结论、实际ImageView、spawn与模型核对分开保存。没有继承作者评价或上一轮审稿。共享文件系统不能提供OS沙箱隔离；运行工具范围已查，仅两次view_image。scripts/vpd_collect_reference_study_review.py复用已有collector，从真实运行记录选择模型/工具/最终结论，不提取推理文本；新作品必须新审。

## 已知失败与保存边界

初始SVG导入SHA257854…有一个空d；作者之后清理同名文件，原字节本地丢失。一次有界恢复未匹配，不声称恢复。清理后SVG SHA59376f…有241个有效path，删除的是非绘制空路径，清理前后透明PNG相同；原导入仍保留在Figma413:3。必须区别原导入字节和清洁资产。初次整页创建回执被截断，后续定点读取确认；V29保护指纹FNV1a32一致仅为一致性证据，不是文件级密码学证明。

Drive归档被自动审批拒绝两次，既有目录元数据未证明归属/可见性；具体目录授权仍待用户答复。未绕过、未生成Drive文件ID。当前成品只有真实Figma和本地PNG/SVG，Drive长期调用未完成。原件与派生像素留在Git忽略目录，不上传公共Git；公共仓库保存代码、来源、引用和真实证据。

流程和可编辑曲线可核验；S2对参考文字的整体复原较S1有实际独立审稿支持，但仍有细边/颜色差距。没有证明原创茶作设计质量、迁移能力、节省时间或真人认可，也没有关闭历史AI通过/真人否决的误放行问题。后续只能依任务锁继续，未经用户确认不恢复茶作海报制作。
