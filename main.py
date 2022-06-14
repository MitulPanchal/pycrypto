from tkinter import *
import requests
import json
import sqlite3

pycrypto = Tk()
pycrypto.title("Crypto Portfolio")

con = sqlite3.connect('cryptocoin.db')
cursorObj = con.cursor()

cursorObj.execute("CREATE TABLE IF NOT EXISTS COIN(ID INTEGER PRIMARY KEY, SYMBOL TEXT, AMOUNT INTEGER, PRICE REAL)")
con.commit()

# Insert data to database
# coins = [
#         {
#             "symbol": "BTC",
#             "amount_owned": 2,
#             "price_per_coin": 28000
#         }, 
#         {
#             "symbol": "ETH",
#             "amount_owned": 3,
#             "price_per_coin": 2000
#         }, 
#         {
#             "symbol": "XRP",
#             "amount_owned": 5,
#             "price_per_coin": 1
#         }, 
#         {
#             "symbol": "DOGE",
#             "amount_owned": 10,
#             "price_per_coin": 1
#         }
#     ]

# id = 0
# for coin in coins:
#     cursorObj.execute("INSERT INTO COIN VALUES(?,?,?,?)",(id, coin["symbol"], coin["amount_owned"], coin["price_per_coin"]))
#     con.commit()
#     id = id + 1


def font_color(amount):
    if amount >= 0:
        return "green"
    else:
        return "red"

# Function to call API and fetch details
def get_data():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=500&convert=USD&CMC_PRO_API_KEY=5a904e6d-6c76-40bd-8dbb-a0b3e4c02471")
    api = json.loads(api_request.content)

    cursorObj.execute("SELECT * FROM COIN")
    coins = cursorObj.fetchall()

    total_pl = 0
    coin_row = 1
    total_current_value = 0

    for i in range(0,500):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:

                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pl_margin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_coin = pl_margin * coin[2] 

                total_pl = total_pl + total_pl_coin
                total_current_value = total_current_value + current_value

                # print(api["data"][i]["name"] + '-' + api["data"][i]["symbol"])
                # print("Price - ${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
                # print("Number of coin -", coin[2])
                # print("Total Amount Paid - ", "${0:.2f}".format(total_paid))
                # print("Current Value - ", "${0:.2f}".format(current_value))
                # print("P/L Margin - ", "${0:.2f}".format(pl_margin))
                # print("Total P/L Margin - ", "${0:.2f}".format(total_pl_coin))
                # print("-----------")    

                name = Label(pycrypto, text=api["data"][i]["symbol"], bg="grey", fg="black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove") 
                name.grid(row=coin_row, column=0, sticky=N+S+E+W)

                price = Label(pycrypto, text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="white" , fg="black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
                price.grid(row=coin_row, column=1, sticky=N+S+E+W)

                amount_owned = Label(pycrypto, text=coin[2], bg="grey" , fg="black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
                amount_owned.grid(row=coin_row, column=2, sticky=N+S+E+W)

                paid_amount = Label(pycrypto, text="${0:.2f}".format(total_paid), bg="white" , fg="black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
                paid_amount.grid(row=coin_row, column=3, sticky=N+S+E+W)

                current_price = Label(pycrypto, text="${0:.2f}".format(current_value), bg="grey" , fg= "black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
                current_price.grid(row=coin_row, column=4, sticky=N+S+E+W)

                pl_margin = Label(pycrypto, text="${0:.2f}".format(pl_margin), bg="white" , fg=font_color(float("{0:.2f}".format(pl_margin))), font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
                pl_margin.grid(row=coin_row, column=5, sticky=N+S+E+W)

                total_pl_margin = Label(pycrypto, text="${0:.2f}".format(total_pl_coin), bg="grey" , fg=font_color(float("{0:.2f}".format(total_pl_coin))), font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
                total_pl_margin.grid(row=coin_row, column=6, sticky=N+S+E+W)

                coin_row = coin_row + 1

    
    total_current_value = Label(pycrypto, text="${0:.2f}".format(total_current_value), bg="grey" , fg="black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    total_current_value.grid(row=coin_row, column=4, sticky=N+S+E+W)

    total_value = Label(pycrypto, text="${0:.2f}".format(total_pl), bg="grey" , fg=font_color(float("{0:.2f}".format(total_pl))), font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    total_value.grid(row=coin_row, column=6, sticky=N+S+E+W)

    api = ""
    
    submit = Button(pycrypto, text="Update", bg= "grey" , fg= "black", command=get_data , font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    submit.grid(row=coin_row + 1, column=6, sticky=N+S+E+W)

    # print("Total P/L Margin for Protfolio - ", "${0:.2f}".format(total_pl))

name = Label(pycrypto, text="Coin Name", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
name.grid(row=0, column=0, sticky=N+S+E+W)

price = Label(pycrypto, text="Price", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
price.grid(row=0, column=1, sticky=N+S+E+W)

amount_owned = Label(pycrypto, text="Quantity", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
amount_owned.grid(row=0, column=2, sticky=N+S+E+W)

paid_amount = Label(pycrypto, text="Paid Amount", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
paid_amount.grid(row=0, column=3, sticky=N+S+E+W)

current_price = Label(pycrypto, text="Current Value", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
current_price.grid(row=0, column=4, sticky=N+S+E+W)

pl_margin = Label(pycrypto, text="P/L Margin", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
pl_margin.grid(row=0, column=5, sticky=N+S+E+W)

total_pl_margin = Label(pycrypto, text="Total P/L Margin", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
total_pl_margin.grid(row=0, column=6, sticky=N+S+E+W)

get_data()
pycrypto.mainloop()

cursorObj.close()
con.close()
print("Portfolio Closed")