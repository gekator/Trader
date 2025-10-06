import pandas as pd
import numpy as np
import json
import os

STATE_FILE = "trader_state.json"  # Файл для сохранения состояния

class Trader():
  def __init__(self,  money, comis, printBool, stock=None):
    self.stock =  stock
    self.posVolume = 0
    self.printBool = printBool
    #self.Stock_Cash = []
    self.my_money = money #мои деньги которые никуда не вложены
    self.table = pd.DataFrame({'Date':[0], 'Stock_Cash':[0], "My_money":[self.my_money], "Account_money":[self.my_money] })
    self.table = self.table.set_index('Date')
    self.dater = []
    self.money_of_stock = 0 #стоимость вложений, используется только для записи в таблицу параметров счета
    self.start_money = 0 #нужен для вычисления шорта
    self.moneyOnStartDeal = 0
    self.state = "zero"
    self.comis = comis[0]
    self.moexComis = comis[1]
    self.price_of_pos = 0
    #print("printBool------------------------------------------------------------------", printBool)

  def save_state(self):
    """Сохраняет текущее состояние в файл"""
    # Подготавливаем таблицу: индекс -> колонка 'Date'
    print("save_state table_df\n ", self.table)
    table_df = self.table.reset_index()
    print("table_df = self.table.reset_index()\n", table_df)
    print("self.table\n ", self.table)
    # Проверяем, что тип индекса был datetime, иначе не трогаем
    if isinstance(self.table.index, pd.DatetimeIndex):
        print("if table_df = self.table.reset_inde # Проверяем, что тип индекса был datetime, иначе не трогаем")
        table_df['Date'] = table_df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        print("if table_df = self.table.reset_inde  иначе не трогаем")
        # Если индекс был не дата — просто преобразуем в строку (на всякий случай)
        table_df['Date'] = table_df['Date'].astype(str)
    print("table_df\n", table_df)
    # Конвертируем в словарь
    table_records = table_df.to_dict('records')
    print("table_records\n", table_records)
    
    state_data = {
        "state": self.state,
        "posVolume": int(self.posVolume),
        "my_money": float(self.my_money),
        "start_money": float(self.start_money),
        "moneyOnStartDeal": float(self.moneyOnStartDeal),
        "price_of_pos":float(self.price_of_pos),
        "table": table_records   # Сохраняем таблицу
    }
    print("state_data json", state_data)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state_data, f, indent=4, ensure_ascii=False)
    if self.printBool:
        print(f"✅ Состояние сохранено в {STATE_FILE}")

  @staticmethod
  def load_state(money, comis, printBool):
      """
      Загружает состояние из файла.
      Если файла нет — создаёт новый Trader.
      """
      
      if not os.path.exists(STATE_FILE):
          if printBool:
              print(f"📁 Файл {STATE_FILE} не найден. Создаём новый аккаунт.")
          backtest =  Trader(money, comis, printBool)
          backtest.save_state()
          return backtest

      try:
          with open(STATE_FILE, 'r', encoding='utf-8') as f:
              state_data = json.load(f)

          # Создаём новый объект
          trader = Trader(money, comis, printBool)
          print("load_state\n ", trader.table)
          # Восстанавливаем поля
          trader.state = state_data["state"]
          trader.posVolume = state_data["posVolume"]
          trader.my_money = state_data["my_money"]
          trader.start_money = state_data["start_money"]
          trader.moneyOnStartDeal = state_data["moneyOnStartDeal"]
          trader.price_of_pos = state_data["price_of_pos"]
          
          # Восстанавливаем таблицу
          # Восстанавливаем таблицу
          if state_data["table"]:
              df = pd.DataFrame(state_data["table"])
              # Попробуем преобразовать 'Date' в datetime
              try:
                  df['Date'] = pd.to_datetime(df['Date'])
                  df = df.set_index('Date')
              except Exception:
                  # Если не получилось — создаём дефолтный индекс
                  df = df.set_index('Date')  # Предполагаем, что 'Date' — это индекс
                  df.index.name = 'Date'
              print("load_state # Восстанавливаем таблицу\n ", trader.table)
              # Приводим к int
              for col in ['Stock_Cash', 'My_money', 'Account_money']:
                  if col in df.columns:
                      df[col] = df[col].astype(float)
              trader.table = df
          else:
              # Пустая таблица
              empty_df = pd.DataFrame({
                  'Stock_Cash': [0],
                  'My_money': [money],
                  'Account_money': [money]
              })
              trader.table = empty_df
              trader.table.index.name = 'Date'
              print("load_state # # Пустая таблица\n ", trader.table)
          if printBool:
              print(f"✅ Состояние загружено: state={trader.state}, posVolume={trader.posVolume}")
          print("load_state # return trader\n ", trader.table)
          return trader

      except Exception as e:
          print(f"❌ Ошибка при загрузке состояния: {e}")
          import traceback
          traceback.print_exc()
          print("Создаём новый аккаунт...")
          return Trader(money, comis, printBool)

  def calcComis(self, prices, volumes):
    return prices*volumes/100*self.comis + self.moexComis
        
  def buy(self, orderVolume, price):
    if self.posVolume < 0:
      if self.printBool == True:
        print("\nBuy with price,", price, "Short_Close_Sum", orderVolume * price, "\n")# Здесь может и не закрыться шорт
      self.my_money = self.my_money + self.start_money + self.start_money - orderVolume * price - self.calcComis(price,abs(orderVolume))
      self.posVolume = self.posVolume + orderVolume
    elif self.posVolume == 0:
      if self.moneyOnStartDeal == 0:# то есть вычисляем только на первой покупке, при входе в позицию, если докупаем, то не считаем, так как нужно будет както усреднять
        self.moneyOnStartDeal = self.calcAccountMoney(price)
        #print("self.moneyOnStartDeal = self.calcAccountMoney(price)", self.moneyOnStartDeal)
      self.posVolume = self.posVolume + orderVolume
    #print("self.posVolume", self.posVolume)
    #print("buying+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #self.Stock_Cash.append(self.posVolume * price)
    if self.posVolume > 0:
      if self.printBool == True:
        print("\nBuy with price", price, "Open_Long_Sum", orderVolume * price, "\n" )
      #print("self.posVolume > 0")
      #print("self.printBool == True", self.printBool == True)
      self.state = "Long"
      self.my_money = self.my_money - orderVolume * price  -  self.calcComis(price,abs(orderVolume))
    elif self.posVolume == 0:
      self.state = "zero"
      self.start_money = 0
      self.moneyOnStartDeal = 0
      #print("stat0000000000000000000000000")
    #return self.my_money
    # 🔥 Сохраняем состояние после сделки
    self.save_state()

  def sell(self, orderVolume, price):
    if self.posVolume > 0:
      if self.printBool == True:
        print("\nSell with price,", price, "Long_Close_Sum", orderVolume * price, "\n")
      self.my_money = self.my_money + orderVolume * price -  self.calcComis(price,abs(orderVolume))
      self.posVolume = self.posVolume - orderVolume
    elif self.posVolume == 0:
      if self.moneyOnStartDeal == 0:# то есть вычисляем только на первой продаже, при входе в позицию, если докупаем, то не считаем, так как нужно будет както усреднять
        self.moneyOnStartDeal = self.calcAccountMoney(price)
      self.posVolume = self.posVolume - orderVolume
      self.my_money = self.my_money - orderVolume * price -  self.calcComis(price,abs(orderVolume))
      
    if self.posVolume < 0:
      if self.printBool == True:
        print("\nSell with price,", price, "Open_Short_sum", orderVolume * price, "\n")
      self.state = "Short"
      self.start_money = abs(orderVolume * price)
      if self.printBool == True:
        print("SELL, self.start_money", self.start_money, "my_money", self.my_money, "\n")
    elif self.posVolume == 0:
      self.state = "zero"
      self.start_money = 0
      self.moneyOnStartDeal = 0
    self.save_state()
  
  def calcAccountMoney(self, price):
    #подсчитывает цену активов
    if self.state == 'Short':
      return self.start_money + self.start_money + self.posVolume * price + self.my_money
    else:
      #print(self.posVolume * price + self.my_money)
      return self.posVolume * price + self.my_money
  
  def quant_money(self, price, date_now):
    #обновляет таблицу по счетам
    self.money_of_stock =abs(self.posVolume * price)
    #self.Stock_Cash.append(self.posVolume * price)
    self.account_money =  self.calcAccountMoney(price) #мои деньги и вложения
    if self.printBool == True:
      print("Quant money: Account_money", self.account_money, "posVolume*price",  self.posVolume*price, "my_money, ", self.my_money, "cur_price, ", price, "\n")
    df = pd.DataFrame({"Date":[date_now],
                      "Stock_Cash":[int(self.money_of_stock)],
                      "My_money":[int(self.my_money)],
                      "Account_money":[int(self.account_money)]})
    df = df.set_index('Date')
    print("quant money df\n", df)
    print("quant money self.table\n", self.table )
    #Некоторая обработка таблицы
    print("self.table.iloc[0, 0]", self.table.iloc[0, 0])
    print("self.table.index", self.table.index)
    print("self.table.index[0]", self.table.index[0])
    print("type self.table.index[0]", type(self.table.index[0]))
    print("date_now", date_now)
    """if self.table.iloc[0, 0] == 0:
      self.table.iloc[0, 0] = date_now"""
    """if self.table.index[0] == 0:
      self.table.index[0] = date_now
      print("if self.table.index[0] == 0:", self.table.index[0])"""
    print("#Некоторая обработка таблицы quant money self.table\n", self.table )
    if self.table.index[0] == df.index[0]:
      print("self.table.index[0] == df.index[0]", self.table.index[0], df.index[0])
      pass
    else:
      print("else quant money self.table\n", self.table )
      print("else quant money df\n", df)
      self.table = pd.concat([self.table, df])
      print("else quant money self.table after self.table = pd.concat([self.table, df])\n", self.table )
      self.table.to_csv('out.csv')
      self.save_state()
    return self.getCurrentProfit(price)

  def getCashResult(self):
    cashFinal = self.table["Account_money"].values[-1] - self.table["Account_money"].values[0]
    print("cashFinal", cashFinal)
    return cashFinal
  
  def getAccountMoneyForCurrentData(self, data):
    #выдает сумму денег и активов на счете
    acm = self.table["Account_money"].values[data]
    return acm
  
  def getCurrentProfit(self, price):
    print("moneyOnStartDeal", self.moneyOnStartDeal)
    print("calcAccountMoney(price)", self.calcAccountMoney(price),"posVolume * price=", self.posVolume * price, "my_money=", + self.my_money)
    print('self.calcComis(price, self.posVolume)', self.calcComis(price, abs(self.posVolume)))
    print("self.calcAccountMoney(price) - self.moneyOnStartDeal)", self.calcAccountMoney(price) - self.moneyOnStartDeal)
    if self.state != "zero":
      return self.calcAccountMoney(price) - self.moneyOnStartDeal - self.calcComis(price, abs(self.posVolume))
    else:
      return 0  