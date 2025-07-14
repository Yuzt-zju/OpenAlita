#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将40行JSON数据重复为80行，格式为aabbcc
"""

def duplicate_jsonl_data(input_file, output_file):
    """
    读取JSONL文件，将每行重复两次，输出到新文件
    
    Args:
        input_file (str): 输入文件路径
        output_file (str): 输出文件路径
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        
        # 去除空行
        lines = [line.strip() for line in lines if line.strip()]
        
        print(f"原始文件有 {len(lines)} 行数据")
        
        # 创建重复的数据
        duplicated_lines = []
        for line in lines:
            # 每行重复两次
            duplicated_lines.append(line)
            duplicated_lines.append(line)
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for line in duplicated_lines:
                outfile.write(line + '\n')
        
        print(f"成功创建输出文件: {output_file}")
        print(f"输出文件有 {len(duplicated_lines)} 行数据")
        print("格式: aabbcc (每行重复两次)")
        
    except FileNotFoundError:
        print(f"错误: 找不到输入文件 {input_file}")
    except Exception as e:
        print(f"处理文件时发生错误: {e}")

def main():
    input_file = "test_gaia_sample_tool_40.jsonl"
    output_file = "test_gaia_sample_tool_80.jsonl"
    
    print("开始处理数据...")
    duplicate_jsonl_data(input_file, output_file)
    
    # 验证结果
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            result_lines = [line.strip() for line in f.readlines() if line.strip()]
        
        print(f"\n验证结果:")
        print(f"输出文件行数: {len(result_lines)}")
        
        # 检查前几行是否按aabbcc格式排列
        if len(result_lines) >= 6:
            print("前6行格式检查:")
            for i in range(0, 6, 2):
                if result_lines[i] == result_lines[i+1]:
                    print(f"行 {i+1} 和行 {i+2}: 相同 ✓")
                else:
                    print(f"行 {i+1} 和行 {i+2}: 不同 ✗")
        
    except Exception as e:
        print(f"验证时发生错误: {e}")

if __name__ == "__main__":
    main() 