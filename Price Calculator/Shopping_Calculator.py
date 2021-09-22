# 2021/09/01 
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
        self.font_txt = 'Cormorant', 12, ''
        self.font_output = 'Cormorant', '12', 'bold'
        self.font_entry = 'Cormorant', 10, ''

        # Setting colours/styling
        self.Mframe = ttk.Style()
        # Just simply import the azure.tcl file

        # Then set the theme you want with the set_theme procedure
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
        
        # get combox box store in variable. then iterate over it till it finds the right one
        self.USD_rate = soup.find_all('td')[2].text # The [number] is = to the table position
        self.AUD_rate = soup.find_all('td')[14].text

    def price_display(self):
        self.product_cost = tk.IntVar()
        self.shipping_cost = tk.IntVar()
        self.GST = 0.15

        lbl_Intro = ttk.Label(self.frm_Price, text="Hello There! \n This little app will allow you to quickly calculate a \n products total cost, GST inclusive! \n Also down below is a USD and AUD converter!",
        font=('Cormorant', 13, 'bold'), justify='center', anchor="center", style='TLabel')
        lbl_Intro.grid(row=0, columnspan=3)

        sep = ttk.Separator(self.frm_Price, orient='horizontal')
        sep.grid(row=1, columnspan=3, sticky='NESW')

        lbl_Calculate = ttk.Label(self.frm_Price, text="product calculator:".title(), font=(self.font_output), style='TLabel')
        lbl_Calculate.grid(row=2, columnspan=3, padx=5, pady=5)

        lbl_Product = ttk.Label(self.frm_Price, text="Product Cost:", font=(self.font_txt), style='TLabel')
        lbl_Product.grid(row=3, column=1, sticky="w", padx=0, pady=15)

        entry_Product = ttk.Entry(self.frm_Price, textvariable=self.product_cost, width=5, font=(self.font_entry))
        entry_Product.grid(row=3, column=1, sticky="e")
        entry_Product.bind("<Return>", lambda event: self.calculate_price())
        entry_Product.focus()

        lbl_Shipping = ttk.Label(self.frm_Price, text="Shipping Cost:", font=(self.font_txt), style='TLabel')
        lbl_Shipping.grid(row=4, column=1, sticky="w", padx=0, pady=10)

        entry_Shipping = ttk.Entry(self.frm_Price, textvariable=self.shipping_cost, width=5, font=(self.font_entry))
        entry_Shipping.grid(row=4, column=1, sticky="e")
        entry_Shipping.bind("<Return>", lambda event: self.calculate_price())

        lbl_GST = ttk.Label(self.frm_Price, text="GST used in the calculation is 15%", font=('Cormorant', 10, 'italic'), anchor="center", style='TLabel')
        lbl_GST.grid(row=5, columnspan=3, pady=5)

        btnCalculate = ttk.Button(self.frm_Price, text="Calculate!", width="20", command=lambda: self.calculate_price())
        btnCalculate.grid(row=6, columnspan=3, pady=10)
        
    def calculate_price(self):
        total_cost = self.product_cost.get() + self.shipping_cost.get()
        total_gst = total_cost * self.GST
        cost_txt = 'Total Cost: ' + '$' + str(round(total_cost + total_gst, 2))

        lbl_Cost = ttk.Label(self.frm_Price, text=cost_txt, font=(self.font_output), style='TLabel')
        lbl_Cost.grid(row=7, columnspan=3, pady=10)

    def conversion_display(self):
        self.currency = {"Currency": None,
                        "USD": Decimal(self.USD_rate), 
                        "AUD": Decimal(self.AUD_rate)}
        self.conversion = tk.StringVar()
        self.conversion_amount = tk.IntVar()

        sep = ttk.Separator(self.frm_Price, orient='horizontal')
        sep.grid(row=8, columnspan=3, sticky='NESW')

        lbl_Convert = ttk.Label(self.frm_Conversion, text="Convert:", font=(self.font_output), style='TLabel')
        lbl_Convert.grid(row=8, columnspan=3, padx=5, pady=0)

        opt_Conversion = ttk.OptionMenu(self.frm_Conversion, self.conversion, *self.currency)
        opt_Conversion.grid(row=9, column=0, sticky="e", padx=10, pady=5)

        entry_Conversion = ttk.Entry(self.frm_Conversion, textvariable=self.conversion_amount, width=5, font=(self.font_entry))
        entry_Conversion.grid(row=9, column=1, sticky="ew", padx=4)
        entry_Conversion.bind("<Return>", (lambda event: self.calculate_conversion()))
    
        btnCalculate = ttk.Button(self.frm_Conversion, text="Calculate!", width="20", command=lambda: self.calculate_conversion())
        btnCalculate.grid(row=10, columnspan=3, pady=10)

    def calculate_conversion(self):
        new_conversion = self.conversion.get()    
        new_amount = self.conversion_amount.get()
        try:
            new_cost = new_amount * self.currency[new_conversion]
        except TypeError:
            lbl_Error = ttk.Label(self.frm_Conversion, text="Please choose a currency".upper(), font=(self.font_output), style='TLabel')
            lbl_Error.grid(row=11, columnspan=3, padx=5, pady=5) 
            self.frm_Price.after(5000, lbl_Error.destroy)

        lbl_Conversion = ttk.Label(self.frm_Conversion, text="NZD $" + str(round(new_cost,2)).upper(), font=(self.font_output), style='TLabel')
        lbl_Conversion.grid(row=11, columnspan=3,  padx=5, pady=5)

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__)) # Ensures directory is right so that the icon does not cause issues.
    root = tk.Tk()
    root.title("Shopping Calculator")
    ShoppingCalculator(root)
    root.mainloop()    
