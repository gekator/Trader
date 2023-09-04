import pandas as pd
import numpy as np

class Trader():
  def __init__(self, stock, money, comis, printBool):
    self.stock =  stock
    self.volume = 0
    self.printBool = printBool
    #self.Stock_Cash = []
    self.my_money = money
    self.table = pd.DataFrame({'Date':[0], 'Stock_Cash':[0], "My_money":[self.my_money], "Account_money":[self.my_money] })
    self.dater = []
    self.money_of_stock = 0
    self.start_money = 0
    self.state = ''
    self.comis = comis
    #print("printBool------------------------------------------------------------------", printBool)
        
  def buy(self, volume, price):
    if self.volume < 0:
      if self.printBool == True:
        print("\nBuy with price,", price, "Short_Close_Sum", volume * price, "\n")
      self.my_money = self.my_money + self.start_money + self.start_money - volume * price - self.comis
    self.volume = self.volume + volume
    #print("self.volume", self.volume)
    #print("buying+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #self.Stock_Cash.append(self.volume * price)
    if self.volume > 0:
      #print("self.volume > 0")
      #print("self.printBool == True", self.printBool == True)
      if self.printBool == True:
        print("\nBuy with price", price, "Open_Long_Sum", volume * price, "\n" )
      self.state = 'Long'
      self.my_money = self.my_money - volume * price  -  self.comis
    elif self.volume == 0:
      self.state = ''
      self.start_money = 0
      #print("stat0000000000000000000000000")
        
  def sell(self, volume, price):
    if self.volume > 0:
      if self.printBool == True:
        print("\nSell with price,", price, "Long_Close_Sum", volume * price, "\n")
      self.my_money = self.my_money + volume * price -  self.comis
      self.volume = self.volume - volume
    elif self.volume == 0:
      self.volume = self.volume - volume
      self.my_money = self.my_money - volume * price -  self.comis
        
    if self.volume < 0:
      if self.printBool == True:
        print("\nSell with price,", price, "Open_Short_sum", volume * price, "\n")
      self.state = 'Short'
      self.start_money = abs(volume * price)
      if self.printBool == True:
        print("SELL, self.start_money", self.start_money, "my_money", self.my_money, "\n")
    elif self.volume == 0:
      self.state = ''
      self.start_money = 0

  def quant_money(self, price, date_now):
    self.money_of_stock =abs(self.volume * price)
    #self.Stock_Cash.append(self.volume * price)
    if self.state == 'Short':#325 + 325 - 314 + 15000
      self.account_money =   self.start_money + self.start_money + self.volume * price + self.my_money
      if self.printBool == True:
        print("Quant money, self.account_money", self.account_money, "self.volume*price",  self.volume*price, "my_money, ", self.my_money, "cur_price, ", price, "\n")
    else:
      self.account_money = self.volume * price + self.my_money
      if self.printBool == True:
        print("Quant money, self.account_money", self.account_money, "self.volume*price",  self.volume*price, "my_money, ", self.my_money, "cur_price, ", price, "\n")
    df = pd.DataFrame({"Date":[date_now],
                      "Stock_Cash":[self.money_of_stock],
                      "My_money":[self.my_money],
                      "Account_money":[self.account_money]})
      #print(df)
      #Некоторая обработка таблицы
    if self.table.iloc[0, 0] == 0:
      self.table.iloc[0, 0] = date_now
    if self.table.iloc[0, 0] == df.iloc[0, 0]:
      pass
    else:
      self.table = pd.concat([self.table, df])
    self.tab = self.table.set_index('Date')