import sublime
import sublime_plugin
import os
import subprocess

class GitkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_path = self.view.file_name()
        if not file_path:
            sublime.error_message("File is not saved")
            return
        file_dir = os.path.dirname(file_path)
        self._run_gitk(file_dir, [file_path])

    def _run_gitk(self, work_dir, paths):
        try:
            # Create startup info for Windows
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            subprocess.check_output(["git", "rev-parse", "--git-dir"], 
                                 cwd=work_dir, 
                                 stderr=subprocess.STDOUT,
                                 startupinfo=startupinfo)
            
            gitk_args = ["gitk"] + paths
            subprocess.Popen(gitk_args, 
                          cwd=work_dir,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          startupinfo=startupinfo)
        
        except subprocess.CalledProcessError:
            sublime.error_message("Directory is not a git repository")
        except FileNotFoundError:
            sublime.error_message("GitK not found. Please ensure it is installed")

class GitkFromSidebarCommand(sublime_plugin.WindowCommand):
    def run(self, files=None, dirs=None):
        selected_paths = files or dirs or []
        if not selected_paths:
            return
            
        path = selected_paths[0]
        
        if os.path.isdir(path):
            work_dir = path
            paths = []
        else:
            work_dir = os.path.dirname(path)
            paths = [path]

        # Create startup info for Windows
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        try:
            subprocess.check_output(["git", "rev-parse", "--git-dir"], 
                                 cwd=work_dir, 
                                 stderr=subprocess.STDOUT,
                                 startupinfo=startupinfo)
            
            gitk_args = ["gitk"] + paths
            subprocess.Popen(gitk_args, 
                          cwd=work_dir,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          startupinfo=startupinfo)
        
        except subprocess.CalledProcessError:
            sublime.error_message("Directory is not a git repository")
        except FileNotFoundError:
            sublime.error_message("GitK not found. Please ensure it is installed")

    def is_visible(self, files=None, dirs=None):
        return bool(files or dirs)