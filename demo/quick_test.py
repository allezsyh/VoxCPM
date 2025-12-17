#!/usr/bin/env python3
"""
快速测试脚本 - 验证 Demo 示例代码语法正确性

仅进行语法检查和导入测试,不实际运行模型
"""

import sys
import importlib.util


def test_script_syntax(script_path):
    """测试脚本语法是否正确"""
    try:
        spec = importlib.util.spec_from_file_location("test_module", script_path)
        module = importlib.util.module_from_spec(spec)
        # 只编译,不执行
        with open(script_path, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, script_path, 'exec')
        return True, "语法正确"
    except SyntaxError as e:
        return False, f"语法错误: {e}"
    except Exception as e:
        return False, f"其他错误: {e}"


def main():
    print("=" * 60)
    print("VoxCPM Demo 脚本语法检查")
    print("=" * 60)

    scripts = [
        "demo/1_basic_tts.py",
        "demo/2_voice_cloning.py",
        "demo/3_streaming_tts.py",
        "demo/4_batch_synthesis.py",
        "demo/5_lora_inference.py",
        "demo/6_parameter_tuning.py",
    ]

    results = {}
    for script in scripts:
        print(f"\n检查 {script}...", end=" ")
        success, message = test_script_syntax(script)
        results[script] = success

        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")

    print("\n" + "=" * 60)
    print("检查总结")
    print("=" * 60)

    success_count = sum(results.values())
    total_count = len(results)

    for script, success in results.items():
        status = "✓ 通过" if success else "✗ 失败"
        print(f"  {script}: {status}")

    print(f"\n总计: {success_count}/{total_count} 脚本语法正确")

    if success_count == total_count:
        print("\n🎉 所有脚本语法检查通过!")
        print("\n下一步: 运行实际测试")
        print("  注意: 首次运行会下载模型 (~2GB), 需要等待几分钟")
        print("  建议运行: python demo/1_basic_tts.py")
    else:
        print("\n⚠️  部分脚本有语法错误,请修复")

    return success_count == total_count


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
