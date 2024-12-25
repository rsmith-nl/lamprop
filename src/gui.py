# file: gui.py
# vim:fileencoding=utf-8:fdm=marker:ft=python
# lamprop GUI - main program.
#
# Copyright © 2018 R.F. Smith <rsmith@xs4all.nl>. All rights reserved.
# Created: 2018-01-21 17:55:29 +0100
# Last modified: 2022-01-29T01:43:13+0100
#
# SPDX-License-Identifier: BSD-2-Clause

from functools import partial
import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter.font import nametofont
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
import lp


class LampropUI(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        if os.name == "posix":
            self.directory = os.getcwd()
        else:
            self.directory = ""
        self.lamfile = tk.StringVar()
        self.lamfile.set("no file selected")
        self.laminates = None
        self.engprop = tk.IntVar()
        self.engprop.set(1)
        self.result = None
        self.matrices = tk.IntVar()
        self.fea = tk.IntVar()
        # Don't show hidden files in the file dialog
        # https://stackoverflow.com/questions/53220711
        try:
            # call a dummy dialog with an impossible option to initialize the file
            # dialog without really getting a dialog window; this will throw a
            # TclError, so we need a try...except :
            try:
                self.tk.call("tk_getOpenFile", "-foobarbaz")
            except tk.TclError:
                pass
            # now set the magic variables accordingly
            self.tk.call("set", "::tk::dialog::file::showHiddenBtn", "1")
            self.tk.call("set", "::tk::dialog::file::showHiddenVar", "0")
        except Exception:
            pass
        self.initialize()

    def initialize(self):
        """Create the GUI."""
        # Set the font
        default_font = nametofont("TkDefaultFont")
        default_font["size"] = 12
        self.option_add("*Font", default_font)
        self.option_add("*tearOff", False)
        # General commands and bindings
        self.rowconfigure(5, weight=1)
        self.columnconfigure(4, weight=1)
        # Create menu.
        menubar = tk.Menu(self)
        self["menu"] = menubar
        file_menu = tk.Menu(menubar)
        file_menu.add_command(label="Open", underline=0, command=self.do_fileopen)
        file_menu.add_command(label="Reload", underline=0, command=self.do_reload)
        file_menu.add_command(
            label="Info",
            underline=0,
            command=self.show_info,
            state="disabled",
        )
        file_menu.add_command(
            label="Warnings",
            underline=0,
            command=self.show_warnings,
            state="disabled",
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Text export",
            underline=0,
            command=self.do_export_txt,
            state="disabled",
        )
        file_menu.add_command(
            label="HTML export",
            underline=0,
            command=self.do_export_html,
            state="disabled",
        )
        file_menu.add_separator()
        file_menu.add_command(label="Quit", underline=0, command=self.quit)
        menubar.add_cascade(label="File", underline=0, menu=file_menu)
        self.file_menu = file_menu
        helpmenu = tk.Menu(menubar)
        helpmenu.add_command(label="About", underline=0, command=self.show_about)
        helpmenu.add_command(label="License", underline=0, command=self.show_license)
        menubar.add_cascade(label="Help", underline=0, menu=helpmenu)
        # Create widgets.
        # Row
        prbut = ttk.Label(self, text="File:", anchor="w")
        prbut.grid(row=0, column=0, sticky="w")
        fnlabel = ttk.Label(self, anchor="w", textvariable=self.lamfile)
        fnlabel.grid(row=0, column=1, columnspan=4, sticky="ew")
        # Row
        cb = partial(self.on_laminate, event=0)
        chkengprop = ttk.Checkbutton(
            self, text="Engineering properties", variable=self.engprop, command=cb
        )
        chkengprop.grid(row=1, column=0, columnspan=3, sticky="w")
        # Row
        chkmat = ttk.Checkbutton(
            self,
            text="ABD & H matrices, stiffness tensor",
            variable=self.matrices,
            command=cb,
        )
        chkmat.grid(row=2, column=0, columnspan=3, sticky="w")
        # Row
        chkmat = ttk.Checkbutton(
            self, text="FEA material data", variable=self.fea, command=cb
        )
        chkmat.grid(row=3, column=0, columnspan=3, sticky="w")
        # Row
        cxlam = ttk.Combobox(self, state="readonly", justify="left")
        cxlam.grid(row=4, column=0, columnspan=5, sticky="we")
        cxlam.bind("<<ComboboxSelected>>", self.on_laminate)
        self.cxlam = cxlam
        # Row
        fixed = nametofont("TkFixedFont")
        fixed["size"] = 12
        res = ScrolledText(self, state="disabled", font=fixed)
        res.grid(row=5, column=0, columnspan=5, sticky="nsew")
        self.result = res

    # Callbacks
    def do_fileopen(self):
        """Open a lamprop file."""
        if not self.directory:
            available = [
                os.environ[k] for k in ("HOME", "HOMEDRIVE") if k in os.environ
            ]
            if available:
                self.directory = available[0]
        fn = filedialog.askopenfile(
            title="Lamprop file to open",
            parent=self,
            defaultextension=".lam",
            filetypes=(("lamprop files", "*.lam"), ("all files", "*.*")),
            initialdir=self.directory,
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
        self.file_menu.entryconfigure("Text export", state="disabled")
        self.file_menu.entryconfigure("HTML export", state="disabled")
        self.file_menu.entryconfigure("Info", state="disabled")
        self.file_menu.entryconfigure("Warnings", state="disabled")
        self.laminates = {lam.name: lam for lam in laminates}
        self.cxlam["values"] = list(self.laminates.keys())
        self.cxlam.current(0)
        self.on_laminate(0)
        self.file_menu.entryconfigure("Text export", state="normal")
        self.file_menu.entryconfigure("HTML export", state="normal")
        self.file_menu.entryconfigure("Info", state="normal")
        if lp.warn:
            self.file_menu.entryconfigure("Warnings", state="normal")
            self.show_warnings()

    def gentxt(self):
        """Generate text output."""
        name = self.cxlam.get()
        text = "\n".join(
            lp.text.out(
                self.laminates[name],
                bool(self.engprop.get()),
                bool(self.matrices.get()),
                bool(self.fea.get()),
            )
        )
        return text

    def on_laminate(self, event):
        """Laminate choice has changed."""
        text = self.gentxt()
        self.result["state"] = "normal"
        self.result.replace("1.0", "end", text)
        self.result["state"] = "disabled"

    def do_export_txt(self):
        """Export current laminate as text."""
        res = filedialog.asksaveasfile(
            title="Save as text",
            parent=self,
            defaultextension=".txt",
            filetypes=(("text files", "*.txt"), ("all files", "*.*")),
            initialdir=self.directory,
            initialfile=self.cxlam.get() + ".txt",
        )
        if not res:
            return
        text = self.gentxt()
        with open(res.name, "w") as tf:
            tf.write(text)

    def do_export_html(self):
        """Export current laminate as HTML."""
        res = filedialog.asksaveasfile(
            title="Save as HTML",
            parent=self,
            defaultextension=".html",
            filetypes=(("HTML files", "*.html"), ("all files", "*.*")),
            initialdir=self.directory,
            initialfile=self.cxlam.get() + ".html",
        )
        if not res:
            return
        name = self.cxlam.get()
        html = "\n".join(
            lp.html.out(
                self.laminates[name],
                bool(self.engprop.get()),
                bool(self.matrices.get()),
                bool(self.fea.get()),
            )
        )
        with open(res.name, "w") as hf:
            hf.write(html)

    def show_about(self):
        message(
            self,
            "Lamprop is a program to calculate physical and mechanical properties\n"
            "of continuous fiber reinforced composite laminates.\n\n"
            "The latest version can be found online at:"
            "https://github.com/rsmith-nl/lamprop\n"
            "Look under “Releases”.\n\n"
            "For more in-depth information, see “lamprop-manual.pdf” in the doc subdirectory.",
            title="About",
        )

    def show_license(self):
        """Display license"""
        message(self, lp.__license__, title="License", height=25)

    def show_info(self):
        """Display parser information"""
        text = "\n".join(lp.info)
        message(self, text, f"Information for {self.lamfile.get()}")

    def show_warnings(self):
        """Display parser warnings"""
        text = "\n".join(lp.warn)
        message(self, text, f"Warnings for {self.lamfile.get()}")


def message(parent, msg, title="Message", width=80, height=10):
    """Create a toplevel window to display a long message."""
    tl = tk.Toplevel(parent)
    tl.title(title)
    tl.rowconfigure(0, weight=1)
    tl.columnconfigure(0, weight=1)
    txt = tk.Text(tl, width=width, height=height)
    txt["bg"] = "lightgrey"
    txt.insert("1.0", msg)
    txt["state"] = "disabled"
    txt.grid(row=0, column=0, sticky="nesw")
    ok = ttk.Button(tl, text="Close", command=tl.destroy)
    ok.grid(row=1, column=0)


if __name__ == "__main__":
    if os.name == "posix":
        if os.fork():
            sys.exit()
    else:
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(
            os.path.join(os.getenv("TEMP"), "stderr-" + os.path.basename(sys.argv[0])),
            "w",
        )
    root = LampropUI(None)
    root.wm_title("Lamprop GUI v" + lp.__version__)
    root.mainloop()
