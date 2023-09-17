import unittest
from Trader import Trader
import pandas as pd

class TestTrader(unittest.TestCase):
  #setUp method is overridden from the parent class TestCase
  def setUp(self):
    df1 = pd.read_csv("CNY000000TOD_22-6-2022_18-7-2023_Test.csv", parse_dates=True)
    df1["Date"] = df1["Date"].apply(pd.to_datetime)
    df1.set_index("Date", inplace=True)
    self.backtester = Trader(df1, 700000, 0.043, False)
  #Each test method starts with the keyword test_
  def test_buy(self):
    #self.assertAlmostEqual(self.backtester.buy(50000, 13.486), 25360.050999999978)
    self.assertEqual(self.backtester.calcAccountMoney(13.486), 699660.051)
    self.assertAlmostEqual(self.backtester.getCurrentProfit(14.000), 25348.99999000004, places=4)
# Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()