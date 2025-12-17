#!/usr/bin/env python3
"""
VoxCPM 模型下载脚本

功能:
- 自动下载 VoxCPM1.5 模型到 models/ 目录
- 支持断点续传
- 显示下载进度
- 验证模型完整性

运行方式:
    python download_models.py

可选参数:
    python download_models.py --model VoxCPM1.5  # 指定模型版本
    python download_models.py --force             # 强制重新下载
"""

import argparse
from pathlib import Path
import sys


def download_voxcpm_model(model_name: str = "VoxCPM1.5", force: bool = False):
    """
    下载 VoxCPM 模型到 models/ 目录

    Args:
        model_name: 模型名称 (VoxCPM1.5 或 VoxCPM-0.5B)
        force: 是否强制重新下载
    """
    print("=== VoxCPM 模型下载工具 ===\n")

    # 1. 检查目标目录
    project_root = Path(__file__).parent
    models_dir = project_root / "models"
    target_dir = models_dir / model_name

    # 创建 models 目录
    models_dir.mkdir(exist_ok=True)

    # 2. 检查是否已存在
    if target_dir.exists() and not force:
        print(f"✓ 模型已存在: {target_dir}")
        print(f"  使用 --force 参数强制重新下载")

        # 验证关键文件
        required_files = ["model.safetensors", "audiovae.pth", "config.json"]
        missing_files = [f for f in required_files if not (target_dir / f).exists()]

        if missing_files:
            print(f"\n⚠ 警告: 缺少文件 {missing_files}")
            print("  建议使用 --force 重新下载")
            return False
        else:
            print("\n✓ 模型文件完整")
            return True

    # 3. 下载模型
    print(f"开始下载模型: {model_name}")
    print(f"目标目录: {target_dir}\n")

    try:
        from huggingface_hub import snapshot_download

        # 构建 HuggingFace 模型 ID
        hf_model_id = f"openbmb/{model_name}"

        print(f"从 HuggingFace Hub 下载: {hf_model_id}")
        print("这可能需要几分钟时间,取决于网络速度...\n")

        # 下载模型
        snapshot_download(
            repo_id=hf_model_id,
            local_dir=str(target_dir),
            local_dir_use_symlinks=False,  # 不使用符号链接,直接下载文件
            resume_download=True,          # 支持断点续传
        )

        print(f"\n✓ 下载完成!")
        print(f"  模型位置: {target_dir}")

        # 4. 验证下载
        required_files = ["model.safetensors", "audiovae.pth", "config.json"]
        missing_files = [f for f in required_files if not (target_dir / f).exists()]

        if missing_files:
            print(f"\n⚠ 警告: 下载后仍缺少文件 {missing_files}")
            return False
        else:
            print("\n✓ 模型验证通过")
            return True

    except ImportError:
        print("错误: 需要安装 huggingface_hub")
        print("\n请运行: pip install huggingface_hub")
        return False

    except Exception as e:
        print(f"\n✗ 下载失败: {e}")
        print("\n可能的解决方案:")
        print("1. 检查网络连接")
        print("2. 确认有足够磁盘空间 (需要约 2GB)")
        print("3. 使用代理或 VPN (如果在国内)")
        print("4. 手动下载后放置到 models/ 目录")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="VoxCPM 模型下载工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python download_models.py                    # 下载默认模型 (VoxCPM1.5)
  python download_models.py --model VoxCPM1.5  # 指定模型版本
  python download_models.py --force            # 强制重新下载

支持的模型:
  - VoxCPM1.5 (推荐): 800M 参数, 44.1kHz 采样率, 高质量
  - VoxCPM-0.5B: 640M 参数, 16kHz 采样率, 更快速度
        """
    )

    parser.add_argument(
        "--model",
        type=str,
        default="VoxCPM1.5",
        choices=["VoxCPM1.5", "VoxCPM-0.5B"],
        help="模型版本 (默认: VoxCPM1.5)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="强制重新下载,即使模型已存在"
    )

    args = parser.parse_args()

    # 下载模型
    success = download_voxcpm_model(args.model, args.force)

    if success:
        print("\n" + "=" * 60)
        print("下载完成!现在可以运行 demo 脚本:")
        print("  python demo/1_basic_tts.py")
        print("=" * 60)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    """
    下载 VoxCPM 模型到 models/ 目录

    示例:
        # 下载默认模型
        python download_models.py

        # 强制重新下载
        python download_models.py --force

        # 下载其他版本
        python download_models.py --model VoxCPM-0.5B
    """
    main()
