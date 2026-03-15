import tkinter as tk


class FlatButton(tk.Frame):
    """
    A fully styleable button using Frame + Label.

    tk.Button ignores most styling on macOS. This class uses a tk.Frame
    (background / border) with a tk.Label inside (text), giving full
    visual control on every platform.

    Supports .config(command=...) as a drop-in for tk.Button / ttk.Button.

    Args:
        parent:       parent widget
        text:         button label
        bg:           normal background
        fg:           normal foreground
        hover_bg:     background on mouse-over
        hover_fg:     foreground on mouse-over (defaults to fg)
        font:         font tuple
        border_color: if set, draws a 1px border (outlined style)
        padx/pady:    inner padding (defaults 24 / 10)
    """

    def __init__(self, parent, text, bg, fg, hover_bg,
                 hover_fg=None, font=("Arial", 11), border_color=None,
                 padx=24, pady=10):
        border_kw = {"highlightbackground": border_color, "highlightthickness": 1} \
                    if border_color else {"highlightthickness": 0}

        super().__init__(parent, bg=bg, cursor="hand2", **border_kw)

        self._command  = None
        self._bg       = bg
        self._fg       = fg
        self._hover_bg = hover_bg
        self._hover_fg = hover_fg or fg

        self._label = tk.Label(
            self, text=text, bg=bg, fg=fg,
            font=font, cursor="hand2", padx=padx, pady=pady
        )
        self._label.pack()

        for w in (self, self._label):
            w.bind("<Enter>",    lambda _: self._set_colors(self._hover_bg, self._hover_fg))
            w.bind("<Leave>",    lambda _: self._set_colors(self._bg, self._fg))
            w.bind("<Button-1>", lambda _: self._on_click())

    def _set_colors(self, bg, fg):
        self.configure(bg=bg)
        self._label.configure(bg=bg, fg=fg)

    def _on_click(self):
        if self._command:
            self._command()

    def config(self, **kwargs):
        if "command" in kwargs:
            self._command = kwargs.pop("command")
        if "text" in kwargs:
            self._label.configure(text=kwargs.pop("text"))
        if kwargs:
            super().config(**kwargs)

    configure = config
