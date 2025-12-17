#!/usr/bin/env python3
"""
Demo 测试脚本 - 快速验证示例代码是否可运行

功能:
- 测试模型加载
- 测试基础 TTS 生成
- 不保存文件,仅验证功能

运行方式:
    python demo/test_demo.py
"""

import sys
import torch
import numpy as np


def test_imports():
    """测试依赖导入"""
    print("=== 测试 1: 依赖导入 ===")
    try:
        import soundfile as sf
        from voxcpm import VoxCPM
        print("✓ 所有依赖导入成功")
        return True
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return False


def test_model_loading():
    """测试模型加载"""
    print("\n=== 测试 2: 模型加载 ===")
    try:
        from voxcpm import VoxCPM

        # 尝试使用本地模型或从 Hub 下载
        print("正在加载模型 (首次运行会下载,请耐心等待)...")
        model = VoxCPM.from_pretrained("openbmb/VoxCPM1.5")

        print(f"✓ 模型加载成功")
        print(f"  采样率: {model.tts_model.sample_rate} Hz")
        print(f"  设备: {next(model.tts_model.parameters()).device}")

        return model
    except Exception as e:
        print(f"✗ 模型加载失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_basic_generation(model):
    """测试基础语音生成"""
    print("\n=== 测试 3: 基础语音生成 ===")

    if model is None:
        print("✗ 跳过测试 (模型未加载)")
        return False

    try:
        # 使用非常短的文本快速测试
        text = "测试。"
        print(f"输入文本: {text}")

        print("正在生成语音...")
        wav = model.generate(
            text=text,
            prompt_wav_path=None,
            prompt_text=None,
            cfg_value=2.0,
            inference_timesteps=5,  # 使用较少步数加快测试
            normalize=False,
            denoise=False,
            retry_badcase=False,
        )

        # 验证输出
        assert isinstance(wav, np.ndarray), "输出应该是 numpy array"
        assert wav.ndim == 1, "输出应该是一维数组"
        assert len(wav) > 0, "输出不应为空"

        duration = len(wav) / model.tts_model.sample_rate
        print(f"✓ 生成成功!")
        print(f"  波形长度: {len(wav)} 样本")
        print(f"  时长: {duration:.2f} 秒")
        print(f"  数据类型: {wav.dtype}")
        print(f"  值域范围: [{wav.min():.3f}, {wav.max():.3f}]")

        return True

    except Exception as e:
        print(f"✗ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_streaming_generation(model):
    """测试流式生成"""
    print("\n=== 测试 4: 流式生成 ===")

    if model is None:
        print("✗ 跳过测试 (模型未加载)")
        return False

    try:
        text = "流式测试。"
        print(f"输入文本: {text}")

        print("正在流式生成...")
        chunks = []
        chunk_count = 0

        for chunk in model.generate_streaming(
            text=text,
            prompt_wav_path=None,
            prompt_text=None,
            cfg_value=2.0,
            inference_timesteps=5,
            normalize=False,
            denoise=False,
        ):
            chunk_count += 1
            chunks.append(chunk)
            print(f"  接收块 {chunk_count}: {len(chunk)} 样本")

        wav = np.concatenate(chunks)
        duration = len(wav) / model.tts_model.sample_rate

        print(f"✓ 流式生成成功!")
        print(f"  总块数: {chunk_count}")
        print(f"  总时长: {duration:.2f} 秒")

        return True

    except Exception as e:
        print(f"✗ 流式生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试流程"""
    print("=" * 60)
    print("VoxCPM Demo 测试脚本")
    print("=" * 60)

    # 显示环境信息
    print(f"\n环境信息:")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  PyTorch: {torch.__version__}")
    print(f"  CUDA: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"  GPU: {torch.cuda.get_device_name(0)}")

    # 运行测试
    results = {}

    # 测试 1: 导入
    results['imports'] = test_imports()
    if not results['imports']:
        print("\n⚠️  依赖导入失败,无法继续测试")
        return

    # 测试 2: 模型加载
    model = test_model_loading()
    results['model_loading'] = model is not None

    if not results['model_loading']:
        print("\n⚠️  模型加载失败,跳过后续测试")
    else:
        # 测试 3: 基础生成
        results['basic_generation'] = test_basic_generation(model)

        # 测试 4: 流式生成
        results['streaming_generation'] = test_streaming_generation(model)

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

    if success_count == total_count:
        print("\n🎉 所有测试通过! Demo 脚本可以正常运行。")
    else:
        print("\n⚠️  部分测试失败,请检查错误信息。")


if __name__ == "__main__":
    main()
