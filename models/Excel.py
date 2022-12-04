import pandas as pd
import re
from flask import jsonify

class Excel:
    def __init__(self, file, date_query):
        self.file = file
        self.date_query = date_query
        self.df = self.read_file()
        self.df = self.rename_column()
        self.df = self.get_rows_valid()
        self.ffill_dates()
        self.df = self.get_df_by_date_query()
        self.df = self.get_card_id_not_null()
        
    def read_file(self):
        return pd.read_excel(self.file)
    
    def rename_column(self):
        return self.df.rename(
            columns={
                "Unnamed: 1": "Date", 
                "Unnamed: 2": "Fullname",
                "Unnamed: 3": "Contract code",
                "Unnamed: 4": "Phone number",
                "Unnamed: 5": "Card id",
                "Unnamed: 6": "Date of birth",
                "Unnamed: 7": "Principal outstanding balance",
                "Unnamed: 8": "Pos",
                "Unnamed: 9": "Payment amount",
                "Unnamed: 10": "Date of payment",
                "Unnamed: 11": "Note",
            }
        )
    
    def get_rows_valid(self):
        self.df = self.df.iloc[1:]
        return self.df[self.df['Fullname'].notna()]
    
    def ffill_dates(self):
        return self.df['Date'].fillna(method='ffill', inplace=True)
    
    def get_df_by_date_query(self):
        return self.df[self.df['Date'] == self.date_query]
    
    def get_card_id_not_null(self):
        return self.df[self.df['Card id'] != 0]
    
    def result(self):
        arr = []
        for i in self.df.index:
            result = {
                "stt": i,
                "phone_number": self.df['Phone number'][i],
                "full_name": self.df['Fullname'][i],
                "full_name_no_accent": self.no_accent_vietnamese(self.df['Fullname'][i]),
                "card_id": self.df['Card id'][i],
                "pos": self.df['Pos'][i],
                "payment_amount": self.df['Payment amount'][i],
                "date_of_payment": self.df['Date of payment'][i],
                "contract_code": self.df['Contract code'][i],
                "principal_outstanding_balance": self.df['Principal outstanding balance'][i],
                # "note": self.df['Note'][i],
            }
            arr.append(result)
        return arr
    
    def no_accent_vietnamese(self, s):
        s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
        s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
        s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
        s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
        s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
        s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
        s = re.sub(r'[ìíịỉĩ]', 'i', s)
        s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
        s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
        s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
        s = re.sub(r'[Đ]', 'D', s)
        s = re.sub(r'[đ]', 'd', s)
        return s