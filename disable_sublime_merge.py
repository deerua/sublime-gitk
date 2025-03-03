import sublime
import sublime_plugin

class DisableSublimeMergeCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        # Отримати налаштування користувача
        settings = sublime.load_settings("Preferences.sublime-settings")
        
        # Встановити налаштування sublime_merge в null
        settings.set("sublime_merge", None)
        
        # Зберегти налаштування
        sublime.save_settings("Preferences.sublime-settings")
        
        sublime.status_message("Sublime Merge integration disabled")

# Автоматично запускається при завантаженні пакета
def plugin_loaded():
    # Автоматично вимикаємо інтеграцію з Sublime Merge
    sublime.active_window().run_command("disable_sublime_merge")
