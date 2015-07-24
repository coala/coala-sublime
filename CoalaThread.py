import os
import json
import threading
import sublime
import tempfile
import subprocess

from .Utils import log, COALA_KEY


class CoalaThread(threading.Thread):
    def __init__(self,
                 view,
                 callback,
                 cwd=None,
                 config_file="",
                 extra_args=[]):
        """
        Creates a thread that runs coala on the sublime view and finally runs
        the callback with the view as an argument.

        :param view:        The view to run coala on.
        :param callback:    The function to run after running coala - gives
                            the view as argument.
        :paran cwd:         The current working directory to set before
                            running coala.
        :param config_file: The config file to use for coala.
        :param extra_args:  List of extra arguments to run coala with.
        """
        self.view = view
        # Save the file name here, since view cannot be accessed
        # from anywhere but the main application thread
        self.file_name = view.file_name()
        self.working_dir = cwd
        self.config_file = config_file
        self.extra_args = extra_args
        self.callback = callback

        if self.working_dir == None:
            self.working_dir = os.path.dirname(self.file_name)

        threading.Thread.__init__(self)

    def run(self):
        command = ["coala-json"]
        options = []

        if self.config_file:
            options.append('--config=%s' % self.config_file)
        else:
            options.append('--find-config')

        options.append('--files=%s' % self.file_name)
        options.extend(self.extra_args)
        command.extend(options)

        stdout_file = tempfile.TemporaryFile()
        kwargs = {"stdout": stdout_file,
                  "cwd": self.working_dir}

        log("kwargs to subprocess:", kwargs)
        log("command run in subprocess:", command)

        process = subprocess.Popen(command, **kwargs)
        retval = process.wait()

        if retval == 1:
            stdout_file.seek(0)
            output_str = stdout_file.read().decode("utf-8", "ignore")
            if output_str:
                log("Output =", output_str)
                # Call set_timeout to have the function run in main thread
                sublime.set_timeout(
                    lambda: self.process_output(output_str),
                    100)
            else:
                log("No results for the file")
        elif retval == 0:
            log("No issues found")
        else:
            log("Exited with:", retval)
        stdout_file.close()

    def process_output(self, output_str):
        view_id = self.view.id()
        output = json.loads(output_str)
        # Save output to the view's setting - the setting is not common to all
        # views, and is only for this view.
        self.view.settings().set(COALA_KEY + ".output", output)
        self.callback(self.view)
