import json
import os

# 路径可根据实际情况调整
json_path = "mcp_tools_registry.json"
output_dir = "src/web/mcp_scripts"  # 建议单独放到一个目录

os.makedirs(output_dir, exist_ok=True)

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for entry in data:
    name = entry.get("name")
    script_content = entry.get("script_content")
    if name and script_content:
        file_path = os.path.join(output_dir, f"{name}.py")
        with open(file_path, "w", encoding="utf-8") as py_file:
            py_file.write(script_content)
        print(f"Saved: {file_path}")
    else:
        print(f"Skipped entry (missing name or script_content): {entry}")

print("All script_content fields have been extracted.")