import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

# Настройки для каждой ОС/дистрибутива
OS_CONFIG = {
    "Linux": {
        "Ubuntu": {
            "icon": "ubuntu.png",
            "color": "#2E3440",
            "package_manager": "sudo -S apt-get install -y git",
            "bypasses": {
                "Shadowsocks": {
                    "command": "sudo -S apt-get install -y shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "Obfs4": {
                    "command": "sudo -S apt-get install -y obfs4proxy",
                    "info": "Obfs4 — обфускация трафика для обхода DPI.",
                    "config_required": False,
                },
                "WireGuard": {
                    "command": "sudo -S apt-get install -y wireguard",
                    "info": "WireGuard — современный VPN для обхода блокировок.",
                    "config_required": True,
                },
            },
        },
        "Arch Linux": {
            "icon": "arch.png",
            "color": "#2E3440",
            "package_manager": "sudo -S pacman -S --needed --noconfirm git",
            "bypasses": {
                "Shadowsocks": {
                    "command": "sudo -S pacman -S --needed --noconfirm shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "Obfs4": {
                    "command": "sudo -S pacman -S --needed --noconfirm obfs4proxy",
                    "info": "Obfs4 — обфускация трафика для обхода DPI.",
                    "config_required": False,
                },
                "WireGuard": {
                    "command": "sudo -S pacman -S --needed --noconfirm wireguard-tools",
                    "info": "WireGuard — современный VPN для обхода блокировок.",
                    "config_required": True,
                },
            },
        },
        "Fedora": {
            "icon": "fedora.png",
            "color": "#2E3440",
            "package_manager": "sudo -S dnf install -y git",
            "bypasses": {
                "Shadowsocks": {
                    "command": "sudo -S dnf install -y shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "Obfs4": {
                    "command": "sudo -S dnf install -y obfs4proxy",
                    "info": "Obfs4 — обфускация трафика для обхода DPI.",
                    "config_required": False,
                },
                "WireGuard": {
                    "command": "sudo -S dnf install -y wireguard-tools",
                    "info": "WireGuard — современный VPN для обхода блокировок.",
                    "config_required": True,
                },
            },
        },
        # Добавим еще дистрибутивы
        "Debian": {
            "icon": "debian.png",
            "color": "#2E3440",
            "package_manager": "sudo -S apt-get install -y git",
            "bypasses": {
                "Shadowsocks": {
                    "command": "sudo -S apt-get install -y shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "Obfs4": {
                    "command": "sudo -S apt-get install -y obfs4proxy",
                    "info": "Obfs4 — обфускация трафика для обхода DPI.",
                    "config_required": False,
                },
            },
        },
        "Gentoo": {
            "icon": "gentoo.png",
            "color": "#2E3440",
            "package_manager": "sudo -S emerge app-portage/git",
            "bypasses": {
                "Shadowsocks": {
                    "command": "sudo -S emerge net-proxy/shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "Obfs4": {
                    "command": "sudo -S emerge net-proxy/obfs4proxy",
                    "info": "Obfs4 — обфускация трафика для обхода DPI.",
                    "config_required": False,
                },
            },
        },
        "OpenSUSE": {
            "icon": "opensuse.png",
            "color": "#2E3440",
            "package_manager": "sudo -S zypper install -y git",
            "bypasses": {
                "Shadowsocks": {
                    "command": "sudo -S zypper install -y shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "Obfs4": {
                    "command": "sudo -S zypper install -y obfs4proxy",
                    "info": "Obfs4 — обфускация трафика для обхода DPI.",
                    "config_required": False,
                },
            },
        },
        "Manjaro": {
            "icon": "manjaro.png",
            "color": "#2E3440",
            "package_manager": "sudo -S pacman -S --needed --noconfirm git",
            "bypasses": {
                "Shadowsocks": {
                    "command": "sudo -S pacman -S --needed --noconfirm shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "Obfs4": {
                    "command": "sudo -S pacman -S --needed --noconfirm obfs4proxy",
                    "info": "Obfs4 — обфускация трафика для обхода DPI.",
                    "config_required": False,
                },
            },
        },
        "Solus": {
            "icon": "solus.png",
            "color": "#2E3440",
            "package_manager": "sudo -S eopkg install -y git",
            "bypasses": {
                "Shadowsocks": {
                    "command": "sudo -S eopkg install -y shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "Obfs4": {
                    "command": "sudo -S eopkg install -y obfs4proxy",
                    "info": "Obfs4 — обфускация трафика для обхода DPI.",
                    "config_required": False,
                },
            },
        },
        "Alpine": {
            "icon": "alpine.png",
            "color": "#2E3440",
            "package_manager": "sudo -S apk add git",
            "bypasses": {
                "Shadowsocks": {
                    "command": "sudo -S apk add shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "Obfs4": {
                    "command": "sudo -S apk add obfs4proxy",
                    "info": "Obfs4 — обфускация трафика для обхода DPI.",
                    "config_required": False,
                },
            },
        },
    },
    "Windows": {
        "Windows 7": {
            "icon": "windows7.png",
            "color": "#2E3440",
            "bypasses": {
                "Shadowsocks": {
                    "command": "curl -O https://example.com/shadowsocks.zip && unzip shadowsocks.zip && cd shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "GoodbyeDPI": {
                    "command": "curl -O https://example.com/GoodbyeDPI.zip && unzip GoodbyeDPI.zip && cd GoodbyeDPI",
                    "info": "GoodbyeDPI — инструмент для обхода DPI.",
                    "config_required": False,
                },
            },
        },
        "Windows 8": {
            "icon": "windows8.png",
            "color": "#2E3440",
            "bypasses": {
                "Shadowsocks": {
                    "command": "curl -O https://example.com/shadowsocks.zip && unzip shadowsocks.zip && cd shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "GoodbyeDPI": {
                    "command": "curl -O https://example.com/GoodbyeDPI.zip && unzip GoodbyeDPI.zip && cd GoodbyeDPI",
                    "info": "GoodbyeDPI — инструмент для обхода DPI.",
                    "config_required": False,
                },
            },
        },
        "Windows 10": {
            "icon": "windows10.png",
            "color": "#2E3440",
            "bypasses": {
                "Shadowsocks": {
                    "command": "curl -O https://example.com/shadowsocks.zip && unzip shadowsocks.zip && cd shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "GoodbyeDPI": {
                    "command": "curl -O https://example.com/GoodbyeDPI.zip && unzip GoodbyeDPI.zip && cd GoodbyeDPI",
                    "info": "GoodbyeDPI — инструмент для обхода DPI.",
                    "config_required": False,
                },
            },
        },
        "Windows 11": {
            "icon": "windows11.png",
            "color": "#2E3440",
            "bypasses": {
                "Shadowsocks": {
                    "command": "curl -O https://example.com/shadowsocks.zip && unzip shadowsocks.zip && cd shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "GoodbyeDPI": {
                    "command": "curl -O https://example.com/GoodbyeDPI.zip && unzip GoodbyeDPI.zip && cd GoodbyeDPI",
                    "info": "GoodbyeDPI — инструмент для обхода DPI.",
                    "config_required": False,
                },
            },
        },
    },
    "macOS": {
        "macOS Monterey": {
            "icon": "macos_monterey.png",
            "color": "#2E3440",
            "package_manager": "sudo -S brew install git",
            "bypasses": {
                "Shadowsocks": {
                    "command": "sudo -S brew install shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "Obfs4": {
                    "command": "sudo -S brew install obfs4proxy",
                    "info": "Obfs4 — обфускация трафика для обхода DPI.",
                    "config_required": False,
                },
            },
        },
        "macOS Big Sur": {
            "icon": "macos_bigsur.png",
            "color": "#2E3440",
            "package_manager": "sudo -S brew install git",
            "bypasses": {
                "Shadowsocks": {
                    "command": "sudo -S brew install shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "Obfs4": {
                    "command": "sudo -S brew install obfs4proxy",
                    "info": "Obfs4 — обфускация трафика для обхода DPI.",
                    "config_required": False,
                },
            },
        },
        "macOS Catalina": {
            "icon": "macos_catalina.png",
            "color": "#2E3440",
            "package_manager": "sudo -S brew install git",
            "bypasses": {
                "Shadowsocks": {
                    "command": "sudo -S brew install shadowsocks",
                    "info": "Shadowsocks — инструмент для обхода блокировок.",
                    "config_required": True,
                },
                "Obfs4": {
                    "command": "sudo -S brew install obfs4proxy",
                    "info": "Obfs4 — обфускация трафика для обхода DPI.",
                    "config_required": False,
                },
            },
        },
    }
}

class UnblockifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unblockify - DPI Bypass Tool")
        self.setup_ui()
        self.set_dark_theme()
        self.resize_elements()

    def set_dark_theme(self):
        self.root.configure(background="#2E3440")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#2E3440", foreground="#D8DEE9", fieldbackground="#3B4252")
        style.configure("TButton", background="#4C566A", foreground="#D8DEE9")
        style.configure("TLabel", background="#2E3440", foreground="#D8DEE9")
        style.configure("TCombobox", fieldbackground="#3B4252", foreground="#D8DEE9")
        style.configure("TEntry", fieldbackground="#3B4252", foreground="#D8DEE9")
        style.configure("TFrame", background="#2E3440")

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.os_label = ttk.Label(self.main_frame, text="Выберите ОС/Дистрибутив:")
        self.os_label.pack(pady=5)
        
        # Создаем комбобокс для выбора ОС
        self.os_combobox = ttk.Combobox(self.main_frame, values=list(OS_CONFIG.keys()))
        self.os_combobox.pack(pady=5, fill=tk.X)
        self.os_combobox.bind("<<ComboboxSelected>>", self.update_ui)

        self.distro_label = ttk.Label(self.main_frame, text="Выберите дистрибутив:")
        self.distro_label.pack(pady=5)
        
        # Создаем комбобокс для выбора дистрибутивов
        self.distro_combobox = ttk.Combobox(self.main_frame, values=[])
        self.distro_combobox.pack(pady=5, fill=tk.X)
        self.distro_combobox.bind("<<ComboboxSelected>>", self.update_bypass_selection)

        self.bypass_label = ttk.Label(self.main_frame, text="Выберите обход:")
        self.bypass_label.pack(pady=5)
        
        self.bypass_combobox = ttk.Combobox(self.main_frame, values=[])
        self.bypass_combobox.pack(pady=5, fill=tk.X)
        self.bypass_combobox.bind("<<ComboboxSelected>>", self.update_bypass_selection)

        self.password_label = ttk.Label(self.main_frame, text="Введите пароль администратора:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.main_frame, show="*")
        self.password_entry.pack(pady=5, fill=tk.X)
        self.password_entry.bind("<KeyRelease>", self.update_button_states)

        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=10)

        self.install_button = ttk.Button(self.buttons_frame, text="Установить", command=self.install, state=tk.DISABLED)
        self.install_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(self.buttons_frame, text="Удалить", command=self.remove, state=tk.DISABLED)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.generate_config_button = ttk.Button(self.buttons_frame, text="Сгенерировать конфиг", command=self.generate_config, state=tk.DISABLED)
        self.generate_config_button.pack(side=tk.LEFT, padx=5)

        self.help_button = ttk.Button(self.buttons_frame, text="Что мне делать?", command=self.show_help)
        self.help_button.pack(side=tk.LEFT, padx=5)

        self.root.bind("<Configure>", self.resize_elements)

    def resize_elements(self, event=None):
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.main_frame.config(width=width, height=height)

    def update_ui(self, event=None):
        selected_os = self.os_combobox.get()
        if selected_os in OS_CONFIG:
            self.distro_combobox["values"] = list(OS_CONFIG[selected_os].keys())
            self.distro_combobox.set('')  # Очищаем выбор дистрибутива
            self.bypass_combobox.set('')  # Очищаем выбор обхода
            self.update_button_states()

    def update_bypass_selection(self, event=None):
        selected_os = self.os_combobox.get()
        selected_distro = self.distro_combobox.get()
        if selected_os in OS_CONFIG and selected_distro in OS_CONFIG[selected_os]:
            self.bypass_combobox["values"] = list(OS_CONFIG[selected_os][selected_distro]["bypasses"].keys())
            self.update_button_states()

    def update_button_states(self, event=None):
        has_os = bool(self.os_combobox.get())
        has_distro = bool(self.distro_combobox.get())
        has_bypass = bool(self.bypass_combobox.get())
        has_password = bool(self.password_entry.get())

        self.install_button["state"] = tk.NORMAL if has_os and has_distro and has_bypass and has_password else tk.DISABLED
        self.remove_button["state"] = tk.NORMAL if has_os and has_distro and has_bypass and self.is_program_installed() else tk.DISABLED
        self.generate_config_button["state"] = tk.NORMAL if has_os and has_distro and has_bypass and OS_CONFIG[self.os_combobox.get()][self.distro_combobox.get()]["bypasses"][self.bypass_combobox.get()]["config_required"] else tk.DISABLED

    def run_command(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if stdout:
            print(stdout.decode())
        if stderr:
            print(stderr.decode())

        return process.returncode

    def is_program_installed(self):
        selected_os = self.os_combobox.get()
        selected_distro = self.distro_combobox.get()
        selected_bypass = self.bypass_combobox.get()

        if selected_os in OS_CONFIG and selected_distro in OS_CONFIG[selected_os] and selected_bypass in OS_CONFIG[selected_os][selected_distro]["bypasses"]:
            # Здесь вы можете проверить, установлена ли программа (например, с помощью команды which или проверка на наличие папки)
            # Это нужно доработать в зависимости от конкретного обходника
            return True  # Предположим, что программа установлена
        return False

    def install_git(self):
        selected_os = self.os_combobox.get()
        selected_distro = self.distro_combobox.get()
        if selected_os not in OS_CONFIG or not OS_CONFIG[selected_os][selected_distro]["package_manager"]:
            return

        print("Проверка наличия git...")
        if self.run_command("which git") != 0:  # Если команда не выполнена успешно
            print("Установка git...")
            self.run_command(f"echo {self.password_entry.get()} | {OS_CONFIG[selected_os][selected_distro]['package_manager']}")
            print("Git установлен.")
        else:
            print("Git уже установлен.")

    def install(self):
        selected_os = self.os_combobox.get()
        selected_distro = self.distro_combobox.get()
        selected_bypass = self.bypass_combobox.get()
        password = self.password_entry.get()
        if not selected_os or not selected_distro or not selected_bypass or not password:
            print("Ошибка: Выберите ОС, дистрибутив, обход и введите пароль!")
            return

        config = OS_CONFIG[selected_os][selected_distro]
        bypass = config["bypasses"][selected_bypass]
        print(f"Установка {selected_bypass} для {selected_distro} на {selected_os}...")

        if selected_os in ["Linux"]:
            self.install_git()

        print(f"Выполнение команды: {bypass['command']}")
        self.run_command(f"echo {password} | {bypass['command']}")
        print("Установка завершена.")

    def remove(self):
        selected_os = self.os_combobox.get()
        selected_distro = self.distro_combobox.get()
        selected_bypass = self.bypass_combobox.get()
        password = self.password_entry.get()
        if not selected_os or not selected_distro or not selected_bypass or not password:
            print("Ошибка: Выберите ОС, дистрибутив, обход и введите пароль!")
            return

        print(f"Удаление {selected_bypass} для {selected_distro} на {selected_os}...")
        # Здесь вы можете добавить логику для удаления программы
        # Например, проверка, как удалить программу
        print("Удаление завершено.")

    def generate_config(self):
        selected_os = self.os_combobox.get()
        selected_distro = self.distro_combobox.get()
        selected_bypass = self.bypass_combobox.get()
        if not selected_os or not selected_distro or not selected_bypass:
            print("Ошибка: Выберите ОС, дистрибутив и обход!")
            return

        print(f"Генерация конфигурации для {selected_bypass}...")
        # Здесь вы можете добавить логику генерации конфигурации
        print("Конфигурация сгенерирована.")

    def show_help(self):
        selected_os = self.os_combobox.get()
        selected_distro = self.distro_combobox.get()
        selected_bypass = self.bypass_combobox.get()
        if selected_os in OS_CONFIG and selected_distro in OS_CONFIG[selected_os] and selected_bypass in OS_CONFIG[selected_os][selected_distro]["bypasses"]:
            info = OS_CONFIG[selected_os][selected_distro]["bypasses"][selected_bypass]["info"]
            messagebox.showinfo("Что мне делать?", info)
        else:
            print("Ошибка: Сначала выберите ОС, дистрибутив и обход!")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnblockifyApp(root)
    root.mainloop()
