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
        data = f.read()

    objects = []
    raw_objects = data.split('--- !u!')  # Each YAML object begins with this

    for obj in raw_objects:
        if 'Button' in obj or 'EventTrigger' in obj:
            lines = obj.splitlines()
            go_name = "Unknown"
            targets = []

            for i, line in enumerate(lines):
                if "m_Name:" in line:
                    go_name = line.split("m_Name:")[-1].strip()

                # Extract UnityEvent targets
                if "m_MethodName:" in line:
                    method = line.split(":")[-1].strip()
                    targets.append(method)

            if targets:
                component_type = "Button" if 'Button' in obj else 'EventTrigger'
                objects.append(UnityUIObject(go_name, component_type, targets))

    return objects

if __name__ == "__main__":
    path = "datasets/open-project-1-main/UOP1_Project/Assets/Scenes/Menus/MainMenu.unity"
    ui_objects = parse_unity_yaml(path)
    for obj in ui_objects:
        print(obj)

