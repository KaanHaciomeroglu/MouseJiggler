import os
import sys
import ctypes
import customtkinter as ctk
from jiggler import JigglerThread
from tray import TrayIcon
from utils import base_path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class JigglerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mouse Jiggler")
        self.geometry("320x360")
        self.resizable(False, False)
        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("MouseJiggler")
        self.iconbitmap(os.path.join(base_path(), "icon.ico"))
        self.protocol("WM_DELETE_WINDOW", self._quit)

        self._jiggler: JigglerThread | None = None
        self._active = False

        self._build_ui()
        self._tray = TrayIcon(
            on_show=self._show_window,
            on_toggle=lambda: self.after(0, self._toggle),
            on_quit=lambda: self.after(0, self._quit),
        )
        self._tray.start()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Mouse Jiggler", font=("Segoe UI", 22, "bold")).grid(
            row=0, column=0, pady=(24, 4)
        )

        self._status_label = ctk.CTkLabel(
            self, text="Durum: PASiF", font=("Segoe UI", 14), text_color="#888"
        )
        self._status_label.grid(row=1, column=0, pady=(0, 20))

        self._toggle_btn = ctk.CTkButton(
            self,
            text="BAŞLAT",
            width=180,
            height=48,
            font=("Segoe UI", 16, "bold"),
            fg_color="#2a9d2a",
            hover_color="#1e7a1e",
            command=self._toggle,
        )
        self._toggle_btn.grid(row=2, column=0, pady=(0, 24))

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=3, column=0, padx=32, sticky="ew")
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Aralık:", font=("Segoe UI", 13)).grid(row=0, column=0, sticky="w", pady=4)
        self._interval_val = ctk.CTkLabel(frame, text="30 sn", font=("Segoe UI", 13, "bold"), width=52)
        self._interval_val.grid(row=0, column=2, sticky="e")
        self._interval_slider = ctk.CTkSlider(
            frame, from_=10, to=120, number_of_steps=22,
            command=self._on_interval_change
        )
        self._interval_slider.set(30)
        self._interval_slider.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 12))

        ctk.CTkLabel(frame, text="Miktar:", font=("Segoe UI", 13)).grid(row=2, column=0, sticky="w", pady=4)
        self._pixels_val = ctk.CTkLabel(frame, text="5 px", font=("Segoe UI", 13, "bold"), width=52)
        self._pixels_val.grid(row=2, column=2, sticky="e")
        self._pixels_slider = ctk.CTkSlider(
            frame, from_=1, to=20, number_of_steps=19,
            command=self._on_pixels_change
        )
        self._pixels_slider.set(5)
        self._pixels_slider.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 4))

        ctk.CTkButton(
            self,
            text="Tray'e Küçült",
            width=160,
            height=32,
            font=("Segoe UI", 12),
            fg_color="transparent",
            border_width=1,
            text_color=("#333", "#aaa"),
            command=self._minimize_to_tray,
        ).grid(row=4, column=0, pady=(20, 8))

    def _on_interval_change(self, val):
        sn = round(val)
        self._interval_val.configure(text=f"{sn} sn")
        if self._jiggler:
            self._jiggler.interval = sn
            self._status_label.configure(text=f"Durum: AKTiF  ({sn} sn'de bir)")

    def _on_pixels_change(self, val):
        px = round(val)
        self._pixels_val.configure(text=f"{px} px")
        if self._jiggler:
            self._jiggler.pixels = px

    def _toggle(self):
        if self._active:
            self._stop()
        else:
            self._start()

    def _start(self):
        self._active = True
        self._jiggler = JigglerThread()
        self._jiggler.interval = round(self._interval_slider.get())
        self._jiggler.pixels = round(self._pixels_slider.get())
        self._jiggler.start()
        self._toggle_btn.configure(text="DURDUR", fg_color="#c0392b", hover_color="#96281b")
        self._status_label.configure(
            text=f"Durum: AKTiF  ({self._jiggler.interval} sn'de bir)",
            text_color="#2ecc71",
        )

    def _stop(self):
        self._active = False
        if self._jiggler:
            self._jiggler.stop()
            self._jiggler.join(timeout=2)
            self._jiggler = None
        self._toggle_btn.configure(text="BAŞLAT", fg_color="#2a9d2a", hover_color="#1e7a1e")
        self._status_label.configure(text="Durum: PASiF", text_color="#888")

    def _minimize_to_tray(self):
        self.withdraw()

    def _show_window(self):
        self.after(0, self.deiconify)
        self.after(0, self.lift)

    def _quit(self):
        if self._jiggler:
            self._jiggler.stop()
            self._jiggler.join(timeout=2)
        self._tray.stop()
        self.quit()
        self.destroy()
