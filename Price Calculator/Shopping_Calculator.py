# Sashin Amichand 2021/09/01 
# First personal python project! It is a simple GUI app that will allow me to calculate costs for products with GST included. Now includes a USD/AUD converter to NZD!
# Next goal: Include a calculator
import os 
import tkinter as tk
from tkinter import ttk
from decimal import Decimal

class ShoppingCalculator:
    def __init__(self, master):
        self.master = master

        # Variables for styling
        self.bg_color = '#3a3657'
        self.master.configure(background=self.bg_color)
        self.txt_color = "#9580ff"
        self.font_txt = 'open sans', 12, ''
        self.font_entry = 'open sans', 10, ''

        # Setting colours/styling
        self.Mframe = ttk.Style()
        self.Mframe.theme_use('clam')
        self.Mframe.configure('MF.TFrame', background=self.bg_color)
        self.TLabel = ttk.Style()
        self.TLabel.configure('TLabel', background=self.bg_color, foreground=self.txt_color)

        # Setting Frames
        self.frm_Price = ttk.Frame(self.master, width=500, height=500, style="MF.TFrame")
        self.frm_Price.grid(row=0, column=0, padx=5, pady=5)

        self.frm_Conversion = ttk.Frame(self.master, width=500, height=200, style="MF.TFrame")
        self.frm_Conversion.grid(row=6, column=0, padx=5, pady=5)
        
        self.get_rates()
        self.price_display()
        self.conversion_display()

    def get_rates(self):
        import bs4, requests
        
        converter = requests.get("https://www.x-rates.com/table/?from=NZD&amount=1") # X-rates is the website in which I source the conversion rates, all rights are theirs.
        soup = bs4.BeautifulSoup(converter.content, 'html.parser')

        self.USD_rate = soup.find_all('td')[2].text # The [number] is = to the table position
        self.AUD_rate = soup.find_all('td')[14].text
        return

    def price_display(self):
        self.product_cost = tk.IntVar()
        self.shipping_cost = tk.IntVar()
        self.GST = 0.15

        lbl_Intro = ttk.Label(self.frm_Price, text="Hello There! \n This little app will allow you to quickly calculate a \n products total cost, GST inclusive! \n Also down below is a USD and AUD converter!",
        font=('open sans', 13, 'bold'), justify='center', anchor="center", style='TLabel')
        lbl_Intro.grid(row=0, columnspan=3)

        lbl_GST = ttk.Label(self.frm_Price, text="GST used in the calculation is 15%", font=('open sans', 10, 'italic'), anchor="center", style='TLabel')
        lbl_GST.grid(row=1, columnspan=3, pady=10)

        lbl_Product = ttk.Label(self.frm_Price, text="Product Cost:", font=(self.font_txt), style='TLabel')
        lbl_Product.grid(row=2, column=1, sticky="w", padx=5, pady=10)

        entry_Product = ttk.Entry(self.frm_Price, textvariable=self.product_cost, width=5, font=(self.font_entry))
        entry_Product.grid(row=2, column=2, sticky="w")
        entry_Product.bind("<Return>", lambda event: self.calculate_price())
        entry_Product.focus()

        lbl_Shipping = ttk.Label(self.frm_Price, text="Shipping Cost:", font=(self.font_txt), style='TLabel')
        lbl_Shipping.grid(row=3, column=1, sticky="w", padx=5, pady=10)

        entry_Shipping = ttk.Entry(self.frm_Price, textvariable=self.shipping_cost, width=5, font=(self.font_entry))
        entry_Shipping.grid(row=3, column=2, sticky="w")
        entry_Shipping.bind("<Return>", lambda event: self.calculate_price())
    
        btnCalculate = ttk.Button(self.frm_Price, text="Calculate!", width="20", command=lambda: self.calculate_price())
        btnCalculate.grid(row=4, columnspan=3, pady=10)

    def calculate_price(self):
        total_cost = self.product_cost.get() + self.shipping_cost.get()
        total_gst = total_cost * self.GST
        cost_txt = 'Total Cost: ' + '$' + str(round(total_cost + total_gst, 2))

        lbl_Cost = ttk.Label(self.frm_Price, text=cost_txt, font=(self.font_txt), style='TLabel', foreground="red")
        lbl_Cost.grid(row=5, columnspan=3, pady=10)
        return

    def conversion_display(self):
        self.currency = {"Currency": None,
                        "USD": Decimal(self.USD_rate), 
                        "AUD": Decimal(self.AUD_rate)}
        self.conversion = tk.StringVar()
        self.conversion_amount = tk.IntVar()

        opt_Conversion = ttk.OptionMenu(self.frm_Conversion, self.conversion, *self.currency)
        opt_Conversion.grid(row=6, column=0, sticky="e", padx=10, pady=5)

        entry_Conversion = ttk.Entry(self.frm_Conversion, textvariable=self.conversion_amount, width=5, font=(self.font_entry))
        entry_Conversion.grid(row=6, column=1, sticky="ew", padx=4)
        entry_Conversion.bind("<Return>", (lambda event: self.calculate_conversion()))
    
        btnCalculate = ttk.Button(self.frm_Conversion, text="Calculate!", width="20", command=lambda: self.calculate_conversion())
        btnCalculate.grid(row=7, columnspan=3, pady=10)

    def calculate_conversion(self):
        new_conversion = self.conversion.get()    
        new_amount = self.conversion_amount.get()
        try:
            new_cost = new_amount * self.currency[new_conversion]
        except TypeError:
            lblError = ttk.Label(self.frm_Conversion, text="Please choose a currency".upper(), font=('open sans', '12', 'bold'), style='TLabel', foreground="red")
            lblError.grid(row=8, columnspan=3, padx=5, pady=5) 
            self.frm_Price.after(5000, lblError.destroy)
            return 

        lblConversion = ttk.Label(self.frm_Conversion, text="NZD $" + str(round(new_cost,2)).upper(), font=('open sans', '12', 'bold'), style='TLabel', foreground="red")
        lblConversion.grid(row=8, columnspan=3,  padx=5, pady=5)
        return

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__)) # Ensures directory is right so that the icon does not cause issues.
    root = tk.Tk()
    root.title("Shopping Calculator")
    root.iconbitmap('logo.ico') # The image used is not mine and all rights go to the rightful owner.
    ShoppingCalculator(root)
    root.mainloop()    