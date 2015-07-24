import sublime_plugin
import sublime
from .CoalaThread import CoalaThread
from .Utils import log


class CoalaCommand(sublime_plugin.TextCommand):
    """
    The CoalaCommand inherits the TextCommand from sublime_plugin and can be
    executed using `view.run_command("coala")` - which executes the `run()`
    function by default.
    """
    def run(self, edit, **kwargs):
        file_name = self.view.file_name()
        log("Trying to run coala on", file_name)
        if file_name:
            thread = CoalaThread(self.view, show_output)
            thread.start()
            self.progress_tracker(thread)
        else:
            sublime.status_message("Save the file to run coala on it")

    def progress_tracker(self, thread, i=0):
        """ Display spinner while coala is running """
        icons = [u"◐", u"◓", u"◑", u"◒"]
        sublime.status_message("Running coala %s" % icons[i])
        if thread and thread.is_alive():
            i = (i + 1) % 4
            sublime.set_timeout(lambda: self.progress_tracker(thread, i), 100)
        else:
            sublime.status_message("")
