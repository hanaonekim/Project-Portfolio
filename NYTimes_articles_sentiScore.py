#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:11:26 2026

@author: hanakim
"""

import pandas as pd
import datetime
import calendar
from time import sleep

from pynytimes import NYTAPI

key="FofkxanM2bUwpDOIoy2sA0GGD2juF054hNSXmOA446xKR4mt"

year = 2025

first_days = []
last_days = []

for month in range(1,13):
    first_days.append(datetime.datetime(year, month, 1))
    
    last_day = calendar.monthrange(year, month)[1]
    last_days.append(datetime.datetime(year, month, last_day))

articles_list = []

companies = ["Apple", "Google", "Microsoft"]

# Loop through the companies.
for company in companies:
    
    # Loop through the months.
    for i in range(12):
        nyt = NYTAPI(key, parse_dates = True)
        articles = nyt.article_search(query = company,
                                      dates = {
                                          "begin": first_days[i],
                                          "end": last_days[i],
                                          },
                                      options = {"sort": "newest"} )
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()
        
        # Loop through the articles.
        for article in articles:
            
            # Get sentiment score.
            score = analyzer.polarity_scores(article["abstract"])
            
            # Save info needed.
            articleD = {
                "company": company,                         # Company name
                "title": article["headline"]["main"],       # Article title
                "date": article["pub_date"].date(),         # Publication date
                "score": score["compound"],                 # Score
                }
            articles_list.append(articleD)      # Add article dictionary to list.
            
        sleep(12)
        
# %%
        
article_df = pd.DataFrame(articles_list)
article_df.to_csv("NYTimes_article_data.csv", index = False)
        