import sublime
import sublime_plugin

# Створюємо заглушки для команд Sublime Merge
class OpenInSublimeMergeCommand(sublime_plugin.WindowCommand):
    def run(self, **kwargs):
        pass

class BlameInSublimeMergeCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        pass
    
    def is_visible(self):
        return False

class GitStatusInSublimeMergeCommand(sublime_plugin.WindowCommand):
    def run(self, **kwargs):
        pass
    
    def is_visible(self):
        return False

class FileHistoryInSublimeMergeCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        pass
    
    def is_visible(self):
        return False

class LineHistoryInSublimeMergeCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        pass
    
    def is_visible(self):
        return False
