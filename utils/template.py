from abc import ABC, abstractmethod


class BaseOperation(ABC):
    """
    Base class for all PDF operations.

    Each operation receives the shared UI shell (params_frame, btn_import,
    btn_export) and is responsible for building its own UI and handling
    import/export logic.

    Subclass contract:
        - Call super().__init__() AFTER initialising any instance state
          that _build_ui() depends on.
        - Implement _build_ui(), import_files(), and export_file().

    Example:
        class MyOperation(BaseOperation):
            def __init__(self, params_frame, btn_import, btn_export):
                self.my_state = {}          # init state first
                super().__init__(params_frame, btn_import, btn_export)

            def _build_ui(self, params_frame):
                ttk.Label(params_frame, text="My Operation").pack()

            def import_files(self):
                files = FM.import_files()
                # process files...

            def export_file(self):
                path = FM.export_file(default_name="output")
                if path:
                    # write output...
                    pass
    """

    def __init__(self, params_frame, btn_import, btn_export):
        self._build_ui(params_frame)
        btn_import.config(command=self.import_files)
        btn_export.config(command=self.export_file)

    @abstractmethod
    def _build_ui(self, params_frame):
        """Build the operation UI inside params_frame."""
        ...

    @abstractmethod
    def import_files(self):
        """Handle file import (triggered by the Import button)."""
        ...

    @abstractmethod
    def export_file(self):
        """Handle file export (triggered by the Export button)."""
        ...
