[← Back to Profile](https://github.com/vlonfat)

# myFriendPDF

Every tool you need to work with PDFs in one place.

## Features

- **Merge PDF** — Combine multiple PDFs in the order you want, page range by page range
- **Split PDF** — Extract a page range or split every page into individual files
- **Compress PDF** — Reduce file size with multiple compression levels, export as PDF, ZIP or TGZ
- **Rotate PDF** — Rotate all pages, a range, or a custom selection
- **PDF to Word** — Convert PDF files to editable .docx
- **Word to PDF** — Convert .docx files to PDF

## Download

Go to the [Releases](../../releases) page and download the executable for your platform:

| Platform | File |
|---|---|
| macOS | `myFriendPDF` |
| Windows | `myFriendPDF.exe` |
| Linux | `myFriendPDF` |

> **Word to PDF** requires Microsoft Word (macOS/Windows) or LibreOffice (Linux) to be installed.

### macOS — first launch

macOS may block the app with a Gatekeeper warning. Open a Terminal in the folder where `myFriendPDF.app` is located and run:

```bash
xattr -cr myFriendPDF.app
```

Then double-click `myFriendPDF.app` to open it normally.

## Run from source

```bash
git clone git@github.com:vlonfat/myFriendPDF.git
cd myFriendPD
pip install -r requirements.txt
python main.py
```

## License

GPL-3.0 — see [LICENSE](LICENSE)

## Credits

App icon by [Roman Káčerek](https://www.flaticon.com)
