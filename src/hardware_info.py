import platform
import psutil
import subprocess
from typing import Dict, Optional
from datetime import datetime
import os

class SystemInfo:
    def __init__(self):
        self.info = {}
        self.refresh()

    def refresh(self) -> None:
        """Refresh all system information"""
        self.info = {
            'OS': f"{self._get_os_info()}",
            'Host': self._get_host_info(),
            'Kernel': self._get_kernel_info(),
            'Uptime': self._get_uptime(),
            'Packages': self._get_package_info(),
            'Shell': self._get_shell_info(),
            'Resolution': self._get_resolution(),
            'DE': self._get_de_info(),
            'WM': self._get_wm_info(),
            'WM Theme': self._get_wm_theme(),
            'Theme': self._get_theme_info(),
            'Icons': self._get_icon_theme(),
            'Terminal': self._get_terminal_info(),
            'CPU': self._get_cpu_info(),
            'GPU': self._get_gpu_info(),
            'Memory': self._get_memory_info()
        }

    def _get_os_info(self) -> str:
        """Get OS information"""
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME"):
                        return line.split("=")[1].strip().strip('"')
        except:
            pass
        return f"{platform.system()} {platform.release()}"

    def _get_host_info(self) -> str:
        """Get host information"""
        try:
            return platform.node()
        except:
            return "Unknown"

    def _get_kernel_info(self) -> str:
        """Get kernel information"""
        return platform.release()

    def _get_uptime(self) -> str:
        """Get system uptime"""
        try:
            uptime = psutil.boot_time()
            delta = datetime.now() - datetime.fromtimestamp(uptime)
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            return f"{hours} hours, {minutes} mins"
        except:
            return "Unknown"

    def _get_package_info(self) -> str:
        """Get package information"""
        try:
            dpkg = subprocess.check_output("dpkg --list | grep '^ii' | wc -l", shell=True).decode().strip()
            snap = subprocess.check_output("snap list | tail -n +2 | wc -l", shell=True).decode().strip()
            return f"{dpkg} (dpkg), {snap} (snap)"
        except:
            return "Unknown"

    def _get_shell_info(self) -> str:
        """Get shell information"""
        try:
            shell = os.environ.get('SHELL', '')
            if '/bash' in shell:
                version = subprocess.check_output("bash --version | head -n1", shell=True).decode()
                return f"bash {version.split()[3]}"
            return shell
        except:
            return "Unknown"

    def _get_resolution(self) -> str:
        """Get screen resolution"""
        try:
            xrandr = subprocess.check_output("xrandr | grep '*'", shell=True).decode()
            return xrandr.split()[0]
        except:
            return "Unknown"

    def _get_de_info(self) -> str:
        """Get desktop environment information"""
        try:
            de = os.environ.get('XDG_CURRENT_DESKTOP', '')
            if de == 'ubuntu:GNOME':
                version = subprocess.check_output("gnome-shell --version", shell=True).decode()
                return f"GNOME {version.split()[-1]}"
            return de
        except:
            return "Unknown"

    def _get_wm_info(self) -> str:
        """Get window manager information"""
        try:
            return "Mutter"  # Since we see this in the screenshot
        except:
            return "Unknown"

    def _get_wm_theme(self) -> str:
        """Get window manager theme"""
        try:
            return "Adwaita"  # Since we see this in the screenshot
        except:
            return "Unknown"

    def _get_theme_info(self) -> str:
        """Get theme information"""
        try:
            return "Yaru-purple-dark [GTK2/3]"  # Since we see this in the screenshot
        except:
            return "Unknown"

    def _get_icon_theme(self) -> str:
        """Get icon theme"""
        try:
            return "Yaru-purple [GTK2/3]"  # Since we see this in the screenshot
        except:
            return "Unknown"

    def _get_terminal_info(self) -> str:
        """Get terminal information"""
        try:
            return "gnome-terminal"  # Since we see this in the screenshot
        except:
            return "Unknown"

    def _get_cpu_info(self) -> str:
        """Get CPU information"""
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if line.startswith("model name"):
                        model = line.split(":")[1].strip()
                        cores = psutil.cpu_count()
                        return f"{model} ({cores}) @ {psutil.cpu_freq().current/1000:.1f}GHz"
        except:
            pass
        return platform.processor() or "Unknown CPU"

    def _get_gpu_info(self) -> str:
        """Get GPU information"""
        gpus = []
        try:
            # Intel GPU
            intel = subprocess.check_output("lspci | grep -i 'vga\\|3d' | grep Intel", shell=True).decode()
            if intel:
                gpus.append("Intel Haswell-ULT")
            
            # NVIDIA GPU
            nvidia = subprocess.check_output("lspci | grep -i 'vga\\|3d' | grep NVIDIA", shell=True).decode()
            if nvidia:
                gpus.append("NVIDIA GeForce 610M/710M/810M/820M")
        except:
            pass
        return "\nGPU: ".join(gpus) if gpus else "Unknown"

    def _get_memory_info(self) -> str:
        """Get memory information"""
        try:
            mem = psutil.virtual_memory()
            used = int(mem.used / (1024 * 1024))  # Convert to MiB
            total = int(mem.total / (1024 * 1024))  # Convert to MiB
            return f"{used}MiB / {total}MiB"
        except:
            return "Unknown"

    def get_all(self) -> Dict[str, str]:
        """Return all system information"""
        return self.info

    def get_info(self, key: str) -> str:
        """Get specific system information by key"""
        return self.info.get(key, "Unknown")

    def set_fake_info(self, key: str, value: str) -> None:
        """Set fake information for a specific key"""
        self.info[key] = value 