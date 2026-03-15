import io
import os
import zipfile
import tarfile
import tkinter as tk
from tkinter import ttk, messagebox
from utils import FileManager as FM
from utils import FileTypes as FT
from utils import BaseOperation
from pypdf import PdfReader, PdfWriter


LEVELS = [
    ("None",    "No PDF compression  (archive only)",       "none"),
    ("Light",   "Remove duplicate objects only",            "light"),
    ("Medium",  "+ Compress content streams",               "medium"),
    ("Maximum", "+ Remove images  (text & structure only)", "maximum"),
]

FORMATS = [
    ("PDF",  "Compressed PDF file",        "pdf"),
    ("ZIP",  "PDF wrapped in a ZIP archive", "zip"),
    ("TGZ",  "PDF wrapped in a TGZ archive", "tgz"),
]


class CompressPDF(BaseOperation):

    def __init__(self, params_frame, btn_import, btn_export):
        self.pdf_path = None
        super().__init__(params_frame, btn_import, btn_export)

    # ── UI ────────────────────────────────────────────────────

    def _build_ui(self, params_frame):
        self.info_label = ttk.Label(params_frame, text="No file imported", foreground="#888888")
        self.info_label.pack(pady=(20, 10))

        ttk.Separator(params_frame, orient="horizontal").pack(fill="x", padx=20, pady=10)

        ttk.Label(params_frame, text="Compression level:").pack(pady=(5, 8))
        self.level = tk.StringVar(value="none")
        for label, desc, value in LEVELS:
            row = ttk.Frame(params_frame)
            row.pack(anchor="w", padx=60, pady=3)
            ttk.Radiobutton(row, text=label, variable=self.level, value=value, width=10).pack(side="left")
            ttk.Label(row, text=desc, foreground="#888888").pack(side="left", padx=5)

        ttk.Separator(params_frame, orient="horizontal").pack(fill="x", padx=20, pady=10)

        ttk.Label(params_frame, text="Output format:").pack(pady=(5, 8))
        self.fmt = tk.StringVar(value="pdf")
        for label, desc, value in FORMATS:
            row = ttk.Frame(params_frame)
            row.pack(anchor="w", padx=60, pady=3)
            ttk.Radiobutton(row, text=label, variable=self.fmt, value=value, width=10).pack(side="left")
            ttk.Label(row, text=desc, foreground="#888888").pack(side="left", padx=5)

    # ── FILE ACTIONS ──────────────────────────────────────────

    def import_files(self):
        path = FM.import_files(multiple=False, fileType=FT.PDF)
        if not path:
            return
        self.pdf_path = path
        size_kb = os.path.getsize(path) // 1024
        name    = os.path.basename(path)
        self.info_label.config(
            text=f"{name}  ({size_kb} KB)",
            foreground="#333333"
        )

    def export_file(self):
        if not self.pdf_path:
            messagebox.showwarning("Warning", "Please import a PDF file first.")
            return

        fmt = self.fmt.get()
        file_type = {"pdf": FT.PDF, "zip": FT.ZIP, "tgz": FT.TGZ}[fmt]
        output_path = FM.export_file(default_name="compressed", fileType=file_type)
        if not output_path:
            return
        self._compress(output_path, fmt)

    # ── CORE LOGIC ────────────────────────────────────────────

    def _compress(self, output_path, fmt):
        try:
            level = self.level.get()

            # step 1 — build PDF bytes (original or compressed)
            if level == "none":
                with open(self.pdf_path, "rb") as f:
                    pdf_bytes = f.read()

                def write_pdf(dest):
                    with open(dest, "wb") as f:
                        f.write(pdf_bytes)

                def get_pdf_bytes():
                    return pdf_bytes
            else:
                reader = PdfReader(self.pdf_path)
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)

                writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)
                if level in ("medium", "maximum"):
                    for page in writer.pages:
                        page.compress_content_streams()
                if level == "maximum":
                    writer.remove_images()

                def write_pdf(dest):
                    with open(dest, "wb") as f:
                        writer.write(f)

                def get_pdf_bytes():
                    buf = io.BytesIO()
                    writer.write(buf)
                    return buf.getvalue()

            # step 2 — write to final format
            if fmt == "pdf":
                write_pdf(output_path)
                out_size_kb = os.path.getsize(output_path) // 1024

            elif fmt == "zip":
                pdf_name = os.path.splitext(os.path.basename(output_path))[0] + ".pdf"
                with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    zf.writestr(pdf_name, get_pdf_bytes())
                out_size_kb = os.path.getsize(output_path) // 1024

            elif fmt == "tgz":
                pdf_name = os.path.splitext(os.path.basename(output_path))[0] + ".pdf"
                data = get_pdf_bytes()
                with tarfile.open(output_path, "w:gz") as tf:
                    info = tarfile.TarInfo(name=pdf_name)
                    info.size = len(data)
                    tf.addfile(info, io.BytesIO(data))
                out_size_kb = os.path.getsize(output_path) // 1024

            original_kb = os.path.getsize(self.pdf_path) // 1024
            saved       = max(0, original_kb - out_size_kb)
            messagebox.showinfo(
                "Success",
                f"File exported to:\n{output_path}\n\n"
                f"Original: {original_kb} KB  →  Output: {out_size_kb} KB  (saved {saved} KB)"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error during compression:\n{str(e)}")
