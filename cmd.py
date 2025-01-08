import sublime
import sublime_plugin
import os
import subprocess

class OpenCmdCommand(sublime_plugin.WindowCommand):
    def run(self, dirs=None):
        if not dirs:
            return
            
        path = dirs[0]
        
        if not os.path.isdir(path):
            path = os.path.dirname(path)

        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.Popen(['cmd'], 
                        cwd=path,
                        startupinfo=startupinfo)

    def is_visible(self, dirs=None):
        return bool(dirs)