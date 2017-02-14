
# coding: utf-8

# In[3]:

import os
import pandas as pd


# In[6]:

class Data(object):
    
    def __init__(self, files = [], ):
        """
        * A Data object containing a set of files from a given directory
        """
        
        self.files = files
        self.tmpFile = ''
        self.ts_data = None
        
    def get_all_files(self, path, extension):
        """
        * Get all files from the path and extension given and
        * save them as a set of Dataframes
        """
        
        for fileName in os.listdir(path):
            
            if self.filter_file(fileName, extension):
                tmpFile = pd.read_csv(path+fileName)
                self.files.append(tmpFile)
                
        return
    
    def filter_file(self, fileName, extension):
        """
        * Detects if a fileName corresponds to the extension desired
        """
        
        if fileName.endswith(extension):
            return True
        
        else:
            return False
    
    def get_file(self,index):
        """
        * Get the file in "index" from the set of Dataframes
        """
        
        try:
            
            tmpFile = self.files[index]
            
        except IndexError:
            print( "ExceptionError: Index out of range")
   
        return tmpFile

    def get_all_data(self):
        """
        * Returns all data stored in Data object
        """
        return self.files
    
    def save_ts_data(self,df):
        """
        * Set all data
        """
        
        self.ts_data = df
        
        return
    
    def write_to_csvfile(self,pred_df,dates_df,path,fileName):
        """
        * Write the predictions of a dataframe into a csv file
        """
        
        if fileName != "FebPredict":
            pred_imp = pd.DataFrame(pred_df,columns=["Pred_Impressions"])
        
            if fileName == "trainPredict":
                dates_df = dates_df.reset_index()
                del dates_df['index']
        
            pred_imp['Date'] = dates_df
        
            pred_imp.to_csv(path+fileName+".csv")
        else:
            
            pred_df[['Date','Pred_Impressions']].to_csv(path+fileName+".csv")
        
        print(fileName+'.csv saved')
        
        return
        
        
    


# In[ ]:




# In[ ]:



