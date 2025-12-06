#!/usr/bin/env python3
import tkinter as tk
import psutil
import GPUtil
import subprocess
import re

UPDATE_INTERVAL_MS = 1000   # stats refresh every 1s
BLINK_INTERVAL_MS = 500     # blink speed

# Thresholds
CPU_WARN_USAGE = 95
CPU_WARN_TEMP = 85
GPU_WARN_USAGE = 95
GPU_WARN_TEMP = 85

NORMAL_COLOR = "#CCCCCC"
ALERT_COLOR = "#FF5555"
BG_COLOR = "black"


def get_cpu_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            values = []
            for entries in temps.values():
                for entry in entries:
                    if entry.current is not None:
                        values.append(entry.current)
            if values:
                return sum(values) / len(values)
    except Exception:
        pass

    # Fallback to `sensors` command
    try:
        result = subprocess.run(["sensors"], capture_output=True, text=True)
        matches = re.findall(r"\+(\d+(\.\d+)?)°C", result.stdout)
        if matches:
            values = [float(m[0]) for m in matches]
            return sum(values) / len(values)
    except Exception:
        pass

    return None


def get_gpu_stats():
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return None, None
        gpu = gpus[0]
        return gpu.load * 100.0, gpu.temperature
    except Exception:
        return None, None


class MiniMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mini Monitor")

        # Small frameless window
        self.root.geometry("150x55")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)  # No title bar
        self.root.configure(bg=BG_COLOR)

        # Container frame (for easier drag)
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(padx=4, pady=4)

        self.cpu_label = tk.Label(
            frame,
            text="CPU:--%|--°C",
            font=("TkFixedFont", 11),
            bg=BG_COLOR,
            fg=NORMAL_COLOR,
        )
        self.cpu_label.pack(anchor="w")

        self.gpu_label = tk.Label(
            frame,
            text="GPU:--%|--°C",
            font=("TkFixedFont", 11),
            bg=BG_COLOR,
            fg=NORMAL_COLOR,
        )
        self.gpu_label.pack(anchor="w")

        # Enable dragging by clicking anywhere on the frame
        for widget in (frame, self.cpu_label, self.gpu_label):
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<B1-Motion>", self.do_move)

        # Alert state
        self.cpu_alert = False
        self.gpu_alert = False
        self.cpu_blink_on = True
        self.gpu_blink_on = True

        self.update_stats()
        self.blink()  # start blink loop

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def do_move(self, event):
        x = event.x_root - self._x
        y = event.y_root - self._y
        self.root.geometry(f"+{x}+{y}")

    @staticmethod
    def format_value(value, suffix):
        if value is None:
            return f"--{suffix}"
        return f"{int(round(value)):02d}{suffix}"

    def update_stats(self):
        cpu_usage = psutil.cpu_percent()
        cpu_temp = get_cpu_temperature()
        gpu_usage, gpu_temp = get_gpu_stats()

        cpu_text = (
            f"CPU:{self.format_value(cpu_usage, '%')}"
            f"|{self.format_value(cpu_temp, '°C')}"
        )
        gpu_text = (
            f"GPU:{self.format_value(gpu_usage, '%')}"
            f"|{self.format_value(gpu_temp, '°C')}"
        )

        self.cpu_label.config(text=cpu_text)
        self.gpu_label.config(text=gpu_text)

        # Determine alerts
        self.cpu_alert = (
            (cpu_usage is not None and cpu_usage >= CPU_WARN_USAGE)
            or (cpu_temp is not None and cpu_temp >= CPU_WARN_TEMP)
        )

        self.gpu_alert = (
            (gpu_usage is not None and gpu_usage >= GPU_WARN_USAGE)
            or (gpu_temp is not None and gpu_temp >= GPU_WARN_TEMP)
        )

        # If no alert, ensure solid normal color
        if not self.cpu_alert:
            self.cpu_label.config(fg=NORMAL_COLOR)
            self.cpu_blink_on = True
        if not self.gpu_alert:
            self.gpu_label.config(fg=NORMAL_COLOR)
            self.gpu_blink_on = True

        self.root.after(UPDATE_INTERVAL_MS, self.update_stats)

    def blink(self):
        # CPU blinking
        if self.cpu_alert:
            self.cpu_label.config(
                fg=ALERT_COLOR if self.cpu_blink_on else NORMAL_COLOR
            )
            self.cpu_blink_on = not self.cpu_blink_on

        # GPU blinking
        if self.gpu_alert:
            self.gpu_label.config(
                fg=ALERT_COLOR if self.gpu_blink_on else NORMAL_COLOR
            )
            self.gpu_blink_on = not self.gpu_blink_on

        self.root.after(BLINK_INTERVAL_MS, self.blink)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    MiniMonitor().run()

