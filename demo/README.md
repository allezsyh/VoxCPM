# VoxCPM 示例脚本

本目录包含 VoxCPM 各种功能的示例脚本,帮助快速上手和理解模型使用方法。

**✨ 所有示例默认使用本地模型 (`models/VoxCPM1.5/`),无需网络下载!**

## 📁 文件列表

### 0️⃣ 本地模型使用
**文件**: `0_local_model_example.py`

演示如何使用工程目录下的本地模型,避免从网络下载。

```bash
python demo/0_local_model_example.py
```

**特点**:
- 使用本地模型文件
- 完全离线可用
- 适合无网络环境

---

### 1️⃣ 基础 TTS 合成
**文件**: `1_basic_tts.py`

最简单的文本转语音示例,无需任何参考音频。

```bash
python demo/1_basic_tts.py
```

**特点**:
- 零样本语音生成
- 自动使用本地模型
- 适合快速测试和演示

---

### 2️⃣ 语音克隆
**文件**: `2_voice_cloning.py`

使用参考音频克隆目标音色,保留音色、节奏、情感等特征。

```bash
python demo/2_voice_cloning.py
```

**特点**:
- 高保真音色复刻
- 仅需 3-10 秒参考音频
- 支持跨语言克隆 (中英)

**前提条件**:
- 准备参考音频 (例如 `examples/example.wav`)
- 参考音频对应的文本转写

---

### 3️⃣ 流式 TTS
**文件**: `3_streaming_tts.py`

演示流式生成模式,逐块输出音频数据。

```bash
python demo/3_streaming_tts.py
```

**特点**:
- 低延迟实时生成
- 适合对话系统、直播等场景
- RTF (Real-Time Factor) ~0.15-0.17

---

### 4️⃣ 批量合成
**文件**: `4_batch_synthesis.py`

从文本文件批量读取并生成语音,适合大规模数据处理。

```bash
python demo/4_batch_synthesis.py
```

**特点**:
- 自动化批处理
- 错误容错处理
- 进度追踪和统计

**前提条件**:
- 准备文本文件 (默认 `examples/input.txt`,每行一条文本)

---

### 5️⃣ LoRA 推理
**文件**: `5_lora_inference.py`

使用 LoRA 微调后的模型进行推理。

```bash
python demo/5_lora_inference.py
```

**特点**:
- 支持加载 LoRA 权重
- 热加载/热切换 LoRA
- 演示微调模型效果

**前提条件**:
- 已训练的 LoRA 权重 (例如 `lora/checkpoint/lora_weights.safetensors`)

---

### 6️⃣ 参数调优
**文件**: `6_parameter_tuning.py`

对比不同参数配置对生成效果的影响。

```bash
python demo/6_parameter_tuning.py
```

**特点**:
- 生成多种参数配置的音频
- 直观对比质量与速度
- 帮助选择最佳参数

**输出**:
- 快速模式 (CFG=1.5, steps=5)
- 标准模式 (CFG=2.0, steps=10) ⭐ 推荐
- 高质量模式 (CFG=2.5, steps=20)
- 强引导模式 (CFG=3.0, steps=10)

---

## 🚀 快速开始

### 安装依赖
```bash
pip install voxcpm
```

### 运行所有示例
```bash
# 按顺序运行
for i in {1..6}; do
    python demo/${i}_*.py
done
```

---

## 📊 参数说明

### 常用参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text` | str | 必填 | 要合成的文本 |
| `prompt_wav_path` | str | None | 参考音频路径 (语音克隆) |
| `prompt_text` | str | None | 参考文本 (语音克隆) |
| `cfg_value` | float | 2.0 | CFG 引导系数 (1.0-3.0) |
| `inference_timesteps` | int | 10 | 推理步数 (4-30) |
| `normalize` | bool | False | 是否进行文本规范化 |
| `denoise` | bool | False | 是否对参考音频降噪 |
| `retry_badcase` | bool | True | 是否自动重试失败 case |

### 参数调优建议

#### CFG 值 (cfg_value)
- **1.0-1.5**: 更自由的生成,适合创意场景
- **2.0**: 推荐默认值,平衡质量与多样性
- **2.5-3.0**: 更强的文本引导,适合精确控制

#### 推理步数 (inference_timesteps)
- **4-5**: 快速模式,适合实时应用
- **10**: 标准模式,推荐日常使用
- **15-30**: 高质量模式,适合最终产品

---

## 🎯 典型使用场景

### 场景 1: 有声读物
```python
# 使用标准参数 + 批量处理
cfg_value=2.0
inference_timesteps=10
参考脚本: 4_batch_synthesis.py
```

### 场景 2: 语音助手
```python
# 使用流式生成 + 快速模式
cfg_value=1.5
inference_timesteps=5
参考脚本: 3_streaming_tts.py
```

### 场景 3: 虚拟主播/配音
```python
# 使用语音克隆 + 高质量模式
cfg_value=2.5
inference_timesteps=20
参考脚本: 2_voice_cloning.py
```

### 场景 4: 个性化语音定制
```python
# 使用 LoRA 微调 + 个性化数据集
参考脚本: 5_lora_inference.py
训练工具: lora_ft_webui.py
```

---

## 🛠️ 高级功能

### 热加载 LoRA
```python
model = VoxCPM.from_pretrained("openbmb/VoxCPM1.5", lora_config=lora_config)

# 加载 LoRA
model.load_lora("lora/checkpoint1")
model.set_lora_enabled(True)

# 切换 LoRA
model.load_lora("lora/checkpoint2")

# 禁用 LoRA (使用基础模型)
model.set_lora_enabled(False)
```

### 文本规范化
```python
# 启用外部文本规范化 (WeTextProcessing)
wav = model.generate(text="...", normalize=True)

# 禁用 (使用原生文本理解,支持音素输入)
wav = model.generate(text="{ni3}{hao3}", normalize=False)
```

### 参考音频降噪
```python
# 启用降噪 (使用 ZipEnhancer,限制采样率 16kHz)
wav = model.generate(
    text="...",
    prompt_wav_path="noisy.wav",
    prompt_text="...",
    denoise=True
)

# 禁用降噪 (保留原始信息,支持 44.1kHz)
denoise=False
```

---

## 📝 注意事项

1. **首次运行**会自动下载模型 (~2GB),需要稳定网络
2. **GPU 推荐**:单张 RTX 4090 可达 RTF ~0.15
3. **参考音频**:3-10 秒为宜,过长会影响生成速度
4. **文本长度**:建议单次不超过 200 字,过长可能不稳定
5. **LoRA 训练**:参考 `docs/finetune.md` 和 `lora_ft_webui.py`

---

## 🔗 相关资源

- **项目主页**: https://github.com/OpenBMB/VoxCPM
- **使用指南**: `docs/usage_guide.md`
- **微调指南**: `docs/finetune.md`
- **技术报告**: https://arxiv.org/abs/2509.24650
- **在线演示**: https://huggingface.co/spaces/OpenBMB/VoxCPM-Demo

---

## 💡 常见问题

### Q: 如何选择模型版本?
A:
- **VoxCPM1.5** (推荐): 800M 参数, 44.1kHz 采样率, 更高质量
- **VoxCPM-0.5B**: 640M 参数, 16kHz 采样率, 更快速度

### Q: 生成的语音不稳定怎么办?
A:
1. 开启 `retry_badcase=True`
2. 调高 CFG 值 (2.5-3.0)
3. 增加推理步数 (15-20)
4. 检查文本长度 (建议 <200 字)

### Q: 如何提高生成速度?
A:
1. 降低 CFG 值 (1.5-2.0)
2. 减少推理步数 (5-10)
3. 使用流式生成 (`generate_streaming`)
4. 使用更强的 GPU

### Q: 语音克隆效果不好?
A:
1. 使用 3-10 秒高质量参考音频
2. 确保参考文本准确
3. 参考音频音质清晰、无噪音
4. 尝试调整 CFG 值

---

## 📞 获取帮助

- **GitHub Issues**: https://github.com/OpenBMB/VoxCPM/issues
- **微信群**: 见项目 README
- **邮箱**: openbmb@gmail.com
