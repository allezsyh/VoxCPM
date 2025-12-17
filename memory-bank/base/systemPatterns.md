# 系统架构与模式

## 目录结构
```
VoxCPM/
├── src/voxcpm/              # 核心库
│   ├── model/               # 模型定义
│   ├── modules/             # 模块组件
│   │   ├── audiovae/        # 音频 VAE
│   │   ├── locenc/          # 局部编码器
│   │   ├── locdit/          # 局部 DiT
│   │   ├── minicpm4/        # MiniCPM-4 主干
│   │   └── layers/          # 自定义层 (LoRA, FSQ)
│   ├── training/            # 训练框架
│   ├── utils/               # 工具函数
│   ├── core.py              # 核心 API
│   └── cli.py               # 命令行接口
├── scripts/                 # 训练脚本
├── conf/                    # 配置文件
├── app.py                   # Gradio Web UI
├── lora_ft_webui.py         # LoRA 微调 Web UI
└── docs/                    # 文档
```

## 核心设计模式

### 1. 端到端连续语音建模
- **无需离散化**: 直接在连续空间建模语音,避免 tokenization 损失
- **分层语言建模**: 通过 FSQ 约束实现语义-声学隐式解耦
- **扩散自回归**: DiTAR 架构融合扩散模型与自回归生成

### 2. 模块化组件
- **AudioVAE**: 音频压缩/重建 (44.1kHz → 6.25Hz latent)
- **MiniCPM-4**: 自回归生成 latent 序列
- **LocDiT**: Flow Matching 精炼局部细节
- **LocEnc**: 提取音色 timbre embedding

### 3. 训练与推理分离
- 训练: `src/voxcpm/training/` 模块化数据加载、打包、加速
- 推理: `src/voxcpm/core.py` 提供统一 API
- CLI/Web: 多种交互方式

### 4. 微调支持
- **全参数微调**: 完全训练所有权重
- **LoRA 微调**: 低秩适应高效训练
- 配置驱动: YAML 配置文件定义训练策略

## 关键技术点

### 语音生成流程
1. 文本输入 → MiniCPM-4 自回归生成 latent 序列
2. Latent + Timbre Embedding → LocDiT 精炼
3. AudioVAE 解码 → 连续波形输出

### 语音克隆
1. 参考音频 → AudioVAE 编码 → LocEnc 提取 timbre
2. Timbre 注入生成过程 → 复制音色、节奏、情感

### 流式生成
- Chunk-based 增量输出
- 低延迟 RTF ~0.15-0.17

## 代码约定
- 模块独立: 各组件可独立加载/替换
- 配置驱动: 使用 YAML/dataclass 管理参数
- 类型提示: 使用 Python type hints
- 错误处理: 快速失败,明确错误信息
