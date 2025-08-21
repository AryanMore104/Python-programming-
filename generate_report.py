import pandas as pd
from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Automated Sales Report - India Division', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_report(report_filename):
    
    sales_data = [
        {'Date': '2023-11-01', 'Salesperson': 'Priya Sharma', 'Product': 'Laptop', 'Quantity': 5, 'Price': 75000},
        {'Date': '2023-11-01', 'Salesperson': 'Rohan Gupta', 'Product': 'Smartphone', 'Quantity': 10, 'Price': 45000},
        {'Date': '2023-11-02', 'Salesperson': 'Anjali Singh', 'Product': 'Headphones', 'Quantity': 15, 'Price': 3000},
        {'Date': '2023-11-03', 'Salesperson': 'Vikram Patel', 'Product': 'Smartwatch', 'Quantity': 8, 'Price': 18000},
        {'Date': '2023-11-04', 'Salesperson': 'Meera Desai', 'Product': 'Keyboard', 'Quantity': 20, 'Price': 2500},
        {'Date': '2023-11-05', 'Salesperson': 'Arjun Reddy', 'Product': 'Mouse', 'Quantity': 30, 'Price': 800},
        {'Date': '2023-11-06', 'Salesperson': 'Sunita Rao', 'Product': 'Monitor', 'Quantity': 7, 'Price': 22000},
        {'Date': '2023-11-07', 'Salesperson': 'Rajesh Kumar', 'Product': 'Laptop', 'Quantity': 3, 'Price': 80000},
        {'Date': '2023-11-08', 'Salesperson': 'Kavita Iyer', 'Product': 'Smartphone', 'Quantity': 12, 'Price': 50000},
        {'Date': '2023-11-09', 'Salesperson': 'Sameer Khan', 'Product': 'Headphones', 'Quantity': 25, 'Price': 2800},
        {'Date': '2023-11-10', 'Salesperson': 'Priya Sharma', 'Product': 'Smartwatch', 'Quantity': 10, 'Price': 17500},
        {'Date': '2023-11-11', 'Salesperson': 'Rohan Gupta', 'Product': 'Keyboard', 'Quantity': 18, 'Price': 2600},
        {'Date': '2023-11-12', 'Salesperson': 'Anjali Singh', 'Product': 'Mouse', 'Quantity': 40, 'Price': 750},
        {'Date': '2023-11-13', 'Salesperson': 'Vikram Patel', 'Product': 'Monitor', 'Quantity': 6, 'Price': 23000},
        {'Date': '2023-11-14', 'Salesperson': 'Meera Desai', 'Product': 'Laptop', 'Quantity': 4, 'Price': 78000},
        {'Date': '2023-11-15', 'Salesperson': 'Arjun Reddy', 'Product': 'Smartphone', 'Quantity': 8, 'Price': 48000},
        {'Date': '2023-11-16', 'Salesperson': 'Sunita Rao', 'Product': 'Headphones', 'Quantity': 22, 'Price': 3200},
        {'Date': '2023-11-17', 'Salesperson': 'Rajesh Kumar', 'Product': 'Smartwatch', 'Quantity': 15, 'Price': 19000},
        {'Date': '2023-11-18', 'Salesperson': 'Kavita Iyer', 'Product': 'Keyboard', 'Quantity': 25, 'Price': 2400},
        {'Date': '2023-11-19', 'Salesperson': 'Sameer Khan', 'Product': 'Mouse', 'Quantity': 50, 'Price': 850},
        {'Date': '2023-11-20', 'Salesperson': 'Priya Sharma', 'Product': 'Monitor', 'Quantity': 5, 'Price': 21000},
        {'Date': '2023-11-21', 'Salesperson': 'Rohan Gupta', 'Product': 'Laptop', 'Quantity': 2, 'Price': 95000},
        {'Date': '2023-11-22', 'Salesperson': 'Anjali Singh', 'Product': 'Smartphone', 'Quantity': 7, 'Price': 55000},
        {'Date': '2023-11-23', 'Salesperson': 'Vikram Patel', 'Product': 'Headphones', 'Quantity': 18, 'Price': 3500},
        {'Date': '2023-11-24', 'Salesperson': 'Meera Desai', 'Product': 'Smartwatch', 'Quantity': 12, 'Price': 20000},
    ]
    
    df = pd.DataFrame(sales_data)
    df['TotalSale'] = df['Quantity'] * df['Price']
    
    total_revenue = df['TotalSale'].sum()
    average_sale = df['TotalSale'].mean()
    top_performer = df.groupby('Salesperson')['TotalSale'].sum().idxmax()

    pdf = PDF()
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '1. Executive Summary', ln=True)
    
    pdf.set_font('Arial', '', 11)
    summary_text = (
        f"  - Total Revenue: INR {total_revenue:,.2f}\n"
        f"  - Average Sale Value: INR {average_sale:,.2f}\n"
        f"  - Top Performing Salesperson: {top_performer}"
    )
    pdf.multi_cell(0, 8, summary_text)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '2. Full Sales Data', ln=True)
    
    pdf.set_font('Arial', 'B', 10)
    col_widths = [25, 35, 35, 20, 30, 35]
    headers = ['Date', 'Salesperson', 'Product', 'Qty', 'Price', 'Total Sale']
    
    for i, header_title in enumerate(headers):
        pdf.cell(col_widths[i], 10, header_title, 1, 0, 'C')
    pdf.ln()
    
    pdf.set_font('Arial', '', 9)
    for index, row in df.iterrows():
        pdf.cell(col_widths[0], 10, str(row['Date']), 1)
        pdf.cell(col_widths[1], 10, str(row['Salesperson']), 1)
        pdf.cell(col_widths[2], 10, str(row['Product']), 1)
        pdf.cell(col_widths[3], 10, str(row['Quantity']), 1, 0, 'C')
        pdf.cell(col_widths[4], 10, f"{row['Price']:,}", 1, 0, 'R')
        pdf.cell(col_widths[5], 10, f"{row['TotalSale']:,}", 1, 0, 'R')
        pdf.ln()
        
    pdf.output(report_filename)
    print(f"Success! Report saved as '{report_filename}'")

if __name__ == "__main__":
    create_report(report_filename='sales_report_india.pdf')