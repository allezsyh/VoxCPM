# VoxCPM 快速开始

## 📦 模型准备

### 选项 1: 使用已复制的本地模型
```bash
# 模型已在: models/VoxCPM1.5/ (1.9 GB)
python demo/0_local_model_example.py
```

### 选项 2: 重新下载模型
```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="openbmb/VoxCPM1.5",
    local_dir="./models/VoxCPM1.5",
    local_dir_use_symlinks=False
)
```

### 选项 3: 使用 HuggingFace 缓存
```python
from voxcpm import VoxCPM

# 会自动从 Hub 下载到缓存
model = VoxCPM.from_pretrained("openbmb/VoxCPM1.5")
```

---

## 🚀 运行示例

### 基础 TTS (最简单)
```bash
python demo/1_basic_tts.py
```

### 语音克隆
```bash
python demo/2_voice_cloning.py
```

### 流式生成
```bash
python demo/3_streaming_tts.py
```

### 批量合成
```bash
python demo/4_batch_synthesis.py
```

### LoRA 推理
```bash
python demo/5_lora_inference.py
```

### 参数调优
```bash
python demo/6_parameter_tuning.py
```

---

## 💻 代码示例

### 基础使用
```python
import soundfile as sf
from voxcpm import VoxCPM

# 加载模型(自动检测本地或 Hub)
model = VoxCPM.from_pretrained("openbmb/VoxCPM1.5")

# 生成语音
wav = model.generate(
    text="你好,这是 VoxCPM 语音合成示例。",
    cfg_value=2.0,
    inference_timesteps=10
)

# 保存
sf.write("output.wav", wav, model.tts_model.sample_rate)
```

### 使用本地模型
```python
from voxcpm import VoxCPM

# 方式 1: 直接指定路径
model = VoxCPM(voxcpm_model_path="models/VoxCPM1.5")

# 方式 2: 使用配置(自动检测)
from demo.config import get_model_path
model = VoxCPM(voxcpm_model_path=get_model_path())
```

### 语音克隆
```python
wav = model.generate(
    text="目标文本内容",
    prompt_wav_path="reference.wav",  # 参考音频
    prompt_text="参考音频的文本",      # 参考文本
    cfg_value=2.0,
    inference_timesteps=10
)
```

---

## 🛠️ 常用命令

### 检查环境
```bash
python demo/test_imports.py
```

### 语法检查
```bash
python demo/quick_test.py
```

### 查看模型信息
```bash
ls -lh models/VoxCPM1.5/
du -sh models/VoxCPM1.5/
```

---

## 🔧 配置调优

### 快速模式 (低延迟)
```python
wav = model.generate(
    text="...",
    cfg_value=1.5,
    inference_timesteps=5
)
```

### 高质量模式
```python
wav = model.generate(
    text="...",
    cfg_value=2.5,
    inference_timesteps=20
)
```

### 标准模式 (推荐)
```python
wav = model.generate(
    text="...",
    cfg_value=2.0,
    inference_timesteps=10
)
```

---

## 📚 更多信息

- **详细文档**: [demo/README.md](demo/README.md)
- **项目主页**: https://github.com/OpenBMB/VoxCPM
- **技术报告**: https://arxiv.org/abs/2509.24650
- **在线演示**: https://huggingface.co/spaces/OpenBMB/VoxCPM-Demo

---

## ⚡ 常见问题

### Q: 首次运行很慢?
A: 首次运行会进行模型编译优化,后续会快很多。

### Q: 生成的语音不稳定?
A: 尝试:
- 开启 `retry_badcase=True`
- 调高 CFG 值 (2.5-3.0)
- 增加推理步数 (15-20)

### Q: 如何节省磁盘空间?
A: 删除缓存:
```bash
rm -rf ~/.cache/huggingface/hub/models--openbmb--VoxCPM1.5
```

### Q: 如何使用 GPU?
A: 自动检测,确保已安装 CUDA 和 PyTorch GPU 版本。

---

## 🎯 下一步

1. ✅ 运行基础示例熟悉功能
2. ✅ 尝试语音克隆
3. ✅ 调整参数找到最佳配置
4. ✅ 使用 LoRA 微调训练个性化模型
5. ✅ 集成到自己的项目中
