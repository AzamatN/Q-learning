import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def get_data(col='Close'):
  """ Returns a 3 x n_step array """
  chk = pd.read_csv('data/0001.HK.csv', usecols=[col])
  hsbc = pd.read_csv('data/0005.HK.csv', usecols=[col])
  citic = pd.read_csv('data/0267.HK.csv', usecols=[col])
  # recent price are at top; reverse it
  return np.array([chk[col].values[::-1],
                   hsbc[col].values[::-1],
                   citic[col].values[::-1]])


def get_scaler(env):
  """ Takes a env and returns a scaler for its observation space """
  low = [0] * (env.n_stock * 2 + 1)

  high = []
  max_price = env.stock_price_history.max(axis=1)
  min_price = env.stock_price_history.min(axis=1)
  max_cash = env.init_invest * 3 # 3 is a magic number...
  max_stock_owned = max_cash // min_price
  for i in max_stock_owned:
    high.append(i)
  for i in max_price:
    high.append(i)
  high.append(max_cash)

  scaler = StandardScaler()
  scaler.fit([low, high])
  return scaler


def maybe_make_dir(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)