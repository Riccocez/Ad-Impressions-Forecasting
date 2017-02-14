
# coding: utf-8

# In[4]:

import pandas as pd
from scipy import stats
from datetime import datetime
import datetime
import numpy as np


# In[2]:

class Manipulate(object):
    
    def __init__(self,df=None):
        """
        * A preprocessing object which allows performing most of the 
        * required transformations to manipulate dataset
        """
        self.df = df
        
    
    def convert_to_timeseries(self,df):
        """
        * Converts a dataframe object into 
        * a set of time series dataframe object
        """
        self.df = df.set_index('Date')
            
        return self.df
    
    def metrics_country_platf(self,df):
        """
        * Return one dataframe per platform 
        * with information per country
        """
        
        try:
            
            ios_df = []
            and_df = []
            
            
            countries = df.Country.unique()
            platforms = df.Platform.unique()

            for platf in platforms:
                for country in countries:
                    tmp_rec = df.loc[(df.Platform == platf) & (df.Country == country)]
        
                    if platf == "iOS":
                        ios_df.append(tmp_rec)
                    elif platf == "Android":
                        and_df.append(tmp_rec) 
                
            ios_df = self.concat_df(ios_df) 
            and_df = self.concat_df(and_df)

            
        except IndexError:
            print("DataFrame doesn't have Country data")    
        
        return ios_df,and_df
    
    def concat_df(self,df):
        """
        * Concatenate a set of DataFrame objects
        """ 
        conc_df = pd.concat(df)
        conc_df = self.set_index(conc_df,"Date")
        #conc_df.set_index("Date")
        return conc_df
    
    def set_index(self,df,columnName):
        """
        * Convert a DataFrame object into a Time Series DataFrame object
        """
        new_df = df.set_index(columnName)
        return new_df
    
    
    def total_metrics_country(self,df):
        """
        * Return a DataFrame object with the collectiong of metrics per country
        """
        try:
            
            
            countries = df.Country.unique()
            dates = df.Date.unique()
            preproc_rec = []
            
            for country in countries:
                for date in dates:
        
                    #Create method that returns sum
                    tmp_dau = self.sum_plaform_field(df,country,date,"DAU")
                    tmp_impres = self.sum_plaform_field(df,country,date,"Impressions")
        
                    tmp_record = [date, country, tmp_dau, tmp_impres]
                    preproc_rec.append(tmp_record)

            new_df = pd.DataFrame(preproc_rec,columns=["Date","Country","DAU","Impressions"])
            new_df = new_df.set_index('Date')
                
            
        except IndexError:
            print("DataFrame doesn't have Country data")
    
        return new_df
    
    
    def sum_plaform_field(self,df,country,date,field):
        """
        * Sum the counts of a particular field in iOS and Android 
        * platform based on a given country and a given date
        """
        
        sum_field = df.loc[(df.Country == country ) & (df.Date == date)][field].sum()
        
        return sum_field
    
    def get_correlation(self,df,varX,varY):
        """
        * Return the Pearson correlation between two variables
        """
        
        corr = stats.pearsonr(df[varX],df[varY])
        
        return corr
    
    def get_corr_percountry(self,df,varX,varY):
        """
        * Return the correlation among two variables per country in a DataFrame
        """
        
        correlation = []

        for country in df.Country.unique():
            tmp_corr = df.loc[df.Country == country].corr()[varX][varY]
            correlation.append((country,tmp_corr))
            
        cor = pd.DataFrame(correlation,columns=["Country","Correlation"])
        cor = cor.set_index("Country")
        
        return cor
    
    def join_corr_platform(self,ios_cor,and_cor):
        """
        * Concatenates correlation DataFrame objects
        """
        plat_cor = [ios_cor,and_cor]
        cor_df = pd.concat(plat_cor,axis=1)
        cor_df.columns = ['iOS',"Android"]
        
        return cor_df
    
    def groupby_games(self,df):
        """
        * Returns a set of DataFrames grouped by game
        """
        
        df_g1 = self.extract_game(df,"game1")
        dfu_g1 = self.groupby_game(df_g1)
        
        df_g2 = self.extract_game(df,"game2")
        dfu_g2 = self.groupby_game(df_g2)
        
        df_g3 = self.extract_game(df,"game3")
        dfu_g3 = self.groupby_game(df_g3)
        
        
        return dfu_g1,dfu_g2,dfu_g3
    
        
        
    def extract_game(self,df,gameName):
        """
        * Extracts records from DataFrame of a specific gameName
        """
        df_game = df.loc[(df.GameId == gameName)]
        return df_game
    
    def groupby_game(self,df):
        """
        * Groups a DataFrame object of a game by Platform
        """
        
        
        tmp_df = df.groupby(["Platform","AdUnit"]).size()
        dfu = tmp_df.unstack("Platform")
        
        return dfu
        
    def game_users(self,df,fieldName):
        """
        * Returns a DataFrame object with the number of users per platform
        * of the games included in df
        """
        
        games = df.GameId.unique()
        gamelist = []
        
        for game in games:
                
                game_df = self.get_field_values(df,game,fieldName)
                gamelist.append(game_df)
                
        
                
        games_df = pd.concat(gamelist,axis=1)
        games_df.columns = games
        
        
        return games_df
    
    def get_field_values(self,df,gameName,fieldName):
        """
        * Return a DataFrame object with the Platform values of a specific game
        """
        
        tmp_df = self.extract_game(df,gameName)
        game_df = pd.DataFrame(tmp_df[fieldName].value_counts())
        
        return game_df
        
    def fix_bugs_datetime(self,values,fieldName):
        """
        * Fix some bugs from datetime library and 
        * set up correct values in values list
        """
        
        if fieldName == 'day':
            for i in range(1,13):
                values[i+13]= i
                
        elif fieldName == "weekofyear":
            for i in range(1,13):
                if i<=7:
                    values[i+13] = 1
                elif i>7:
                    values[i+13] = 2        
        return values
    
    def create_dates(self,month,year,daysinmonth):
        """
        * Generate dates of month
        """
        month = month
        year = year
        dates = []
        
        for i in range(1,daysinmonth+1):
            if i <=9:
                day = str(0) + str(i)
            else:
                day = str(i)
            date = day + '.' + month + '.' + year
            dates.append(date)
            
            
        return dates
    
        # convert an array of values into a dataset matrix
    def create_dataset(self,dataset, look_back=1):
        """
        * Create a dataset with look_back information
        """
        dataX, dataY = [], []
        
        for i in range(len(dataset)-look_back-1):
            tmp_rec = dataset[i:(i+look_back), 0]
            dataX.append(tmp_rec)
            dataY.append(dataset[i + look_back, 0])
            
        return np.array(dataX), np.array(dataY)
    
    
    def create_dataset_no_look(self, dataset, look_back=0):
        """
        * Create a dataset withouth look_back information
        """
        
        dataX, dataY = [], []
        
        for i in range(len(dataset)-1):
            feats = dataset[i:(i+1), 1:]
            dataX.append(feats[0])
            dataY.append(dataset[i:(i+1),0])
            
        return np.array(dataX), np.array(dataY)

    
    
        
    def build_features(self,df):
        """
        * Build features related to datetime information in DataFrame
        """
        
        df['Date'] = [pd.datetime.strptime(date, '%d.%m.%Y') for date in df['Date']]
        dt_data = pd.DatetimeIndex(df['Date'])
        
        df['dayofweek'] = dt_data.dayofweek
        df['dayofyear'] = dt_data.dayofyear
        df['day'] =  dt_data.day 
        df['weekofyear'] = dt_data.weekofyear 
        df['year'] = dt_data.year

        df['Prev_DAU'] = np.append([np.NaN],df.DAU.values[0:-1])
        df['Prev_Impressions'] = np.append([np.NaN],df.Impressions.values[0:-1])
        
        return df
    
    def select_features(self,df,features,indexfield='Date'):
        """
        * Return a Dataframe object with the selected features
        * and indexed by indexfield
        """
        
        selected_df = df[features][1:]
        selected_df = selected_df.set_index(indexfield)
        
        return selected_df
    
    def get_test_data(self,df,features,size):
        """
        * Return a Dataframe with the selected features 
        * for testing predictor model
        """
        
        test_df = df[features][size:]
        
        return test_df
    
    def split_train_test(self, dataset,size=0.67):
        """
        * Split data into train and test sets
        """
        
        train_size = int(len(dataset) * size)
        test_size = len(dataset) - train_size
        train, test = dataset[0: train_size,:], dataset[train_size:len(dataset),:]
        print("Size of Train data: ",len(train), "Size of Test data: ", len(test))
        
        return train,test,train_size
    
    def build_df_predictions(self,predicts,columnName,field_df,minthres,maxthres=-1):
        """
        * Return a dataframe object of the predictions of predicts
        """

        pred_df = pd.DataFrame(predicts.round(),
                               columns=[columnName + 'Impressions']).set_index(field_df.index[minthres:maxthres])
        return pred_df
        


# In[ ]:



