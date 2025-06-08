# Basic sample GUI for ChatFlow
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

window = ttk.Window(themename="superhero")
btn_send = ttk.Button(window, text="Send", bootstyle="success")
btn_send.pack(side=LEFT, padx=5, pady=10)
btn_attach = ttk.Button(window, text="Attach", bootstyle="info-outline")
btn_attach.pack(side=LEFT, padx=5, pady=10)

window.mainloop()
