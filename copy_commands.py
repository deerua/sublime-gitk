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
        sublime.status_message("Copied: {0}".format(name))
        
    def is_visible(self, files=None, dirs=None):
        return bool(files or dirs)

class CopyGitPathCommand(sublime_plugin.WindowCommand):
    def run(self, files=None, dirs=None):
        selected_paths = files or dirs or []
        if not selected_paths:
            return
            
        path = selected_paths[0]
        git_root = utils.get_git_root(path)
        if not git_root:
            return
            
        # Отримуємо ім'я репозиторію (останній компонент шляху кореня git)
        repo_name = os.path.basename(git_root)
        
        # Отримуємо відносний шлях у репозиторії
        rel_path = utils.get_git_path(path)
        
        if rel_path:
            # Формуємо повний шлях у форматі repo_name/path
            full_git_path = "{0}/{1}".format(repo_name, rel_path)
            
            sublime.set_clipboard(full_git_path)
            sublime.status_message("Copied Git path: {0}".format(full_git_path))
        
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
            structure = ["📁 {0}/".format(dir_name)]
            structure.extend(utils.get_project_structure(path, depth=depth))
        else:
            file_name = os.path.basename(path)
            structure = ["📄 {0}".format(file_name)]
        
        # Формуємо текст для копіювання
        structure_text = "\n".join(structure)
        
        sublime.set_clipboard(structure_text)
        sublime.status_message("Copied project structure with depth {0}".format(depth))
        
    def is_visible(self, files=None, dirs=None):
        return bool(files or dirs)
