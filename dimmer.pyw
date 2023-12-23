import ctypes
from ctypes import wintypes
import time

class DISPLAY_DEVICEW(ctypes.Structure):
    _fields_ = [
        ('cb', wintypes.DWORD),
        ('DeviceName', wintypes.WCHAR * 32),
        ('DeviceString', wintypes.WCHAR * 128),
        ('StateFlags', wintypes.DWORD),
        ('DeviceID', wintypes.WCHAR * 128),
        ('DeviceKey', wintypes.WCHAR * 128)
    ]

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


def get_screen_names():
    screen_names = []
    def monitor_enum_callback(device_name, device_context, device_flags, dwData):
        screen_names.append(device_name)
        return 1  # Continue enumeration
    user32.EnumDisplayDevicesW(None, 0, ctypes.pointer(DISPLAY_DEVICEW()), 0)
    device_name = wintypes.WCHAR * 32  # Adjust the size as needed
    display_device = DISPLAY_DEVICEW()
    display_device.cb = ctypes.sizeof(display_device)
    index = 0
    while user32.EnumDisplayDevicesW(None, index, ctypes.pointer(display_device), 0):
        monitor_enum_callback(display_device.DeviceName, None, 0, 0)
        index += 1
    return screen_names

hdcs = []
for screen_name in get_screen_names():
    hdc = ctypes.windll.gdi32.CreateDCW(screen_name, None, None, 0)
    print("Found", screen_name, "as", hdc)
    hdcs.append(hdc)

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def reset_gamma():
    set_gamma(1, 1, 1, 1, 0)

def set_gamma(r, g, b, v = 1, o = 0):
    gamma_ramp = (ctypes.c_ushort * 256 * 3)()
    for i in range(256):
        value = (i / 255 + o)
        gamma_ramp[0][i] = int(65535 * clamp(value * r * v, 0, 1))
        gamma_ramp[1][i] = int(65535 * clamp(value * g * v, 0, 1))
        gamma_ramp[2][i] = int(65535 * clamp(value * b * v, 0, 1))
    # Set the gamma ramp values
    for hdc in hdcs:
        ctypes.windll.gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(gamma_ramp))


import tkinter as tk

red_slider: tk.Scale
green_slider: tk.Scale
blue_slider: tk.Scale
all_slider: tk.Scale
offest_slider: tk.Scale

def on_value_change(value):
    set_gamma(red_slider.get(), green_slider.get(), blue_slider.get(), all_slider.get(), offest_slider.get())

presets = {
    "default": (1, 1, 1, 1, 0),
    "dark": (1, 1, 1, 0.5, 0),
    "dark-warm": (1, 0.5, 0.3, 0.5, 0),
    "dark-fire": (1, 0.3, 0.1, 0.1, 0),
}

root = tk.Tk()
root.title("RGB Sliders")

def on_select_preset(*preset):
    red_slider.set(preset[0])
    green_slider.set(preset[1])
    blue_slider.set(preset[2])
    all_slider.set(preset[3])
    offest_slider.set(preset[4])
    set_gamma(*preset)

for preset_name, preset in presets.items():
    tk.Button(root, text=preset_name, command=lambda preset=preset: on_select_preset(*preset)).pack()

red_slider = tk.Scale(root, from_=0.1, to=1, resolution=0.01, length=200, label="Red", orient=tk.HORIZONTAL, command=on_value_change)
red_slider.set(1)
red_slider.pack()

green_slider = tk.Scale(root, from_=0.1, to=1, resolution=0.01, length=200, label="Green", orient=tk.HORIZONTAL, command=on_value_change)
green_slider.set(1)
green_slider.pack()

blue_slider = tk.Scale(root, from_=0.1, to=1, resolution=0.01, length=200, label="Blue", orient=tk.HORIZONTAL, command=on_value_change)
blue_slider.set(1)
blue_slider.pack()

all_slider = tk.Scale(root, from_=0.05, to=2, resolution=0.01, length=200, label="All", orient=tk.HORIZONTAL, command=on_value_change)
all_slider.set(1)
all_slider.pack()

offest_slider = tk.Scale(root, from_=-1, to=1, resolution=0.01, length=200, label="offset", orient=tk.HORIZONTAL, command=on_value_change)
offest_slider.set(0)
offest_slider.pack()

root.mainloop()
