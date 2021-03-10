from fpdf import FPDF
import pandas as pd
from datetime import datetime

WIDTH = 210
HEIGHT = 297

class PDF(FPDF):
    def create_header(self, date, cust_acct, cust_name, cust_street, cust_city, cust_state, cust_zip):
        self.set_font('Arial', '', 11)
        self.image('assets/logo.png', (WIDTH/3)*2-20, 20, WIDTH/3)

        # Customer Address
        self.ln(10)
        self.cell(10)
        self.multi_cell(90, 6, f"""
Customer ID: {cust_acct}                             {date}
{cust_name}
{cust_street}
{cust_city}, {cust_state} {cust_zip}
""", 0)
        self.ln(10)

    # table of items
    def create_table_header(self, widths, columns):
        """
        Pass in a list a values to create headers
        """
        self.set_font('Arial', 'B', 11)
        self.set_fill_color(0,150,0)
        self.set_text_color(255)

        for width, header in zip(widths, columns):
            self.cell(width, 5, header, 1,0,'C',True)

        self.set_text_color(0)
        self.set_fill_color(255,255,255)
        self.ln()


    def create_table_row(self, widths, row):
        self.set_font_size(9)
        for idx, (width, datum) in enumerate(zip(widths, row)):
            if idx == 2:
                self.cell(width, 5, self.format_data(datum), 1,0,'',True)
            else:
                self.cell(width, 5, self.format_data(datum), 1,0,'C',True)
        self.ln()

    def create_table_footer(self):
        self.ln(20)
        self.set_font('Arial', '', 11)
        # Signature Area
        self.cell(5)
        self.cell(65, 5, 'Name', 'T', 0, 'C')
        self.cell(7)
        self.cell(65, 5, 'Signature', 'T', 0, 'C')
        self.cell(7)
        self.cell(30, 5, 'Date', 'T' ,0, 'C')

    def format_data(self, datum):

        if type(datum) == str:
            if len(datum) > 30:
                datum = datum[:30] + '...'
        elif type(datum) == float:
            datum = f'${datum:0.02f}'
            if datum == '$nan':
                datum = ''
        elif type(datum) == pd._libs.tslibs.timestamps.Timestamp:
            datum = f'{datum.date().strftime("%m/%d/%Y")}'
        
        return datum

df = pd.read_excel("data/data.xlsx", converters={'Acct': str, 'Customer Zip': int})
grouped_df = df.groupby(['Acct'])

for cust_acct, data in grouped_df:

    pdf = PDF()
    pdf.add_page()

    acct    = cust_acct
    name    = data.iloc[0]["Name"]
    street  = data.iloc[0]["Customer Street"]
    city    = data.iloc[0]["Customer City"]
    state   = data.iloc[0]["Customer State"]
    zipcode = data.iloc[0]["Customer Zip"]
    date    = datetime.today().strftime("%m/%d/%Y")

    pdf.create_header(date, acct, name, street, city, state, zipcode)

    item_df = data[["Item #", 'Customer Part #', 'Item Name', 'Unit', 'New Price', 'Effective Date']]

    widths = [28, 32, 60, 12, 30, 30]
    pdf.create_table_header(widths, item_df.columns)

    for df_idx, row in item_df.iterrows():
        datum = [row["Item #"],
                 row["Customer Part #"],
                 row["Item Name"],
                 row["Unit"],
                 row["New Price"],
                 row["Effective Date"]]
        pdf.create_table_row(widths, datum)
    
    pdf.create_table_footer()
    
    name = ''.join([c for c in name if c not in '\\/?:*<>|'])
    pdf.output(f'output/{name} ({acct}).pdf', 'F')

    #pdf.output('test.pdf', 'F')
    #print()
