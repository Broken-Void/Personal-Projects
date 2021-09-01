# Sashin Amichand 2021/09/01 
# First personal python project! It is a simple GUI app that will allow me to calculate costs for products with GST included.
# Plan to add: USD/AUD to NZD conversion.
import tkinter as tk
from tkinter import Tk, ttk
from PIL import ImageTk, Image
import sys, tkinter.messagebox

root = tk.Tk()
root.title("Product Price Calculator")

# Variables Used
GST = 0.15
product_cost = tk.IntVar()
shipping_cost = tk.IntVar()
bg_color = '#3a3657'
txt_color = "#9580ff"
font_txt = 'open sans', 12, ''
font_entry = 'open sans', 10, ''
intro = "Hello there! \n This little app will allow you to quickly calculate a \n product total cost, GST inclusive!\n"

# Setting colours/styling
root.configure(background=bg_color)

MFrame = ttk.Style()
MFrame.theme_use('clam')
MFrame.configure('MF.TFrame', background=bg_color)
TLabel = ttk.Style()
TLabel.configure('L.TLabel', background=bg_color, foreground=txt_color)

# Setting Frames
mainFrame = ttk.Frame(root, width=500, height=500, style="MF.TFrame")
mainFrame.grid(row=0, column=0, padx=5, pady=5)

btnFrame = ttk.Frame(root, width=500, height=500)
btnFrame.grid(row=2, column=0, padx=5, pady=5)

# Labels lbluser = ttk.Label(userlogin2, text="Enter your name:", font=('arial', 12,''), anchor = 'w', style='L.TLabel', foreground=self.master.txtcolor)
lblIntro = ttk.Label(mainFrame, text=intro, font=('open sans', 13, 'bold'), justify='center', anchor="center", style='L.TLabel')
lblIntro.grid(row=0, columnspan=2)

lblProduct = ttk.Label(mainFrame, text="Product Cost:", font=(font_txt), style='L.TLabel')
lblProduct.grid(row=1, column=0, sticky="e", padx=10, pady=20)

productEntry = ttk.Entry(mainFrame, textvariable=product_cost, width=5, font=(font_entry))
productEntry.grid(row=1, column=1, sticky="w")
productEntry.focus()

lblShipping = ttk.Label(mainFrame, text="Shipping Cost:", font=(font_txt), style='L.TLabel')
lblShipping.grid(row=2, column=0, sticky="e", padx=10, pady=5)

shippingEntry = ttk.Entry(mainFrame, textvariable=shipping_cost, width=5, font=(font_entry))
shippingEntry.grid(row=2, column=1, sticky="w")

lblGST = ttk.Label(mainFrame, text="GST used in the calculation is 15%", font=('open sans', 10, 'italic'), anchor="center", style='L.TLabel')
lblGST.grid(row=3, columnspan=2, pady=10)

# Functions
def calculation():
    total_cost = (product_cost.get()) + (shipping_cost.get())
    total_gst = total_cost * GST
    cost_txt = "Total Cost Of: " + str(total_cost + total_gst)
    lblCost = ttk.Label(mainFrame, text=cost_txt, font=(font_txt), style='L.TLabel')
    lblCost.grid(row=4, columnspan=2)

# Buttons
btnCalculate = ttk.Button(btnFrame, text="Calculate!", width="20", command=lambda: calculation())
btnCalculate.grid(row=5, column=2)

root.mainloop()   