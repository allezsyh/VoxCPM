#!/usr/bin/env python3
"""
使用本地模型的示例

功能:
- 使用工程目录下的本地模型
- 避免从 HuggingFace Hub 下载
- 适合离线环境或自定义模型

运行方式:
    python demo/0_local_model_example.py

前提条件:
    - 模型已复制到 models/VoxCPM1.5/
"""

import soundfile as sf
from voxcpm import VoxCPM
from pathlib import Path


def main():
    print("=== VoxCPM 本地模型示例 ===\n")

    # 1. 配置本地模型路径
    project_root = Path(__file__).parent.parent
    local_model_path = project_root / "models" / "VoxCPM1.5"

    # 检查模型是否存在
    if not local_model_path.exists():
        print(f"错误: 本地模型不存在: {local_model_path}")
        print("\n请先将模型复制到工程目录:")
        print("  cp -rL ~/.cache/huggingface/hub/models--openbmb--VoxCPM1.5/snapshots/*/  models/VoxCPM1.5/")
        return

    print(f"使用本地模型: {local_model_path}\n")

    # 2. 加载本地模型
    print("正在加载模型...")
    model = VoxCPM(
        voxcpm_model_path=str(local_model_path),
        zipenhancer_model_path=None,  # 不使用降噪模型
        enable_denoiser=False,         # 禁用降噪器
    )
    print("模型加载完成!\n")

    # 3. 准备文本
    text = "这是使用本地模型生成的语音示例。"
    print(f"输入文本: {text}\n")

    # 4. 生成语音
    print("正在生成语音...")
    wav = model.generate(
        text=text,
        prompt_wav_path=None,
        prompt_text=None,
        cfg_value=2.0,
        inference_timesteps=10,
        normalize=False,
        denoise=False,
        retry_badcase=True,
    )

    # 5. 保存音频
    output_path = project_root / "demo" / "output_local_model.wav"
    sf.write(str(output_path), wav, model.tts_model.sample_rate)

    # 6. 显示信息
    duration = len(wav) / model.tts_model.sample_rate
    print(f"✓ 生成完成!")
    print(f"  输出文件: {output_path}")
    print(f"  采样率: {model.tts_model.sample_rate} Hz")
    print(f"  时长: {duration:.2f} 秒")
    print(f"\n✓ 本地模型运行成功!")


if __name__ == "__main__":
    """
    示例中使用的可执行入口点
    """
    main()
