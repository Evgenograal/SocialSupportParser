import os
import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem
    
def load_json_file(file_path):
    with open(file_path, "r", encoding = "utf-8") as f:
        return json.load(f)

def build_folder_tree(tree_widget, folder):
    tree_widget.clear()

    nodes = {}

    for root, _, files in os.walk(folder):
        relative_root = os.path.relpath(root, folder)
        
        if relative_root == ".":
            parent = tree_widget.invisibleRootItem()

        else:
            parent = tree_widget.invisibleRootItem()

            current_path = ""

            for part in relative_root.split(os.sep):
                current_path = os.path.join(current_path, part)

                if current_path not in nodes:
                    item = QTreeWidgetItem([part])

                    parent.addChild(item)

                    nodes[current_path] = item
                
                parent = nodes[current_path]
            
        for file in files:
            if not file.lower().endswith(".json"):
                continue

            item = QTreeWidgetItem([file])

            item.setData(
                0,
                Qt.UserRole,
                os.path.join(root, file)
            )

            parent.addChild(item)

def build_json_tree(parent, data):
    
    if isinstance(data, dict):
        for key, value in data.items():
            item = QTreeWidgetItem([str(key)])

            parent.addChild(item)

            build_json_tree(item, value)

    elif isinstance(data, list):
        for i, value in enumerate(data):

            item = QTreeWidgetItem([f"[{i}]"])

            parent.addChild(item)

            build_json_tree(item, value)
        
    else:
        parent.setText(1, str(data))

def filter_json_tree(item, text):
    visible = False

    for i in range(item.childCount()):
        child = item.child(i)

        child_visible = filter_json_tree(child, text)

        visible = visible or child_visible

    match = (text in item.text(0).lower() or text in item.text(1).lower())

    visible = visible or match

    item.setHidden(not visible)

    return visible