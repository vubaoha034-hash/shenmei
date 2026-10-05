# V28独立设计诊断（2026-10-05）

独立AI诊断，实际gpt-6.1-sol / max已由执行turn_context核实。实际原像素读取S、R、T28、P共4次view_image(detail=original)；R仅上1080×720广告进入判断。此记录不是项目外正式冷审、真人审核或AI_PASS，不修改业务状态和旧冻结资产。

T28的三个主要问题：主句大小/密度分成两组却横跨产品；汉字重竖、宽横与密集字腔的视觉重量失衡；“茶”长尾挤入鲜叶关系而未改善读序。当前字图蒸馏把参考的紧凑双行、产品重心和负空间误换成大字加接物长笔，须修订这一实现。不能由这次诊断推出整套蒸馏有效或无效。

唯一下一方向：**“山野 / 慢饮”四字双行，在右上暗部成紧凑字块，杯盘仍是画面主角。** 七变量：四字文案；右上盘上方位置；约350–375px宽、245–265px高的同字号双行；较轻且字腔清楚的手写字；光学字距/行距；现有米白单色；靠尺寸与负空间建立杯盘关系。放弃V28七字轮廓续修和茶长尾，不制作备选。坐标/尺度只作起点，不晋升成taste硬门槛。

保留摄影7fd和V9品牌dd8e，品牌x=285、y=198、width=205。下一版要在整图、正常显示和缩略显示比较产品主次与四字可读性，机器只验证保护与文字正确；收益须由下一实际成品证明，真人最终验收仍待执行。

实际方法阅读：[Figma字体设计](https://www.figma.com/resource-library/typography-in-design/)、[Figma图形设计原则](https://www.figma.com/resource-library/graphic-design-principles/)、[Glyphs字间距](https://glyphsapp.com/learn/spacing)、[Glyphs字偶距](https://glyphsapp.com/zh/learn/kerning)。仅迁移视觉重量、真实尺寸校样和字形白空间判断；不把UI字号或拉丁边距比例当中文品牌规范。Figma资料为通用基础，不冒称完成高级品牌课程。

完整私有诊断、输入/来源/像素工具证据、执行audit各一文件，保存在 `.liu-visual-private/v28-independent-design-diagnosis-20261005/`。本子代理0出图、0业务写入、0旧冻结资产修改、0Skill/validator修改。默认Python的原生检查因缺PIL执行失败；root承担实际原生状态检查，本诊断不认证状态技术通过。

