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
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_yaml = f.read()

    objects = raw_yaml.split('--- !u!')
    parsed_objects = []
    fileID_to_name = {}

    # Step 1: First pass - collect GameObject names
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

            except yaml.YAMLError as e:
                continue

    # Step 2: Second pass - collect Button components
    for obj in objects:
        if 'Button:' in obj:
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

                        # Find onClick event handlers
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

            except yaml.YAMLError as e:
                continue

    return parsed_objects

# Example run
if __name__ == "__main__":
    path = "datasets/open-project-1-main/UOP1_Project/Assets/Scenes/Menus/SettingsMenu.unity"
    ui_objects = parse_unity_yaml(path)
    for obj in ui_objects:
        print(obj)
