import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import mysql.connector

class BillGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Bill Generator")

        # Customer details will be taken here
        self.label_customer = tk.Label(master, text="Customer Name:")
        self.label_customer.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.input_customer = tk.Entry(master)
        self.input_customer.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.label_address = tk.Label(master, text="Customer Address:")
        self.label_address.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.input_address = tk.Entry(master)
        self.input_address.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Product details will be taken here
        self.products_frame = tk.Frame(master)
        self.products_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.product_labels = []
        self.quantity_input = []
        self.price_input = []

        # Create fields for the products
        self.add_product()

        # product button 
        self.add_product_button = tk.Button(master, text="Add Product", command=self.add_product)
        self.add_product_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # button of generating invoices/bill 
        self.button = tk.Button(master, text="Generate Invoice", command=self.generate_invoice)
        self.button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

         # Connection to MySQL database pydb
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sql@123",
            database="pydb"
        )

    #product adding function
    def add_product(self):
         
        label_product = tk.Label(self.products_frame, text="Product Name:")
        label_product.grid(row=2, column=0,padx=10, pady=5, sticky="e")

        input_product = tk.Entry(self.products_frame)
        input_product.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.product_labels.append(input_product)

        label_quantity = tk.Label(self.products_frame, text="Quantity:")
        label_quantity.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        input_quantity = tk.Entry(self.products_frame)
        input_quantity.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.quantity_input.append(input_quantity)

        label_price = tk.Label(self.products_frame, text="Price:")
        label_price.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        input_price = tk.Entry(self.products_frame)
        input_price.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.price_input.append(input_price)

   
   #function for generate invoices/bills
    def generate_invoice(self):
        # Get customer details
        customer_name = self.input_customer.get()
        customer_address = self.input_address.get()

        products = []
        for i in range(len(self.product_labels)):
            product_name = self.product_labels[i].get()
            quantity_str = self.quantity_input[i].get()
            price_str = self.price_input[i].get()

            #input files are empty or not
            if quantity_str and price_str:
                quantity = int(quantity_str)
                price = float(price_str)
                total = quantity * price
                products.append([product_name, quantity, price, total])
            else:
                # if empty than show error 
                messagebox.showerror("Error", "Please fill in quantity and price for all products.")
                return  


        # Save data to MySQL database pydb
        cursor = self.conn.cursor()
        for product in products:
            cursor.execute("INSERT INTO invoices (customer_name, customer_address, product_name, quantity, price, total) VALUES (%s, %s, %s, %s, %s, %s)",
                        (customer_name, customer_address, product[0], product[1], product[2], product[3]))
        self.conn.commit()

        # pdf will be generated with customer name
        pdf_filename = "{}_invoice.pdf".format(customer_name.replace(" ", "_"))  # Replace spaces in customer name with underscores
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        data = [["Customer Name", "Customer Address", "Product Name", "Quantity", "Price", "Total"]]
        for p in products:
            data.append([customer_name, customer_address, p[0], p[1], p[2], p[3]])
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        doc.build([table])

        # invoice generated message
        print("Invoice Generated Successfully!!")
        messagebox.showinfo("Success", "Invoice generated successfully. Invoice saved as '{}'.".format(pdf_filename))

# window of Tkinter
root = tk.Tk()
app = BillGeneratorApp(root)
root.mainloop()
