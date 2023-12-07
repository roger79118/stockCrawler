# origin
import time
import json
import pandas as pd
import os
import csv

# installed
import requests

#env setting
pd.set_option("display.unicode.ambiguous_as_wide", True)
pd.set_option("display.unicode.east_asian_width", True)

class Company:

    def __init__(self, comp_id: int) -> None: 

        self.comp_id = comp_id
        self.data = None
        self.select = None
        
        self.date = self.today()
        self.pulled = self.pull(self.comp_id, self.today())


    def today(self):

        now = time.localtime()
        fmt = "%Y%m%d"
    
        return time.strftime(fmt, now) 


    def fmtdate(self, year=None, month=None, day=1):

        now = time.localtime()
        fmt = "%Y%m%d"

        if not year or not month:
            date = time.strftime(fmt, now)
            print(f"\nEmpty date! use today: {date}\n")

            return date

        else:
            date = str(year) + "{0:02d}".format(month) + "{0:02d}".format(day)
        
        try: # Use this method to check user input 
            check = time.strptime(date, fmt)
            if check > now:
                print("Can not predict future data!\n")

                return time.strftime(fmt, now)
            
            else:

                return date
            
        except Exception as e:
            print(e)

            return time.strftime(fmt, now)


    def pull(self, company, date): ## need to update avoid request rejection

        #url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY" #chinese from
        url = "https://www.twse.com.tw/en/exchangeReport/STOCK_DAY" #english form
        Company_params = {
            "response": "json",
            "date": date, 
            "stockNo": company
        }
        request_data = requests.get(url, params = Company_params)
        self.data = json.loads(request_data.content)
        self.data = self.clean(self.data)

        return self.data
        

    def clean(self, source):
        
        df = pd.DataFrame(source["data"], columns=source["fields"])
        df["Date"] = list(map(lambda x: x.replace('/', ''), df["Date"])) # remove"/" in date format ex.2023/01/02 -> 20230102

        return df


    def month_info(self, year=None, month=None):

        date = self.fmtdate(year, month)
        
        if self.date != date:
            self.select = self.pull(self.comp_id, date)
            
            return self.select
        
        else:

            return self.data


    def today_info(self):

        try:
            print(f"\nToday's infomation -> Stock No.: [{self.comp_id}]\n")
            result_today = self.data[self.data["Date"] == self.date]
        
            return result_today
        
        except Exception as e:
            print(e)
        
        
    def day_info(self, year=None, month=None, day=None):
        
        date = self.fmtdate(year, month, day)
        
        if self.date != date:
            self.select = self.pull(self.comp_id, date)
            result_today = self.select[self.select["Date"] == date]
            
            return result_today
        
        else:
            result_today = self.data[self.data["Date"] == self.date]
            
            return result_today


    def save(self):

        if not os.path.isdir("stocks"):
            os.mkdir("stocks")            

        data_path = os.path.join("stocks", f"{self.comp_id}.csv")

        if not os.path.isfile(data_path):
            opfile = open(data_path, mode = "w", newline = "")
            opfilewriter = csv.writer(opfile)
            opfilewriter.writerow(self.data.columns)
            
            for i in self.data.index:
                opfilewriter.writerow(self.data.iloc[i])
        else:
            pass





