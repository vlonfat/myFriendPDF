import os
from tkinter import ttk, messagebox
from utils import FileManager as FM
from utils import FileTypes as FT
from utils import BaseOperation


class WordToPDF(BaseOperation):

    def __init__(self, params_frame, btn_import, btn_export):
        self.docx_path = None
        super().__init__(params_frame, btn_import, btn_export)

    # ── UI ────────────────────────────────────────────────────

    def _build_ui(self, params_frame):
        self.info_label = ttk.Label(params_frame, text="No file imported", foreground="#888888")
        self.info_label.pack(pady=(20, 10))

        ttk.Separator(params_frame, orient="horizontal").pack(fill="x", padx=20, pady=10)

        ttk.Label(params_frame,
                  text="Converts .docx to PDF.\nRequires Microsoft Word (macOS/Windows)\nor LibreOffice (Linux).",
                  foreground="#888888", justify="center").pack(pady=5)

    # ── FILE ACTIONS ──────────────────────────────────────────

    def import_files(self):
        path = FM.import_files(multiple=False, fileType=FT.WORD)
        if not path:
            return
        self.docx_path = path
        name = os.path.basename(path)
        self.info_label.config(text=name, foreground="#333333")

    def export_file(self):
        if not self.docx_path:
            messagebox.showwarning("Warning", "Please import a Word file first.")
            return
        default = os.path.splitext(os.path.basename(self.docx_path))[0]
        output_path = FM.export_file(default_name=default, fileType=FT.PDF)
        if not output_path:
            return
        self._convert(output_path)

    # ── CORE LOGIC ────────────────────────────────────────────

    def _convert(self, output_path):
        try:
            from docx2pdf import convert
            convert(self.docx_path, output_path)
            messagebox.showinfo("Success", f"PDF exported to:\n{output_path}")
        except ImportError:
            messagebox.showerror("Error", "docx2pdf is not installed.\nRun: pip install docx2pdf")
        except Exception as e:
            messagebox.showerror("Error", f"Error during conversion:\n{str(e)}")
