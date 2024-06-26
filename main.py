# import os
# import random
# import string
# import winreg
# import netifaces
# import tkinter
# from tkinter import messagebox


# def get_values(key):
#     key_dict = {}
#     i = 0
#     while True:
#         try:
#             sub_value = winreg.EnumValue(key, i)
#         except WindowsError:
#             break
#         key_dict[sub_value[0]] = sub_value[1:]
#         i += 1
#     return key_dict


# def get_correct_interface():
#     current_interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
#     print(current_interface)

#     with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
#         path = string.Template("SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\$n1")
#         key_index = -1

#         while True:
#             key_index += 1
#             key_string = f"{key_index}"
#             key = ("0000" + key_string)[len(key_string):]

#             try:
#                 sub_key = winreg.OpenKey(hkey, path.substitute(n1=key), 0, winreg.KEY_ALL_ACCESS)
#                 selected_interface_values = get_values(sub_key)

#                 if selected_interface_values["NetCfgInstanceId"][0] == current_interface:
#                     return sub_key

#             except PermissionError:
#                 messagebox.showwarning(title="<3", message="This program requires administrator privileges to run.")
#                 root.destroy()
#                 break

#             except WindowsError:
#                 break


# def spoof_mac():
#     sub_key = get_correct_interface()

#     if type(sub_key).__name__ != "PyHKEY":
#         print("No Interface")
#         return

#     winreg.SetValueEx(sub_key, "NetworkAddress", 0, winreg.REG_SZ, f"DE{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}")
#     winreg.CloseKey(sub_key)

#     response = messagebox.askyesno(title="<3",
#                                    message="Your PC Needs To Restart For The Changes To Take Affect.\nRestart Now?")
#     if response:
#         os.system("shutdown /r /t 0")


# def undo_spoof():
#     sub_key = get_correct_interface()

#     if type(sub_key).__name__ != "PyHKEY":
#         print("No Interface")
#         return

#     try:
#         winreg.DeleteValue(sub_key, "NetworkAddress")
#     except WindowsError:
#         messagebox.showinfo(title="<3", message="There Are No Changes To Undo.\nSpoof Is Not Currently Active.")
#         return

#     winreg.CloseKey(sub_key)

#     response = messagebox.askyesno(title="<3",
#                                    message="Your PC Needs To Restart For The Changes To Take Affect.\nRestart Now?")
#     if response:
#         os.system("shutdown /r /t 0")


# root = tkinter.Tk()

# root.title("<3")
# root.geometry("400x200+50+50")
# root.resizable(False, False)

# tkinter.Label(root, text="I am awaiting your command...", width=200, font=("default", 15)).pack(pady=20)
# tkinter.Button(root, text="Spoof Mac Address", command=spoof_mac, font=("default", 10)).pack(pady=5)
# tkinter.Button(root, text="Set Back To Default", command=undo_spoof, font=("default", 10)).pack(pady=5)
# tkinter.Label(root, text="v 1.0.0").pack(side="bottom")

# root.mainloop()






##################
# ALL OS VERSION #
##################

import os
import subprocess
import random
import string

def get_current_mac(interface):
    command = f"ifconfig {interface} | grep ether | awk '{print $2}'" if os.name == "posix" else f"ipconfig /all | findstr /R /C:\"{interface}\" | findstr /R /C:. . .:.. .. .. .. .."
    return subprocess.check_output(command, shell=True).decode().strip()

def change_mac(interface, new_mac):
    if os.name == "posix":
        command = f"ifconfig {interface} down"
        subprocess.check_call(command, shell=True)

        command = f"ifconfig {interface} hw ether {new_mac}"
        subprocess.check_call(command, shell=True)

        command = f"ifconfig {interface} up"
        subprocess.check_call(command, shell=True)
    elif os.name == "nt":
        command = f"wmic nic where netenabled=true get macaddress,index /format:table"
        output = subprocess.check_output(command, shell=True).decode().strip()
        lines = output.split("\n")
        for line in lines:
            if interface in line:
                index = line.split()[1]
                command = f"wmic nic where index={index} call setmacaddress /value {new_mac}"
                subprocess.check_call(command, shell=True)

def generate_random_mac():
    mac = ':'.join('{:02x}'.format(random.randint(0, 255)) for _ in range(6))
    return mac

def spoof_mac(interface):
    current_mac = get_current_mac(interface)
    print(f"Current MAC: {current_mac}")

    new_mac = generate_random_mac()
    print(f"New MAC: {new_mac}")

    change_mac(interface, new_mac)

    print("MAC address has been changed. Please restart the network interface or the system for the changes to take effect.")

def undo_spoof(interface):
    current_mac = get_current_mac(interface)
    print(f"Current MAC: {current_mac}")

    original_mac = "00:11:22:33:44:55"  # Replace with the original MAC address

    change_mac(interface, original_mac)

    print("MAC address has been changed back to the original. Please restart the network interface or the system for the changes to take effect.")

# Replace 'en0' with your network interface name
spoof_mac('en0')
# undo_spoof('en0')
