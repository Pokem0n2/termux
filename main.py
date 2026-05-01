#!/usr/bin/env python3
"""
HKA - Hyperlink Keyboard App
5x5 grid launcher with browser open, config saved to hka-config.json
"""
import os
import sys
import json
import webbrowser
import tkinter as tk
from tkinter import simpledialog, messagebox

CONFIG_FILE = "hka-config.json"
GRID_SIZE = 5

class HKAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HKA - Hyperlink Keyboard App")
        self.root.resizable(False, False)
        self.cfg = self._load_config()
        self.buttons = {}
        self._build_ui()

    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_config(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cfg, f, ensure_ascii=False, indent=2)

    def _grid_pos(self, idx):
        return idx % GRID_SIZE, idx // GRID_SIZE

    def _build_ui(self):
        for idx in range(GRID_SIZE * GRID_SIZE):
            x, y = self._grid_pos(idx)
            key = str(idx)
            data = self.cfg.get(key, {})
            label = data.get("name", "")
            link = data.get("link", "")

            btn = tk.Button(
                self.root,
                text=label if label else "+",
                font=("Arial", 11),
                width=12,
                height=3,
                command=lambda k=key: self._on_click(k),
            )
            btn.grid(row=y, column=x, padx=3, pady=3, sticky="nsew")
            self.buttons[key] = {"btn": btn, "link": link}

        for i in range(GRID_SIZE):
            self.root.grid_columnconfigure(i, weight=1, minsize=80)
            self.root.grid_rowconfigure(i, weight=1, minsize=50)

    def _on_click(self, key):
        data = self.cfg.get(key, {})
        if data.get("link"):
            webbrowser.open(data["link"])
        else:
            self._edit_button(key)

    def _edit_button(self, key):
        data = self.cfg.get(key, {})
        dlg = EditDialog(self.root, data)
        if dlg.result:
            name = dlg.result.get("name", "").strip()
            link = dlg.result.get("link", "").strip()
            if name or link:
                self.cfg[key] = {"name": name, "link": link}
            else:
                self.cfg.pop(key, None)
            self._save_config()
            self._update_button(key)

    def _update_button(self, key):
        data = self.cfg.get(key, {})
        label = data.get("name", "") or "+"
        self.buttons[key]["btn"].config(text=label)
        self.buttons[key]["link"] = data.get("link", "")


class EditDialog(tk.Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.result = None
        self.title("Edit Button")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="w", padx=8, pady=4)
        self.name_var = tk.StringVar(value=data.get("name", ""))
        tk.Entry(self, textvariable=self.name_var, width=40).grid(row=0, column=1, padx=8, pady=4)

        tk.Label(self, text="Link:").grid(row=1, column=0, sticky="w", padx=8, pady=4)
        self.link_var = tk.StringVar(value=data.get("link", ""))
        tk.Entry(self, textvariable=self.link_var, width=40).grid(row=1, column=1, padx=8, pady=4)

        frm = tk.Frame(self)
        frm.grid(row=2, column=0, columnspan=2, pady=8)
        tk.Button(frm, text="Save", width=8, command=self._on_save).pack(side="left", padx=4)
        tk.Button(frm, text="Clear", width=8, command=self._on_clear).pack(side="left", padx=4)
        tk.Button(frm, text="Cancel", width=8, command=self.destroy).pack(side="left", padx=4)

        self.name_var.set(self.name_var.get())
        self.geometry("+%d+%d" % (parent.winfo_x() + 50, parent.winfo_y() + 50))
        self.wait_window()

    def _on_save(self):
        self.result = {
            "name": self.name_var.get(),
            "link": self.link_var.get(),
        }
        self.destroy()

    def _on_clear(self):
        self.result = {"name": "", "link": ""}
        self.destroy()


def main():
    root = tk.Tk()
    app = HKAApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
