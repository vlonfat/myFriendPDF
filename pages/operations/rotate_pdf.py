import os
import tkinter as tk
from tkinter import ttk, messagebox
from utils import FileManager as FM
from utils import FileTypes as FT
from utils import BaseOperation
from pypdf import PdfReader, PdfWriter


class RotatePDF(BaseOperation):

    def __init__(self, params_frame, btn_import, btn_export):
        self.pdf_path = None
        self.page_max = 0
        super().__init__(params_frame, btn_import, btn_export)

    # ── UI ────────────────────────────────────────────────────

    def _build_ui(self, params_frame):
        self.info_label = ttk.Label(params_frame, text="No file imported", foreground="#888888")
        self.info_label.pack(pady=(20, 10))

        ttk.Separator(params_frame, orient="horizontal").pack(fill="x", padx=20, pady=10)

        # rotation angle
        ttk.Label(params_frame, text="Rotation angle:").pack(pady=(5, 3))
        self.angle = tk.IntVar(value=90)
        angle_frame = ttk.Frame(params_frame)
        angle_frame.pack(pady=5)
        for label, value in [("90°", 90), ("180°", 180), ("270°", 270)]:
            ttk.Radiobutton(angle_frame, text=label, variable=self.angle, value=value).pack(side="left", padx=15)

        ttk.Separator(params_frame, orient="horizontal").pack(fill="x", padx=20, pady=10)

        # apply to
        ttk.Label(params_frame, text="Apply to:").pack(pady=(5, 3))
        self.scope = tk.StringVar(value="all")
        scope_frame = ttk.Frame(params_frame)
        scope_frame.pack(pady=5)
        ttk.Radiobutton(scope_frame, text="All pages",    variable=self.scope,
                        value="all",       command=self._toggle_scope).pack(side="left", padx=15)
        ttk.Radiobutton(scope_frame, text="Page range",   variable=self.scope,
                        value="range",     command=self._toggle_scope).pack(side="left", padx=15)
        ttk.Radiobutton(scope_frame, text="Page selection", variable=self.scope,
                        value="selection", command=self._toggle_scope).pack(side="left", padx=15)

        # range controls
        self.range_frame = ttk.Frame(params_frame)
        ttk.Label(self.range_frame, text="From page").pack(side="left", padx=5)
        self.entry_start = ttk.Entry(self.range_frame, width=5)
        self.entry_start.pack(side="left", padx=3)
        ttk.Label(self.range_frame, text="to").pack(side="left")
        self.entry_end = ttk.Entry(self.range_frame, width=5)
        self.entry_end.pack(side="left", padx=3)

        # selection controls
        self.selection_frame = ttk.Frame(params_frame)
        ttk.Label(self.selection_frame, text="Pages (e.g. 1 4 6):").pack(side="left", padx=5)
        self.entry_pages = ttk.Entry(self.selection_frame, width=20)
        self.entry_pages.pack(side="left", padx=3)

    def _toggle_scope(self):
        self.range_frame.pack_forget()
        self.selection_frame.pack_forget()
        if self.scope.get() == "range":
            self.range_frame.pack(pady=10)
        elif self.scope.get() == "selection":
            self.selection_frame.pack(pady=10)

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
        output_path = FM.export_file(default_name="rotated")
        if not output_path:
            return
        self._rotate(output_path)

    # ── CORE LOGIC ────────────────────────────────────────────

    def _rotate(self, output_path):
        try:
            reader = PdfReader(self.pdf_path)
            writer = PdfWriter()
            angle  = self.angle.get()
            rotate_indices = self._get_rotate_indices()

            for i, page in enumerate(reader.pages):
                if i in rotate_indices:
                    page.rotate(angle)
                writer.add_page(page)

            with open(output_path, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Success", f"Rotated PDF exported to:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error during rotation:\n{str(e)}")

    def _get_rotate_indices(self):
        """Return a set of 0-based page indices to rotate."""
        scope = self.scope.get()
        if scope == "all":
            return set(range(self.page_max))
        if scope == "range":
            start = FM.parse_page(self.entry_start.get())
            end   = FM.parse_page(self.entry_end.get())
            return set(range(start - 1, end))
        if scope == "selection":
            return {int(p) - 1 for p in self.entry_pages.get().split() if p.isdigit()}
        return set()

    # ── VALIDATION ────────────────────────────────────────────

    def _validate(self):
        if not self.pdf_path:
            messagebox.showwarning("Warning", "Please import a PDF file first.")
            return False

        scope = self.scope.get()

        if scope == "range":
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

        if scope == "selection":
            raw = self.entry_pages.get().split()
            if not raw:
                messagebox.showwarning("Warning", "Please enter at least one page number.")
                return False
            invalid = [p for p in raw if not p.isdigit()]
            if invalid:
                messagebox.showwarning("Warning", f"Invalid page numbers: {' '.join(invalid)}")
                return False
            out_of_range = [p for p in raw if int(p) < 1 or int(p) > self.page_max]
            if out_of_range:
                messagebox.showwarning("Warning",
                    f"Pages out of range (1–{self.page_max}): {' '.join(out_of_range)}")
                return False

        return True
