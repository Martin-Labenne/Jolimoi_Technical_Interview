"""
This file is useful for the report. 
It have no other goal than facilitate readibility of the report.
"""

# data storage and algebra
import pandas as pd
import numpy as np

# data query
import sqlite3 as sql

# plot data
import seaborn as sns
import matplotlib.pyplot as plt

import os
cwd = os.getcwd()

path = "../data/"
db = path + "artists.db"
connector = sql.connect("../data/artists.db")

######## Question 2 ######## 
def topTenArtists() : 
    topTen = pd.read_sql("""SELECT Name, COUNT(*) AS nbOfArtworks
               FROM artworks
               WHERE Name NOT NULL
               AND Name NOT LIKE 'Unknown photographer'
               GROUP BY Name
               ORDER BY nbOfArtworks DESC 
               LIMIT 10;
            """
            , connector)

    sns.set(style="white", context="talk") # general theme

    f, ax = plt.subplots(1, 1, figsize=(12, 6), sharex=True)
    x = [ label.replace(' ', '\n') for label in topTen['Name'] ] # label wrapping
    y = topTen['nbOfArtworks']
    sns.barplot(x=x, y=y, palette="rocket") # data attribution and colors

    ax.axhline(0, color="k", clip_on=False) 
    sns.despine(bottom=True)
    
    ax.set_ylabel("Number of Artworks")
    ax.set_xlabel("Artists")

    plt.title("Top 10 artists by the number of artworks")
    plt.tight_layout()
    
######## Question 3 ######## 
def topTenArtistsByArea() : 
    artistAndArea_df = pd.read_csv(cwd+"\\files\\artists_and_area.csv")
    sortedArea = artistAndArea_df.groupby('Artist').agg(['sum'])['Area'].sort_values(by=['sum'], ascending=False)
    sortedRoundedInGoodDimensionArea = (sortedArea/10000).apply(lambda x : round(x,2)) # cm² to m² conversion

    sns.set(style="white", context="talk") # general theme

    f, ax = plt.subplots(1, 1, figsize=(13, 6), sharex=True)
    x = [ label.replace(' ', '\n') for label in sortedRoundedInGoodDimensionArea.head(10).index ] # label wrapping
    y = sortedRoundedInGoodDimensionArea.head(10)['sum']
    sns.barplot(x=x, y=y, palette="rocket") # data attribution and colors

    ax.axhline(0, color="k", clip_on=False) 
    sns.despine(bottom=True)

    ax.set_ylabel("Total Area (m²)")
    ax.set_xlabel("Artists")

    plt.title("Top 10 artists who has created the most 2D artwork by total surface area")
    plt.tight_layout()
       
######## Question 4 ######## 
def lifeTimeAquirement() : 
    alive = pd.read_csv(cwd+"\\files\\aquisition_during_life_alive.csv")
    dead = pd.read_csv(cwd+"\\files\\aquisition_during_life_dead.csv")
     
    sns.set(style="white", context="talk") # general theme

    f, ax = plt.subplots(1, 1, figsize=(10, 6), sharex=True)
    sns.distplot( alive['Acquisition'], color="blue", label="Still Alive" )
    sns.distplot( dead['Acquisition'], color="red", label="Alredy Dead" )

    ax.set_xlabel("Acquistion Year")
    ax.set_ylabel("Proportion")
    ax.axhline(0, color="k", clip_on=False) 
    sns.despine(bottom=True)

    plt.title("Aquisition years of artworks during the life time of their artist")
    plt.legend()
    plt.tight_layout()    
    
######## Question 5 ######## 
def header() : 
    return pd.DataFrame({'Artist ID' : [], 'Nationality' : [], 'Gender' : [],
                         'Birth Year' : [], 'Death Year' : [], 'Area' : [],
                         'Artwork ID' : [], 'Title' : [], 'Name' : [], 'Date' : [],
                         'Acquisition Date' : [], 'Credit' : [], 'Catalogue' : [], 
                         'Classification' : []})
    
 
######## Question 6 ######## 
def clusters() : 
    return pd.DataFrame({'Birth Year' : [1865, 1908, 1942],
                         'Production Date' : [1912, 1953, 1986], 
                         'Acquisition Date' : [1966, 1970, 2001], 
                         'Nationality' : ['French', 'American', 'America'], 
                         'Gender' : ['Male', 'Male', 'Male'],
                         'Credit' : ['The Louis E. Stern Collection','The Louis E. Stern Collection','Gift of the artist'], 
                         'Classification' : ['Photograph','Illustrated Book','Print']})