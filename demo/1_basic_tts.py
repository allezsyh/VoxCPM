#!/usr/bin/env python3
"""
基础 TTS 语音合成示例

功能:
- 加载 VoxCPM 模型
- 从文本生成语音
- 保存为 WAV 文件

运行方式:
    python demo/1_basic_tts.py
"""

import soundfile as sf
from voxcpm import VoxCPM
from pathlib import Path

# 导入配置
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import get_model_path, get_output_dir


def main():
    print("=== VoxCPM 基础 TTS 示例 ===\n")

    # 1. 加载模型(优先使用本地模型)
    print("正在加载模型...")
    model = VoxCPM(voxcpm_model_path=get_model_path(), enable_denoiser=False)
    print("模型加载完成!\n")

    # 2. 准备文本
    text = "VoxCPM 是一个创新的端到端 TTS 模型,能够生成高度真实的语音。"
    print(f"输入文本: {text}\n")

    # 3. 生成语音
    print("正在生成语音...")
    wav = model.generate(
        text=text,
        prompt_wav_path=None,      # 不使用语音克隆
        prompt_text=None,
        cfg_value=2.0,             # 引导系数
        inference_timesteps=10,    # 推理步数
        normalize=False,           # 文本规范化
        denoise=False,             # 降噪
        retry_badcase=True,        # 自动重试失败 case
    )

    # 4. 保存音频
    output_dir = get_output_dir()
    output_path = output_dir / "1_basic_tts.wav"
    sf.write(str(output_path), wav, model.tts_model.sample_rate)

    # 5. 显示信息
    duration = len(wav) / model.tts_model.sample_rate
    print(f"✓ 生成完成!")
    print(f"  输出文件: {output_path}")
    print(f"  采样率: {model.tts_model.sample_rate} Hz")
    print(f"  时长: {duration:.2f} 秒")


if __name__ == "__main__":
    """
    示例中使用的可执行入口点
    """
    main()
