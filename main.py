import tkinter as tk
from tkinter import ttk
import importlib
from utils import Constant as Cst
from utils import Operations as Op
from utils import Version 
from utils import FlatButton
from pages.op_page import OpPage


def main():
    root = tk.Tk()
    root.geometry(Cst.DEFAULT_RESOLUTION)
    root.resizable(True, True)
    root.configure(background=Cst.BG)
    root.title("myFriendPdf " + Version.version)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    try:
        _icon = tk.PhotoImage(file=Cst.ICON_PATH)
        root.iconphoto(True, _icon)
    except Exception:
        pass  # icon not found, use system default

    # ── GLOBAL STYLES ─────────────────────────────────────────
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TFrame",        background=Cst.BG)
    style.configure("TLabel",        background=Cst.BG, foreground=Cst.TEXT_PRIMARY)
    style.configure("TRadiobutton",  background=Cst.BG, foreground=Cst.TEXT_PRIMARY)
    style.configure("TCheckbutton",  background=Cst.BG, foreground=Cst.TEXT_PRIMARY)
    style.configure("TSeparator",    background="#e0e0e0")
    style.configure("TEntry",        fieldbackground="white", borderwidth=1, relief="solid")
    style.configure("TCombobox",     fieldbackground="white", borderwidth=1)

    style.configure("Header.TFrame", background=Cst.HEADER_BACKGROUND)
    style.configure("Header.TLabel", background=Cst.HEADER_BACKGROUND,
                    foreground="white", font=("Arial", 24, "bold"))
    style.configure("Subtitle.TLabel", background=Cst.BG,
                    foreground=Cst.TEXT_MUTED, font=("Arial", 12))

    style.configure("TButton",
                    background=Cst.CARD_BG, foreground=Cst.TEXT_PRIMARY,
                    font=("Arial", 10), borderwidth=0, relief="flat", padding=(12, 6))
    style.map("TButton",
              background=[("active", Cst.CARD_HOVER), ("pressed", "#dedede")])

    # ── ABOUT DIALOG ──────────────────────────────────────────
    def show_about():
        win = tk.Toplevel(root)
        win.title("About")
        win.resizable(False, False)
        win.configure(bg=Cst.BG)
        win.grab_set()

        tk.Label(win, text="myFriendPdf", font=("Arial", 18, "bold"),
                 bg=Cst.BG, fg=Cst.TEXT_PRIMARY).pack(pady=(30, 4))
        tk.Label(win, text=Version.version, font=("Arial", 11),
                 bg=Cst.BG, fg=Cst.TEXT_MUTED).pack()

        tk.Frame(win, bg="#e0e0e0", height=1).pack(fill="x", padx=30, pady=20)

        tk.Label(win, text="Every tool you need to work with PDFs in one place.",
                 font=("Arial", 10), bg=Cst.BG, fg=Cst.TEXT_MUTED,
                 wraplength=260, justify="center").pack(padx=30)

        tk.Frame(win, bg="#e0e0e0", height=1).pack(fill="x", padx=30, pady=20)

        tk.Label(win, text="Credits", font=("Arial", 11, "bold"),
                 bg=Cst.BG, fg=Cst.TEXT_PRIMARY).pack()
        tk.Label(win, text="App icon by Roman Káčerek",
                 font=("Arial", 10), bg=Cst.BG, fg=Cst.TEXT_MUTED).pack(pady=(6, 0))

        close_btn = FlatButton(win, text="Close",
                               bg=Cst.HEADER_BACKGROUND, fg="white", hover_bg="#c41c23",
                               font=("Arial", 10, "bold"))
        close_btn.config(command=win.destroy)
        close_btn.pack(pady=30)

        win.update_idletasks()
        x = root.winfo_x() + (root.winfo_width()  - win.winfo_width())  // 2
        y = root.winfo_y() + (root.winfo_height() - win.winfo_height()) // 2
        win.geometry(f"+{x}+{y}")

    # ── HOME PAGE ─────────────────────────────────────────────
    container = ttk.Frame(root)
    container.grid(row=0, column=0, sticky="nsew")
    container.rowconfigure(2, weight=1)
    container.columnconfigure(0, weight=1)

    header = ttk.Frame(container, style="Header.TFrame")
    header.grid(row=0, column=0, sticky="ew")
    header.columnconfigure(0, weight=1)
    ttk.Label(header, text="myFriendPdf", style="Header.TLabel", anchor="center").grid(
        row=0, column=0, pady=20
    )
    about_btn = tk.Label(header, text="?", font=("Arial", 13, "bold"),
                         bg=Cst.HEADER_BACKGROUND, fg="white", cursor="hand2",
                         padx=14, pady=6)
    about_btn.place(relx=1.0, rely=0.5, anchor="e")
    about_btn.bind("<Button-1>", lambda _: show_about())

    ttk.Label(
        container,
        text="Every tool you need to work with PDFs in one place",
        style="Subtitle.TLabel",
        anchor="center"
    ).grid(row=1, column=0, pady=18)

    canvas = tk.Canvas(container, bg=Cst.BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(row=2, column=0, sticky="nsew")
    scrollbar.grid(row=2, column=1, sticky="ns")

    home = ttk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=home, anchor="nw")

    def on_canvas_resize(event):  # noqa: ANN001
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", on_canvas_resize)

    def on_frame_resize(_):
        canvas.configure(scrollregion=canvas.bbox("all"))
    home.bind("<Configure>", on_frame_resize)

    def on_mousewheel(event):  # noqa: ANN001
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # ── OPERATION PAGE ────────────────────────────────────────
    op_page = OpPage(root, on_back=lambda: container.tkraise())
    op_page.grid(row=0, column=0, sticky="nsew")

    # ── NAVIGATION ────────────────────────────────────────────
    def show_operation(title, module_name, class_name):
        module = importlib.import_module(f"pages.operations.{module_name}")
        operation_class = getattr(module, class_name)
        op_page.load(title, operation_class)
        op_page.tkraise()

    # ── OPERATION CARDS GRID ──────────────────────────────────
    cols = 3
    for i, (icon, title, desc, module_name, class_name) in enumerate(Op.operations):
        r, c = divmod(i, cols)
        home.columnconfigure(c, weight=1)

        card = tk.Frame(home, bg=Cst.CARD_BG, relief="flat", borderwidth=0,
                        width=220, height=180)
        card.grid(row=r, column=c, padx=16, pady=16)
        card.grid_propagate(False)
        card.columnconfigure(0, weight=1)
        card.rowconfigure(0, weight=1)
        card.rowconfigure(1, weight=1)
        card.rowconfigure(2, weight=1)

        tk.Label(card, text=icon, font=("Arial", 30), bg=Cst.CARD_BG,
                 anchor="center").grid(row=0, column=0, sticky="ew", pady=(20, 4))
        tk.Label(card, text=title, font=("Arial", 11, "bold"),
                 fg=Cst.TEXT_PRIMARY, bg=Cst.CARD_BG, anchor="center").grid(
                     row=1, column=0, sticky="ew", pady=4)
        tk.Label(card, text=desc, font=("Arial", 9),
                 fg=Cst.TEXT_MUTED, bg=Cst.CARD_BG, anchor="center",
                 wraplength=175).grid(row=2, column=0, sticky="ew", pady=(0, 20))

        all_widgets = [card] + list(card.winfo_children())
        for w in all_widgets:
            w.configure(cursor="hand2")
            w.bind("<Enter>", lambda _, widgets=all_widgets: [
                x.configure(bg=Cst.CARD_HOVER) for x in widgets])
            w.bind("<Leave>", lambda _, widgets=all_widgets: [
                x.configure(bg=Cst.CARD_BG) for x in widgets])
            w.bind("<Button-1>", lambda _, t=title, m=module_name, cn=class_name:
                   show_operation(t, m, cn))

    container.tkraise()
    root.mainloop()


if __name__ == "__main__":
    main()
