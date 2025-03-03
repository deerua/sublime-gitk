import sublime
import sublime_plugin
import os
import subprocess

class OpenTerminalCommand(sublime_plugin.WindowCommand):
    TERMINALS = {
        'cmd': {
            'command': 'cmd',
            'args': '/K "cd /d "{path}""',
            'name': 'CMD'
        },
        'powershell': {
            'command': 'powershell',
            'args': '-NoExit -Command "Set-Location \'{path}\'"',
            'name': 'PowerShell'
        }
    }

    def run(self, dirs=None, terminal_type='cmd'):
        print("OpenTerminalCommand.run called with dirs:", dirs)
        print("Terminal type:", terminal_type)
        
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

            terminal = self.TERMINALS.get(terminal_type)
            if not terminal:
                raise ValueError("Unknown terminal type: {0}".format(terminal_type))

            # Виправлення для CMD: не використовуємо 'start' (це усуває подвійне відкриття)
            if terminal_type == 'cmd':
                # Запускаємо cmd безпосередньо з правильними аргументами
                cmd_args = [
                    terminal['command'],
                    '/K', 
                    'cd /d "{0}"'.format(path)
                ]
                
                print("Starting {0} in: {1} with args: {2}".format(terminal['name'], path, cmd_args))
                process = subprocess.Popen(
                    cmd_args,
                    cwd=path,
                    startupinfo=startupinfo
                )
            else:
                # Для інших терміналів (PowerShell тощо) залишаємо як є
                cmd = 'start {command} {args}'.format(
                    command=terminal['command'],
                    args=terminal['args'].format(path=path)
                )
                
                print("Starting {0} in: {1}".format(terminal['name'], path))
                process = subprocess.Popen(
                    cmd,
                    cwd=path,
                    startupinfo=startupinfo,
                    shell=True
                )
                
            print("{0} process started: {1}".format(terminal['name'], process.pid))
            
        except Exception as e:
            error_msg = "Error starting {0}: {1}".format(terminal['name'], str(e))
            print(error_msg)
            sublime.error_message(error_msg)
            
    def is_visible(self, dirs=None, terminal_type='cmd'):
        is_vis = bool(dirs) and os.name == 'nt'
        print("OpenTerminalCommand.is_visible: {0} dirs: {1}".format(is_vis, dirs))
        return is_vis
