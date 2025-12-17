# 常用模式总结

## 模型加载模式
```python
# 统一加载入口
model = VoxCPM.from_pretrained("openbmb/VoxCPM1.5")

# 支持本地路径或 HuggingFace 仓库
# 自动下载和缓存
# 返回可直接使用的模型实例
```

## 生成模式

### 非流式生成
```python
wav = model.generate(
    text="...",
    prompt_wav_path=None,  # 可选音色参考
    prompt_text=None,      # 可选参考文本
    cfg_value=2.0,         # 引导强度
    inference_timesteps=10, # 推理步数
    normalize=False,       # 文本规范化
    denoise=False,         # 降噪
    retry_badcase=True,    # 自动重试
)
```

### 流式生成
```python
chunks = []
for chunk in model.generate_streaming(text="...", ...):
    chunks.append(chunk)
wav = np.concatenate(chunks)
```

## 配置模式
```yaml
# conf/voxcpm_v1.5/voxcpm_finetune_lora.yaml
model_path: "openbmb/VoxCPM1.5"
lora:
  rank: 8
  alpha: 16
  target_modules: ["q_proj", "v_proj"]
training:
  batch_size: 4
  learning_rate: 1e-4
  num_epochs: 10
```

## 微调数据模式
```python
# training/data.py
# 数据集应返回:
# - text: 文本
# - audio: 音频波形
# - sample_rate: 采样率
```

## CLI 模式
```bash
# 直接合成
voxcpm --text "..." --output out.wav

# 语音克隆
voxcpm --text "..." \
  --prompt-audio voice.wav \
  --prompt-text "..." \
  --output out.wav

# 批处理
voxcpm --input texts.txt --output-dir outs
```

## Web UI 模式
```python
# app.py - Gradio 界面
# 1. 语音克隆: 上传参考音频 + 输入文本
# 2. 语音创作: 仅输入文本

# lora_ft_webui.py - LoRA 微调界面
# 1. 配置数据集
# 2. 设置 LoRA 参数
# 3. 启动训练
# 4. 测试推理
```

## 重试模式
```python
# 检测生成失败 (长度比例异常)
if len(wav) / len(text) > retry_badcase_ratio_threshold:
    # 自动重试,最多 retry_badcase_max_times 次
    # 针对无法停止生成的 bad case
```

## 常见组合

### 高质量生成
```python
wav = model.generate(
    text="...",
    cfg_value=2.5,           # 更高引导
    inference_timesteps=20,  # 更多步数
    denoise=True,            # 开启降噪
)
```

### 快速生成
```python
wav = model.generate(
    text="...",
    cfg_value=1.5,           # 较低引导
    inference_timesteps=5,   # 较少步数
)
```

### 语音克隆
```python
wav = model.generate(
    text="...",
    prompt_wav_path="reference.wav",
    prompt_text="reference text",
    cfg_value=2.0,
)
```
