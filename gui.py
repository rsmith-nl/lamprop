# file: gui.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
# lamprop GUI - main program.
#
# Copyright © 2018,2019 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2018-01-21 17:55:29 +0100
# Last modified: 2020-10-03T09:22:54+0200
#
# SPDX-License-Identifier: BSD-2-Clause
"""
Calculate the elastic properties of a fibrous composite laminate, using a GUI.

See lamprop(5) for the manual of the data file format.
"""

from functools import partial
import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter.font import nametofont
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
import lp

__version__ = lp.__version__


class LampropUI(tk.Tk):

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.directory = ''
        self.lamfile = tk.StringVar()
        self.lamfile.set('no file selected')
        self.laminates = None
        self.engprop = tk.IntVar()
        self.engprop.set(1)
        self.result = None
        self.matrices = tk.IntVar()
        self.initialize()

    def initialize(self):
        """Create the GUI."""
        # Set the font
        default_font = nametofont("TkDefaultFont")
        default_font['size'] = 12
        self.option_add("*Font", default_font)
        # General commands and bindings
        self.bind_all('q', self.do_exit)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(3, weight=1)
        # Create widgets.
        # First row
        prbut = ttk.Button(self, text="File:", command=self.do_fileopen)
        prbut.grid(row=0, column=0, sticky='w')
        fnlabel = ttk.Label(self, anchor='w', textvariable=self.lamfile)
        fnlabel.grid(row=0, column=1, columnspan=4, sticky='ew')
        # Second row
        rldbut = ttk.Button(self, text="Reload", command=self.do_reload)
        rldbut.grid(row=1, column=0, sticky='w')
        # Third row
        cb = partial(self.on_laminate, event=0)
        chkengprop = ttk.Checkbutton(
            self, text='Engineering properties', variable=self.engprop,
            command=cb
        )
        chkengprop.grid(row=2, column=0, columnspan=3, sticky='w')
        # Fourth row
        chkmat = ttk.Checkbutton(
            self, text='ABD & abd matrices', variable=self.matrices,
            command=cb
        )
        chkmat.grid(row=3, column=0, columnspan=3, sticky='w')
        # Fifth row
        cxlam = ttk.Combobox(self, state='readonly', justify='left')
        cxlam.grid(row=4, column=0, columnspan=5, sticky='we')
        cxlam.bind("<<ComboboxSelected>>", self.on_laminate)
        self.cxlam = cxlam
        # Sixth row
        fixed = nametofont('TkFixedFont')
        fixed['size'] = 12
        res = ScrolledText(self, state='disabled', font=fixed)
        res.grid(row=5, column=0, columnspan=5, sticky='nsew')
        self.result = res

    # Callbacks
    def do_exit(self, event):
        """
        Callback to handle quitting.

        This is necessary since the quit method does not take arguments.
        """
        self.quit()

    def do_fileopen(self):
        if not self.directory:
            self.directory = ''
            available = [
                os.environ[k] for k in ('HOME', 'HOMEDRIVE') if k in os.environ
            ]
            if available:
                self.directory = available[0]
        fn = filedialog.askopenfile(
            title='Lamprop file to open', parent=self, defaultextension='.lam',
            filetypes=(('lamprop files', '*.lam'), ('all files', '*.*')),
            initialdir=self.directory
        )
        if not fn:
            return
        self.directory = os.path.dirname(fn.name)
        self.lamfile.set(fn.name)
        self.do_reload()

    def do_reload(self):
        """Reload the laminates."""
        laminates = lp.parse(self.lamfile.get())
        if not laminates:
            return
        self.laminates = {lam.name: lam for lam in laminates}
        self.cxlam['values'] = list(self.laminates.keys())
        self.cxlam.current(0)
        self.on_laminate(0)

    def on_laminate(self, event):
        """Laminate choice has changed."""
        name = self.cxlam.get()
        text = ''
        if self.engprop.get():
            text += '\n'.join(lp.text.engprop(self.laminates[name]))
        if self.matrices.get():
            if text:
                text += '\n'
            text += '\n'.join(lp.text.matrices(self.laminates[name]))
        self.result['state'] = 'normal'
        self.result.replace('1.0', 'end', text)
        self.result['state'] = 'disabled'


def main():
    """Main entry point for lamprop GUI."""
    if os.name == 'posix':
        if os.fork():
            sys.exit()
    else:
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(
            os.path.join(os.getenv("TEMP"), "stderr-"+os.path.basename(sys.argv[0])), "w")
    root = LampropUI(None)
    root.wm_title('Lamprop GUI v' + __version__)
    root.mainloop()


if __name__ == '__main__':
    main()
