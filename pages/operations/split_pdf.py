import os
import tkinter as tk
from tkinter import ttk, messagebox
from utils import FileManager as FM
from utils import FileTypes as FT
from utils import BaseOperation
from pypdf import PdfReader, PdfWriter


class SplitPDF(BaseOperation):

    def __init__(self, params_frame, btn_import, btn_export):
        self.pdf_path  = None
        self.page_max  = 0
        super().__init__(params_frame, btn_import, btn_export)

    # ── UI ────────────────────────────────────────────────────

    def _build_ui(self, params_frame):
        self.info_label = ttk.Label(params_frame, text="No file imported", foreground="#888888")
        self.info_label.pack(pady=(20, 10))

        ttk.Separator(params_frame, orient="horizontal").pack(fill="x", padx=20, pady=10)

        # mode selection
        self.mode = tk.StringVar(value="range")
        mode_frame = ttk.Frame(params_frame)
        mode_frame.pack(pady=5)
        ttk.Radiobutton(mode_frame, text="Extract page range", variable=self.mode,
                        value="range", command=self._toggle_mode).pack(side="left", padx=15)
        ttk.Radiobutton(mode_frame, text="Split all pages", variable=self.mode,
                        value="all", command=self._toggle_mode).pack(side="left", padx=15)

        # range controls
        self.range_frame = ttk.Frame(params_frame)
        self.range_frame.pack(pady=10)
        ttk.Label(self.range_frame, text="From page").pack(side="left", padx=5)
        self.entry_start = ttk.Entry(self.range_frame, width=5)
        self.entry_start.pack(side="left", padx=3)
        ttk.Label(self.range_frame, text="to").pack(side="left")
        self.entry_end = ttk.Entry(self.range_frame, width=5)
        self.entry_end.pack(side="left", padx=3)

    def _toggle_mode(self):
        if self.mode.get() == "range":
            self.range_frame.pack(pady=10)
        else:
            self.range_frame.pack_forget()

    # ── FILE ACTIONS ──────────────────────────────────────────

    def import_files(self):
        path = FM.import_files(multiple=False, fileType=FT.PDF)
        if not path:
            return
        reader = PdfReader(path)
        self.pdf_path = path
        self.page_max = len(reader.pages)
        name = os.path.basename(path)
        self.info_label.config(
            text=f"{name}  ({self.page_max} pages)",
            foreground="#333333"
        )

    def export_file(self):
        if not self._validate():
            return

        if self.mode.get() == "all":
            folder = FM.select_directory()
            if not folder:
                return
            self._split_all(folder)
        else:
            start = FM.parse_page(self.entry_start.get())
            end   = FM.parse_page(self.entry_end.get())
            output_path = FM.export_file(default_name=f"split_p{start}-p{end}")
            if not output_path:
                return
            self._split_range(start, end, output_path)

    # ── CORE LOGIC ────────────────────────────────────────────

    def _split_range(self, start, end, output_path):
        try:
            reader = PdfReader(self.pdf_path)
            writer = PdfWriter()
            for i in range(start - 1, end):
                writer.add_page(reader.pages[i])
            with open(output_path, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Success", f"PDF exported to:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error during split:\n{str(e)}")

    def _split_all(self, folder):
        try:
            reader   = PdfReader(self.pdf_path)
            basename = os.path.splitext(os.path.basename(self.pdf_path))[0]
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                out = os.path.join(folder, f"{basename}_page_{i + 1}.pdf")
                with open(out, "wb") as f:
                    writer.write(f)
            messagebox.showinfo("Success", f"{len(reader.pages)} pages exported to:\n{folder}")
        except Exception as e:
            messagebox.showerror("Error", f"Error during split:\n{str(e)}")

    # ── VALIDATION ────────────────────────────────────────────

    def _validate(self):
        if not self.pdf_path:
            messagebox.showwarning("Warning", "Please import a PDF file first.")
            return False
        if self.mode.get() == "range":
            start = FM.parse_page(self.entry_start.get())
            end   = FM.parse_page(self.entry_end.get())
            if not start or not end:
                messagebox.showwarning("Warning", "Please enter a valid page range.")
                return False
            if start > end:
                messagebox.showwarning("Warning", "Start page must be ≤ end page.")
                return False
            if end > self.page_max:
                messagebox.showwarning("Warning", f"End page cannot exceed {self.page_max}.")
                return False
        return True
