#!/usr/bin/env python3
"""vnc-typer - Send text or file content via vncdotool"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyperclip
import os
import subprocess
import threading
import sys
import locale
import json
from pathlib import Path

try:
    from version import APP_VERSION
except ImportError:
    APP_VERSION = os.environ.get("VNC_TYPER_VERSION", "dev")

APP_NAME = "vnc-typer"
PROJECT_URL = "https://github.com/hailinzeng/vnc-typer"

# === Theme Colors ===
BG_DARK = "#181a20"
BG_PANEL = "#22252d"
BG_INPUT = "#111318"
FG_MAIN = "#e6e8ee"
FG_DIM = "#9aa3b2"
FG_ACCENT = "#60a5fa"
FG_GREEN = "#16a34a"
FG_RED = "#dc2626"

ACCENT = "#2563eb"
BTN_BG = "#374151"
BTN_HOVER = "#4b5563"
BTN_PRIMARY = "#2563eb"
BTN_PRIMARY_HOVER = "#1d4ed8"
PANEL_BG = "#22252d"
STATUS_BG = "#111318"
LABEL_COLOR = "#9aa3b2"

FONT_MAIN = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_MONO = ("Consolas", 10)

LANGUAGE_NAMES = {
    "zh": "中文",
    "en": "English",
}

TEXT = {
    "zh": {
        "subtitle": "通过 vncdotool 向 VNC 服务器发送文本",
        "language": "语言",
        "about": "关于",
        "about_title": "关于 vnc-typer",
        "about_message": (
            "vnc-typer {version}\n\n"
            "向不支持剪贴板粘贴的 VNC 会话输入文本。\n\n"
            "{url}\n\n"
            "请仅在授权的 VNC 服务器和系统上使用。"
        ),
        "file_selection": "文件",
        "choose_file": "选择文件",
        "copy_to_input": "复制到输入框",
        "text_input": "文本输入",
        "paste": "粘贴",
        "clear": "清空",
        "copy": "复制",
        "input_hint": "提示：支持中英文混合输入",
        "vnc_config": "连接",
        "ip_address": "IP 地址",
        "port": "端口",
        "password": "密码",
        "send_text": "发送文本",
        "send_file": "发送文件内容",
        "ready": "就绪",
        "no_file": "未选择文件",
        "vnc_ip_tip": "VNC 服务器 IP",
        "vnc_port_tip": "VNC 端口，默认 5900",
        "vnc_password_tip": "VNC 密码（可选）",
        "selected_file": "已选择: {name}",
        "choose_file_warning": "请先选择文件",
        "warning_title": "警告",
        "file_copied": "已复制 {name} 的内容到输入框",
        "read_file_failed": "读取文件失败: {error}",
        "error_title": "错误",
        "pasted": "已粘贴",
        "paste_failed": "粘贴失败: {error}",
        "cleared": "已清空",
        "copied": "已复制到剪贴板",
        "empty_input": "输入框为空",
        "missing_ip": "请输入 VNC 服务器 IP 地址",
        "missing_port": "请输入 VNC 端口",
        "sending": "正在发送...",
        "send_success": "发送成功",
        "send_failed": "发送失败",
        "vnc_error_title": "VNC 错误",
        "unknown_error": "未知错误",
        "send_timeout": "发送超时 (30秒)",
        "timeout_title": "超时",
        "timeout_message": "VNC 命令执行超时",
        "vncdo_missing_status": "未找到 vncdo，请安装 vncdotool: pip install vncdotool",
        "vncdo_missing_message": "未找到 vncdo 命令，请安装 vncdotool",
        "config_error_title": "配置错误",
        "enter_text_warning": "请输入要发送的文本",
        "empty_file_warning": "文件内容为空",
        "sending_file": "发送文件: {name}",
    },
    "en": {
        "subtitle": "Send text to a VNC server through vncdotool",
        "language": "Language",
        "about": "About",
        "about_title": "About vnc-typer",
        "about_message": (
            "vnc-typer {version}\n\n"
            "Type text into VNC sessions that do not support clipboard paste.\n\n"
            "{url}\n\n"
            "Use only with VNC servers and systems you are authorized to access."
        ),
        "file_selection": "File",
        "choose_file": "Choose File",
        "copy_to_input": "Copy to Input",
        "text_input": "Text Input",
        "paste": "Paste",
        "clear": "Clear",
        "copy": "Copy",
        "input_hint": "Tip: mixed Chinese and English input is supported",
        "vnc_config": "Connection",
        "ip_address": "IP Address",
        "port": "Port",
        "password": "Password",
        "send_text": "Send Text",
        "send_file": "Send File Content",
        "ready": "Ready",
        "no_file": "No file selected",
        "vnc_ip_tip": "VNC server IP",
        "vnc_port_tip": "VNC port, default 5900",
        "vnc_password_tip": "VNC password (optional)",
        "selected_file": "Selected: {name}",
        "choose_file_warning": "Choose a file first",
        "warning_title": "Warning",
        "file_copied": "Copied {name} into the input box",
        "read_file_failed": "Failed to read file: {error}",
        "error_title": "Error",
        "pasted": "Pasted",
        "paste_failed": "Paste failed: {error}",
        "cleared": "Cleared",
        "copied": "Copied to clipboard",
        "empty_input": "Input box is empty",
        "missing_ip": "Enter the VNC server IP address",
        "missing_port": "Enter the VNC port",
        "sending": "Sending...",
        "send_success": "Sent successfully",
        "send_failed": "Send failed",
        "vnc_error_title": "VNC Error",
        "unknown_error": "Unknown error",
        "send_timeout": "Send timed out (30 seconds)",
        "timeout_title": "Timeout",
        "timeout_message": "The VNC command timed out",
        "vncdo_missing_status": "vncdo not found. Install vncdotool: pip install vncdotool",
        "vncdo_missing_message": "vncdo command not found. Install vncdotool",
        "config_error_title": "Config Error",
        "enter_text_warning": "Enter text to send",
        "empty_file_warning": "File content is empty",
        "sending_file": "Sending file: {name}",
    },
}


def default_language():
    language = locale.getlocale()[0] or ""
    return "zh" if language.lower().startswith("zh") else "en"


def config_path():
    if os.name == "nt":
        base_dir = os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming"
    elif sys.platform == "darwin":
        base_dir = Path.home() / "Library" / "Application Support"
    else:
        base_dir = os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config"
    return Path(base_dir) / APP_NAME / "config.json"


def load_preferences():
    try:
        with config_path().open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}

    prefs = {}
    if data.get("language") in TEXT:
        prefs["language"] = data["language"]
    if isinstance(data.get("ip"), str):
        prefs["ip"] = data["ip"]
    if isinstance(data.get("port"), str):
        prefs["port"] = data["port"]
    return prefs


def save_preferences(language, ip, port):
    path = config_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump({"language": language, "ip": ip, "port": port}, f, indent=2)
    except OSError:
        pass


def resource_path(name):
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, name)


def bundled_command(name):
    base_dir = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else __file__)
    exe_name = f"{name}.exe" if os.name == "nt" else name
    candidates = [
        os.path.join(base_dir, exe_name),
        os.path.join(base_dir, name, exe_name),
    ]
    for path in candidates:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    return None


class ToolTip:
    """Simple tooltip."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tooltip = tk.Toplevel()
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, bg=BTN_BG, fg=FG_MAIN,
                         font=("Segoe UI", 9), padx=8, pady=4, relief="solid", bd=1)
        label.pack()

    def hide(self, _event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class VNCTyperGUI:
    def __init__(self, root):
        self.root = root
        prefs = load_preferences()
        self.language = prefs.get("language", default_language())
        self.ip_value = prefs.get("ip", "")
        self.port_value = prefs.get("port", "5900")
        self.password_value = ""
        self.text_value = ""
        self.selected_file = tk.StringVar(value=self.t("no_file"))
        self.root.title(f"vnc-typer {APP_VERSION}")
        self.root.geometry("760x540")
        self.root.resizable(True, True)
        self.root.configure(bg=BG_DARK)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Window icon
        try:
            self.icon = tk.PhotoImage(file=resource_path("icon.png"))
            self.root.iconphoto(True, self.icon)
        except Exception:
            pass

        # Style ttk widgets
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._apply_ttk_style()

        self.create_widgets()

    def t(self, key, **kwargs):
        value = TEXT[self.language][key]
        return value.format(**kwargs) if kwargs else value

    def save_current_preferences(self):
        ip = self.ip_entry.get().strip() if hasattr(self, "ip_entry") else self.ip_value
        port = self.port_entry.get().strip() if hasattr(self, "port_entry") else self.port_value
        save_preferences(self.language, ip, port)

    def on_close(self):
        self.save_current_preferences()
        self.root.destroy()

    def change_language(self, _event=None):
        selected = self.language_var.get()
        language = next((code for code, name in LANGUAGE_NAMES.items() if name == selected), self.language)
        if language == self.language:
            return

        old_no_file = self.t("no_file")
        self.ip_value = self.ip_entry.get()
        self.port_value = self.port_entry.get()
        self.password_value = self.password_entry.get()
        self.text_value = self.text_area.get("1.0", "end-1c")
        no_file_selected = self.selected_file.get() == old_no_file

        self.language = language
        if no_file_selected:
            self.selected_file.set(self.t("no_file"))
        self.save_current_preferences()

        for child in self.root.winfo_children():
            child.destroy()
        self.create_widgets()

    def show_about(self):
        messagebox.showinfo(
            self.t("about_title"),
            self.t("about_message", version=APP_VERSION, url=PROJECT_URL),
        )

    def _apply_ttk_style(self):
        s = self.style
        s.configure("TFrame", background=BG_DARK)
        s.configure("Dark.TFrame", background=BG_DARK)
        s.configure("Panel.TLabelframe", background=PANEL_BG, foreground=FG_MAIN)
        s.configure("Panel.TLabelframe.Label", background=PANEL_BG, foreground=FG_ACCENT,
                    font=FONT_BOLD)
        s.configure("TLabel", background=BG_DARK, foreground=FG_MAIN, font=FONT_MAIN)
        s.configure("Dim.TLabel", foreground=LABEL_COLOR)
        s.configure("TEntry", fieldbackground=BG_INPUT, foreground=FG_MAIN,
                    insertcolor=FG_MAIN, borderwidth=0, padding=(6, 4))
        s.configure("TCombobox", fieldbackground=BG_INPUT, background=BTN_BG,
                    foreground=FG_MAIN, arrowcolor=FG_MAIN, borderwidth=0)
        s.configure("TButton", background=BTN_BG, foreground=FG_MAIN, font=FONT_BOLD,
                    borderwidth=0, padding=(10, 5))
        s.map("TButton",
              background=[("active", BTN_HOVER), ("pressed", BTN_BG)],
              foreground=[("active", FG_MAIN)])
        s.configure("File.TButton", background=BTN_BG, foreground=FG_MAIN, font=FONT_BOLD,
                    borderwidth=0, padding=(8, 5))
        s.map("File.TButton", background=[("active", BTN_HOVER), ("pressed", BTN_BG)])

    def _btn(self, parent, text, cmd, style="TButton", side="left", **kwargs):
        btn = ttk.Button(parent, text=text, command=cmd, style=style)
        btn.pack(side=side, padx=4, pady=2, **kwargs)
        return btn

    def create_widgets(self):
        # === Header ===
        header = tk.Frame(self.root, bg=BG_DARK)
        header.pack(fill="x", padx=18, pady=(14, 6))

        tk.Label(header, text="vnc-typer", font=FONT_TITLE, fg=FG_MAIN,
                 bg=BG_DARK).pack(side="left")
        tk.Label(header, text=self.t("subtitle"), font=FONT_MAIN,
                 fg=LABEL_COLOR, bg=BG_DARK).pack(side="left", padx=(14, 0))
        lang_box = tk.Frame(header, bg=BG_DARK)
        lang_box.pack(side="right")
        ttk.Button(lang_box, text=self.t("about"), command=self.show_about).pack(side="left", padx=(0, 12))
        tk.Label(lang_box, text=self.t("language"), font=FONT_MAIN,
                 fg=LABEL_COLOR, bg=BG_DARK).pack(side="left", padx=(0, 8))
        self.language_var = tk.StringVar(value=LANGUAGE_NAMES[self.language])
        language_menu = ttk.Combobox(lang_box, textvariable=self.language_var,
                                     values=list(LANGUAGE_NAMES.values()), width=9,
                                     state="readonly")
        language_menu.pack(side="left")
        language_menu.bind("<<ComboboxSelected>>", self.change_language)

        tk.Frame(self.root, height=1, bg="#2f333d").pack(fill="x", padx=18, pady=(0, 8))

        # === Connection ===
        config_frame = ttk.LabelFrame(self.root, text=self.t("vnc_config"), style="Panel.TLabelframe")
        config_frame.pack(fill="x", padx=18, pady=(0, 6))

        inner_cfg = tk.Frame(config_frame, bg=PANEL_BG)
        inner_cfg.pack(fill="x", padx=10, pady=8)

        tk.Label(inner_cfg, text=self.t("ip_address"), font=FONT_BOLD, fg=FG_MAIN,
                 bg=PANEL_BG).pack(side="left", padx=(0, 8))
        self.ip_entry = tk.Entry(inner_cfg, font=FONT_MONO, bg=BG_INPUT, fg=FG_MAIN,
                                  insertbackground=FG_MAIN, relief="flat", bd=0,
                                  width=19, highlightthickness=1,
                                  highlightcolor=ACCENT, highlightbackground="#343946")
        self.ip_entry.insert(0, self.ip_value)
        self.ip_entry.pack(side="left", padx=(0, 16), ipady=3)
        self.ip_entry.bind("<FocusOut>", lambda _event: self.save_current_preferences())
        ToolTip(self.ip_entry, self.t("vnc_ip_tip"))

        tk.Label(inner_cfg, text=self.t("port"), font=FONT_BOLD, fg=FG_MAIN,
                 bg=PANEL_BG).pack(side="left", padx=(0, 8))
        self.port_entry = tk.Entry(inner_cfg, font=FONT_MONO, bg=BG_INPUT, fg=FG_MAIN,
                                    insertbackground=FG_MAIN, relief="flat", bd=0,
                                    width=8, highlightthickness=1,
                                    highlightcolor=ACCENT, highlightbackground="#343946")
        self.port_entry.insert(0, self.port_value)
        self.port_entry.pack(side="left", padx=(0, 16), ipady=3)
        self.port_entry.bind("<FocusOut>", lambda _event: self.save_current_preferences())
        ToolTip(self.port_entry, self.t("vnc_port_tip"))

        tk.Label(inner_cfg, text=self.t("password"), font=FONT_BOLD, fg=FG_MAIN,
                 bg=PANEL_BG).pack(side="left", padx=(0, 8))
        self.password_entry = tk.Entry(inner_cfg, font=FONT_MONO, bg=BG_INPUT, fg=FG_MAIN,
                                        insertbackground=FG_MAIN, relief="flat", bd=0,
                                        width=20, show="•", highlightthickness=1,
                                        highlightcolor=ACCENT, highlightbackground="#343946")
        self.password_entry.insert(0, self.password_value)
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=3)
        ToolTip(self.password_entry, self.t("vnc_password_tip"))

        # === File Selection ===
        file_frame = ttk.LabelFrame(self.root, text=self.t("file_selection"), style="Panel.TLabelframe")
        file_frame.pack(fill="x", padx=18, pady=(0, 6))

        inner_file = tk.Frame(file_frame, bg=PANEL_BG)
        inner_file.pack(fill="x", padx=10, pady=8)

        self._btn(inner_file, self.t("choose_file"), self.select_file, "File.TButton")
        self._btn(inner_file, self.t("copy_to_input"), self.copy_file_content, "TButton")
        tk.Label(inner_file, textvariable=self.selected_file, font=FONT_MAIN,
                 fg=LABEL_COLOR, bg=PANEL_BG, anchor="w").pack(side="left", padx=12, fill="x", expand=True)

        # === Text Input ===
        text_frame = ttk.LabelFrame(self.root, text=self.t("text_input"), style="Panel.TLabelframe")
        text_frame.pack(fill="both", expand=True, padx=18, pady=(0, 6))

        inner_text = tk.Frame(text_frame, bg=PANEL_BG)
        inner_text.pack(fill="both", expand=True, padx=10, pady=(4, 4))

        text_container = tk.Frame(inner_text, bg=PANEL_BG)
        text_container.pack(fill="both", expand=True)

        self.text_area = tk.Text(text_container, wrap="word", font=FONT_MONO,
                                  bg=BG_INPUT, fg=FG_MAIN, insertbackground=FG_MAIN,
                                  relief="flat", bd=0, height=6, padx=8, pady=6,
                                  highlightthickness=1, highlightcolor=ACCENT,
                                  highlightbackground="#343946")
        self.text_area.pack(side="left", fill="both", expand=True)
        self.text_area.insert("1.0", self.text_value)

        text_scroll = tk.Scrollbar(text_container, command=self.text_area.yview,
                                    bg=BG_INPUT, troughcolor=BG_INPUT)
        text_scroll.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=text_scroll.set)

        text_btn_bar = tk.Frame(inner_text, bg=PANEL_BG)
        text_btn_bar.pack(fill="x", pady=(4, 0))
        self._btn(text_btn_bar, self.t("paste"), self.paste_from_clipboard)
        self._btn(text_btn_bar, self.t("clear"), self.clear_text)
        self._btn(text_btn_bar, self.t("copy"), self.copy_text)
        tk.Label(text_btn_bar, text=self.t("input_hint"), font=("Segoe UI", 8),
                 fg="#6c7086", bg=PANEL_BG).pack(side="right", padx=8)

        # === Action Buttons ===
        action_frame = tk.Frame(self.root, bg=BG_DARK)
        action_frame.pack(fill="x", padx=18, pady=(2, 6))

        self.send_btn = tk.Button(action_frame, text=self.t("send_text"),
                                   font=FONT_BOLD, bg=BTN_PRIMARY, fg=FG_MAIN,
                                   activebackground=BTN_PRIMARY_HOVER, activeforeground=FG_MAIN,
                                   relief="flat", padx=15, pady=8,
                                   cursor="hand2", command=self.send_text)
        self.send_btn.pack(side="left", padx=(0, 8), fill="x", expand=True)

        self.send_file_btn = tk.Button(action_frame, text=self.t("send_file"),
                                        font=FONT_BOLD, bg=BTN_BG, fg=FG_MAIN,
                                        activebackground=BTN_HOVER, activeforeground=FG_MAIN,
                                        relief="flat", padx=15, pady=8,
                                        cursor="hand2", command=self.send_file)
        self.send_file_btn.pack(side="left", padx=(0, 0), fill="x", expand=True)

        # === Status Bar ===
        status_frame = tk.Frame(self.root, bg=STATUS_BG, relief="sunken", bd=0)
        status_frame.pack(fill="x", padx=0, pady=(4, 0))

        self.status_var = tk.StringVar(value=self.t("ready"))
        tk.Label(status_frame, textvariable=self.status_var, font=("Segoe UI", 9),
                 fg=LABEL_COLOR, bg=STATUS_BG, anchor="w", padx=15, pady=6).pack(fill="x")

    def select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.selected_file.set(path)
            self.status_var.set(self.t("selected_file", name=os.path.basename(path)))

    def copy_file_content(self):
        path = self.selected_file.get()
        if not path or path == self.t("no_file"):
            messagebox.showwarning(self.t("warning_title"), self.t("choose_file_warning"))
            return
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            pyperclip.copy(content)
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", content)
            self.status_var.set(self.t("file_copied", name=os.path.basename(path)))
        except Exception as e:
            messagebox.showerror(self.t("error_title"), self.t("read_file_failed", error=e))

    def paste_from_clipboard(self):
        try:
            text = pyperclip.paste()
            self.text_area.insert("end", text)
            self.status_var.set(self.t("pasted"))
        except Exception as e:
            self.status_var.set(self.t("paste_failed", error=e))

    def clear_text(self):
        self.text_area.delete("1.0", "end")
        self.status_var.set(self.t("cleared"))

    def copy_text(self):
        text = self.text_area.get("1.0", "end-1c")
        if text.strip():
            pyperclip.copy(text)
            self.status_var.set(self.t("copied"))
        else:
            self.status_var.set(self.t("empty_input"))

    def get_vnc_command(self, text):
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        password = self.password_entry.get().strip()

        if not ip:
            raise ValueError(self.t("missing_ip"))
        if not port:
            raise ValueError(self.t("missing_port"))
        self.save_current_preferences()

        vncdo = bundled_command("vncdo")
        if not vncdo:
            vncdo = os.path.join(os.path.dirname(sys.executable), "Scripts", "vncdo.exe")
            if not os.path.exists(vncdo):
                vncdo = "vncdo"

        host = f"{ip}::{port}" if port else ip
        cmd = [vncdo, "-s", host]

        if password:
            cmd.extend(["--password", password])

        lines = text.split("\n")
        for i, line in enumerate(lines):
            if line:
                cmd.extend(["type", line])
            if i < len(lines) - 1:
                cmd.extend(["key", "return"])
        return cmd

    def run_vnc_command(self, cmd):
        try:
            self.status_var.set(self.t("sending"))
            self.send_btn.config(state="disabled", bg="#1e3a8a")
            self.send_file_btn.config(state="disabled", bg="#2f3744")

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                self.status_var.set(self.t("send_success"))
            else:
                err = result.stderr or self.t("unknown_error")
                self.status_var.set(self.t("send_failed"))
                messagebox.showerror(self.t("vnc_error_title"), err)
        except subprocess.TimeoutExpired:
            self.status_var.set(self.t("send_timeout"))
            messagebox.showerror(self.t("timeout_title"), self.t("timeout_message"))
        except FileNotFoundError:
            self.status_var.set(self.t("vncdo_missing_status"))
            messagebox.showerror(self.t("error_title"), self.t("vncdo_missing_message"))
        except Exception as e:
            self.status_var.set(f"{self.t('error_title')}: {e}")
            messagebox.showerror(self.t("error_title"), str(e))
        finally:
            self.send_btn.config(state="normal", bg=BTN_PRIMARY)
            self.send_file_btn.config(state="normal", bg=BTN_BG)

    def send_text(self):
        text = self.text_area.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning(self.t("warning_title"), self.t("enter_text_warning"))
            return
        try:
            cmd = self.get_vnc_command(text)
            threading.Thread(target=self.run_vnc_command, args=(cmd,), daemon=True).start()
        except ValueError as e:
            messagebox.showwarning(self.t("config_error_title"), str(e))

    def send_file(self):
        path = self.selected_file.get()
        if not path or path == self.t("no_file"):
            messagebox.showwarning(self.t("warning_title"), self.t("choose_file_warning"))
            return
        import os as os_mod
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if not content.strip():
                messagebox.showwarning(self.t("warning_title"), self.t("empty_file_warning"))
                return
            cmd = self.get_vnc_command(content)
            self.status_var.set(self.t("sending_file", name=os_mod.path.basename(path)))
            threading.Thread(target=self.run_vnc_command, args=(cmd,), daemon=True).start()
        except Exception as e:
            messagebox.showerror(self.t("error_title"), self.t("read_file_failed", error=e))


if __name__ == "__main__":
    root = tk.Tk()
    app = VNCTyperGUI(root)
    root.mainloop()
