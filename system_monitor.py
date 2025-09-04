import psutil
import tkinter as tk
from tkinter import ttk
import GPUtil
from threading import Thread
import time
import platform

class ModernSystemMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")
        self.root.geometry("1200x1200")
        
        # Initialize theme settings first
        self.dark_mode = tk.BooleanVar(value=True)  # Dark mode by default
        self.style = ttk.Style()
        
        # Create main frame before applying theme
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Apply theme
        self.apply_theme()
        
        # Theme switcher
        theme_frame = ttk.Frame(self.root, style='Custom.TFrame')
        theme_frame.pack(fill=tk.X, padx=10, pady=5)
        theme_switch = ttk.Checkbutton(theme_frame, 
                                     text="Dark Mode",
                                     variable=self.dark_mode,
                                     command=self.apply_theme,
                                     style='Custom.TCheckbutton')
        theme_switch.pack(side=tk.RIGHT)
        
        # CPU Section
        self.cpu_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.cpu_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(self.cpu_frame, text="CPU", style='Title.TLabel').pack(anchor='w')
        self.cpu_temp = ttk.Label(self.cpu_frame, text="0", style='BigNumber.TLabel')
        self.cpu_temp.pack(anchor='w')
        
        # CPU Process bar
        self.cpu_process_frame = ttk.Frame(self.cpu_frame, style='Custom.TFrame')
        self.cpu_process_frame.pack(fill=tk.X, pady=15)
        ttk.Label(self.cpu_process_frame, text="Process :", 
                 style='Custom.TLabel').pack(side=tk.LEFT)
        self.cpu_progress = ttk.Progressbar(self.cpu_process_frame, 
                                          style='Custom.Horizontal.TProgressbar',
                                          length=400, mode='determinate')
        self.cpu_progress.pack(side=tk.LEFT, padx=10)
        self.cpu_percent = ttk.Label(self.cpu_process_frame, text="0%",
                                   style='Custom.TLabel')
        self.cpu_percent.pack(side=tk.LEFT)
        
        # CPU Cores Section with switcher
        cores_header_frame = ttk.Frame(self.cpu_frame, style='Custom.TFrame')
        cores_header_frame.pack(fill=tk.X, pady=5)
        
        # Add the switcher
        self.show_percentage = tk.BooleanVar(value=True)  # True for percentage, False for temperature
        cores_switch = ttk.Checkbutton(cores_header_frame,
                                     text="Show Percentage",
                                     variable=self.show_percentage,
                                     style='Custom.TCheckbutton')
        cores_switch.pack(side=tk.RIGHT)
        
        # Cores display
        self.cores_frame = ttk.Frame(self.cpu_frame, style='Custom.TFrame')
        self.cores_frame.pack(fill=tk.X, pady=5)
        self.core_labels = []
        cores_per_row = 4
        total_cores = psutil.cpu_count()
        
        for i in range(total_cores):
            if i % cores_per_row == 0:
                row_frame = ttk.Frame(self.cores_frame, style='Custom.TFrame')
                row_frame.pack(fill=tk.X)
            core_text = ttk.Label(row_frame, 
                                text=f"core {i+1}: 0%",
                                style='Custom.TLabel',
                                width=20)
            core_text.pack(side=tk.LEFT, padx=5)
            self.core_labels.append(core_text)
        
        # GPU Section
        self.gpu_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.gpu_frame.pack(fill=tk.X, pady=20)
        
        gpu_header_frame = ttk.Frame(self.gpu_frame, style='Custom.TFrame')
        gpu_header_frame.pack(fill=tk.X)
        ttk.Label(gpu_header_frame, text="GPU :",
                 style='Title.TLabel').pack(side=tk.LEFT)
        
        # GPU Dropdown
        self.gpu_var = tk.StringVar()
        self.gpu_dropdown = ttk.Combobox(gpu_header_frame, 
                                       textvariable=self.gpu_var,
                                       state='readonly',
                                       width=30)
        self.gpu_dropdown.pack(side=tk.LEFT)
        
        self.gpu_temp = ttk.Label(self.gpu_frame, text="0",
                                style='BigNumber.TLabel')
        self.gpu_temp.pack(anchor='w')
        
        # GPU Process bar
        self.gpu_process_frame = ttk.Frame(self.gpu_frame, style='Custom.TFrame')
        self.gpu_process_frame.pack(fill=tk.X, pady=5)
        ttk.Label(self.gpu_process_frame, text="Process :",
                 style='Custom.TLabel').pack(side=tk.LEFT)
        self.gpu_progress = ttk.Progressbar(self.gpu_process_frame,
                                          style='Custom.Horizontal.TProgressbar',
                                          length=400, mode='determinate')
        self.gpu_progress.pack(side=tk.LEFT, padx=10)
        self.gpu_percent = ttk.Label(self.gpu_process_frame, text="0%",
                                   style='Custom.TLabel')
        self.gpu_percent.pack(side=tk.LEFT)
        
        # VRAM bar
        self.vram_frame = ttk.Frame(self.gpu_frame, style='Custom.TFrame')
        self.vram_frame.pack(fill=tk.X, pady=5)
        ttk.Label(self.vram_frame, text="VRAM :",
                 style='Custom.TLabel').pack(side=tk.LEFT)
        self.vram_progress = ttk.Progressbar(self.vram_frame,
                                           style='Custom.Horizontal.TProgressbar',
                                           length=400, mode='determinate')
        self.vram_progress.pack(side=tk.LEFT, padx=10)
        self.vram_text = ttk.Label(self.vram_frame, text="0 MB / 0 MB",
                                 style='Custom.TLabel')
        self.vram_text.pack(side=tk.LEFT)
        
        # RAM Section
        self.ram_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.ram_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(self.ram_frame, text="RAM :",
                 style='Title.TLabel').pack(anchor='w')
        
        ram_content_frame = ttk.Frame(self.ram_frame, style='Custom.TFrame')
        ram_content_frame.pack(fill=tk.X, pady=5)
        
        self.ram_progress = ttk.Progressbar(ram_content_frame,
                                          style='Custom.Horizontal.TProgressbar',
                                          length=400, mode='determinate')
        self.ram_progress.pack(side=tk.LEFT, pady=5)
        
        self.ram_text = ttk.Label(ram_content_frame, text="0 GB / 0 GB",
                                style='Custom.TLabel')
        self.ram_text.pack(side=tk.LEFT, padx=10)
        
        # Power Consumption Section
        self.power_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        self.power_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(self.power_frame, text="Total System Power:",
                 style='Title.TLabel').pack(side=tk.LEFT)
        self.power_text = ttk.Label(self.power_frame, text="0W",
                                  style='Custom.TLabel')
        self.power_text.pack(side=tk.LEFT, padx=10)
        
        # Initialize GPU list
        self.update_gpu_list()
        
        # Start monitoring
        self.monitoring = True
        self.monitor_thread = Thread(target=self.update_stats, daemon=True)
        self.monitor_thread.start()

    def apply_theme(self):
        is_dark = self.dark_mode.get()
        bg_color = '#0a192f' if is_dark else 'white'  # Dark blue background
        fg_color = '#4ade80' if is_dark else '#1E90FF'  # Light green text for dark mode
        
        # Configure root and main background
        self.root.configure(bg=bg_color)
        self.main_frame.configure(style='Custom.TFrame')
        
        # Configure styles with consistent background
        self.style.configure('Custom.TFrame', background=bg_color)
        self.style.configure('Custom.TLabel', 
                           background=bg_color, 
                           foreground=fg_color,
                           font=('Arial', 16))
        self.style.configure('Title.TLabel',
                           background=bg_color,
                           foreground=fg_color,
                           font=('Arial', 16))
        self.style.configure('BigNumber.TLabel',
                           background=bg_color,
                           foreground=fg_color,
                           font=('Arial', 96, 'bold'))
        self.style.configure('Custom.Horizontal.TProgressbar',
                           background=fg_color,
                           troughcolor=bg_color,
                           bordercolor=bg_color)
        self.style.configure('Custom.TCheckbutton',
                           background=bg_color,
                           foreground=fg_color,
                           font=('Arial', 16))

    def get_cpu_temperature(self):
        try:
            if platform.system() == "Linux":
                temps = psutil.sensors_temperatures()
                if 'coretemp' in temps:
                    # Get the package temperature (overall CPU temp)
                    for temp in temps['coretemp']:
                        if 'Package' in temp.label:
                            return temp.current
                    # If no package temp found, return highest core temp
                    return max(t.current for t in temps['coretemp'])
                elif 'k10temp' in temps:  # For AMD processors
                    return temps['k10temp'][0].current
                elif 'zenpower' in temps:  # For AMD Zen processors
                    return temps['zenpower'][0].current
                return 0
            elif platform.system() == "Windows":
                try:
                    import wmi
                    w = wmi.WMI(namespace=r"root\OpenHardwareMonitor")
                    temperature_infos = w.Sensor()
                    for sensor in temperature_infos:
                        if sensor.SensorType==u'Temperature' and 'CPU Package' in sensor.Name:
                            return float(sensor.Value)
                    return 0
                except:
                    # Alternative method using PowerShell for Windows
                    try:
                        import subprocess
                        cmd = "powershell \"Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace root/wmi | Select CurrentTemperature\""
                        output = subprocess.check_output(cmd, shell=True)
                        temp = float(output.decode().split('\n')[3].strip()) / 10.0 - 273.15
                        return temp
                    except:
                        return 0
        except Exception as e:
            print(f"Error reading CPU temperature: {e}")
            return 0

    def get_core_temperatures(self):
        try:
            if platform.system() == "Linux":
                temps = psutil.sensors_temperatures()
                if 'coretemp' in temps:
                    # Filter out the package temperature and only get core temps
                    core_temps = [t.current for t in temps['coretemp'] if 'Core' in t.label]
                    return core_temps
                elif 'k10temp' in temps:  # For AMD processors
                    # AMD might show per-CCD temperatures
                    return [temps['k10temp'][0].current] * psutil.cpu_count()
                elif 'zenpower' in temps:  # For AMD Zen processors
                    return [temps['zenpower'][0].current] * psutil.cpu_count()
            elif platform.system() == "Windows":
                try:
                    import wmi
                    w = wmi.WMI(namespace=r"root\OpenHardwareMonitor")
                    temperature_infos = w.Sensor()
                    core_temps = []
                    for sensor in temperature_infos:
                        if sensor.SensorType==u'Temperature' and 'CPU Core' in sensor.Name:
                            core_temps.append(float(sensor.Value))
                    if core_temps:
                        return core_temps
                except:
                    pass
            return [0] * psutil.cpu_count()
        except Exception as e:
            print(f"Error reading core temperatures: {e}")
            return [0] * psutil.cpu_count()

    def get_system_power(self):
        try:
            # This is a simplified estimation
            # For more accurate readings, you'd need to use platform-specific tools
            cpu_power = psutil.cpu_percent() * 1.5  # Rough estimate
            gpu_power = 0
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    gpu_power = gpu.load * 250  # Assuming max TDP of 250W
            except:
                pass
            
            # Add base system power (rough estimate)
            base_power = 50
            return int(cpu_power + gpu_power + base_power)
        except:
            return 0

    def update_gpu_list(self):
        try:
            gpus = GPUtil.getGPUs()
            gpu_names = [f"{gpu.name} ({gpu.id})" for gpu in gpus]
            self.gpu_dropdown['values'] = gpu_names
            if gpu_names:
                self.gpu_dropdown.set(gpu_names[0])
        except:
            self.gpu_dropdown['values'] = ["No GPU detected"]
            self.gpu_dropdown.set("No GPU detected")

    def update_stats(self):
        while self.monitoring:
            # Update CPU temperature
            cpu_temp = self.get_cpu_temperature()
            self.cpu_temp.config(text=f"{int(cpu_temp)}")
            
            # Update CPU usage
            cpu_percent = psutil.cpu_percent()
            self.cpu_progress['value'] = cpu_percent
            self.cpu_percent.config(text=f"{cpu_percent}%")
            
            # Update core stats
            core_temps = self.get_core_temperatures()
            core_percentages = psutil.cpu_percent(percpu=True)
            
            for i in range(len(self.core_labels)):
                if self.show_percentage.get():
                    if i < len(core_percentages):
                        self.core_labels[i].config(
                            text=f"core {i+1}: {int(core_percentages[i])}%")
                else:
                    if i < len(core_temps):
                        self.core_labels[i].config(
                            text=f"core {i+1}: {int(core_temps[i])}°C")
            
            # Update GPU stats
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]  # Using first GPU for now
                    self.gpu_temp.config(text=f"{int(gpu.temperature)}")
                    self.gpu_progress['value'] = gpu.load * 100
                    self.gpu_percent.config(text=f"{int(gpu.load * 100)}%")
                    
                    vram_used = gpu.memoryUsed
                    vram_total = gpu.memoryTotal
                    vram_percent = (vram_used / vram_total) * 100
                    self.vram_progress['value'] = vram_percent
                    self.vram_text.config(
                        text=f"{vram_used:.2f} GB / {vram_total:.2f} GB")
            except Exception as e:
                print(f"Error updating GPU stats: {e}")
            
            # Update RAM stats
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            ram_used = ram.used / (1024**3)  # Convert to GB
            ram_total = ram.total / (1024**3)
            self.ram_progress['value'] = ram_percent
            self.ram_text.config(
                text=f"{ram_used:.2f} GB / {ram_total:.2f} GB")
            
            # Update power consumption
            power = self.get_system_power()
            self.power_text.config(text=f"{power}W")
            
            time.sleep(1)
    
    def on_closing(self):
        self.monitoring = False
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ModernSystemMonitor(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()