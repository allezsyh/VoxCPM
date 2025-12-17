#!/usr/bin/env python3
"""
参数调优示例

功能:
- 演示不同参数对生成效果的影响
- 对比 CFG 值、推理步数等参数
- 生成多个版本进行对比

运行方式:
    python demo/6_parameter_tuning.py
"""

import soundfile as sf
from pathlib import Path
from voxcpm import VoxCPM

# 导入配置
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import get_model_path


def main():
    print("=== VoxCPM 参数调优示例 ===\n")

    # 1. 加载模型(优先使用本地模型)
    print("正在加载模型...")
    model = VoxCPM(voxcpm_model_path=get_model_path(), enable_denoiser=False)
    print("模型加载完成!\n")

    # 2. 准备文本
    text = "VoxCPM 支持多种参数配置,可以根据需求调整生成质量和速度。"
    print(f"输入文本: {text}\n")

    # 3. 创建输出目录
    output_dir = Path("demo/parameter_comparison")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 4. 测试不同参数组合
    test_configs = [
        {
            "name": "快速模式",
            "cfg_value": 1.5,
            "inference_timesteps": 5,
            "description": "低 CFG + 少步数 = 快速生成"
        },
        {
            "name": "标准模式",
            "cfg_value": 2.0,
            "inference_timesteps": 10,
            "description": "推荐配置,平衡质量与速度"
        },
        {
            "name": "高质量模式",
            "cfg_value": 2.5,
            "inference_timesteps": 20,
            "description": "高 CFG + 多步数 = 高质量生成"
        },
        {
            "name": "强引导模式",
            "cfg_value": 3.0,
            "inference_timesteps": 10,
            "description": "高 CFG = 更强的文本引导"
        },
    ]

    print("正在生成不同参数配置的音频...\n")

    for i, config in enumerate(test_configs, 1):
        print(f"[{i}/{len(test_configs)}] {config['name']}")
        print(f"  描述: {config['description']}")
        print(f"  CFG: {config['cfg_value']}, 步数: {config['inference_timesteps']}")

        # 生成音频
        wav = model.generate(
            text=text,
            prompt_wav_path=None,
            prompt_text=None,
            cfg_value=config['cfg_value'],
            inference_timesteps=config['inference_timesteps'],
            normalize=False,
            denoise=False,
            retry_badcase=True,
        )

        # 保存文件
        safe_name = config['name'].replace(" ", "_")
        output_file = output_dir / f"{i}_{safe_name}.wav"
        sf.write(str(output_file), wav, model.tts_model.sample_rate)

        duration = len(wav) / model.tts_model.sample_rate
        print(f"  ✓ 已保存: {output_file} ({duration:.2f}s)\n")

    # 5. 总结
    print("=" * 60)
    print(f"参数对比生成完成!")
    print(f"输出目录: {output_dir}")
    print(f"\n建议:")
    print("  - 播放对比不同参数生成的音频")
    print("  - 快速模式适合实时应用")
    print("  - 高质量模式适合最终产品")
    print("  - CFG 值影响对文本的贴合度")
    print("  - 推理步数影响生成质量")


if __name__ == "__main__":
    """
    示例中使用的可执行入口点
    """
    main()
