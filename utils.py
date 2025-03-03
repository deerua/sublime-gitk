import sublime
import os
import subprocess
import re

def get_git_root(path):
    try:
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        git_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], 
            cwd=os.path.dirname(path) if os.path.isfile(path) else path,
            stderr=subprocess.STDOUT,
            startupinfo=startupinfo,
            universal_newlines=True
        ).strip()
        
        return git_root
    except subprocess.CalledProcessError:
        sublime.error_message("Directory is not a git repository")
        return None
    except (OSError, IOError) as e:
        sublime.error_message("Git not found. Please ensure it is installed")
        return None

def get_git_path(path):
    git_root = get_git_root(path)
    if not git_root:
        return None
    
    norm_git_root = os.path.normpath(git_root)
    norm_path = os.path.normpath(path)
    
    rel_path = os.path.relpath(norm_path, norm_git_root)
    
    git_path = rel_path.replace('\\', '/')
    
    return git_path

def is_ignored_by_git(path, git_root=None):
    if not git_root:
        git_root = get_git_root(path)
        if not git_root:
            return False

    try:
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        result = subprocess.call(
            ["git", "check-ignore", "-q", path],
            cwd=git_root,
            startupinfo=startupinfo
        )
        
        return result == 0
    except:
        return False

def is_hidden(path):
    name = os.path.basename(path)
    
    if name.startswith('.'):
        return True
        
    if os.name == 'nt':
        try:
            import stat
            return bool(os.stat(path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
        except:
            return name.startswith('.')
            
    return False

def get_project_structure(path, depth=None, current_depth=0):
    directory_items = []
    file_items = []
    
    if os.path.isfile(path):
        return [os.path.basename(path)]
    
    if depth is not None and current_depth > depth:
        return []
    
    git_root = get_git_root(path)
    
    try:
        items = sorted(os.listdir(path))
        
        for item in items:
            item_path = os.path.join(path, item)
            
            if is_hidden(item_path):
                continue
                
            if git_root and is_ignored_by_git(item_path, git_root):
                continue
            
            prefix = '   ' * current_depth
            
            if os.path.isdir(item_path):
                directory_items.append("{0}📁 {1}/".format(prefix, item))
                
                children = get_project_structure(item_path, depth, current_depth + 1)
                directory_items.extend(children)
            else:
                file_items.append("{0}📄 {1}".format(prefix, item))
    
    except (OSError, IOError) as e:
        return ["Error accessing {0}: {1}".format(path, str(e))]
    
    return directory_items + file_items
