import os
import json
import openai
import requests

# 1. 读取注册表
# 跳过已优化的工具
def load_tools_registry(path):
    with open(path, 'r', encoding='utf-8') as f:
        tools = json.load(f)
        # 只返回未优化的工具
        return [tool for tool in tools if not tool.get('optimized', False)]

# 2. 构造 prompt
def build_prompt(tools, trajectory=None):
    prompt = (
        "You are an AI code optimization expert. You are given a JSON tool registry, where each tool contains fields such as name, description, and script_content.\n"
        "Your tasks are as follows:\n"
        "1. For any tool with an unclear or ambiguous description, rewrite the description to be precise, accurate, and helpful for correct invocation.\n"
        "2. For each tool, the description must explicitly specify the required query format, including the exact regex pattern used to match the query, what fields are extracted, and provide at least one example query.\n"
        "3. Check each tool implementation for potential bugs or unused parameters.\n"
        "4. Do NOT merge or combine any tools, even if they are similar. Keep all tools separate.\n"
        "5. Output the optimized tool registry as a JSON array (do not include any extra explanation, only the optimized JSON).\n"
        "Here is the original registry:\n"
        f"{json.dumps(tools, ensure_ascii=False, indent=2)}\n"
    )
    if trajectory:
        prompt += f"\nHere is the tool usage trajectory for reference (reflect on tool usage, errors, and improvement opportunities):\n{trajectory}\n"
    prompt += "Please strictly output only the optimized JSON registry as your answer."
    return prompt

def get_response(query, model):
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-23649b693560427fac8d83b9c6702f86"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": query}],
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
# 3. 调用GPT-4o
def optimize_tools_with_gpt4o(tools, trajectory=None):
    openai.api_key = "sk-23649b693560427fac8d83b9c6702f86"
    prompt = build_prompt(tools, trajectory)
    # print("Prompt:", prompt, sep='\n', end='\n\n')
    # exit()
    response = get_response(prompt, "gpt-4o-2024-11-20")
    # 提取优化后的JSON
    content = response['choices'][0]['message']['content']
    # print("Response:", content, sep='\n')
    # 尝试只提取JSON部分
    try:
        start = content.index('[')
        end = content.rindex(']') + 1
        optimized_json = content[start:end]
        optimized_tools = json.loads(optimized_json)
        # 为每个优化后的工具添加optimized标识
        for tool in optimized_tools:
            tool['optimized'] = True
        return optimized_tools
    except Exception:
        print("GPT返回内容无法直接解析为JSON，请手动检查输出。")
        print(content)
        return None

# 4. 保存优化后的注册表
def save_optimized_registry(tools, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)

def optimize_tool_registry(src, dst, trajectory_path=None):
    tools = load_tools_registry(src)
    if not tools:
        print("没有需要优化的工具，已全部完成优化。")
        return
    trajectory = None
    if trajectory_path and os.path.exists(trajectory_path):
        with open(trajectory_path, 'r', encoding='utf-8') as f:
            trajectory = f.read()
    optimized_tools = optimize_tools_with_gpt4o(tools, trajectory)
    if optimized_tools:
        save_optimized_registry(optimized_tools, dst)
        print(f"优化完成，已保存到 {dst}")
    else:
        print("未能自动生成优化后的注册表，请检查上面输出。")

def main():
    src = "mcp_tools_registry.json"
    dst = "mcp_tools_registry.json"
    trajectory_path = "history/unknown_1_trajectory.txt"
    optimize_tool_registry(src, dst, trajectory_path)

if __name__ == "__main__":
    main()