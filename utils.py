import sublime
import os
import subprocess
import re

def get_git_root(path):
    """Отримати корінь git репозиторію для даного шляху"""
    try:
        # Створюємо інформацію для запуску для Windows
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
    """Отримати шлях файлу відносно кореня git репозиторію"""
    git_root = get_git_root(path)
    if not git_root:
        return None
    
    # Нормалізуємо шляхи для порівняння
    norm_git_root = os.path.normpath(git_root)
    norm_path = os.path.normpath(path)
    
    # Отримуємо відносний шлях
    rel_path = os.path.relpath(norm_path, norm_git_root)
    
    # Замінюємо зворотні слеші на прямі (для git)
    git_path = rel_path.replace('\\', '/')
    
    return git_path

def get_project_structure(path, depth=None, current_depth=0):
    """Рекурсивно отримати структуру проекту (папки/файли)"""
    result = []
    
    # Якщо шлях - це файл, повертаємо тільки ім'я файлу
    if os.path.isfile(path):
        return [os.path.basename(path)]
    
    # Якщо ми досягли максимальної глибини, повертаємо порожній список
    if depth is not None and current_depth > depth:
        return []
    
    # Отримуємо список файлів та директорій
    try:
        items = sorted(os.listdir(path))
        
        for item in items:
            item_path = os.path.join(path, item)
            
            # Додаємо префікс для візуального представлення
            prefix = '   ' * current_depth
            
            if os.path.isdir(item_path):
                # Якщо це директорія, додаємо її з слешем
                result.append("{0}📁 {1}/".format(prefix, item))
                
                # Рекурсивно отримуємо вміст цієї директорії
                children = get_project_structure(item_path, depth, current_depth + 1)
                result.extend(children)
            else:
                # Якщо це файл, просто додаємо його
                result.append("{0}📄 {1}".format(prefix, item))
    
    except (PermissionError, OSError, IOError) as e:
        result.append("Error accessing {0}: {1}".format(path, str(e)))
    
    return result
