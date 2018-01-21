# file: lamprop-gui.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
#
# Author: R.F. Smith <rsmith@xs4all.nl>
# Created: 2018-01-21 17:55:29 +0100
# Last modified: 2018-01-21 20:30:05 +0100
"""
Calculate the elastic properties of a fibrous composite laminate, using a GUI.

See lamprop(5) for the manual of the data file format.
"""

from sys import exit as sys_exit
import os
import lp
import tkinter as tk
from tkinter import ttk
from tkinter.font import nametofont
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

__version__ = lp.__version__


class LampropUI(tk.Tk):

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.directory = ''
        self.lamfile = tk.StringVar()
        self.laminates = None
        self.result = tk.StringVar()
        self.engprop = tk.IntVar()
        self.matrices = tk.IntVar()
        self.initialize()

    def initialize(self):
        """Create the GUI."""
        # Set the font
        default_font = nametofont("TkDefaultFont")
        default_font.configure(size=12)
        self.option_add("*Font", default_font)
        # General commands and bindings
        self.bind_all('q', self.do_exit)
        # Create widgets.
        # First row
        prbut = ttk.Button(self, text="File:", command=self.do_fileopen)
        prbut.grid(row=0, column=0, sticky='w')
        fnlabel = ttk.Label(self, anchor='w', textvariable=self.lamfile)
        fnlabel.grid(row=0, column=1, columnspan=4, sticky='w')
        # Second row
        rldbut = ttk.Button(self, text="Reload", command=self.do_reload)
        rldbut.grid(row=1, column=0, sticky='w')
        # Third row
        chkengprop = ttk.Checkbutton(
            self, text='Engineering properties', variable=self.engprop
        )
        chkengprop.grid(row=2, column=0, columnspan=3, sticky='w')
        # Fourth row
        chkmat = ttk.Checkbutton(
            self, text='ABD & abd matrices', variable=self.matrices
        )
        chkmat.grid(row=3, column=0, columnspan=3, sticky='w')
        # Fifth row
        cxlam = ttk.Combobox(self, state='readonly', justify='left')
        cxlam.grid(row=4, column=0, columnspan=5, sticky='we')
        cxlam.bind("<<ComboboxSelected>>", self.on_laminate)
        self.cxlam = cxlam
        res = ScrolledText(self)
        res.grid(row=5, column=0, columnspan=5, sticky='ew')

    # Callbacks
    def do_exit(self, event):
        """
        Callback to handle quitting.

        This is necessary since the quit method does not take arguments.
        """
        self.quit()

    def do_fileopen(self):
        if not self.directory:
            self.directory = os.environ['HOME']
        fn = filedialog.askopenfile(
            title='Lamprop file to open', parent=self, defaultextension='.lam',
            filetypes=(('lamprop files', '*.lam'), ('all files', '*.*')),
            initialdir=self.directory
        )
        if not fn:
            return
        self.lamfile.set(fn.name)
        self.do_reload()

    def do_reload(self):
        """Reload the laminates."""
        self.laminates = lp.parse(self.lamfile.get())
        if not self.laminates:
            return
        names = [lam.name for lam in self.laminates]
        self.cxlam['values'] = names
        self.cxlam.current(0)

    def on_laminate(self, event):
        """Laminate choice has changed."""
        pass


if __name__ == '__main__':
    if os.name == 'posix':
        if os.fork():
            sys_exit()
    root = LampropUI(None)
    root.wm_title('Lamprop GUI v' + __version__)
    root.mainloop()
