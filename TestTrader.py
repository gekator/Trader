import unittest
from Trader import Trader
import pandas as pd

class TestTrader(unittest.TestCase):
  #setUp method is overridden from the parent class TestCase
  def setUp(self):
    df1 = pd.read_csv("CNY000000TOD_22-6-2022_18-7-2023_Test.csv", parse_dates=True)
    df1["Date"] = df1["Date"].apply(pd.to_datetime)
    df1.set_index("Date", inplace=True)
    self.backtester = Trader(df1, 100000, [0.1, 0], True) #0,05%
  #Each test method starts with the keyword test_
  def test_calcComis(self):
    self.assertEqual(self.backtester.calcComis(10.000, 5000), 50)#return prices*volumes/100*self.comis + self.moexComis
    #10.000*5000/100*0.1 + 0 = 50

  def test_calcAccountMoney(self):
    self.assertEqual(self.backtester.calcAccountMoney(10.000), 100000)#return self.posVolume * price + self.my_money
    #0 * 10.000 + 100000 = 100000

  def test_buy(self):

    #my_money = 100000
    self.backtester.buy(5000, 10.000)#self.my_money = self.my_money - orderVolume * price  -  self.calcComis(price,orderVolume)
    self.assertAlmostEqual(self.backtester.my_money, 49950.0)
    #orderVolume * price =  5000 * 10.000 = 50000 
    #self.calcComis(price,orderVolume) = prices*volumes/100*self.comis + self.moexComis = 10.000*50000/100*0.1 + 0 = 50
    #my_money = 100000 - 50000 - 50 = 49950 Ok!
    self.assertEqual(self.backtester.posVolume, 5000)
    self.assertEqual(self.backtester.state, 'Long')
    self.assertEqual(self.backtester.calcAccountMoney(10.000), 99950.0) #self.posVolume * price + self.my_money
    #my_money = 49950
    #self.posVolume * price = 5000 * 10.000 = 50000
    #self.posVolume * price + self.my_money = 50000 + 49950 = 99950 Ok!
    self.assertAlmostEqual(self.backtester.getCurrentProfit(20.000), 49850.0, places=4)#self.calcAccountMoney(price) - self.moneyOnStartDeal - self.calcComis(price, self.posVolume)
    #self.moneyOnStartDeal = self.calcAccountMoney(10.000) = self.posVolume * price + self.my_money = 0 * 10.000 + 100000 = 0 + 100000 = 100000
    #self.calcAccountMoney(20.000) = self.posVolume * price + self.my_money = 5000 * 20.000 + 49950 = 100000 + 49950 = 149950
    #self.calcComis(price,orderVolume) = prices*volumes/100*self.comis + self.moexComis =  20.000*5000/100*0.1 + 0 = 100
    #self.calcAccountMoney(price) - self.moneyOnStartDeal - self.calcComis(price, self.posVolume) = 149950 - 100000 - 100 = 49850
  def test_sell(self):
    #my_money = 100000
    self.backtester.sell(5000, 10.000)#self.my_money=self.my_money-orderVolume*price-self.calcComis(price,orderVolume)
    self.assertAlmostEqual(self.backtester.my_money, 49950.0)
    #self.my_money=100000
    #orderVolume * price =  5000 * 10.000 = 50000 
    #self.calcComis(price,orderVolume) = prices*volumes/100*self.comis + self.moexComis = 10.000*50000/100*0.1 + 0 = 50
    #my_money = 100000 - 50000 - 50 = 49950 Ok!
    self.assertEqual(self.backtester.posVolume, -5000)
    self.assertEqual(self.backtester.state, 'Short')
    self.assertEqual(self.backtester.calcAccountMoney(10.000), 99950.0) #self.posVolume * price + self.my_money
    #my_money = 49950
    #self.posVolume * price = 5000 * 10.000 = 50000
    #self.posVolume * price + self.my_money = 50000 + 49950 = 99950 Ok!
    self.assertAlmostEqual(self.backtester.getCurrentProfit(5.000), 24925.0, places=4)#self.calcAccountMoney(price) - self.moneyOnStartDeal - self.calcComis(price, self.posVolume)
    #self.moneyOnStartDeal = self.calcAccountMoney(10.000) = self.start_money + self.start_money + self.posVolume * price + self.my_money = 100000
    #self.calcAccountMoney(5.000) = self.posVolume * price + self.my_money = 5000 * 5.000 + 49950 = 25000 + 49950 = 74950
    #self.calcComis(price,orderVolume) = prices*volumes/100*self.comis + self.moexComis =  5.000*5000/100*0.1 + 0 = 25
    #self.calcAccountMoney(price) - self.moneyOnStartDeal - self.calcComis(price, self.posVolume) = 100000 - 74950 - 25 = 25025

  def test_getCashResult(self):
    # Сначала нужно обновить таблицу данными
    # Открываем позицию
    self.backtester.buy(5000, 10.000)
    # Обновляем таблицу
    self.backtester.quant_money(10.000, "2023-01-01")
    
    # Закрываем позицию
    self.backtester.sell(5000, 20.000)
    # Обновляем таблицу
    self.backtester.quant_money(20.000, "2023-01-02")
    
    # Теперь проверяем результат
    # Разница между последним и первым значением Account_money
    expected_result = 49900 # Приблизительное значение прибыли
    self.assertAlmostEqual(self.backtester.getCashResult(), expected_result, delta=100)
# Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()