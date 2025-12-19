#!/usr/bin/env python3
"""
语音克隆示例

功能:
- 使用参考音频克隆音色
- 保留音色、节奏、情感等特征
- 生成目标文本的语音

运行方式:
    python demo/2_voice_cloning.py

前提条件:
    - 准备参考音频文件 (例如 examples/example.wav)
    - 准备参考音频对应的文本
"""

import soundfile as sf
from voxcpm import VoxCPM
from pathlib import Path

# 导入配置
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import get_model_path, get_output_dir


def main():
    print("=== VoxCPM 语音克隆示例 ===\n")

    # 1. 加载模型(优先使用本地模型)
    print("正在加载模型...")
    model = VoxCPM(voxcpm_model_path=get_model_path(), enable_denoiser=False)
    print("模型加载完成!\n")

    # 2. 配置参考音频
    prompt_audio = "examples/example.wav"
    prompt_text = "Just by listening a few minutes a day, you'll be able to eliminate negative thoughts by conditioning your mind to be more positive."

    # 检查文件是否存在
    if not Path(prompt_audio).exists():
        print(f"错误: 参考音频文件不存在: {prompt_audio}")
        print("请确保 examples/example.wav 文件存在,或修改 prompt_audio 路径")
        return

    print(f"参考音频: {prompt_audio}")
    print(f"参考文本: {prompt_text}\n")

    # 3. 目标文本
    target_text = "VoxCPM is an innovative end-to-end TTS model from ModelBest, designed to generate highly realistic speech."
    print(f"目标文本: {target_text}\n")

    # 4. 生成语音 (克隆音色)
    print("正在克隆音色并生成语音...")
    wav = model.generate(
        text=target_text,
        prompt_wav_path=prompt_audio,  # 提供参考音频
        prompt_text=prompt_text,       # 提供参考文本
        cfg_value=2.0,
        inference_timesteps=10,
        normalize=False,
        denoise=False,  # 可选:是否对参考音频降噪
    )

    # 5. 保存音频
    output_dir = get_output_dir()
    output_path = output_dir / "2_voice_cloning.wav"
    sf.write(str(output_path), wav, model.tts_model.sample_rate)

    # 6. 显示信息
    duration = len(wav) / model.tts_model.sample_rate
    print(f"✓ 克隆完成!")
    print(f"  输出文件: {output_path}")
    print(f"  采样率: {model.tts_model.sample_rate} Hz")
    print(f"  时长: {duration:.2f} 秒")
    print(f"\n提示: 生成的语音应该具有参考音频的音色特征")


if __name__ == "__main__":
    """
    示例中使用的可执行入口点
    """
    main()
