
# coding: utf-8

# In[4]:

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec


# In[3]:

class Visualization(object):
    
    def __init(self):
        """
        * Generate Visualization object in order to create
        * diverse visualizations of a given set of information
        *
        *
        """
    def country_comparisson(self,df,country):
        """
        * Generate visual comparisson of DAU and Impressions of a particular country
        """
        
        ax = df.loc[df.Country == country][['DAU','Impressions']].plot(kind='bar', 
                                                                       title ="DAU vs Impressions : s" + country,
                                                                       figsize=(10, 7), legend=True, fontsize=12)
            
        ax.set_ylabel("Number of Users", fontsize=12)
        plt.grid(True)
        plt.legend(loc='best')
        plt.show()
        
        
                
        
        return
    
    def plot_all_countries(self,df,fieldName):
        """
        * Generate a plot of fieldName for each country in dataframe
        """
        
        countries = df.Country.unique()
        fig = plt.figure(figsize=(14,6))
        plt.grid(True)
        
        for country in countries:
            df.loc[df.Country == country][fieldName].plot(legend=True,label=country)
        plt.title("Distribution of " + fieldName + " per country")    
        plt.legend(loc='best')
        plt.show()
            
        return
    
    def plot_correlation(self,df,varX,varY):
        """
        * Generate a scatter plot of relationship
        * among two variables
        """
        
        fig = plt.figure(figsize=(14,6))
        plt.scatter(df[varX], df[varY])
        plt.grid(True)
        plt.title("Correlation among " + varX + " " + varY)
        plt.xlabel(varX)
        plt.ylabel(varY)
        plt.show()
        
        return
    
    def plot_country_corr(self,cor,message = ""):
        """
        * Generate a bar plot of the correlation values per each country
        """
        
        fig = plt.figure(figsize=(14,6))
        cor.Correlation.plot(kind="bar",label='Country')
        plt.grid(True)
        plt.title("Correlation between DAU and Impressions per country " + message)
        plt.ylabel("Correlation * 100%")
        plt.show()
        
        return
    def compare_platf_corr(self,cor_df):
        """
        * Plot platform comparison of correlations between platforms
        """
        cor_df.plot.bar(figsize=(14,6),grid=True,title = "Correlation rates of DAU and Impressions: iOS vs Android per Country")
        
        return
    
    def plot_adsDist_games(self,dfu_g1,dfu_g2,dfu_g3):
        """
        * Plot ads distribution of players in 3 games
        """
        
        fig = plt.figure(figsize=(19, 6)) 
        gs = gridspec.GridSpec(1, 3, width_ratios=[2.5, 2,1.5])
        
        ax0 = plt.subplot(gs[0])
        ax0.set_ylabel("No. of players")
        dfu_g1.plot( ax=ax0,kind="bar",title='Game1',grid=True)
        
        ax1 = plt.subplot(gs[1])
        ax1.set_ylabel("No. of players")
        dfu_g3.plot( ax=ax1,kind="bar",title="Game3",grid=True)
        
        ax2 = plt.subplot(gs[2])
        ax2.set_ylabel("No. of players")
        dfu_g2.plot( ax=ax2,kind="bar",title="Game2",grid=True)
        plt.show()
        
        return
    
    def plot_games_visual(self,games_df,users_df):
        """
        * Plos visualization of players per platform and total number of players
        * in the three games
        """
        
        
        fig = plt.figure(figsize=(19, 6)) 
        gs = gridspec.GridSpec(1, 2, width_ratios=[2.5, 2.5])
        
        ax0 = plt.subplot(gs[0])
        ax0.set_ylabel("No. of players")
        games_df.plot( ax=ax0,kind="bar",title="Distribution of users per platform for the 3 games analyzed",grid=True)
        
        ax1 = plt.subplot(gs[1])
        ax1.set_ylabel("No. of players")
        users_df.plot( ax=ax1,kind="bar",title="Number of players per game",grid=True)

        


# In[ ]:



