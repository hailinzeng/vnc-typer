# vnc-typer

`vnc-typer` is a small desktop tool for typing text into VNC sessions that do not support clipboard paste.

中文：向不支持剪贴板粘贴的 VNC 会话输入文本。

## Features

- Send typed text to a VNC server.
- Send the contents of a selected text file.
- Copy selected file content into the input box before sending.
- Preserve line breaks by sending `Return` key events between lines.
- Optional VNC password support.
- Chinese and English interface languages.

## Requirements

- Python 3
- Tkinter
- `pyperclip`
- `vncdotool`

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

If Tkinter is missing, install it through your Python distribution or system package manager.

## Usage

Run the app from the project root:

```bash
python3 main.py
```

In the app:

1. Enter the VNC server IP address.
2. Enter the VNC port, usually `5900`.
3. Enter the VNC password if needed.
4. Type text into the input box, paste from the clipboard, or choose a file.
5. Click the send button for text or file content.

Use the language selector in the top-right corner to switch between Chinese and English.

## Notes

The app calls the `vncdo` command installed by `vncdotool`. On Windows, it also checks for `vncdo.exe` under the active Python environment's `Scripts` directory.

For a quick command-line check, run:

```bash
vncdo --help
```

## Responsible Use

Use this tool only with VNC servers and systems you are authorized to access. Do not use it to send confidential data to unapproved environments. Follow your organization's policies for remote access, automation, and credential handling.

## Releases

GitHub Actions builds release downloads when you push a version tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The release workflow creates downloadable archives for macOS, Linux, and Windows. Each archive includes the `vnc-typer` app and a bundled `vncdo` command built from `vncdotool`.

## Project Files

- `main.py` - Tkinter application.
- `icon.png` - Window icon.
- `requirements.txt` - Python runtime dependencies.
- `vncdo_launcher.py` - Release-build entry point for the bundled `vncdo` command.
