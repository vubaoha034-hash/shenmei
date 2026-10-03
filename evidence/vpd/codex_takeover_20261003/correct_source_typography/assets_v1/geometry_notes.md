# 茶作文字资产的几何依据

这是同一个摄影方向的一组文字资产。品牌来源于自身笔画：横画有浅弧、右端轻提，竖画与撇捺有连续的粗细变化。没有独立叶子或随机破损。

品牌共 16 条原创封闭贝塞尔路径：茶 9 条，作 7 条。`lettering_construction.json` 保存每一条的控制点、组件身份和实测轮廓边界；`build_lettering.py` 通过 fontTools SVGPathPen 实际生成路径。Source Han Serif 的品牌轮廓只用于核对茶作结构，最终字标没有导入它的轮廓。

标题准确为“一杯茶，慢下来”，换行为“一杯茶，”和“慢下来”。字体是有 OFL 1.1 许可的 Adobe Source Han Serif SC Regular 2.003，原始 OTF SHA256 为 78aa7a328fd974df2d688c8a9fd74a33d8334dfa84ab24d9d11efb2ffc464117。标题保持真实字形；第一行 68 px、字距 7 px，第二行 104 px、字距 12 px，右侧墨迹边界相齐。第二行从上行向左下移 93 px，接向溪流和茶碗方向。文件 `headline-live-text.svg` 保留准确 Unicode；`headline.svg` 是逐字可编辑轮廓。

建议直接使用 `typography-overlay.svg` 或其透明 PNG，在原摄影上按 1536×1024、x=0、y=0 合成。字标框 x=92、y=77、宽224、高约104.83；标题框 x=1018、y=125、宽344、高218。颜色统一为 #F5F5EF。产品区域没有文字。

本资产制作角色没有看或审核完成资产，也不提供审美评分；独立复审需实际查看它们与原摄影组成的成品。
