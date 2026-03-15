import tkinter as tk
from tkinter import ttk, messagebox
import os
from utils import Constant as Cst
from utils import FileManager as FM
from utils import FileTypes as FT
from utils import BaseOperation
from pypdf import PdfWriter, PdfReader


MAX_SEGMENTS = 13


class MergePDF(BaseOperation):

    def __init__(self, params_frame, btn_import, btn_export):
        self.files    = {}
        self.segments = []
        super().__init__(params_frame, btn_import, btn_export)

    # ── UI ────────────────────────────────────────────────────

    def _build_ui(self, params_frame):
        self._build_file_library(params_frame)
        self._build_separator(params_frame)
        self._build_segments(params_frame)

    def _build_file_library(self, parent):
        """Zone 1 — imported files library."""
        ttk.Label(parent, text="Imported files:").pack(pady=(10, 5))

        self.file_list = tk.Listbox(
            parent, height=4, bg="white", fg="#333333",
            relief="solid", borderwidth=1, highlightthickness=0,
            selectbackground=Cst.HEADER_BACKGROUND, selectforeground="white"
        )
        self.file_list.pack(fill="x", padx=20)

        ttk.Button(parent, text="✕ Remove", command=self._remove_file).pack(pady=5)

    def _build_segments(self, parent):
        """Zone 2 — merge segments."""
        ttk.Label(parent, text="Merge segments:").pack(pady=(0, 5))

        self.segments_frame = tk.Frame(parent, bg=Cst.BG)
        self.segments_frame.pack(fill="x", padx=20)

        self.btn_add_segment = ttk.Button(parent, text="+ Add segment", command=self._add_segment)
        self.btn_add_segment.pack(pady=10)

    def _build_separator(self, parent):
        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=20, pady=15)

    def _on_combo_change(self, combo, label_pages):
        """Update the min/max label when the user changes the selected file."""
        name = combo.get()
        info = self.files[name]
        label_pages.config(text=f"pages (1 to {info['page_max']})")

    def _add_segment(self):
        if not self.files:
            messagebox.showwarning("Warning", "Please import at least one PDF file first.")
            return
        if len(self.segments) >= MAX_SEGMENTS:
            messagebox.showwarning("Warning", f"Maximum {MAX_SEGMENTS} segments allowed.")
            return

        row = tk.Frame(self.segments_frame, bg=Cst.BG)
        row.pack(fill="x", pady=3)

        combo = ttk.Combobox(row, values=list(self.files.keys()), state="readonly", width=20)
        combo.current(0)
        combo.pack(side="left", padx=5)

        # dynamic label showing "pages (1 to X)"
        label_pages = ttk.Label(row, text="", background=Cst.BG)
        label_pages.pack(side="left")

        entry_start = ttk.Entry(row, width=5)
        entry_start.pack(side="left", padx=3)
        ttk.Label(row, text="to", background=Cst.BG).pack(side="left")
        entry_end = ttk.Entry(row, width=5)
        entry_end.pack(side="left", padx=3)

        # update label immediately for the default file, then on each change
        combo.bind("<<ComboboxSelected>>", lambda _: self._on_combo_change(combo, label_pages))
        self._on_combo_change(combo, label_pages)

        idx = len(self.segments)
        ttk.Button(row, text="▲", width=3, command=lambda i=idx: self._move_segment_up(i)).pack(side="left", padx=2)
        ttk.Button(row, text="▼", width=3, command=lambda i=idx: self._move_segment_down(i)).pack(side="left", padx=2)
        ttk.Button(row, text="✕", width=3, command=lambda r=row, i=idx: self._remove_segment(r, i)).pack(side="left", padx=2)

        self.segments.append({
            "filename":   combo,
            "page_start": entry_start,
            "page_end":   entry_end,
            "row":        row
        })

        if len(self.segments) >= MAX_SEGMENTS:
            self.btn_add_segment.pack_forget()

    # ── FILE ACTIONS ──────────────────────────────────────────

    def import_files(self):
        files = FM.import_files(multiple=True, fileType=FT.PDF)
        for f in files:
            name = os.path.basename(f)
            if name not in self.files:
                reader = PdfReader(f)
                self.files[name] = {
                    "path":     f,
                    "page_min": 1,
                    "page_max": len(reader.pages)
                }
                self.file_list.insert("end", f"{name} ({len(reader.pages)} pages)")
                self._refresh_combos()

    def _remove_file(self):
        idx = self.file_list.curselection()
        if not idx:
            return
        full_text = self.file_list.get(idx[0])
        name = full_text.split(" (")[0]  # strip "(X pages)" suffix
        self.file_list.delete(idx[0])
        del self.files[name]
        self._refresh_combos()

    def _refresh_combos(self):
        """Update all comboboxes with the current file list."""
        for segment in self.segments:
            segment["filename"]["values"] = list(self.files.keys())

    # ── SEGMENT ACTIONS ───────────────────────────────────────

    def _remove_segment(self, row, idx):
        """Remove a segment from the UI and from self.segments."""
        row.destroy()
        self.segments.pop(idx)
        if len(self.segments) < MAX_SEGMENTS:
            self.btn_add_segment.pack(pady=10)

    def _move_segment_up(self, idx):
        """Move a segment one position up."""
        if idx == 0:
            return
        self.segments[idx], self.segments[idx - 1] = self.segments[idx - 1], self.segments[idx]
        self._rebuild_segments_ui()

    def _move_segment_down(self, idx):
        """Move a segment one position down."""
        if idx == len(self.segments) - 1:
            return
        self.segments[idx], self.segments[idx + 1] = self.segments[idx + 1], self.segments[idx]
        self._rebuild_segments_ui()

    def _rebuild_segments_ui(self):
        """Rebuild the segments UI after a reorder."""
        saved = []
        for s in self.segments:
            saved.append({
                "filename":   s["filename"].get(),
                "page_start": s["page_start"].get(),
                "page_end":   s["page_end"].get()
            })

        for s in self.segments:
            s["row"].destroy()
        self.segments.clear()

        for s in saved:
            self._add_segment()
            self.segments[-1]["filename"].set(s["filename"])
            self.segments[-1]["page_start"].insert(0, s["page_start"])
            self.segments[-1]["page_end"].insert(0, s["page_end"])

    # ── EXPORT ────────────────────────────────────────────────

    def export_file(self):
        """Open a save dialog then run the merge. Does nothing if cancelled or validation fails."""
        if not self._validate():
            return
        output_path = FM.export_file(default_name="merged")
        if not output_path:
            return
        self._merge(output_path)

    # ── CORE LOGIC ────────────────────────────────────────────

    def _merge(self, output_path):
        """
        Merge segments in order and write the result to output_path.

        Args:
            output_path (str): destination file path
        """
        try:
            writer = PdfWriter()

            for segment in self.segments:
                filename = segment["filename"].get()
                file     = self.files[filename]
                reader   = PdfReader(file["path"])
                start    = FM.parse_page(segment["page_start"].get())
                end      = FM.parse_page(segment["page_end"].get())

                if start and end:
                    for i in range(start - 1, end):
                        writer.add_page(reader.pages[i])
                else:
                    for page in reader.pages:
                        writer.add_page(page)

            with open(output_path, "wb") as f:
                writer.write(f)

            messagebox.showinfo("Success", f"Merged PDF exported to:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Error during merge:\n{str(e)}")

    # ── VALIDATION ────────────────────────────────────────────

    def _validate(self):
        if len(self.files) < 2:
            messagebox.showwarning("Warning", "Please import at least two PDFs.")
            return False
        if len(self.segments) < 1:
            messagebox.showwarning("Warning", "Please add at least one segment.")
            return False
        for segment in self.segments:
            try:
                start = FM.parse_page(segment["page_start"].get())
                end   = FM.parse_page(segment["page_end"].get())
                if start and end and start > end:
                    messagebox.showwarning("Warning", f"Page start > page end in segment '{segment['filename'].get()}'.")
                    return False
            except tk.TclError:
                messagebox.showerror("Error", "A segment is invalid, please remove and recreate it.")
                return False
        return True
