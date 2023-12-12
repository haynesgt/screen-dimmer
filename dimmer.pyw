import ctypes
import time

# Get the screen DC (device context)
user32 = ctypes.windll.user32
hdc = user32.GetDC(0)

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def reset_gamma():
    set_gamma(1, 1, 1, 1)

def set_gamma(r, g, b, v, o):
    gamma_ramp = (ctypes.c_ushort * 256 * 3)()
    for i in range(256):
        value = (i / 255 + o)
        gamma_ramp[0][i] = int(65535 * clamp(value * r * v, 0, 1))
        gamma_ramp[1][i] = int(65535 * clamp(value * g * v, 0, 1))
        gamma_ramp[2][i] = int(65535 * clamp(value * b * v, 0, 1))
    # Set the gamma ramp values
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
