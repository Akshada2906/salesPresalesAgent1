import os
import json

def read_md_files(folder_path):
    md_data = {}
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            key_name = os.path.splitext(filename)[0].lower().replace(" ", "_")
            
            with open(file_path, "r") as file:
                content = file.read().strip()
                
            md_data[key_name] = {
                "title": key_name.replace("_", " ").title(),
                "content": content,
                "layout_rank": len(md_data) + 1
            }
    
    return md_data

folder_path = "server/app/pipelines/proposal_generator/data"
json_data = read_md_files(folder_path)


output_path = "server/app/pipelines/proposal_generator/proposal_template_1.json"
with open(output_path, "w", encoding="utf-8") as json_file:
    json.dump(json_data, json_file, indent=2, ensure_ascii=False)

print(f"JSON data saved to {output_path}")
