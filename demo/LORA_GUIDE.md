# LoRA 训练与推理指南

本指南介绍如何使用 LoRA (Low-Rank Adaptation) 对 VoxCPM 模型进行微调,以实现定制化语音合成。

---

## 📚 目录

1. [什么是 LoRA?](#什么是-lora)
2. [快速开始](#快速开始)
3. [数据准备](#数据准备)
4. [训练方法](#训练方法)
5. [推理使用](#推理使用)
6. [常见问题](#常见问题)

---

## 什么是 LoRA?

### 核心概念

**LoRA (Low-Rank Adaptation)** 是一种参数高效的模型微调技术:

```
基础模型 (VoxCPM1.5)  +  LoRA 权重  =  定制化模型
    800M 参数               10-50MB        个性化语音
  (保持冻结)              (仅训练这部分)   (音色/风格定制)
```

### 优势对比

| 对比项 | 全量微调 | LoRA 微调 |
|--------|---------|----------|
| 训练参数量 | 800M (100%) | ~10M (1-2%) |
| 存储空间 | ~2GB | ~50MB |
| 训练时间 | 数天 | 数小时 |
| GPU 内存 | 24GB+ | 16GB 可训练 |
| 灵活性 | 一个模型 | 多个 LoRA 可切换 |

### 应用场景

- 🎭 **定制音色**: 克隆特定人物语音
- 🗣️ **方言口音**: 适配地区口音(如粤语、四川话)
- 🎨 **风格调整**: 调整语速、语调、情感
- 📚 **专业领域**: 优化专业术语发音
- 🎮 **游戏角色**: 为角色定制独特语音

---

## 快速开始

### 方法 1: WebUI 训练 (推荐新手)

```bash
# 1. 启动 WebUI
python lora_ft_webui.py

# 2. 打开浏览器
http://localhost:7860

# 3. 在 Training 标签页配置并训练
# 4. 在 Inference 标签页测试生成
```

**WebUI 特点**:
- ✅ 图形化界面,易于使用
- ✅ 实时显示训练进度
- ✅ 自动参数验证
- ✅ 集成推理测试

### 方法 2: 命令行训练 (推荐高级用户)

```bash
# 1. 准备配置文件
cp conf/voxcpm_v1.5/voxcpm_finetune_lora.yaml my_lora_config.yaml

# 2. 编辑配置
vim my_lora_config.yaml

# 3. 开始训练
python scripts/train_voxcpm_finetune.py --args my_lora_config.yaml
```

---

## 数据准备

### 数据格式

**JSONL 格式** (每行一个 JSON 对象):

```jsonl
{"audio": "speaker1/001.wav", "text": "这是第一句话。"}
{"audio": "speaker1/002.wav", "text": "这是第二句话。"}
{"audio": "speaker1/003.wav", "text": "这是第三句话。"}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `audio` | string | ✅ | 音频文件路径(相对或绝对) |
| `text` | string | ✅ | 音频对应的文本转写 |
| `duration` | float | ❌ | 音频时长(秒),可加速采样 |
| `dataset_id` | int | ❌ | 数据集 ID,用于多数据集训练 |

### 数据要求

**音频质量**:
- 格式: WAV, MP3, FLAC 等
- 采样率: 44.1kHz (VoxCPM1.5) 或 16kHz (VoxCPM-0.5B)
- 音质: 清晰、无噪音、无混响
- 时长: 每条 2-15 秒为宜

**数据量**:
- 最少: 10-20 条 (可尝试,效果有限)
- 推荐: 100-500 条 (效果较好)
- 最佳: 1000+ 条 (专业质量)

**数据多样性**:
- ✅ 覆盖不同句子类型(陈述、疑问、感叹)
- ✅ 包含常见词汇和专业术语
- ✅ 多种语调和情感表达

### 数据准备示例

```bash
# 1. 创建数据目录
mkdir -p data/my_speaker

# 2. 准备音频文件
data/my_speaker/
├── 001.wav
├── 002.wav
├── 003.wav
└── ...

# 3. 创建 manifest 文件
cat > data/my_speaker/train.jsonl << 'EOF'
{"audio": "data/my_speaker/001.wav", "text": "第一句话内容", "duration": 3.5}
{"audio": "data/my_speaker/002.wav", "text": "第二句话内容", "duration": 4.2}
{"audio": "data/my_speaker/003.wav", "text": "第三句话内容", "duration": 3.8}
EOF

# 4. (可选) 创建验证集
head -n 10 data/my_speaker/train.jsonl > data/my_speaker/val.jsonl
tail -n +11 data/my_speaker/train.jsonl > data/my_speaker/train_subset.jsonl
mv data/my_speaker/train_subset.jsonl data/my_speaker/train.jsonl
```

---

## 训练方法

### 使用 WebUI 训练

#### 步骤 1: 启动 WebUI

```bash
python lora_ft_webui.py
```

访问: http://localhost:7860

#### 步骤 2: 配置训练参数

在 **Training** 标签页:

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| Pretrained Model Path | `models/VoxCPM1.5` | 基础模型路径 |
| Train Manifest | `data/train.jsonl` | 训练数据 |
| Val Manifest | `data/val.jsonl` | 验证数据(可选) |
| Learning Rate | `0.0001` | 学习率 |
| Max Iterations | `2000` | 训练步数 |
| Batch Size | `16` | 批次大小(根据 GPU 调整) |
| LoRA Rank | `32` | LoRA 秩(越大越强,但占用更多内存) |
| LoRA Alpha | `16` | 缩放因子 |
| Save Interval | `1000` | 每 N 步保存一次 |

#### 步骤 3: 开始训练

1. 点击 **Start Training**
2. 在 **Training Logs** 查看进度
3. 训练完成后,LoRA 权重保存在 `lora/` 目录

#### 步骤 4: 测试推理

在 **Inference** 标签页:

1. 加载训练好的 LoRA checkpoint
2. 输入测试文本
3. 点击 **Generate** 生成语音
4. 下载或播放生成的音频

---

### 使用命令行训练

#### 步骤 1: 准备配置文件

复制并编辑配置模板:

```bash
cp conf/voxcpm_v1.5/voxcpm_finetune_lora.yaml my_lora_config.yaml
```

编辑 `my_lora_config.yaml`:

```yaml
# 模型和数据路径
pretrained_path: models/VoxCPM1.5/
train_manifest: data/my_speaker/train.jsonl
val_manifest: data/my_speaker/val.jsonl

# 音频参数
sample_rate: 44100

# 训练参数
batch_size: 16                # 根据 GPU 内存调整
grad_accum_steps: 1           # 梯度累积步数
num_iters: 2000               # 训练迭代次数
learning_rate: 0.0001         # 学习率
warmup_steps: 100             # 预热步数

# 日志和保存
log_interval: 10              # 每 N 步记录一次日志
save_interval: 1000           # 每 N 步保存一次 checkpoint
save_path: lora/my_speaker    # 保存路径
tensorboard: logs/my_speaker  # TensorBoard 日志

# LoRA 配置
lora:
  enable_lm: true             # 在语言模型层启用
  enable_dit: true            # 在扩散模型层启用
  enable_proj: false          # 投影层通常不需要
  r: 32                       # LoRA rank
  alpha: 16                   # LoRA alpha
  dropout: 0.0                # Dropout 率
```

#### 步骤 2: 开始训练

```bash
# 基础训练
python scripts/train_voxcpm_finetune.py --args my_lora_config.yaml

# 使用多 GPU (DDP)
CUDA_VISIBLE_DEVICES=0,1 python scripts/train_voxcpm_finetune.py \
    --args my_lora_config.yaml

# 从 checkpoint 恢复训练
python scripts/train_voxcpm_finetune.py \
    --args my_lora_config.yaml \
    --resume lora/my_speaker/checkpoint_1000
```

#### 步骤 3: 监控训练

```bash
# 查看 TensorBoard
tensorboard --logdir logs/my_speaker

# 查看保存的 checkpoint
ls -lh lora/my_speaker/
# checkpoint_1000/
# checkpoint_2000/
# ...
```

#### 步骤 4: 训练参数调优

| 参数 | 调小 | 调大 |
|------|------|------|
| `batch_size` | 减少内存占用 | 加快训练,更稳定 |
| `learning_rate` | 更稳定,防止过拟合 | 更快收敛 |
| `lora.r` | 减少参数量 | 更强表达能力 |
| `num_iters` | 更快完成 | 更好效果 |

---

## 推理使用

### 方法 1: 使用 demo 脚本

```bash
# 1. 确保 LoRA 权重已训练并保存
ls lora/my_speaker/checkpoint_2000/

# 2. 编辑 demo/5_lora_inference.py
vim demo/5_lora_inference.py

# 修改 lora_path
lora_path = "lora/my_speaker/checkpoint_2000"

# 3. 运行推理
python demo/5_lora_inference.py
```

### 方法 2: 使用 WebUI

1. 启动 WebUI: `python lora_ft_webui.py`
2. 切换到 **Inference** 标签
3. 加载 LoRA checkpoint
4. 输入文本并生成

### 方法 3: 使用 Python API

```python
import soundfile as sf
from voxcpm import VoxCPM
from voxcpm.model.voxcpm import LoRAConfig

# 1. 配置 LoRA
lora_config = LoRAConfig(
    enable_lm=True,
    enable_dit=True,
    r=32,
    alpha=16,
)

# 2. 加载模型 + LoRA
model = VoxCPM(
    voxcpm_model_path="models/VoxCPM1.5",
    lora_config=lora_config,
    lora_weights_path="lora/my_speaker/checkpoint_2000"
)

# 3. 生成语音
wav = model.generate(
    text="使用 LoRA 微调后的模型生成的语音。",
    cfg_value=2.0,
    inference_timesteps=10,
)

# 4. 保存
sf.write("output_lora.wav", wav, model.tts_model.sample_rate)
```

### LoRA 热切换

```python
# 加载 LoRA
model.load_lora("lora/my_speaker/checkpoint_2000")
wav1 = model.generate(text="使用 LoRA A")

# 切换到另一个 LoRA
model.load_lora("lora/another_speaker/checkpoint_1000")
wav2 = model.generate(text="使用 LoRA B")

# 禁用 LoRA (使用基础模型)
model.set_lora_enabled(False)
wav3 = model.generate(text="使用基础模型")

# 重新启用
model.set_lora_enabled(True)
```

---

## 常见问题

### Q1: 需要多少训练数据?

**A**: 取决于目标质量:
- **10-20 条**: 可尝试,效果有限
- **100-500 条**: 推荐,效果较好
- **1000+ 条**: 专业级质量

数据质量比数量更重要!

---

### Q2: 训练需要多长时间?

**A**: 取决于数据量和 GPU:

| 数据量 | GPU | 训练时间 (2000 步) |
|--------|-----|-------------------|
| 100 条 | RTX 4090 | ~30 分钟 |
| 500 条 | RTX 4090 | ~2 小时 |
| 1000 条 | RTX 4090 | ~4 小时 |
| 100 条 | RTX 3090 | ~1 小时 |

---

### Q3: 训练失败怎么办?

**A**: 常见问题和解决方案:

1. **OOM (内存不足)**
   - 减小 `batch_size` (如 16 -> 8 -> 4)
   - 减小 `max_batch_tokens`
   - 使用梯度累积 `grad_accum_steps: 2`

2. **损失不收敛**
   - 降低 `learning_rate` (如 1e-4 -> 5e-5)
   - 增加 `warmup_steps`
   - 检查数据质量

3. **音频质量差**
   - 检查原始音频质量
   - 确保文本转写准确
   - 增加训练数据
   - 调高 `num_iters`

---

### Q4: 如何评估训练效果?

**A**: 评估方法:

1. **查看 TensorBoard**
   ```bash
   tensorboard --logdir logs/
   ```
   - 观察 `loss/diff` 和 `loss/stop` 曲线
   - 损失应该持续下降

2. **定期测试生成**
   - 每 1000 步生成测试样本
   - 主观评估音质和相似度

3. **对比基础模型**
   - 使用相同文本对比 LoRA 和基础模型
   - 评估定制化程度

---

### Q5: LoRA 权重能共享吗?

**A**: 可以!

**共享方式**:
```bash
# 压缩 LoRA checkpoint
tar -czf my_lora.tar.gz lora/my_speaker/checkpoint_2000/

# 分享给其他人
# 接收方解压后即可使用:
tar -xzf my_lora.tar.gz -C lora/
python demo/5_lora_inference.py
```

**注意事项**:
- ✅ LoRA 权重很小(~50MB),易于分享
- ✅ 不需要分享基础模型(接收方自己下载)
- ⚠️ 确保接收方使用相同版本的基础模型

---

### Q6: 如何选择 LoRA 参数?

**A**: 参数选择指南:

| 参数 | 小值(省内存) | 中值(推荐) | 大值(高表达) |
|------|------------|-----------|------------|
| `r` | 8 | 32 | 64 |
| `alpha` | 8 | 16 | 32 |

**经验法则**:
- `r=32, alpha=16` 适合大多数场景
- 数据少时用小 `r` (防止过拟合)
- 数据多时用大 `r` (更强表达)
- 通常 `alpha = r / 2`

---

## 相关资源

- **完整文档**: [docs/finetune.md](../docs/finetune.md)
- **配置模板**: [conf/voxcpm_v1.5/voxcpm_finetune_lora.yaml](../conf/voxcpm_v1.5/voxcpm_finetune_lora.yaml)
- **训练脚本**: [scripts/train_voxcpm_finetune.py](../scripts/train_voxcpm_finetune.py)
- **WebUI**: [lora_ft_webui.py](../lora_ft_webui.py)
- **推理示例**: [demo/5_lora_inference.py](5_lora_inference.py)

---

## 故障排除

遇到问题? 检查以下几点:

1. ✅ 确认 VoxCPM 已正确安装: `pip list | grep voxcpm`
2. ✅ 确认 GPU 可用: `python -c "import torch; print(torch.cuda.is_available())"`
3. ✅ 确认数据格式正确: 检查 manifest 文件
4. ✅ 确认配置路径正确: 使用绝对路径
5. ✅ 查看日志输出: 寻找错误信息

**获取帮助**:
- GitHub Issues: https://github.com/OpenBMB/VoxCPM/issues
- 项目文档: [docs/](../docs/)

---

祝训练顺利! 🎉
