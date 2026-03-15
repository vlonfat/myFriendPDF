import os
from tkinter import ttk, messagebox
from utils import FileManager as FM
from utils import FileTypes as FT
from utils import BaseOperation


class PDFtoWord(BaseOperation):

    def __init__(self, params_frame, btn_import, btn_export):
        self.pdf_path = None
        super().__init__(params_frame, btn_import, btn_export)

    # ── UI ────────────────────────────────────────────────────

    def _build_ui(self, params_frame):
        self.info_label = ttk.Label(params_frame, text="No file imported", foreground="#888888")
        self.info_label.pack(pady=(20, 10))

        ttk.Separator(params_frame, orient="horizontal").pack(fill="x", padx=20, pady=10)

        ttk.Label(params_frame, text="Converts PDF text and layout to an editable .docx file.",
                  foreground="#888888", justify="center").pack(pady=5)

    # ── FILE ACTIONS ──────────────────────────────────────────

    def import_files(self):
        path = FM.import_files(multiple=False, fileType=FT.PDF)
        if not path:
            return
        self.pdf_path = path
        name = os.path.basename(path)
        self.info_label.config(text=name, foreground="#333333")

    def export_file(self):
        if not self.pdf_path:
            messagebox.showwarning("Warning", "Please import a PDF file first.")
            return
        default = os.path.splitext(os.path.basename(self.pdf_path))[0]
        output_path = FM.export_file(default_name=default, fileType=FT.WORD)
        if not output_path:
            return
        self._convert(output_path)

    # ── CORE LOGIC ────────────────────────────────────────────

    def _convert(self, output_path):
        try:
            from pdf2docx import Converter
            cv = Converter(self.pdf_path)
            cv.convert(output_path)
            cv.close()
            messagebox.showinfo("Success", f"Word file exported to:\n{output_path}")
        except ImportError:
            messagebox.showerror("Error", "pdf2docx is not installed.\nRun: pip install pdf2docx")
        except Exception as e:
            messagebox.showerror("Error", f"Error during conversion:\n{str(e)}")
