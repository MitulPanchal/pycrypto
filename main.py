from tkinter import *
from tkinter import messagebox, Menu
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
def reset():
    for frame in pycrypto.winfo_children():
        frame.destroy()

    app_nav()
    app_header()
    get_data()

def app_nav():

    def clear_all():
        cursorObj.execute("DELETE FROM COIN")
        con.commit()

        messagebox.showwarning("Portfolio Notification", "Portfolio Cleared - Add New Coins")
        reset()

    def exit_app():
        pycrypto.destroy()

    menu = Menu(pycrypto)

    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio', command=clear_all)
    file_item.add_command(label='Close App', command=exit_app)
    menu.add_cascade(label="File", menu=file_item)

    help_item = Menu(menu)
    help_item.add_command(label='Check Update', )
    help_item.add_command(label='About', )
    help_item.add_command(label='Contact Us', )
    menu.add_cascade(label="Help", menu=help_item)

    pycrypto.config(menu=menu)

# Function to call API and fetch details
def get_data():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=500&convert=USD&CMC_PRO_API_KEY=5a904e6d-6c76-40bd-8dbb-a0b3e4c02471")
    api = json.loads(api_request.content)

    cursorObj.execute("SELECT * FROM COIN")
    coins = cursorObj.fetchall()

    def font_color(amount):
        if amount >= 0:
            return "green"
        else:
            return "red"

    def insert_coin():
        cursorObj.execute("INSERT INTO COIN( SYMBOL, PRICE, AMOUNT) VALUES(?,?,?)",(symbol_txt.get(), price_txt.get(), amount_txt.get()))
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Coin Added Successfully in Portfolio.")
        reset()

    def update_coin():
        cursorObj.execute("UPDATE COIN SET SYMBOL=?, PRICE=?, AMOUNT=? WHERE ID=?",(symbol_update_txt.get(), price_update_txt.get(), amount_update_txt.get(), portfolio_update_id.get()))
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Coin Updated Successfully in Portfolio.")
        reset()

    def delete_coin():
        cursorObj.execute("DELETE FROM COIN WHERE ID = ?", (portfolio_id.get(),))
        con.commit()

        messagebox.showinfo("Portfolio Notification", "Coin Deleted Successfully from Portfolio.")
        reset()

    total_pl = 0
    coin_row = 1
    total_current_value = 0
    total_amount_paid = 0

    for i in range(0,500):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:

                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pl_margin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_coin = pl_margin * coin[2] 

                total_pl += total_pl_coin
                total_current_value += current_value
                total_amount_paid += total_paid

                # print(api["data"][i]["name"] + '-' + api["data"][i]["symbol"])
                # print("Price - ${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
                # print("Number of coin -", coin[2])
                # print("Total Amount Paid - ", "${0:.2f}".format(total_paid))
                # print("Current Value - ", "${0:.2f}".format(current_value))
                # print("P/L Margin - ", "${0:.2f}".format(pl_margin))
                # print("Total P/L Margin - ", "${0:.2f}".format(total_pl_coin))
                # print("-----------")    

                id_lb = Label(pycrypto, text=coin[0], bg="grey", fg="black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove") 
                id_lb.grid(row=coin_row, column=0, sticky=N+S+E+W)

                name = Label(pycrypto, text=api["data"][i]["symbol"], bg="grey", fg="black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove") 
                name.grid(row=coin_row, column=1, sticky=N+S+E+W)

                price = Label(pycrypto, text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="white" , fg="black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
                price.grid(row=coin_row, column=2, sticky=N+S+E+W)

                amount_owned = Label(pycrypto, text=coin[2], bg="grey" , fg="black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
                amount_owned.grid(row=coin_row, column=3, sticky=N+S+E+W)

                paid_amount = Label(pycrypto, text="${0:.2f}".format(total_paid), bg="white" , fg="black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
                paid_amount.grid(row=coin_row, column=4, sticky=N+S+E+W)

                current_price = Label(pycrypto, text="${0:.2f}".format(current_value), bg="grey" , fg= "black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
                current_price.grid(row=coin_row, column=5, sticky=N+S+E+W)

                pl_margin = Label(pycrypto, text="${0:.2f}".format(pl_margin), bg="white" , fg=font_color(float("{0:.2f}".format(pl_margin))), font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
                pl_margin.grid(row=coin_row, column=6, sticky=N+S+E+W)

                total_pl_margin = Label(pycrypto, text="${0:.2f}".format(total_pl_coin), bg="grey" , fg=font_color(float("{0:.2f}".format(total_pl_coin))), font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
                total_pl_margin.grid(row=coin_row, column=7, sticky=N+S+E+W)

                coin_row += coin_row 

    api = ""

    # Insert Data
    symbol_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_txt.grid(row=coin_row+1, column=1)
    
    price_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    price_txt.grid(row=coin_row+1, column=2)
    
    amount_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_txt.grid(row=coin_row+1, column=3)

    add_coin = Button(pycrypto, text="Add Coin", bg= "grey" , fg= "black", command=insert_coin , font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    add_coin.grid(row=coin_row+1, column=4, sticky=N+S+E+W)

    # Update Coin
    portfolio_update_id = Entry(pycrypto, borderwidth=2, relief="groove")
    portfolio_update_id.grid(row=coin_row+2, column=0)

    symbol_update_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_update_txt.grid(row=coin_row+2, column=1)
    
    price_update_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    price_update_txt.grid(row=coin_row+2, column=2)
    
    amount_update_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_update_txt.grid(row=coin_row+2, column=3)

    update_coin_txt = Button(pycrypto, text="Update Coin", bg= "grey" , fg= "black", command=update_coin , font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    update_coin_txt.grid(row=coin_row + 2, column=4, sticky=N+S+E+W)

    # Delete Coin
    portfolio_id = Entry(pycrypto, borderwidth=2, relief="groove")
    portfolio_id.grid(row=coin_row+3, column=0)

    delete_coin_txt = Button(pycrypto, text="Delete Coin", bg= "grey" , fg= "black", command=delete_coin , font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    delete_coin_txt.grid(row=coin_row + 3, column=4, sticky=N+S+E+W)

    # Total Value Display Section
    total_amount_paid_lb = Label(pycrypto, text="${0:.2f}".format(total_amount_paid), bg="grey" , fg="black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    total_amount_paid_lb.grid(row=coin_row, column=4, sticky=N+S+E+W)

    total_current_value = Label(pycrypto, text="${0:.2f}".format(total_current_value), bg="grey" , fg="black", font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    total_current_value.grid(row=coin_row, column=5, sticky=N+S+E+W)

    total_value = Label(pycrypto, text="${0:.2f}".format(total_pl), bg="grey" , fg=font_color(float("{0:.2f}".format(total_pl))), font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    total_value.grid(row=coin_row, column=7, sticky=N+S+E+W)
    
    refresh = Button(pycrypto, text="Refresh", bg= "grey" , fg= "black", command=reset , font= "Lato 12", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    refresh.grid(row=coin_row + 1, column=7, sticky=N+S+E+W)

    # print("Total P/L Margin for Protfolio - ", "${0:.2f}".format(total_pl))

def app_header():

    portfolio_id = Label(pycrypto, text="Portfolio ID", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    portfolio_id.grid(row=0, column=0, sticky=N+S+E+W)

    name = Label(pycrypto, text="Coin Name", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    name.grid(row=0, column=1, sticky=N+S+E+W)

    price = Label(pycrypto, text="Price", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    price.grid(row=0, column=2, sticky=N+S+E+W)

    amount_owned = Label(pycrypto, text="Quantity", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    amount_owned.grid(row=0, column=3, sticky=N+S+E+W)

    paid_amount = Label(pycrypto, text="Paid Amount", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    paid_amount.grid(row=0, column=4, sticky=N+S+E+W)

    current_price = Label(pycrypto, text="Current Value", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    current_price.grid(row=0, column=5, sticky=N+S+E+W)

    pl_margin = Label(pycrypto, text="P/L Margin", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    pl_margin.grid(row=0, column=6, sticky=N+S+E+W)

    total_pl_margin = Label(pycrypto, text="Total P/L Margin", bg="#142E54" , fg="white", font= "Lato 12 bold", padx= "5", pady= "5", borderwidth= 2, relief= "groove")
    total_pl_margin.grid(row=0, column=7, sticky=N+S+E+W)

app_nav()
app_header()
get_data()
pycrypto.mainloop()

cursorObj.close()
con.close()
print("Portfolio Closed")