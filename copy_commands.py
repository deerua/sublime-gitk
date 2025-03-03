import sublime
import sublime_plugin
import os
from . import utils

class CopyNameCommand(sublime_plugin.WindowCommand):
    def run(self, files=None, dirs=None):
        selected_paths = files or dirs or []
        if not selected_paths:
            return
            
        path = selected_paths[0]
        name = os.path.basename(path)
        
        sublime.set_clipboard(name)
        sublime.status_message(f"Copied: {name}")
        
    def is_visible(self, files=None, dirs=None):
        return bool(files or dirs)

class CopyGitPathCommand(sublime_plugin.WindowCommand):
    def run(self, files=None, dirs=None):
        selected_paths = files or dirs or []
        if not selected_paths:
            return
            
        path = selected_paths[0]
        git_path = utils.get_git_path(path)
        
        if git_path:
            sublime.set_clipboard(git_path)
            sublime.status_message(f"Copied Git path: {git_path}")
        
    def is_visible(self, files=None, dirs=None):
        return bool(files or dirs)

class CopyProjectStructureCommand(sublime_plugin.WindowCommand):
    def run(self, files=None, dirs=None, depth=3):
        selected_paths = files or dirs or []
        if not selected_paths:
            return
            
        path = selected_paths[0]
        
        # Визначаємо, чи це директорія чи файл
        if os.path.isdir(path):
            dir_name = os.path.basename(path)
            structure = [f"📁 {dir_name}/"]
            structure.extend(utils.get_project_structure(path, depth=depth))
        else:
            file_name = os.path.basename(path)
            structure = [f"📄 {file_name}"]
        
        # Формуємо текст для копіювання
        structure_text = "\n".join(structure)
        
        sublime.set_clipboard(structure_text)
        sublime.status_message(f"Copied project structure with depth {depth}")
        
    def is_visible(self, files=None, dirs=None):
        return bool(files or dirs)
