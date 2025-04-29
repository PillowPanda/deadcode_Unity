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

    # Split Unity YAML into individual objects
    objects = raw_yaml.split('--- !u!')
    parsed_objects = []

    for obj in objects:
        if 'Button:' in obj:
            try:
                # Preprocess to remove Unity header lines
                obj_lines = obj.splitlines()
                obj_body = "\n".join(line for line in obj_lines if not line.strip().startswith('---') and ':' in line)

                # Parse this object's YAML body only
                data = yaml.safe_load(obj_body)

                if not data:
                    continue

                # Look for GameObject name
                go_name = "UnknownButton"
                targets = []

                # Navigate inside the parsed structure
                for key, value in data.items():
                    if isinstance(value, dict):
                        if "m_Name" in value:
                            go_name = value.get("m_Name", "UnknownButton")

                        # Find onClick event handlers
                        if "m_OnClick" in value:
                            calls = value.get("m_OnClick", {}).get("m_PersistentCalls", {}).get("m_Calls", [])
                            if isinstance(calls, list):
                                for call in calls:
                                    if isinstance(call, dict):
                                        method = call.get("m_MethodName", None)
                                        if method:
                                            targets.append(method)

                parsed_objects.append(UnityUIObject(go_name, "Button", targets))

            except yaml.YAMLError as e:
                print(f"YAML error while parsing object: {e}")
                continue

    return parsed_objects

# Example run
if __name__ == "__main__":
    path = "datasets/open-project-1-main/UOP1_Project/Assets/Scenes/Menus/MainMenu.unity"  # Update to your real file
    ui_objects = parse_unity_yaml(path)
    for obj in ui_objects:
        print(obj)
