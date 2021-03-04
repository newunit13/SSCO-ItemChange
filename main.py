import pandas as pd
from fpdf import FPDF



#create PDF object
class PDF(FPDF):
    pass

pdf = PDF(format='Letter')
pdf.add_page()




df = pd.read_excel("data/data.xlsx")

grouped_df = df.groupby(['Acct'])

for customer_df in grouped_df:

    items_df = customer_df[1]

    if len(items_df) == 1:
        record = items_df[['Name', 'Item #', 'Item Name', 'Customer Part #', 'Unit', 'New Price']]
        customer = record['Name'].item()
        item_no = record['Item #'].item()
        item_name = record['Item Name'].item().strip()
        cust_item_no = record['Customer Part #']
        item_uom = record['Unit']
        price = float(record['New Price'].item())
        
        print(f"Customer: {customer}\n\tItem: {item_no}\tDescription: {item_name}\tNew Price: {price:02f}")
    else:
        print(f"\nCustomer: {customer_df[1]['Name'].iloc[0]}")
        for record in customer_df[1][['Name', 'Item #', 'Item Name', 'Customer Part #', 'Unit', 'New Price']].iterrows():
            item_no = record[1]['Item #']
            item_name = record[1]['Item Name'].strip()
            cust_item_no = record[1]['Customer Part #']
            item_uom = record[1]['Unit']
            price = float(record[1]['New Price'])
            print(f"\tItem: {item_no}\tDescription: {item_name}\tNew Price: {price:02f}")
        print()
