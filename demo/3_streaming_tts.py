#!/usr/bin/env python3
"""
流式 TTS 语音合成示例

功能:
- 使用流式生成模式
- 逐块输出音频数据
- 适合实时应用场景

运行方式:
    python demo/3_streaming_tts.py
"""

import numpy as np
import soundfile as sf
from voxcpm import VoxCPM
from pathlib import Path

# 导入配置
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import get_model_path, get_output_dir


def main():
    print("=== VoxCPM 流式 TTS 示例 ===\n")

    # 1. 加载模型(优先使用本地模型)
    print("正在加载模型...")
    model = VoxCPM(voxcpm_model_path=get_model_path(), enable_denoiser=False)
    print("模型加载完成!\n")

    # 2. 准备文本
    text = "VoxCPM 是一个创新的端到端 TTS 模型,能够生成高度真实的语音。"
    print(f"输入文本: {text}\n")

    # 3. 流式生成
    print("正在流式生成语音...")
    chunks = []
    chunk_count = 0

    for chunk in model.generate_streaming(
        text=text,
        prompt_wav_path=None,
        prompt_text=None,
        cfg_value=2.0,
        inference_timesteps=10,
        normalize=False,
        denoise=False,
    ):
        chunk_count += 1
        chunks.append(chunk)

        # 显示进度
        chunk_duration = len(chunk) / model.tts_model.sample_rate
        print(f"  接收第 {chunk_count} 个音频块: {len(chunk)} 样本 ({chunk_duration:.3f} 秒)")

    # 4. 合并所有音频块
    print("\n正在合并音频块...")
    wav = np.concatenate(chunks)

    # 5. 保存音频
    output_dir = get_output_dir()
    output_path = output_dir / "3_streaming_tts.wav"
    sf.write(str(output_path), wav, model.tts_model.sample_rate)

    # 6. 显示信息
    duration = len(wav) / model.tts_model.sample_rate
    print(f"✓ 流式生成完成!")
    print(f"  输出文件: {output_path}")
    print(f"  总块数: {chunk_count}")
    print(f"  总时长: {duration:.2f} 秒")
    print(f"  采样率: {model.tts_model.sample_rate} Hz")


if __name__ == "__main__":
    """
    示例中使用的可执行入口点
    """
    main()
