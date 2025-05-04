import os
from parsers.android_filter import is_android_project
from parsers.ui_reachability_analyzer import find_reachable_ui_nodes
from parsers.dead_ui_report import generate_dead_ui_report


def main(project_root='datasets/open-project-1-main/UOP1_Project',
         gexf_path='outputs/ui_navigation_graph.gexf',
         output_csv='outputs/dead_ui_report.csv'):

    print("🔍 Checking if the Unity project targets Android...")
    if not is_android_project(project_root):
        print("❌ Not an Android-targeted Unity project. Skipping analysis.")
        return

    print("✅ Android project detected. Proceeding with UI analysis.")

    print("📊 Running reachability analysis...")
    reachable_nodes, dead_nodes = analyze_ui_reachability(gexf_path)

    print(f"✅ Analysis complete: {len(dead_nodes)} dead UI elements found.")

    print("📝 Writing report...")
    generate_dead_ui_report(reachable_nodes, dead_nodes, output_csv)
    print(f"✅ Report saved to {output_csv}")


if __name__ == '__main__':
    main()
