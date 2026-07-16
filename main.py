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

# === Theme Colors ===
BG_DARK = "#1e1e2e"
BG_PANEL = "#2a2a3e"
BG_INPUT = "#313145"
FG_MAIN = "#cdd6f4"
FG_DIM = "#a6adc8"
FG_ACCENT = "#89b4fa"
FG_GREEN = "#a6e3a1"
FG_YELLOW = "#f9e2af"
FG_RED = "#f38ba8"
FG_PURPLE = "#cba6f7"

ACCENT = "#89b4fa"
BTN_BG = "#3b3b52"
BTN_HOVER = "#4a4a66"
PANEL_BG = "#26263a"
LABEL_COLOR = "#a6adc8"

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
        "file_selection": "  📁  文件选择  ",
        "choose_file": "📂  选择文件",
        "copy_to_input": "📋  复制到输入框",
        "text_input": "  📝  文本输入  ",
        "paste": "📥  粘贴",
        "clear": "🗑️  清空",
        "copy": "📋  复制",
        "input_hint": "提示：支持中英文混合输入",
        "vnc_config": "  🖥️  VNC 服务器配置  ",
        "ip_address": "IP 地址",
        "port": "端口",
        "password": "密码",
        "send_text": "🚀  发送文本到 VNC",
        "send_file": "📄  发送文件内容到 VNC",
        "ready": "✅ 就绪",
        "no_file": "未选择文件",
        "vnc_ip_tip": "VNC 服务器 IP",
        "vnc_port_tip": "VNC 端口，默认 5900",
        "vnc_password_tip": "VNC 密码（可选）",
        "selected_file": "📂 已选择: {name}",
        "choose_file_warning": "请先选择文件",
        "warning_title": "⚠️ 警告",
        "file_copied": "✅ 已复制 {name} 的内容到输入框",
        "read_file_failed": "读取文件失败: {error}",
        "error_title": "❌ 错误",
        "pasted": "📥 已粘贴",
        "paste_failed": "❌ 粘贴失败: {error}",
        "cleared": "🗑️ 已清空",
        "copied": "✅ 已复制到剪贴板",
        "empty_input": "⚠️ 输入框为空",
        "missing_ip": "请输入 VNC 服务器 IP 地址",
        "missing_port": "请输入 VNC 端口",
        "sending": "⏳ 正在发送...",
        "send_success": "✅ 发送成功",
        "send_failed": "❌ 发送失败",
        "vnc_error_title": "VNC 错误",
        "unknown_error": "未知错误",
        "send_timeout": "❌ 发送超时 (30秒)",
        "timeout_title": "超时",
        "timeout_message": "VNC 命令执行超时",
        "vncdo_missing_status": "❌ 未找到 vncdo，请安装 vncdotool: pip install vncdotool",
        "vncdo_missing_message": "未找到 vncdo 命令，请安装 vncdotool",
        "config_error_title": "⚠️ 配置错误",
        "enter_text_warning": "请输入要发送的文本",
        "empty_file_warning": "文件内容为空",
        "sending_file": "📄 发送文件: {name}",
    },
    "en": {
        "subtitle": "Send text to a VNC server through vncdotool",
        "language": "Language",
        "file_selection": "  📁  File Selection  ",
        "choose_file": "📂  Choose File",
        "copy_to_input": "📋  Copy to Input",
        "text_input": "  📝  Text Input  ",
        "paste": "📥  Paste",
        "clear": "🗑️  Clear",
        "copy": "📋  Copy",
        "input_hint": "Tip: mixed Chinese and English input is supported",
        "vnc_config": "  🖥️  VNC Server Config  ",
        "ip_address": "IP Address",
        "port": "Port",
        "password": "Password",
        "send_text": "🚀  Send Text to VNC",
        "send_file": "📄  Send File Content to VNC",
        "ready": "✅ Ready",
        "no_file": "No file selected",
        "vnc_ip_tip": "VNC server IP",
        "vnc_port_tip": "VNC port, default 5900",
        "vnc_password_tip": "VNC password (optional)",
        "selected_file": "📂 Selected: {name}",
        "choose_file_warning": "Choose a file first",
        "warning_title": "⚠️ Warning",
        "file_copied": "✅ Copied {name} into the input box",
        "read_file_failed": "Failed to read file: {error}",
        "error_title": "❌ Error",
        "pasted": "📥 Pasted",
        "paste_failed": "❌ Paste failed: {error}",
        "cleared": "🗑️ Cleared",
        "copied": "✅ Copied to clipboard",
        "empty_input": "⚠️ Input box is empty",
        "missing_ip": "Enter the VNC server IP address",
        "missing_port": "Enter the VNC port",
        "sending": "⏳ Sending...",
        "send_success": "✅ Sent successfully",
        "send_failed": "❌ Send failed",
        "vnc_error_title": "VNC Error",
        "unknown_error": "Unknown error",
        "send_timeout": "❌ Send timed out (30 seconds)",
        "timeout_title": "Timeout",
        "timeout_message": "The VNC command timed out",
        "vncdo_missing_status": "❌ vncdo not found. Install vncdotool: pip install vncdotool",
        "vncdo_missing_message": "vncdo command not found. Install vncdotool",
        "config_error_title": "⚠️ Config Error",
        "enter_text_warning": "Enter text to send",
        "empty_file_warning": "File content is empty",
        "sending_file": "📄 Sending file: {name}",
    },
}


def default_language():
    language = locale.getlocale()[0] or ""
    return "zh" if language.lower().startswith("zh") else "en"


def resource_path(name):
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, name)


def bundled_command(name):
    base_dir = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else __file__)
    exe_name = f"{name}.exe" if os.name == "nt" else name
    path = os.path.join(base_dir, exe_name)
    return path if os.path.exists(path) else None


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
        label = tk.Label(self.tooltip, text=self.text, bg="#3b3b52", fg="#cdd6f4",
                         font=("Segoe UI", 9), padx=8, pady=4, relief="solid", bd=1)
        label.pack()

    def hide(self, _event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class VNCTyperGUI:
    def __init__(self, root):
        self.root = root
        self.language = default_language()
        self.ip_value = "192.168.50.13"
        self.port_value = "5900"
        self.password_value = ""
        self.text_value = ""
        self.selected_file = tk.StringVar(value=self.t("no_file"))
        self.root.title("vnc-typer")
        self.root.geometry("720x580")
        self.root.resizable(True, True)
        self.root.configure(bg=BG_DARK)

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

        for child in self.root.winfo_children():
            child.destroy()
        self.create_widgets()

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
                    insertcolor=FG_MAIN, borderwidth=0)
        s.configure("TButton", background=BTN_BG, foreground=FG_MAIN, font=FONT_BOLD,
                    borderwidth=0, padding=(8, 5))
        s.map("TButton",
              background=[("active", BTN_HOVER), ("pressed", BTN_BG)],
              foreground=[("active", FG_MAIN)])
        s.configure("Send.TButton", background="#2f6f9f", foreground=FG_MAIN, font=FONT_BOLD,
                    borderwidth=0, padding=(8, 6))
        s.map("Send.TButton", background=[("active", "#3d8fc0"), ("pressed", "#2f6f9f")])
        s.configure("SendFile.TButton", background="#4f3f8f", foreground=FG_MAIN, font=FONT_BOLD,
                    borderwidth=0, padding=(8, 6))
        s.map("SendFile.TButton", background=[("active", "#5f4faf"), ("pressed", "#4f3f8f")])
        s.configure("File.TButton", background="#3b523a", foreground=FG_GREEN, font=FONT_BOLD,
                    borderwidth=0, padding=(8, 5))
        s.map("File.TButton", background=[("active", "#4b6249"), ("pressed", "#3b523a")])

    def _btn(self, parent, text, cmd, style="TButton", side="left", **kwargs):
        btn = ttk.Button(parent, text=text, command=cmd, style=style)
        btn.pack(side=side, padx=4, pady=2, **kwargs)
        return btn

    def create_widgets(self):
        # === Header ===
        header = tk.Frame(self.root, bg=BG_DARK)
        header.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(header, text="🔑 vnc-typer", font=FONT_TITLE, fg=FG_ACCENT,
                 bg=BG_DARK).pack(side="left")
        tk.Label(header, text=self.t("subtitle"), font=FONT_MAIN,
                 fg=LABEL_COLOR, bg=BG_DARK).pack(side="left", padx=(15, 0))
        lang_box = tk.Frame(header, bg=BG_DARK)
        lang_box.pack(side="right")
        tk.Label(lang_box, text=self.t("language"), font=FONT_MAIN,
                 fg=LABEL_COLOR, bg=BG_DARK).pack(side="left", padx=(0, 8))
        self.language_var = tk.StringVar(value=LANGUAGE_NAMES[self.language])
        language_menu = ttk.Combobox(lang_box, textvariable=self.language_var,
                                     values=list(LANGUAGE_NAMES.values()), width=9,
                                     state="readonly")
        language_menu.pack(side="left")
        language_menu.bind("<<ComboboxSelected>>", self.change_language)

        # Separator
        tk.Frame(self.root, height=1, bg="#3a3a52").pack(fill="x", padx=15, pady=(0, 8))

        # === Panel 1: File Selection ===
        file_frame = ttk.LabelFrame(self.root, text=self.t("file_selection"), style="Panel.TLabelframe")
        file_frame.pack(fill="x", padx=18, pady=(5, 6))

        inner_file = tk.Frame(file_frame, bg=PANEL_BG)
        inner_file.pack(fill="x", padx=10, pady=8)

        self._btn(inner_file, self.t("choose_file"), self.select_file, "File.TButton")
        tk.Label(inner_file, textvariable=self.selected_file, font=FONT_MAIN,
                 fg=LABEL_COLOR, bg=PANEL_BG).pack(side="left", padx=12, fill="x", expand=True)
        self._btn(inner_file, self.t("copy_to_input"), self.copy_file_content, "TButton", side="right")

        # === Panel 2: Text Input ===
        text_frame = ttk.LabelFrame(self.root, text=self.t("text_input"), style="Panel.TLabelframe")
        text_frame.pack(fill="both", expand=True, padx=18, pady=(5, 6))

        inner_text = tk.Frame(text_frame, bg=PANEL_BG)
        inner_text.pack(fill="both", expand=True, padx=10, pady=(4, 4))

        text_container = tk.Frame(inner_text, bg=PANEL_BG)
        text_container.pack(fill="both", expand=True)

        self.text_area = tk.Text(text_container, wrap="word", font=FONT_MONO,
                                  bg=BG_INPUT, fg=FG_MAIN, insertbackground=FG_MAIN,
                                  relief="flat", bd=0, height=6, padx=8, pady=6,
                                  highlightthickness=1, highlightcolor=ACCENT,
                                  highlightbackground="#3a3a52")
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

        # === Panel 3: VNC Config ===
        config_frame = ttk.LabelFrame(self.root, text=self.t("vnc_config"), style="Panel.TLabelframe")
        config_frame.pack(fill="x", padx=18, pady=(5, 6))

        inner_cfg = tk.Frame(config_frame, bg=PANEL_BG)
        inner_cfg.pack(fill="x", padx=10, pady=8)

        # Row 1: IP + Port
        row1 = tk.Frame(inner_cfg, bg=PANEL_BG)
        row1.pack(fill="x", pady=(0, 6))
        tk.Label(row1, text=self.t("ip_address"), font=FONT_BOLD, fg=FG_MAIN,
                 bg=PANEL_BG).pack(side="left", padx=(0, 8))
        self.ip_entry = tk.Entry(row1, font=FONT_MONO, bg=BG_INPUT, fg=FG_MAIN,
                                  insertbackground=FG_MAIN, relief="flat", bd=0,
                                  width=18, highlightthickness=1,
                                  highlightcolor=ACCENT, highlightbackground="#3a3a52")
        self.ip_entry.insert(0, self.ip_value)
        self.ip_entry.pack(side="left", padx=(0, 20))
        ToolTip(self.ip_entry, self.t("vnc_ip_tip"))

        tk.Label(row1, text=self.t("port"), font=FONT_BOLD, fg=FG_MAIN,
                 bg=PANEL_BG).pack(side="left", padx=(0, 8))
        self.port_entry = tk.Entry(row1, font=FONT_MONO, bg=BG_INPUT, fg=FG_MAIN,
                                    insertbackground=FG_MAIN, relief="flat", bd=0,
                                    width=8, highlightthickness=1,
                                    highlightcolor=ACCENT, highlightbackground="#3a3a52")
        self.port_entry.insert(0, self.port_value)
        self.port_entry.pack(side="left")
        ToolTip(self.port_entry, self.t("vnc_port_tip"))

        # Row 2: Password
        row2 = tk.Frame(inner_cfg, bg=PANEL_BG)
        row2.pack(fill="x")
        tk.Label(row2, text=self.t("password"), font=FONT_BOLD, fg=FG_MAIN,
                 bg=PANEL_BG).pack(side="left", padx=(0, 22))
        self.password_entry = tk.Entry(row2, font=FONT_MONO, bg=BG_INPUT, fg=FG_MAIN,
                                        insertbackground=FG_MAIN, relief="flat", bd=0,
                                        width=20, show="•", highlightthickness=1,
                                        highlightcolor=ACCENT, highlightbackground="#3a3a52")
        self.password_entry.insert(0, self.password_value)
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 0))
        ToolTip(self.password_entry, self.t("vnc_password_tip"))

        # === Action Buttons ===
        action_frame = tk.Frame(self.root, bg=BG_DARK)
        action_frame.pack(fill="x", padx=18, pady=(8, 5))

        self.send_btn = tk.Button(action_frame, text=self.t("send_text"),
                                   font=FONT_BOLD, bg="#2f6f9f", fg=FG_MAIN,
                                   activebackground="#3d8fc0", activeforeground=FG_MAIN,
                                   relief="flat", padx=15, pady=8,
                                   cursor="hand2", command=self.send_text)
        self.send_btn.pack(side="left", padx=(0, 8), fill="x", expand=True)

        self.send_file_btn = tk.Button(action_frame, text=self.t("send_file"),
                                        font=FONT_BOLD, bg="#4f3f8f", fg=FG_MAIN,
                                        activebackground="#5f4faf", activeforeground=FG_MAIN,
                                        relief="flat", padx=15, pady=8,
                                        cursor="hand2", command=self.send_file)
        self.send_file_btn.pack(side="left", padx=(0, 0), fill="x", expand=True)

        # === Status Bar ===
        status_frame = tk.Frame(self.root, bg="#1a1a2e", relief="sunken", bd=0)
        status_frame.pack(fill="x", padx=0, pady=(4, 0))

        self.status_var = tk.StringVar(value=self.t("ready"))
        tk.Label(status_frame, textvariable=self.status_var, font=("Segoe UI", 9),
                 fg=LABEL_COLOR, bg="#1a1a2e", anchor="w", padx=15, pady=6).pack(fill="x")

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
            self.send_btn.config(state="disabled", bg="#2a4a6a")
            self.send_file_btn.config(state="disabled", bg="#3a2f6a")

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
            self.send_btn.config(state="normal", bg="#2f6f9f")
            self.send_file_btn.config(state="normal", bg="#4f3f8f")

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
