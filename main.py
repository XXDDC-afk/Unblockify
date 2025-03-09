#Импорты

import os
import sys
import subprocess
import pexpect
import platform
import distro
import tkinter

#Переменные

user_os = sys.platform
win_ver = platform.release
linux_distro = distro.name()
user_password = ""
git_local = ""
brew_local = ""
child = pexpect.spawn("sudo -s")
child.expect("password for")
child.sendline(user_password)


#Линукс

arch_manjaro = {"manager": "pacman", "manager2": "git"}
ubuntu_debian_mint_kali = {"manager": "apt", "manager2": "git"}
fedora_centos = {"manager": "dnf", "manager2": "git"}
opensuse = {"manager": "zypper", "manager2": "git"}
gentoo = {"manager": "emerge", "manager2": "git"}
freebsd = {"manager": "pkg", "manager2": "git"}

#Виндовс

windows7_8 = {"manager": "curl", "manager2": "git"}
windows10_11 = {"manager": "winget", "manager2": "git"}

#Мак

macos_any = {"manager": "brew", "manager2": "git"}

#Скрипты

#Линукс

if user_os == "linux":
    print(f"Найден {linux_distro}")

    user_password = input("Введите пароль для SUDO: ")

    child.interact()

    git = os.popen("which git").read()
    print(git)
    if git:
        print(f"Git найден по пути {git}")
        git_local = True
    else:
        print("Git не найден.")
        git_local = False



    if linux_distro == "Arch Linux" or "Manjaro Linux":
        if git_local == False:
            os.system("pacman -S git --noconfirm")


#Виндовс

if user_os == "win32":
    print(f"Найден Windows {win_ver}")

    git = os.popen("where git").read()
    print(git)
    if git:
        print(f"Git найден по пути {git}")
        git_local = True
    else:
        print("Git не найден.")
        git_local = False

#Мак

if user_os == "darwin":
    print("Найден MacOs")

    brew = os.popen("which brew").read()
    print(brew)
    if brew:
        print(f"Brew найден по пути {brew}")
        brew_local = True
    else:
        print("Brew не найден.")
        brew_local = False

    git = os.popen("which git").read()
    print(git)
    if git:
        print(f"Git найден по пути {git}")
        git_local = True
    else:
        print("Git не найден.")
        git_local = False