# Third-Party Notices

`vnc-typer` is licensed under the MIT License. Runtime dependencies are installed from `requirements.txt` by the source launchers.

## Current Runtime Dependencies

- `pyperclip` - clipboard helper library.
- `vncdotool` - VNC automation library and `vncdo` command provider.
- `tkinter` / Tk - GUI toolkit provided by the user's Python/system installation.

`vncdotool` installs additional transitive dependencies such as Twisted, Pillow, cryptography, cffi, attrs, hyperlink, incremental, and zope.interface. Review installed package metadata in the generated `.venv` for exact versions and license texts.

## Planned GUI Migration Candidate

- `PySide6` - official Qt for Python bindings.

`PySide6` is not currently required by this Tkinter version and is intentionally not listed in `requirements.txt`. If the project migrates to PySide6 later, the source launcher model should keep PySide6/Qt as dynamically installed runtime dependencies rather than bundling them into a frozen executable.
