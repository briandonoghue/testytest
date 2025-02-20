import logging
import threading
import time
import tkinter as tk
from tkinter import scrolledtext

class ErrorDisplay:
    def __init__(self, root, log_file="logs/error_handler.log"):
        """
        Initializes the error display UI.

        :param root: Tkinter root window.
        :param log_file: Path to the error log file.
        """
        self.root = root
        self.log_file = log_file
        self.root.title("Error Log Monitor")
        self.root.geometry("600x400")

        # Error Log Display
        self.error_log = scrolledtext.ScrolledText(root, width=80, height=15)
        self.error_log.pack(pady=10)
        self.error_log.insert(tk.END, "Error log initialized...\n")
        self.error_log.config(state=tk.DISABLED)

        # Start auto-refresh
        self.update_error_log()

    def update_error_log(self):
        """ Updates error log dynamically. """
        threading.Thread(target=self._refresh_log, daemon=True).start()

    def _refresh_log(self):
        """ Reads the last 10 errors and updates the display. """
        while True:
            with open(self.log_file, "r") as file:
                errors = file.readlines()

            self.error_log.config(state=tk.NORMAL)
            self.error_log.delete("1.0", tk.END)

            # Show last 10 errors with color-coding
            for line in errors[-10:]:
                if "CRITICAL" in line:
                    self.error_log.insert(tk.END, line, "critical")
                elif "WARNING" in line:
                    self.error_log.insert(tk.END, line, "warning")
                else:
                    self.error_log.insert(tk.END, line, "info")

            self.error_log.tag_config("critical", foreground="red")
            self.error_log.tag_config("warning", foreground="orange")
            self.error_log.tag_config("info", foreground="blue")

            self.error_log.config(state=tk.DISABLED)
            time.sleep(5)

# Example Usage
if __name__ == "__main__":
    root = tk.Tk()
    error_display = ErrorDisplay(root)
    root.mainloop()
