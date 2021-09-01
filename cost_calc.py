# Sashin Amichand 2021/09/01 
# First personal python project! It is a simple GUI app that will allow me to calculate costs for products with GST included. Now includes a USD/AUD converter to NZD!
# Next goal: Include a calculator

import tkinter as tk
from tkinter import ttk
import bs4, requests
from decimal import Decimal

root = tk.Tk()
root.title("Price Calculator")

# Gets the converter website (x-rate)
converter = requests.get("https://www.x-rates.com/table/?from=NZD&amount=1")
soup = bs4.BeautifulSoup(converter.content, 'html.parser')

# General Variables Used
GST = 0.15
product_cost = tk.IntVar()
shipping_cost = tk.IntVar()

# Variables for currency conversion
USD_rate = soup.find_all('td')[2].text # The number is = to the table position
AUD_rate = soup.find_all('td')[14].text
currency = {"USD": Decimal(USD_rate), "AUD": Decimal(AUD_rate)}
conversion = tk.StringVar()
conversion.set("Currency")
convert_amount = tk.IntVar()

# Variables for styling
bg_color = '#3a3657'
txt_color = "#9580ff"
font_txt = 'open sans', 12, ''
font_entry = 'open sans', 10, ''
intro = "Hello There! \n This little app will allow you to quickly calculate a \n products total cost, GST inclusive! \n Also down below is a USD and AUD converter!"

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

# Labels
lblIntro = ttk.Label(mainFrame, text=intro, font=('open sans', 13, 'bold'), justify='center', anchor="center", style='L.TLabel')
lblIntro.grid(row=0, columnspan=3)

lblGST = ttk.Label(mainFrame, text="GST used in the calculation is 15%", font=('open sans', 10, 'italic'), anchor="center", style='L.TLabel')
lblGST.grid(row=1, columnspan=3, pady=10)

lblProduct = ttk.Label(mainFrame, text="Product Cost:", font=(font_txt), style='L.TLabel')
lblProduct.grid(row=2, column=1, sticky="w", padx=5, pady=10)

productEntry = ttk.Entry(mainFrame, textvariable=product_cost, width=5, font=(font_entry))
productEntry.grid(row=2, column=2, sticky="w")
productEntry.focus()

lblShipping = ttk.Label(mainFrame, text="Shipping Cost:", font=(font_txt), style='L.TLabel')
lblShipping.grid(row=3, column=1, sticky="w", padx=5, pady=10)

shippingEntry = ttk.Entry(mainFrame, textvariable=shipping_cost, width=5, font=(font_entry))
shippingEntry.grid(row=3, column=2, sticky="w")

conversionOption = ttk.OptionMenu(mainFrame, conversion, *currency)
conversionOption.grid(row=6, column=0, sticky="e", padx=10, pady=5)

conversionEntry = ttk.Entry(mainFrame, textvariable=convert_amount, width=5, font=(font_entry))
conversionEntry.grid(row=6, column=1, sticky="ew", padx=4)

# Functions
def calculation():
    total_cost = (product_cost.get()) + (shipping_cost.get())
    total_gst = total_cost * GST
    cost_txt = "Total Cost: " + '$' + str(round(total_cost + total_gst, 2))
    lblCost = ttk.Label(mainFrame, text=cost_txt, font=(font_txt), style='L.TLabel')
    lblCost.grid(row=5, columnspan=3, pady=10)

def convert():
    new_conversion = conversion.get()
    new_amount = convert_amount.get()
    new_cost = new_amount * currency[new_conversion]

    lblConversion = ttk.Label(mainFrame, text='NZD $' + str(round(new_cost,2)), font=(font_txt), style='L.TLabel')
    lblConversion.grid(row=7, columnspan=3, padx=5, pady=5)

# Buttons
btnCalculate = ttk.Button(mainFrame, text="Calculate!", width="20", command=lambda: calculation())
btnCalculate.grid(row=4, columnspan=3, pady=10)

btnConvert = ttk.Button(mainFrame, text="Convert!", width="20", command=lambda: convert())
btnConvert.grid(row=6, column=2, sticky='w', padx=5, pady=10)

root.mainloop()   