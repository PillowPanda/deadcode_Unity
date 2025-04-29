import yaml
import os

class UnityUIObject:
    def __init__(self, go_name, component_type, targets):
        self.name = go_name
        self.type = component_type
        self.targets = targets

    def __repr__(self):
        return f"{self.type}: {self.name} → {self.targets}"

def parse_unity_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_yaml = f.read()
    except Exception as e:
        print(f"Error opening file {file_path}: {e}")
        return []

    objects = raw_yaml.split('--- !u!')
    parsed_objects = []
    fileID_to_name = {}

    # Step 1: Collect GameObject names
    for obj in objects:
        if 'GameObject:' in obj:
            try:
                obj_lines = obj.splitlines()
                obj_body = "\n".join(line for line in obj_lines if not line.strip().startswith('---') and ':' in line)
                data = yaml.safe_load(obj_body)

                if not data:
                    continue

                for key, value in data.items():
                    if isinstance(value, dict):
                        name = value.get('m_Name', None)
                        fileID = None
                        for line in obj_lines:
                            if 'fileID:' in line:
                                parts = line.split('fileID:')
                                if len(parts) > 1:
                                    fileID = parts[1].strip()
                                    break

                        if name and fileID:
                            fileID_to_name[fileID] = name

            except yaml.YAMLError:
                continue

    # Step 2: Collect UI Components (Buttons, EventTriggers)
    for obj in objects:
        if 'Button:' in obj or 'EventTrigger:' in obj:
            try:
                obj_lines = obj.splitlines()
                obj_body = "\n".join(line for line in obj_lines if not line.strip().startswith('---') and ':' in line)
                data = yaml.safe_load(obj_body)

                if not data:
                    continue

                go_file_id = None
                targets = []

                for key, value in data.items():
                    if isinstance(value, dict):
                        if "m_GameObject" in value:
                            go_ref = value.get("m_GameObject", {})
                            if isinstance(go_ref, dict):
                                go_file_id = str(go_ref.get("fileID", None))

                        if "m_OnClick" in value:
                            calls = value.get("m_OnClick", {}).get("m_PersistentCalls", {}).get("m_Calls", [])
                            if isinstance(calls, list):
                                for call in calls:
                                    if isinstance(call, dict):
                                        method = call.get("m_MethodName", None)
                                        if method:
                                            targets.append(method)

                go_name = fileID_to_name.get(go_file_id, f"UnknownButton({go_file_id})")
                parsed_objects.append(UnityUIObject(go_name, "Button", targets))

            except yaml.YAMLError:
                continue

    return parsed_objects

def parse_all_prefabs(prefabs_root_folder):
    all_ui_objects = []

    for root, _, files in os.walk(prefabs_root_folder):
        for file in files:
            if file.endswith('.prefab'):
                full_path = os.path.join(root, file)
                print(f"Parsing prefab: {full_path}")
                all_ui_objects += parse_unity_yaml(full_path)

    return all_ui_objects

# Example run
if __name__ == "__main__":
    prefab_root = "datasets/open-project-1-main/UOP1_Project/Assets/Prefabs/UI"
    ui_objects = parse_all_prefabs(prefab_root)
    for obj in ui_objects:
        print(obj)
