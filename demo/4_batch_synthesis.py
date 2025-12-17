#!/usr/bin/env python3
"""
批量语音合成示例

功能:
- 从文本文件批量读取
- 逐条生成语音
- 保存到指定目录

运行方式:
    python demo/4_batch_synthesis.py

前提条件:
    - 准备输入文本文件 (默认使用 examples/input.txt)
"""

import soundfile as sf
from pathlib import Path
from voxcpm import VoxCPM

# 导入配置
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import get_model_path


def main():
    print("=== VoxCPM 批量语音合成示例 ===\n")

    # 1. 配置
    input_file = "examples/input.txt"
    output_dir = Path("demo/batch_outputs")

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    # 2. 读取文本列表
    if not Path(input_file).exists():
        print(f"错误: 输入文件不存在: {input_file}")
        print("请创建该文件,每行一条文本")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        texts = [line.strip() for line in f if line.strip()]

    if not texts:
        print("错误: 输入文件为空")
        return

    print(f"从 {input_file} 读取到 {len(texts)} 条文本\n")

    # 3. 加载模型(优先使用本地模型)
    print("正在加载模型...")
    model = VoxCPM(voxcpm_model_path=get_model_path(), enable_denoiser=False)
    print("模型加载完成!\n")

    # 4. 批量生成
    success_count = 0
    for i, text in enumerate(texts, 1):
        print(f"[{i}/{len(texts)}] 正在处理: {text[:50]}...")

        try:
            # 生成语音
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

            # 保存文件
            output_file = output_dir / f"output_{i:03d}.wav"
            sf.write(str(output_file), wav, model.tts_model.sample_rate)

            duration = len(wav) / model.tts_model.sample_rate
            print(f"  ✓ 成功: {output_file} ({duration:.2f}s)\n")
            success_count += 1

        except Exception as e:
            print(f"  ✗ 失败: {e}\n")

    # 5. 总结
    print("=" * 50)
    print(f"批量合成完成: {success_count}/{len(texts)} 成功")
    print(f"输出目录: {output_dir}")


if __name__ == "__main__":
    """
    示例中使用的可执行入口点
    """
    main()
