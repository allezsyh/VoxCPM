"""
Demo 示例脚本配置

定义模型路径和默认参数
"""

from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 模型路径配置
LOCAL_MODEL_PATH = PROJECT_ROOT / "models" / "VoxCPM1.5"
LOCAL_ZIPENHANCER_PATH = PROJECT_ROOT / "models" / "zipenhancer"

# HuggingFace Hub 模型 ID
HF_MODEL_ID = "openbmb/VoxCPM1.5"
ZIPENHANCER_MODEL_ID = "iic/speech_zipenhancer_ans_multiloss_16k_base"

# 模型加载策略
# 优先使用本地模型,如果不存在则从 Hub 下载
USE_LOCAL_MODEL = LOCAL_MODEL_PATH.exists()

# 默认生成参数
DEFAULT_CFG_VALUE = 2.0
DEFAULT_INFERENCE_TIMESTEPS = 10
DEFAULT_NORMALIZE = False
DEFAULT_DENOISE = False
DEFAULT_RETRY_BADCASE = True

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / "demo"


def get_model_path():
    """获取模型路径(优先本地,其次 Hub)"""
    if USE_LOCAL_MODEL:
        return str(LOCAL_MODEL_PATH)
    else:
        return HF_MODEL_ID


def get_zipenhancer_path():
    """获取降噪模型路径"""
    if LOCAL_ZIPENHANCER_PATH.exists():
        return str(LOCAL_ZIPENHANCER_PATH)
    else:
        return ZIPENHANCER_MODEL_ID


def print_model_info():
    """打印模型配置信息"""
    print("=" * 60)
    print("模型配置")
    print("=" * 60)
    print(f"使用本地模型: {USE_LOCAL_MODEL}")
    if USE_LOCAL_MODEL:
        print(f"本地模型路径: {LOCAL_MODEL_PATH}")
    else:
        print(f"HuggingFace 模型: {HF_MODEL_ID}")
    print("=" * 60)
    print()
