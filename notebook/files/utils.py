"""
This file is usful for the report 
and have no other goal than facilitate readibility in the report
"""

# data storage and algebra
import pandas as pd
import numpy as np

# data query
import sqlite3 as sql

# plot data
import seaborn as sns
import matplotlib.pyplot as plt

# others
from datetime import datetime

path = "../data/"
db = path + "artists.db"
connector = sql.connect("../data/artists.db")
######## Question 1 ######## 
topTen = pd.read_sql("""SELECT Name, COUNT(*) AS nbOfArtworks
               FROM artworks
               WHERE Name NOT NULL
               AND Name NOT LIKE 'Unknown photographer'
               GROUP BY Name
               ORDER BY nbOfArtworks DESC 
               LIMIT 10;
            """
            , connector)

def topTenArtists() : 
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
    
######## Question 2 ######## 
dimensions = pd.read_sql(""" SELECT IFNULL(`Diameter (cm)`, 0) AS Diameter,
                                    IFNULL(`Circumference (cm)`, 0) AS Circumference, 
                                    IFNULL(`Height (cm)`, 0) as Height, 
                                    IFNULL(`Width (cm)`, 0) AS Width, 
                                    IFNULL(`Depth (cm)`, 0) AS Depth,
                                    Name As Artist
                             FROM artworks 
                             WHERE Artist IS NOT NULL
                             AND Artist NOT LIKE '%Unknown%';
                         """
                         , connector) 
artistAndArea = {"Artist" : [], "Area" : []}
def areafromDiameter(x) :
    return (np.pi/4)*(x**2)
def areafromCircumference(x) : 
    return (x**2)/(4*np.pi)
def areafromDimensions(x,y,z) : 
    if ( x*y*z != 0 ) :
        return 0 # 3D artwork
    else :
        xy = x*y
        yz = y*z
        xz = x*z
        if ( xy != 0 or yz != 0 or xz != 0 ) : 
            return (xy if xy != 0 else (yz if yz != 0 else xz)) # 2D artworks
        else : 
            return 0
        
indexList = dimensions.index
for index in indexList : 
    diameter = dimensions['Diameter'][index]
    if ( diameter != 0 ) :
        artistAndArea['Area'].append(areafromDiameter(diameter))
    else : 
        circumference = dimensions['Circumference'][index] != 0 
        if (circumference != 0) : 
            artistAndArea['Area'].append(areafromCircumference(circumference))
        else : 
            artistAndArea['Area'].append(areafromDimensions(dimensions['Height'][index], 
                                                          dimensions['Width'][index], 
                                                          dimensions['Depth'][index]))
    artistAndArea['Artist'].append(dimensions['Artist'][index])
    
artistAndArea_df = pd.DataFrame(artistAndArea)
artistAndArea_df['Area'].replace(to_replace=0, value=np.NaN, inplace=True)
artistAndArea_df.dropna(subset=['Area'], inplace=True)
sortedArea = artistAndArea_df.groupby('Artist').agg(['sum'])['Area'].sort_values(by=['sum'], ascending=False)
sortedRoundedInGoodDimensionArea = (sortedArea/10000).apply(lambda x : round(x,2)) # cm² to m² conversion

def topTenArtistsByArea() : 
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