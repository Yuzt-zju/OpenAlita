import json

input_file = 'test_gaia_sample.jsonl'
output_file = 'test_gaia_sample_tool.jsonl'

with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8') as fout:
    for line in fin:
        data = json.loads(line)
        tools_str = data.get('Annotator Metadata', {}).get('Tools', '')
        # Split tools by line and remove leading numbers and periods
        tools = [t.strip() for t in tools_str.split('\n') if t.strip()]
        # Remove leading numbers and periods, and lowercase for comparison
        cleaned_tools = []
        for t in tools:
            t_clean = t
            if '.' in t:
                t_clean = t.split('.', 1)[1].strip()
            t_clean = t_clean.lower()
            if t_clean not in ['web browser', 'search engine']:
                cleaned_tools.append(t.strip())
        if cleaned_tools:
            # 保留原始Tools字段
            fout.write(json.dumps(data, ensure_ascii=False) + '\n')
        # 如果cleaned_tools为空，则不写入该条数据 