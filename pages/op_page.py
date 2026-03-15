import tkinter as tk
from tkinter import ttk
from utils import Constant as Cst
from utils import Operations as Op
from utils import FlatButton


class OpPage(ttk.Frame):
    def __init__(self, parent, on_back):
        super().__init__(parent)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # red header title
        self.op_title = tk.Label(
            self, text="", anchor="center",
            background=Cst.HEADER_BACKGROUND, foreground="white",
            font=("Arial", 20, "bold")
        )
        self.op_title.grid(row=0, column=0, sticky="ew", ipady=18)

        # operation-specific content
        self.params_frame = ttk.Frame(self)
        self.params_frame.grid(row=1, column=0, sticky="nsew", padx=40)

        # import / export buttons
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, pady=30)

        self.btn_import = FlatButton(
            btn_frame,
            text=Op.IMPORT_PDF,
            bg=Cst.HEADER_BACKGROUND, fg="white",
            hover_bg="#c41c23",
            font=("Arial", 11, "bold"),
        )
        self.btn_import.pack(side="left", padx=12)

        self.btn_export = FlatButton(
            btn_frame,
            text=Op.EXPORT_PDF,
            bg=Cst.BG, fg=Cst.HEADER_BACKGROUND,
            hover_bg="#fff0f0",
            font=("Arial", 11),
            border_color=Cst.HEADER_BACKGROUND,
        )
        self.btn_export.pack(side="left", padx=12)

        # back link
        back_btn = FlatButton(
            self,
            text="← Back",
            bg=Cst.BG, fg=Cst.TEXT_MUTED,
            hover_bg=Cst.BG, hover_fg=Cst.TEXT_PRIMARY,
            font=("Arial", 10),
        )
        back_btn.config(command=on_back)
        back_btn.grid(row=3, column=0, pady=(0, 16))

    def load(self, title, operation_class):
        """Load an operation into the page shell."""
        self.op_title.config(text=title)
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        operation_class(self.params_frame, self.btn_import, self.btn_export)
