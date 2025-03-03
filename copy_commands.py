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
            
        repo_name = os.path.basename(git_root)
        
        rel_path = utils.get_git_path(path)
        
        if rel_path:
            full_git_path = "{0}/{1}".format(repo_name, rel_path)
            
            sublime.set_clipboard(full_git_path)
            sublime.status_message("Copied Git path: {0}".format(full_git_path))
        
    def is_visible(self, files=None, dirs=None):
        return bool(files or dirs)

class CopyProjectStructureCommand(sublime_plugin.WindowCommand):
    IGNORED_DIRS = ['node_modules', '.git', '.idea', '.vscode', 'dist', 'build']
    
    def run(self, files=None, dirs=None, depth=10):
        selected_paths = files or dirs or []
        if not selected_paths:
            return
            
        path = selected_paths[0]
        
        if os.path.isdir(path):
            structure = []
            self._process_directory(path, structure, 0, depth)
        else:
            file_name = os.path.basename(path)
            structure = ["📄 {0}".format(file_name)]
        
        structure_text = "\n".join(structure)
        
        sublime.set_clipboard(structure_text)
        sublime.status_message("Copied project structure with depth {0}".format(depth))
    
    def _process_directory(self, path, result, current_depth, max_depth):
        """Рекурсивно обробляє директорію для структури проекту"""
        if max_depth is not None and current_depth > max_depth:
            return
        
        dir_name = os.path.basename(path)
        
        if dir_name in self.IGNORED_DIRS:
            return
            
        prefix = '   ' * current_depth
        result.append("{0}📁 {1}/".format(prefix, dir_name))
        
        git_root = utils.get_git_root(path)
        
        try:
            items = sorted(os.listdir(path))
            
            dirs = []
            files = []
            
            for item in items:
                item_path = os.path.join(path, item)
                
                if utils.is_hidden(item_path):
                    continue
                if item in self.IGNORED_DIRS:
                    continue
                if git_root and utils.is_ignored_by_git(item_path, git_root):
                    continue
                
                if os.path.isdir(item_path):
                    dirs.append(item)
                else:
                    files.append(item)
            
            for dir_item in dirs:
                dir_path = os.path.join(path, dir_item)
                self._process_directory(dir_path, result, current_depth + 1, max_depth)
            
            for file_item in files:
                file_prefix = '   ' * (current_depth + 1)
                result.append("{0}📄 {1}".format(file_prefix, file_item))
                
        except (OSError, IOError) as e:
            error_prefix = '   ' * (current_depth + 1)
            result.append("{0}Error: {1}".format(error_prefix, str(e)))
        
    def is_visible(self, files=None, dirs=None):
        return bool(files or dirs)


class CopyNameTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        if not view.file_name():
            return
            
        path = view.file_name()
        name = os.path.basename(path)
        
        sublime.set_clipboard(name)
        sublime.status_message("Copied: {0}".format(name))
        
    def is_visible(self):
        return bool(self.view.file_name())

class CopyGitPathTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        if not view.file_name():
            return
            
        path = view.file_name()
        git_root = utils.get_git_root(path)
        if not git_root:
            return
            
        repo_name = os.path.basename(git_root)
        
        rel_path = utils.get_git_path(path)
        
        if rel_path:
            full_git_path = "{0}/{1}".format(repo_name, rel_path)
            
            sublime.set_clipboard(full_git_path)
            sublime.status_message("Copied Git path: {0}".format(full_git_path))
        
    def is_visible(self):
        return bool(self.view.file_name())
