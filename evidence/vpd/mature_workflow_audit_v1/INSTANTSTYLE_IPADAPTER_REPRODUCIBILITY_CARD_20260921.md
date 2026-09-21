# 首个免训练成熟方案可复现卡｜InstantStyle / IP-Adapter（Diffusers 原生路线）

日期：2026-09-21
项目：visual-aesthetic-vpd
状态：METHOD_COMPATIBLE_EXECUTION_ENVIRONMENT_NOT_READY
性质：只读兼容性审计结果；不是视觉通过证明，不是训练授权，不是出图授权。

## 1. 为什么选它作为第一个候选

本轮只选一个免训练候选，不同时铺开多条训练路线。

候选由三部分组成：
1. Stable Diffusion XL（SDXL）作为可控开源基座；
2. Hugging Face Diffusers 原生 IP-Adapter 作为参考图视觉条件；
3. InstantStyle 的 style-only 注入方式，只在风格相关注意力层启用图像条件，优先学习颜色、材质、氛围等风格信息，降低直接复制参考图内容/构图的风险。

它与本项目核心问题直接对应：当前 Prompt Capsule 把大量像素关系压缩成文字，容易丢失参考图中无法完全语言化的视觉信息；InstantStyle/IP-Adapter 可以直接输入参考图特征，同时与文字内容提示分离。

本轮不采用 ComfyUI 自定义节点作为第一正式实现，原因是增加节点版本/插件维护变量。第一复现优先使用 Diffusers 原生支持，减少第三方依赖。ComfyUI 可作为以后可视化封装，不作为首轮真实性判断前提。

## 2. 实际核验过的上游资料与落地链

已实际读取/核验：
- Hugging Face Diffusers 当前 IP-Adapter 使用文档：
  https://huggingface.co/docs/diffusers/using-diffusers/ip_adapter
- Hugging Face Diffusers 当前安装文档：
  https://huggingface.co/docs/diffusers/main/installation
- Hugging Face Diffusers 当前 SDXL 与内存优化文档：
  https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_xl
  https://huggingface.co/docs/diffusers/main/optimization/memory
- InstantStyle 官方仓库 README 与实际推理脚本：
  https://github.com/instantX-research/InstantStyle
  infer_style.py
  infer_style_plus.py
- IP-Adapter 官方仓库与模型：
  https://github.com/tencent-ailab/IP-Adapter
  https://huggingface.co/h94/IP-Adapter
- SDXL 基座：
  https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0

关键事实：
- Diffusers 已原生支持 IP-Adapter，并提供按 transformer block 设置 scale 的接口。
- 官方文档明确给出 InstantStyle 的 style-only 配置：只启用 up block 0 的第二个 transformer，未列出的层 scale 为 0。
- IP-Adapter 可直接输入一张参考图；无需训练本项目 LoRA。
- SDXL 是大模型，官方建议显存不足时使用 model CPU offload、VAE tiling 等优化，但官方资料没有给出“6GB 单卡一定可用”的承诺。
- InstantStyle 老仓库示例使用自带 wrapper；本项目首轮不采用该 wrapper，而采用维护中的 Diffusers 原生实现，避免旧依赖和重复封装。
- 旧 InstantStyle 示例存在 image.resize(...) 未接回变量的细节，因此不能机械复制示例脚本，必须以当前 Diffusers 文档为执行依据。

## 3. 固定的首轮软件与模型边界

为避免版本漂移，首轮方案建议固定而不是跟随 main：

- Python：3.11
- Diffusers：稳定发行版，执行前记录精确版本；当前官方安装页显示最新稳定线为 v0.40.0
- PyTorch：按实际 GPU/CUDA 环境安装的稳定版本
- Transformers / Accelerate：与上述 Diffusers 兼容版本，执行前冻结 pip freeze
- 基座：stabilityai/stable-diffusion-xl-base-1.0
- 图像条件：h94/IP-Adapter
- Adapter：sdxl_models/ip-adapter_sdxl.safetensors
- 图像编码器：h94/IP-Adapter 对应 SDXL image encoder
- 第一轮不加载 ControlNet、不加载 LoRA、不加载额外 composition adapter、不叠第二张参考图

文件体量参考：
- SDXL base 单 safetensors 约 6.94 GB；
- IP-Adapter SDXL adapter safetensors 约 703 MB；
- 对应 SDXL image encoder safetensors 约 3.69 GB。
实际缓存还包含配置、文本编码器、tokenizer 等，磁盘预算不能只按三项相加。

许可：
- IP-Adapter 模型页标示 Apache-2.0；
- SDXL 模型页为 OpenRAIL++。
首轮仅做内部技术验证；若以后用于正式商业交付，另做一次当时版本的许可复核，不把本卡当法律意见。

## 4. 我们实际要怎么跑

### 4.1 输入

只使用一张已经有明确像素身份的批准参考作为 style image。
首轮开发实验与旧 H1-H4 正式实验隔离，不得把开发输出回填成旧 holdout。

参考图读取时记录：
- 原文件名
- SHA-256
- 像素尺寸
- 色彩模式
- 来源/批准身份

不把后来生成图、Figma 修复图或失败候选混进参考图列表。

### 4.2 风格注入

首轮采用 InstantStyle 的 style-only block 配置，而不是全层 IP-Adapter：

```python
scale = {
    "up": {"block_0": [0.0, 1.0, 0.0]},
}
pipeline.set_ip_adapter_scale(scale)
```

目的：尽量让参考图贡献颜色、材质和氛围，而不是直接搬运布局/主体。

### 4.3 首轮固定生成参数（提案，尚未授权执行）

- width = 768
- height = 1024
- num_images_per_prompt = 1
- num_inference_steps = 30
- guidance_scale = 5
- seed = 42
- 同一路线始终保存原始 PNG
- 关闭任何 best-of-N 选择
- 第一轮不做后处理/Figma

参数一旦开始对照，中途不能为了“更好看”单边调整。

### 4.4 输出与 provenance

每次输出必须保存：
- 原始 PNG
- reference SHA-256
- prompt 原文和 SHA-256
- negative prompt
- base model ID/revision
- adapter ID/revision
- Diffusers/PyTorch/Transformers/Accelerate 版本
- seed
- width/height
- steps
- guidance scale
- IP-Adapter block-scale 配置
- 实际输出 SHA-256 与像素尺寸
- 启动时间、结束时间
- 是否发生 CPU offload / VAE tiling
- 错误与重试记录

不得只保存“最好的一张”。

## 5. 当前环境兼容性结论

### ChatGPT 当前执行容器

已实际只读检查：
- Python 3.13.5
- PyTorch 2.10.0+cpu
- CUDA available = false
- 没有 nvidia-smi
- 当前未安装 diffusers

结论：**不能作为本方案的实际 SDXL/IP-Adapter GPU 复现环境。**

### 用户现有本机

已知本机属于旧款低显存 Windows 设备。为避免把个人硬件细节写进公开仓库，本卡不记录具体型号。
结合 SDXL 体量与官方内存优化说明，当前本机不作为首轮正式复现目标。

结论：**需要另一个受控 GPU 执行环境，或者在用户明确批准后再选择云端 GPU。**
目前未选择供应商、未创建实例、未产生费用。

说明：官方 Diffusers 提供 model CPU offload、sequential CPU offload 与 VAE tiling；这些方法可以减少显存，但会增加系统内存占用/传输开销或显著变慢。它们不构成当前低配本机已经被证明可用。

## 6. 与现行路线怎么比较

不能把不同基座的结果硬解释为“InstantStyle 算法一定比 ChatGPT Image 好”。

首轮只回答业务问题：
1. 参考图风格是否比 Prompt Capsule 更稳定地保留下来；
2. 新内容是否减少参考主体/构图的内容泄漏；
3. 摄影可信度是否至少不劣；
4. 是否更容易稳定控制画幅和单张输出；
5. 操作成本是否可接受。

现行成果全部保留为 baseline；新方案没有通过同条件人工比较前，不替换任何旧模块。

## 7. 有界测试预算

当前授权：
- 新生成图片：0
- 训练：0
- 付费 GPU：0
- Figma 写入：0

下一阶段预算提案（尚未授权）：
1. 技术 smoke test：现行基线 1 张 + InstantStyle 1 张；
2. 若技术 smoke test 正确，再用 2 个新内容任务各做两路各 1 张；
3. 全部最多 6 张新输出；
4. 任何已经开始生成的技术失败也计入次数；
5. 不允许 hidden variants / best-of-N；
6. 每个错误只有在根因明确且有修复依据时才提出一次受控重试。

## 8. 失败即停止条件

以下任一发生，本候选暂停，不用更多图片“试到成功”：
- 无法证明只绑定指定参考图；
- 输出数量不是 1；
- width/height 未按冻结值执行；
- 内容明显复制参考主体或参考文案；
- 模型/adapter/encoder 版本无法固定；
- 环境 OOM 且一次官方 offload 方案仍不能稳定运行；
- 原始 PNG/provenance 不能完整保存；
- 单次兼容性补查后仍无法解释依赖冲突；
- 开始产生付费资源但事前没有用户明确授权。

## 9. 本卡结论

方法状态：**可落地，值得做首个无训练 baseline。**

环境状态：**当前不可执行。**
- ChatGPT 容器：CPU-only，无 Diffusers/CUDA。
- 现有本机：不作为 SDXL + InstantStyle 的正式首轮复现目标。
- 缺失：一个可控、可记录版本、能运行 SDXL + IP-Adapter 的 GPU 环境。

因此当前不能直接跳到“生成两张看看”。

下一步只能是：
**选择并核验一个 GPU 执行环境，记录 GPU/显存、系统内存、CUDA/PyTorch、磁盘、模型下载和输出回传路径；在费用为 0 或获得用户明确付费授权前，不启动生成。**

## 10. 不影响旧成果

本卡不修改：
- Style Capsule V1.1 Candidate
- H1-H4 frozen payload
- Attempt 1-4 历史身份/结论
- 茶作 197:2 / 201:2 / 205:2
- 已认可字标/版式
- Figma 上传 relay
- Visual Master Freeze Guard

新方案只能作为独立候选进入后续有界对照。
