import sublime
import sublime_plugin
import os
import subprocess

class OpenCmdCommand(sublime_plugin.WindowCommand):
    def run(self, dirs=None):
        print("OpenCmdCommand.run called with dirs:", dirs)
        
        if not dirs:
            print("No directories provided")
            return
            
        path = dirs[0]
        print("Selected path:", path)
        
        if not os.path.isdir(path):
            path = os.path.dirname(path)
            print("Using parent directory:", path)

        try:
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            print("Starting CMD in:", path)
            process = subprocess.Popen(
                'cmd.exe /k cd /d ' + path,
                cwd=path,
                startupinfo=startupinfo
            )
            print("CMD process started:", process.pid)

        except Exception as e:
            print("Error starting CMD:", str(e))
            sublime.error_message("Error starting CMD: " + str(e))

    def is_visible(self, dirs=None):
        is_vis = bool(dirs)
        print("OpenCmdCommand.is_visible:", is_vis, "dirs:", dirs)
        return is_vis