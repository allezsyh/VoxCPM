#!/usr/bin/env python3
"""
导入测试 - 验证所有示例脚本的导入是否正常

不实际运行生成,只测试代码导入和基础结构
"""

import sys
import os


def test_basic_imports():
    """测试基础依赖导入"""
    print("=== 测试基础依赖 ===")
    try:
        import torch
        import numpy as np
        import soundfile as sf
        from pathlib import Path
        print(f"✓ PyTorch {torch.__version__}")
        print(f"✓ NumPy {np.__version__}")
        print(f"✓ SoundFile 已安装")
        return True
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return False


def test_voxcpm_import():
    """测试 VoxCPM 库导入"""
    print("\n=== 测试 VoxCPM 库 ===")
    try:
        from voxcpm import VoxCPM
        from voxcpm.model.voxcpm import LoRAConfig
        print("✓ VoxCPM 核心模块")
        print("✓ LoRAConfig 配置类")
        return True
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        print("  提示: 请确保已安装 voxcpm (pip install voxcpm)")
        return False


def test_demo_structure():
    """测试 Demo 文件结构"""
    print("\n=== 测试 Demo 文件结构 ===")

    required_files = [
        "demo/README.md",
        "demo/1_basic_tts.py",
        "demo/2_voice_cloning.py",
        "demo/3_streaming_tts.py",
        "demo/4_batch_synthesis.py",
        "demo/5_lora_inference.py",
        "demo/6_parameter_tuning.py",
    ]

    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (缺失)")
            all_exist = False

    return all_exist


def test_example_files():
    """测试示例文件"""
    print("\n=== 测试示例文件 ===")

    if os.path.exists("examples/example.wav"):
        print("✓ examples/example.wav (语音克隆参考音频)")
    else:
        print("⚠ examples/example.wav (缺失,语音克隆示例将无法运行)")

    if os.path.exists("examples/input.txt"):
        print("✓ examples/input.txt (批量合成输入)")
    else:
        print("⚠ examples/input.txt (缺失,批量合成示例将无法运行)")

    return True


def simulate_basic_api():
    """模拟基础 API 调用 (不实际生成)"""
    print("\n=== 模拟 API 调用 ===")

    try:
        from voxcpm.model.voxcpm import LoRAConfig

        # 测试 LoRAConfig 创建
        lora_config = LoRAConfig(
            enable_lm=True,
            enable_dit=True,
            r=32,
            alpha=16,
        )
        print(f"✓ LoRAConfig 创建成功")
        print(f"  - r={lora_config.r}, alpha={lora_config.alpha}")

        # 测试参数字典
        params = {
            'text': "测试文本",
            'cfg_value': 2.0,
            'inference_timesteps': 10,
        }
        print(f"✓ 参数配置正确")
        print(f"  - cfg_value={params['cfg_value']}")
        print(f"  - inference_timesteps={params['inference_timesteps']}")

        return True

    except Exception as e:
        print(f"✗ API 模拟失败: {e}")
        return False


def main():
    print("=" * 60)
    print("VoxCPM Demo 导入和结构测试")
    print("=" * 60)
    print()

    results = {}

    # 测试 1: 基础依赖
    results['basic_imports'] = test_basic_imports()

    # 测试 2: VoxCPM 库
    results['voxcpm_import'] = test_voxcpm_import()

    # 测试 3: Demo 文件结构
    results['demo_structure'] = test_demo_structure()

    # 测试 4: 示例文件
    results['example_files'] = test_example_files()

    # 测试 5: API 模拟
    results['api_simulation'] = simulate_basic_api()

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    for test_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {test_name}: {status}")

    success_count = sum(results.values())
    total_count = len(results)

    print(f"\n总计: {success_count}/{total_count} 测试通过")

    if results['basic_imports'] and results['voxcpm_import'] and results['demo_structure']:
        print("\n✅ 核心测试通过! Demo 脚本已就绪")
        print("\n建议下一步:")
        print("  1. 运行简单示例: python demo/1_basic_tts.py")
        print("  2. 首次运行会自动下载模型 (~2GB)")
        print("  3. 需要 CUDA GPU 以获得最佳性能")
    else:
        print("\n❌ 部分核心测试失败,请检查环境配置")

    return success_count == total_count


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
