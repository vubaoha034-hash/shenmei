# 固定字体工程试用恢复

24MB SourceHanSerifSC-Regular.otf试用输入不提交Git，原许可与固定来源清单已提交。恢复单一输入时下载以下固定提交文件，先核对SHA，再运行已经试用过的helper；不要重跑acquire_upstream重新选择main最新版本。

- 来源：https://github.com/adobe-fonts/source-han-serif/blob/7889f11bf31170b5d092a083b357c8c8130f89e0/OTF/SimplifiedChinese/SourceHanSerifSC-Regular.otf
- raw：https://raw.githubusercontent.com/adobe-fonts/source-han-serif/7889f11bf31170b5d092a083b357c8c8130f89e0/OTF/SimplifiedChinese/SourceHanSerifSC-Regular.otf
- 版本2.003、24543332字节、SHA `78aa7a328fd974df2d688c8a9fd74a33d8334dfa84ab24d9d11efb2ffc464117`，OFL1.1，Reserved Font Name Source。
- 放回 `fonttools_bounded_probe_v1/upstream/adobe-fonts/source-han-serif/OTF/SimplifiedChinese/SourceHanSerifSC-Regular.otf`，或任意私有路径并向helper传入绝对路径。

```text
python probe_glyph_metrics.py --font <已校验的字体> --text 茶作 --output <新的JSON路径>
```

Python3.11.15、fontTools4.63.0已实际运行；不需GPU、付费服务或模型训练。已保存的CHAZUO_GLYPH_METRICS_TRIAL_01.json为真实旧试用，不得用重跑覆盖。字体未改制，本轮字标不是该字体轮廓。本试用仅证实缺字/实际轮廓/面积重心可追溯，审美收益未验证。
