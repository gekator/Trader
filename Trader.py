import pandas as pd
import numpy as np

class Trader():
  def __init__(self, stock, money, comis, printBool):
    self.stock =  stock
    self.posVolume = 0
    self.printBool = printBool
    #self.Stock_Cash = []
    self.my_money = money #мои деньги которые никуда не вложены
    self.table = pd.DataFrame({'Date':[0], 'Stock_Cash':[0], "My_money":[self.my_money], "Account_money":[self.my_money] })
    self.dater = []
    self.money_of_stock = 0 #стоимость вложений, используется только для записи в таблицу параметров счета
    self.start_money = 0 #нужен для вычисления шорта
    self.money
    self.state = ''
    self.comis = comis
    self.moexComis = 50
    #print("printBool------------------------------------------------------------------", printBool)

  def calcComis(self, prices, volumes):
    return prices*volumes/100*self.comis + self.moexComis
        
  def buy(self, orderVolume, price):
    if self.posVolume < 0:
      if self.printBool == True:
        print("\nBuy with price,", price, "Short_Close_Sum", orderVolume * price, "\n")# Здесь может и не закрыться шорт
      self.my_money = self.my_money + self.start_money + self.start_money - orderVolume * price - self.calcComis(price,orderVolume)
    self.posVolume = self.posVolume + orderVolume
    #print("self.posVolume", self.posVolume)
    #print("buying+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #self.Stock_Cash.append(self.posVolume * price)
    if self.posVolume > 0:
      #print("self.posVolume > 0")
      #print("self.printBool == True", self.printBool == True)
      if self.printBool == True:
        print("\nBuy with price", price, "Open_Long_Sum", orderVolume * price, "\n" )
      self.state = 'Long'
      self.my_money = self.my_money - orderVolume * price  -  self.calcComis(price,orderVolume)
    elif self.posVolume == 0:
      self.state = ''
      self.start_money = 0
      #print("stat0000000000000000000000000")
        
  def sell(self, orderVolume, price):
    if self.posVolume > 0:
      if self.printBool == True:
        print("\nSell with price,", price, "Long_Close_Sum", orderVolume * price, "\n")
      self.my_money = self.my_money + orderVolume * price -  self.calcComis(price,orderVolume)
      self.posVolume = self.posVolume - orderVolume
    elif self.posVolume == 0:
      self.posVolume = self.posVolume - orderVolume
      self.my_money = self.my_money - orderVolume * price -  self.calcComis(price,orderVolume)
        
    if self.posVolume < 0:
      if self.printBool == True:
        print("\nSell with price,", price, "Open_Short_sum", orderVolume * price, "\n")
      self.state = 'Short'
      self.start_money = abs(orderVolume * price)
      if self.printBool == True:
        print("SELL, self.start_money", self.start_money, "my_money", self.my_money, "\n")
    elif self.posVolume == 0:
      self.state = ''
      self.start_money = 0
  
  def calcAccountMoney(self, price):
    if self.state == 'Short':
      return self.start_money + self.start_money + self.posVolume * price + self.my_money
    else:
      return self.posVolume * price + self.my_money

  def quant_money(self, price, date_now):
    self.money_of_stock =abs(self.posVolume * price)
    #self.Stock_Cash.append(self.posVolume * price)
    self.account_money =  self.calcAccountMoney(price) #мои деньги и вложения
    if self.printBool == True:
      print("Quant money: Account_money", self.account_money, "posVolume*price",  self.posVolume*price, "my_money, ", self.my_money, "cur_price, ", price, "\n")
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

  def getCashResult(self):
    cashFinal = self.tab["Account_money"].values[-1] - self.tab["Account_money"].values[0]
    return cashFinal
  
  def getAccountMoneyFroCurrentData(self, data):
    acm = self.tab["Account_money"].values[data]
    return acm