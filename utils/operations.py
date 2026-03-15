class Operations:
    """Registry of all available PDF operations shown on the home page."""

    operations = [
        ("🔗", "Merge PDF",     "Combine PDFs in the order you want",        "merge_pdf",    "MergePDF"),
        ("✂️", "Split PDF",     "Separate one page or a whole set",           "split_pdf",    "SplitPDF"),
        ("📦", "Compress PDF",  "Reduce file size while optimising quality",  "compress_pdf", "CompressPDF"),
        ("📝", "PDF to Word",   "Easily convert your PDF files to Word",      "pdf_to_word",  "PDFtoWord"),
        ("📄", "Word to PDF",   "Make DOC and DOCX files easy to read",       "word_to_pdf",  "WordToPDF"),
        ("🔄", "Rotate PDF",    "Rotate your PDFs the way you need them",     "rotate_pdf",   "RotatePDF"),
    ]

    IMPORT_PDF = "📂 Import PDF"
    EXPORT_PDF = "💾 Export PDF"
