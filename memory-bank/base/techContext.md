# 技术栈

## 核心框架
- **Python**: >=3.10
- **PyTorch**: >=2.5.0
- **TorchAudio**: >=2.5.0
- **Transformers**: >=4.36.2

## 关键依赖
- einops - 张量操作
- gradio - Web UI
- modelscope - 模型管理
- datasets - 数据加载
- huggingface-hub - 模型托管
- soundfile - 音频 I/O
- funasr - 语音识别
- argbind - CLI 参数绑定
- safetensors - 模型权重

## 架构组件
- **MiniCPM-4**: 语言模型主干 (0.5B/800M 参数)
- **AudioVAE**: 音频编解码器 (基于 DAC)
- **LocDiT**: 局部扩散 Transformer (Flow Matching)
- **LocEnc**: 局部编码器
- **FSQ**: 有限标量量化层

## 模型版本
- **VoxCPM1.5** (最新): 800M 参数, 44.1kHz 采样率, 6.25Hz token 率
- **VoxCPM-0.5B**: 640M 参数, 16kHz 采样率, 12.5Hz token 率

## 训练特性
- 支持全参数微调 (SFT)
- 支持 LoRA 高效微调
- 分布式训练支持
