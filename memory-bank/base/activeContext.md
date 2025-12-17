# 当前上下文

## 最新状态
- **日期**: 2025-12-17
- **分支**: dev
- **最新提交**: ee5f256 "FIX:When a prompt is present, concatenate two patches as the context for VAE decoding"

## 当前活动
- ✅ 已创建 memory-bank/ 项目记忆库
- ✅ 已创建 demo/ 示例脚本目录
- ✅ 完成示例代码测试验证
- ✅ 模型迁移到工程目录完成
- ✅ 所有 demo 脚本更新为使用本地模型
- ✅ 已删除 HuggingFace 缓存节省空间
- ✅ 创建自动化模型下载脚本

## 最近完成

### 2025-12-17 创建自动化模型下载脚本
**任务**: 提供便捷的模型下载工具,方便在其他机器上部署

**完成内容**:
1. 创建 `download_models.py` 自动下载脚本
2. 更新 `models/README.md` 添加快速开始指南
3. 更新主 `README.md` 推荐使用自动下载脚本
4. 测试脚本功能验证

**脚本特性**:
- ✅ 自动下载模型到 `models/` 目录
- ✅ 支持断点续传
- ✅ 自动验证文件完整性
- ✅ 检测模型是否已存在
- ✅ 支持强制重新下载 (`--force`)
- ✅ 支持选择模型版本 (`--model`)
- ✅ 清晰的帮助信息和使用示例

**使用方式**:
```bash
# 下载默认模型 (VoxCPM1.5)
python download_models.py

# 强制重新下载
python download_models.py --force

# 下载其他版本
python download_models.py --model VoxCPM-0.5B
```

**测试结果**:
- ✅ 帮助信息正确显示
- ✅ 能正确检测已存在的模型
- ✅ 文件完整性验证正常
- ✅ 命令行参数解析正确

**优势**:
- 方便团队成员在新机器上快速部署
- 统一下载位置 (`models/` 而非缓存)
- 支持离线使用场景
- 自动化程度高,减少人工操作



### 2025-12-17 删除 HuggingFace 缓存
**任务**: 清理系统缓存节省磁盘空间

**完成内容**:
1. 删除整个 `~/.cache/huggingface` 目录 (1.9 GB)
2. 验证 demo 脚本仍能正常运行
3. 确认项目完全独立于缓存

**执行详情**:
- 删除前大小: 1.9 GB
- 执行命令: `rm -rf ~/.cache/huggingface`
- 验证测试: `python demo/1_basic_tts.py` ✅ 成功

**测试结果**:
- ✅ 缓存删除成功
- ✅ 模型从本地加载: `models/VoxCPM1.5/`
- ✅ 语音生成正常: 6.08 秒音频
- ✅ 完全离线可用
- ✅ 节省磁盘空间: ~1.9 GB

**最终状态**:
- 项目模型: `models/VoxCPM1.5/` (1.9 GB) ✅
- 系统缓存: 已删除 ✅
- Demo 脚本: 全部使用本地模型 ✅
- 离线运行: 完全可用 ✅



### 2025-12-17 Demo 脚本更新使用本地模型
**任务**: 更新所有示例脚本使用本地模型而非缓存

**完成内容**:
1. 更新 6 个核心示例脚本使用 `config.get_model_path()`
2. 统一使用 `VoxCPM(voxcpm_model_path=get_model_path())`
3. 禁用降噪器避免下载额外模型 `enable_denoiser=False`
4. 更新 demo/README.md 说明本地模型使用

**更新脚本**:
- ✅ `1_basic_tts.py` - 使用本地模型
- ✅ `2_voice_cloning.py` - 使用本地模型
- ✅ `3_streaming_tts.py` - 使用本地模型
- ✅ `4_batch_synthesis.py` - 使用本地模型
- ✅ `5_lora_inference.py` - 使用本地模型
- ✅ `6_parameter_tuning.py` - 使用本地模型

**测试结果**:
- ✅ 语法检查: 6/6 通过
- ✅ 功能测试: demo/1_basic_tts.py 运行成功
- ✅ 模型加载: 从本地路径加载
- ✅ 语音生成: 5.92 秒音频正常生成

**关键改进**:
```python
# OLD: 从 Hub/缓存加载
model = VoxCPM.from_pretrained("openbmb/VoxCPM1.5")

# NEW: 从本地模型加载
from config import get_model_path
model = VoxCPM(voxcpm_model_path=get_model_path(), enable_denoiser=False)
```

**优势**:
- 完全离线可用(模型已在本地)
- 不依赖 ~/.cache/ 目录
- 可安全删除缓存节省 ~2GB 空间
- 配置自动检测(本地优先,Hub 降级)

### 2025-12-17 模型迁移到工程目录
**任务**: 将模型从系统缓存迁移到工程目录

**完成内容**:
1. 复制 VoxCPM1.5 模型到 `models/VoxCPM1.5/` (1.9 GB)
2. 创建本地模型示例脚本 `demo/0_local_model_example.py`
3. 创建配置管理文件 `demo/config.py`
4. 更新 `.gitignore` 排除模型文件
5. 创建 `models/README.md` 说明文档
6. 测试验证本地模型运行正常

**迁移详情**:
- 源位置: `~/.cache/huggingface/hub/models--openbmb--VoxCPM1.5/`
- 目标位置: `./models/VoxCPM1.5/`
- 复制方式: `cp -rL` (跟随符号链接复制实际文件)
- 测试结果: ✅ 成功生成 3.04 秒语音

**配置特性**:
- 优先使用本地模型
- 本地模型不存在时自动从 Hub 下载
- 支持配置化管理模型路径

### 2025-12-16 Demo 示例脚本创建
创建了完整的 demo 示例脚本集合:

**核心示例** (7个):
0. `0_local_model_example.py` - 本地模型使用
1. `1_basic_tts.py` - 基础 TTS 语音合成
2. `2_voice_cloning.py` - 语音克隆
3. `3_streaming_tts.py` - 流式生成
4. `4_batch_synthesis.py` - 批量合成
5. `5_lora_inference.py` - LoRA 推理
6. `6_parameter_tuning.py` - 参数调优对比

**测试脚本** (3个):
- `quick_test.py` - 语法检查
- `test_imports.py` - 导入和结构测试
- `test_demo.py` - 完整功能测试

**配置文件**:
- `config.py` - 模型路径和参数配置

**文档**:
- `README.md` - 详细使用指南 (已更新)

**验证结果**:
- ✅ 所有脚本语法正确 (7/7)
- ✅ 本地模型加载成功
- ✅ 语音生成测试通过
- ✅ 完全不依赖缓存目录

## 当前目录结构
```
VoxCPM/
├── models/                    # 本地模型目录
│   ├── VoxCPM1.5/            # 主模型 (1.9 GB)
│   ├── zipenhancer/          # 降噪模型配置
│   ├── .gitkeep
│   └── README.md             # 模型下载说明
├── demo/                      # 示例脚本
│   ├── config.py             # 配置管理(自动检测本地)
│   ├── 0_local_model_example.py
│   ├── 1-6_*.py              # 核心示例(全部使用本地)
│   ├── test_*.py             # 测试脚本
│   └── README.md             # 使用指南(已更新)
├── memory-bank/              # 项目记忆库
└── QUICK_START.md            # 快速开始
```

## 待处理事项
无

## 下一步建议
用户可以:
1. 运行任意示例验证: `python demo/1_basic_tts.py`
2. 根据需求修改示例参数
3. 开发新功能或修复 Bug
4. 进行 LoRA 微调训练
5. 完全离线环境使用(模型已在本地)
6. 将项目分享给团队(其他成员需自行下载模型到 `models/VoxCPM1.5/`)
