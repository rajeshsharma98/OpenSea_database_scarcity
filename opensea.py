# 1. Fetch collection -> items -> owner name
# 2. Filter owner name joined platform before Jan 26
# 3. Folter all items that have activity before Feb 26 

#-------------------------------------------------------- IMPORT
from dataclasses import dataclass
from multiprocessing import parent_process
from tqdm import trange
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import requests
import json
import time
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

#-------------------------------------------------------- Dummy DATASET

def kaggle_dataset():
  # Create a new DataFrame to store values
  df = pd.read_csv('opensea_collections.csv')
  slug = df.slug.tolist()
  nt = []

  # Empty data rame with common columns
  df1 = pd.DataFrame(columns=['editors', 'payment_tokens', 'primary_asset_contracts',
        'banner_image_url', 'chat_url', 'created_date', 'default_to_fiat',
        'description', 'dev_buyer_fee_basis_points',
        'dev_seller_fee_basis_points', 'discord_url', 'external_url',
        'featured', 'featured_image_url', 'hidden', 'safelist_request_status',
        'image_url', 'is_subject_to_whitelist', 'large_image_url',
        'medium_username', 'name', 'only_proxied_transfers',
        'opensea_buyer_fee_basis_points', 'opensea_seller_fee_basis_points',
        'payout_address', 'require_email', 'short_description', 'slug',
        'telegram_url', 'twitter_username', 'instagram_username', 'wiki_url',
        'is_nsfw', 'stats.one_day_volume', 'stats.one_day_change',
        'stats.one_day_sales', 'stats.one_day_average_price',
        'stats.seven_day_volume', 'stats.seven_day_change',
        'stats.seven_day_sales', 'stats.seven_day_average_price',
        'stats.thirty_day_volume', 'stats.thirty_day_change',
        'stats.thirty_day_sales', 'stats.thirty_day_average_price',
        'stats.total_volume', 'stats.total_sales', 'stats.total_supply',
        'stats.count', 'stats.num_owners', 'stats.average_price',
        'stats.num_reports', 'stats.market_cap', 'stats.floor_price',
        'display_data.card_display_style','display_data.images']) 

  z = 0
  for i in trange(len(slug)):
    url = "https://api.opensea.io/api/v1/collection/"+slug[i]
    # print(slug[i])
    response = requests.get(url)

    # =========================
    ''' I think Error 429 is after fetching 40 requests at a one stretch'''
    if i%4 == 0:
      time.sleep(2)
    
    # =========================

    # Check if response status not 200 store the slug value else procees
    if response.status_code != 200:
      z += 1
      print('Error status_code: ',response.status_code,' Count: ',z)
      nt.append(slug[i])

    else:
      json_data = json.loads(response.text)
      df2 = pd.json_normalize(json_data['collection'])
    
      extra_clmns = (list(set(list(df2.columns)) - set(list(df1.columns))))
      # Extra clmns especially traits key of json_file is removed

      df2.drop(extra_clmns, axis=1, inplace=True)
    
      df1 = df1.append(df2)
    # =========================

  # Store values to a new dataframe
  df1.to_csv('kaggle_fetched.csv')

  # Store all the slug names that got 404 error
  with open('not_found.txt', 'w') as fp:
        fp.write('\n'.join(nt))

  ''' Extra columns example'''
  eurl = "https://api.opensea.io/api/v1/collection/doodles-official"
  response = requests.get(eurl)
  print(response.text)


