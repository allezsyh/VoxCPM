#!/usr/bin/env python3
"""
LoRA 微调模型推理示例

功能:
- 加载基础模型 + LoRA 权重
- 使用微调后的模型生成语音
- 支持热加载和切换 LoRA

运行方式:
    python demo/5_lora_inference.py

前提条件:
    - 已训练好的 LoRA 权重 (例如 lora/checkpoint/lora_weights.safetensors)
"""

import soundfile as sf
from pathlib import Path
from voxcpm import VoxCPM
from voxcpm.model.voxcpm import LoRAConfig

# 导入配置
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import get_model_path


def main():
    print("=== VoxCPM LoRA 推理示例 ===\n")

    # 1. 配置 LoRA
    lora_path = "lora/checkpoint"  # 修改为你的 LoRA 路径

    # 检查 LoRA 是否存在
    if not Path(lora_path).exists():
        print(f"警告: LoRA 路径不存在: {lora_path}")
        print("将使用基础模型进行演示\n")
        lora_path = None

    # 2. 创建 LoRA 配置
    lora_config = None
    lora_weights_path = None

    if lora_path:
        lora_config = LoRAConfig(
            enable_lm=True,     # 在 LM 层启用 LoRA
            enable_dit=True,    # 在 DiT 层启用 LoRA
            enable_proj=False,  # 投影层通常不需要
            r=32,               # LoRA rank
            alpha=16,           # LoRA alpha 缩放
            dropout=0.0,        # Dropout 率
        )
        lora_weights_path = lora_path
        print(f"LoRA 配置: r={lora_config.r}, alpha={lora_config.alpha}")
        print(f"LoRA 路径: {lora_weights_path}\n")

    # 3. 加载模型(优先使用本地模型)
    print("正在加载模型...")
    model = VoxCPM(
        voxcpm_model_path=get_model_path(),
        enable_denoiser=False,
        lora_config=lora_config,
        lora_weights_path=lora_weights_path,
    )
    print("模型加载完成!\n")

    # 4. 准备文本
    text = "这是使用 LoRA 微调模型生成的语音示例。"
    print(f"输入文本: {text}\n")

    # 5. 生成语音
    print("正在生成语音...")
    wav = model.generate(
        text=text,
        prompt_wav_path=None,
        prompt_text=None,
        cfg_value=2.0,
        inference_timesteps=10,
        normalize=False,
        denoise=False,
    )

    # 6. 保存音频
    output_path = "demo/output_lora_inference.wav"
    sf.write(output_path, wav, model.tts_model.sample_rate)

    # 7. 显示信息
    duration = len(wav) / model.tts_model.sample_rate
    print(f"✓ 生成完成!")
    print(f"  输出文件: {output_path}")
    print(f"  采样率: {model.tts_model.sample_rate} Hz")
    print(f"  时长: {duration:.2f} 秒")

    # 8. 演示热加载 LoRA (可选)
    if lora_path and Path(lora_path).exists():
        print("\n=== 演示 LoRA 热加载 ===")

        # 禁用 LoRA
        model.set_lora_enabled(False)
        print("已禁用 LoRA,使用基础模型")

        # 重新启用 LoRA
        model.set_lora_enabled(True)
        print("已重新启用 LoRA")

        # 加载另一个 LoRA (如果有的话)
        # model.load_lora("lora/another_checkpoint")


if __name__ == "__main__":
    """
    示例中使用的可执行入口点
    """
    main()
