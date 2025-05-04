import os

def is_android_project(project_root):
    """
    Checks whether the Unity project targets Android by scanning for:
    - Android-specific plugin folders
    - AndroidManifest.xml
    - Gradle-related files
    - Android platform metadata in ProjectSettings
    """
    indicators = []

    # Plugins/Android folder
    plugins_android = os.path.join(project_root, 'Assets', 'Plugins', 'Android')
    indicators.append(os.path.exists(plugins_android))

    # AndroidManifest.xml in Plugins/Android
    manifest = os.path.join(plugins_android, 'AndroidManifest.xml')
    indicators.append(os.path.exists(manifest))

    # Gradle build files (Unity export path)
    gradle_project_path = os.path.join(project_root, 'Temp', 'gradleOut')
    gradle_build = os.path.join(gradle_project_path, 'build.gradle')
    indicators.append(os.path.exists(gradle_build))

    # Android platform setting in ProjectSettings.asset
    settings_file = os.path.join(project_root, 'ProjectSettings', 'ProjectSettings.asset')
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'Android' in content or 'defaultPlatform: Android' in content:
                    indicators.append(True)
        except Exception as e:
            print(f"⚠️ Could not read ProjectSettings.asset: {e}")

    return any(indicators)
