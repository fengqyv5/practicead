import argparse
import os
from pathlib import Path

def process_files(input_files, output_file):
    """
    合并多个文件去重后处理
    :param input_files: 输入文件路径列表
    :param output_file: 输出文件路径
    """
    temp_path = f"{output_file}.tmp"  # 临时文件路径
    seen_lines = set()  # 用于记录已处理的行

    with open(temp_path, 'w', encoding='utf-8') as fout:
        for file_path in input_files:
            with open(file_path, 'r', encoding='utf-8') as fin:
                for line in fin:
                    # 去重检查（基于原始行内容）
                    if line in seen_lines:
                        continue
                    seen_lines.add(line)

                    # 删除注释行（忽略行首空格）
                    stripped = line.lstrip()
                    if stripped.startswith(('#', '!')):
                        continue

                    # 删除空白行
                    if not line.strip():
                        continue

                    # 添加前缀并写入
                    fout.write(f"*{line}")

    # 原子替换最终文件
    os.replace(temp_path, output_file)

if __name__ == "__main__":
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description='Process multiple files')
    parser.add_argument('--input', nargs='+', required=True, 
                       help='Input file paths (支持通配符)')
    parser.add_argument('--output', required=True,
                       help='Output file path')
    
    args = parser.parse_args()
    
    # 解析通配符路径
    input_files = []
    for pattern in args.input:
        input_files.extend(Path().glob(pattern))
    
    # 确保输出目录存在
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    process_files(input_files, output_path)
