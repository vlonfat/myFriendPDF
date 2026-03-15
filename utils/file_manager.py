from tkinter import filedialog
from .constants import FileTypes


class FileManager:
    """Generic file import/export handler used by all operation pages."""

    @staticmethod
    def import_files(multiple=True, fileType=FileTypes.PDF):
        """
        Opens a file picker dialog.

        Args:
            multiple (bool): True  → returns a tuple of paths
                             False → returns a single path (str)
            fileType (tuple): extension filter, defaults to FileTypes.PDF

        Returns:
            tuple[str] | str | None if cancelled
        """
        if multiple:
            return filedialog.askopenfilenames(filetypes=fileType)
        else:
            return filedialog.askopenfilename(filetypes=fileType)

    @staticmethod
    def export_file(default_name="output", fileType=FileTypes.PDF):
        """
        Opens a save-as dialog.

        Args:
            default_name (str): pre-filled filename, defaults to "output"
            fileType (tuple):   extension filter, defaults to FileTypes.PDF

        Returns:
            str | None if cancelled
        """
        path = filedialog.asksaveasfilename(
            defaultextension=fileType[0][1].replace("*", ""),
            filetypes=fileType,
            initialfile=default_name
        )
        return path if path else None

    @staticmethod
    def select_directory():
        """
        Opens a folder picker dialog.

        Returns:
            str | None if cancelled
        """
        path = filedialog.askdirectory()
        return path if path else None

    @staticmethod
    def parse_page(value):
        """
        Converts a page field value to int, or None if empty.

        Args:
            value (str): value from an Entry widget

        Returns:
            int | None
        """
        value = value.strip()
        return int(value) if value.isdigit() else None
