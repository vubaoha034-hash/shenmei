# GPU 执行环境选择与核验卡｜首个免训练候选

日期：2026-09-21
项目：visual-aesthetic-vpd
状态：ENVIRONMENT_SELECTED_NOT_PROVISIONED
授权边界：只读审计；未授权付费实例、出图、训练或 Figma 写入。

## 1. 当前候选

视觉方法：
- SDXL
- Hugging Face Diffusers 原生 IP-Adapter
- InstantStyle style-only block 注入
- 单参考图
- 无训练

对应可复现卡：
`evidence/vpd/mature_workflow_audit_v1/INSTANTSTYLE_IPADAPTER_REPRODUCIBILITY_CARD_20260921.md`

## 2. 环境筛选结论

### 首选
**RunPod Secure Cloud，单卡 NVIDIA A40 48GB。**

选择理由：
1. 48GB VRAM，明显高于首轮 24GB 方案，足以把 SDXL、IP-Adapter 和图像编码器留在 GPU 侧，减少为了省显存引入 CPU offload 变量。
2. RunPod 当前 Secure Cloud A40 标价为 $0.49/GPU-hour；同页 RTX 4090 24GB 为 $0.74/hour。对本实验，显存余量比峰值推理速度更重要。
3. RunPod 提供官方 PyTorch 2.8 / Python 3.11 / CUDA 12.8.1 模板：
   `runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu`
4. Pod 可通过 SSH、Web terminal/Jupyter 操作；CLI 可显式指定 GPU、磁盘、端口、CUDA 最低版本以及 stop/terminate 时间。
5. Secure Cloud 支持独立 network volume；若后续需要持久模型缓存，可在不同 Pod 之间复用。
6. Pod 计费按实际运行时长；首轮可设置自动终止，避免忘记关机造成成本漂移。

上游资料：
- https://www.runpod.io/pricing
- https://docs.runpod.io/
- https://docs.runpod.io/runpodctl/reference/runpodctl-remove-pods
- https://www.runpod.io/articles/guides/pytorch-2-8-cuda-12-8
- https://docs.runpod.io/pods/troubleshooting/zero-gpus

### 备选一：RunPod Secure Cloud RTX A6000 48GB
- 当前标价约 $0.53/hour。
- 同为 48GB VRAM。
- 仅在 A40 无可用库存或模板兼容性异常时作为同平台替代。
- 不允许因为“更快/更新”随意切换。

### 备选二：Vast.ai verified RTX 4090
- 当前公开市场可见较低报价，价格随市场与主机变化。
- 提供 SSH/Jupyter，部分 verified 主机可靠性较高。
- 但主机硬件、CUDA、磁盘、带宽和价格是 marketplace 级动态变量。
- 首轮目标是“可重复”，所以不优先使用。

资料：
- https://vast.ai/article/how-much-does-it-cost-to-rent-a-gpu-in-the-cloud-live-pricing-guide
- https://console.vast.ai/faq/

### 备选三：Lambda Cloud RTX A6000 48GB
- 当前公开价格约 $1.09/hour。
- 环境更标准化，PyTorch/CUDA 预装。
- 成本高于 RunPod A40，首轮没有充分理由支付额外费用。

资料：
- https://lambda.ai/pricing
- https://lambda.ai/instances

## 3. 首轮拟固定硬件/系统

在真正创建实例前冻结：

- Provider: RunPod
- Cloud tier: Secure Cloud
- GPU: 1 × NVIDIA A40
- VRAM: 48GB
- GPU count: 1
- System RAM: 以实际 Pod 分配结果记录；当前价格页示例约 50GB
- vCPU: 以实际 Pod 分配结果记录；当前价格页示例约 9 vCPU
- OS/container: Ubuntu-based official RunPod PyTorch image
- Python: 3.11
- CUDA runtime: 12.8.1
- PyTorch base: 2.8.0
- Container image:
  `runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu`

GPU/CPU/RAM 以实例启动后的 `nvidia-smi`、`lscpu`、`free -h` 实际回读为准；价格页仅作预选依据，不能冒充运行时证据。

## 4. 首轮磁盘策略

### Smoke test
第一轮不创建长期 network volume，避免在测试尚未证明有价值时产生持续存储成本。

建议：
- Container/volume 工作空间：至少 60GB，建议 80GB。
- 模型缓存：`/workspace/hf-cache`
- 代码：`/workspace/vpd-repro`
- 原始输入：`/workspace/input`
- 原始输出：`/workspace/output`
- provenance：`/workspace/provenance`

理由：
- SDXL base 单主权重约 6.94GB；
- IP-Adapter SDXL adapter 约 703MB；
- SDXL image encoder 约 3.69GB；
- 还存在文本编码器、VAE、配置、tokenizer、pip wheel/cache 等额外占用。
60–80GB 可减少首次 smoke test 因磁盘不足引入新的技术失败。

如果首轮证明方案有价值，再考虑 network volume。当前标准 network storage under 1TB 标价为 $0.07/GB/month；不提前建立。

## 5. 连接和文件进出

### 进入 Pod
优先：
1. RunPod Web terminal / Jupyter；
2. SSH；
3. runpodctl 作为后续自动化。

### 输入
只允许上传：
- 一个已经批准并有 SHA-256 的视觉参考；
- 固定的 inference script；
- 固定 prompt 输入；
- requirements/版本锁。

不得把茶作候选、旧失败输出或其它视觉参考顺手放进同一 reference 输入目录。

### 输出
Smoke test 必须在终止 Pod 前把以下内容导出到受控持久位置：
- 原始 PNG
- metadata/provenance JSON
- `pip freeze`
- `nvidia-smi`
- Python/PyTorch/CUDA/Diffusers/Transformers/Accelerate 版本
- 运行日志

首轮允许通过 Jupyter/browser 直接下载；自动回传到 Drive 的方案只有在 smoke test 通过后再做，不为了一张测试图先建立 OAuth/密钥链。

## 6. 实例启动后的零图预检

即使未来获得付费授权，也不能启动后直接生成。

必须先只运行：
```bash
nvidia-smi
python --version
python - <<'PY'
import torch
print(torch.__version__)
print(torch.version.cuda)
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)
print(torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else None)
PY
df -h
free -h
```

之后安装/冻结：
- diffusers
- transformers
- accelerate
- safetensors
- huggingface_hub
- pillow

记录 `pip freeze`。

然后只下载模型并完成“加载测试”，不生成图片：
1. SDXL pipeline 能加载；
2. image encoder 能加载；
3. IP-Adapter 能加载；
4. style-only scale 能设置；
5. reference image 能读取并 SHA-256 一致；
6. 目标 768×1024 参数能进入 pipeline 调用对象。

任何一步失败，先停止并记录，不进入图像生成。

## 7. 成本边界提案（尚未授权）

当前真实授权仍为：
- Paid GPU spend: $0
- Image generation: 0
- Training: 0

若用户后续明确批准首轮 smoke test，提议硬上限：
- Provider/GPU：RunPod Secure A40 48GB
- 自动终止：2 小时
- 当前 compute 标价：$0.49/hour
- 理论 2h compute 上限：$0.98（不含税/存储等附加项）
- 为价格与少量存储波动预留的**总付费授权上限建议：$2**

超过 $2 或需要延长超过 2 小时，必须再次请求用户批准。

## 8. 为什么不选 4090 作为第一台

RTX 4090 的推理速度更高，但首轮目标不是追求吞吐，而是排除环境变量：
- 24GB VRAM 会更容易逼迫 offload/省显存策略；
- A40 有 48GB VRAM；
- RunPod 当前 Secure Cloud A40 价格反而低于 4090。

因此首轮以 A40 的“简单、余量大、便宜”为优先。

如果后续证明 A40 运行速度对批量生产成为瓶颈，再单独比较 4090/L40S；不能在方法是否有效之前优化吞吐。

## 9. 安全与停止条件

- 未获得明确付费授权，不创建 GPU Pod。
- 不提交 RunPod API key、Hugging Face token、SSH private key 到 public repo。
- 若使用 Hugging Face 登录，只在实例 secret/env 中使用，不写入日志或 provenance。
- Pod 创建时设置自动终止。
- 任何 output 都先回传/校验，再终止实例。
- 若实例实际不是 A40 48GB、CUDA 不满足、torch.cuda=false、磁盘不足或官方模板版本与记录不符，停止，不生成。
- 若 A40 没库存，不能自动切到更贵 GPU；只能记录并选择已登记备选。

## 10. 当前结论

环境选择：**PASS_FOR_PREPARATION**
实际环境验证：**NOT_EXECUTED**
付费资源：**NOT_STARTED**
图片生成：**0**
训练：**0**

唯一下一步不是出图，而是：
**在保持 $0 支出的前提下，修复/核验项目 full-state validator 对当前 read-only audit 状态的兼容性；只有 validator 可通过，并且用户明确批准最多 $2 的 RunPod smoke-test 预算后，才允许真正创建 Pod。**
