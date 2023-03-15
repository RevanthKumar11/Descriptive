import pandas as pd
import numpy as np
class Univariate():
    
    def SplitDataSet(dataSet):
        Quan = []
        Qual = []
        for column in dataSet.columns:
            if dataSet[column].dtypes == "O":
                Qual.append(column)
            else:
                Quan.append(column)
        return Quan,Qual 
   
    def FrequencyTabel(columnName, dataSet):
        frequency_table = pd.DataFrame(columns=['Unique_values', 'Frequency', 'Relative_Frequency', 'Cumsum'])
        frequency_table['Unique_values'] = dataSet[columnName].value_counts().index
        frequency_table['Frequency'] = dataSet[columnName].value_counts().values
        frequency_table['Relative_Frequency'] = (frequency_table['Frequency']/frequency_table['Unique_values'].size)
        frequency_table['Cumsum'] = frequency_table['Relative_Frequency'].cumsum()
        return frequency_table
    
    def Descriptive(quan, dataSet):
        descriptive = pd.DataFrame(index=                                ['Mean','Median','Mode','0%','25%','50%','75%','99%','100%','IQR','1.5rules','Lesser','Greater','Min','Max','skewness','kurtosis'], columns = quan)
        for columns in quan:
             #find the center point 
            descriptive[columns]['Mean'] = dataSet[columns].mean()
            descriptive[columns]['Median'] = dataSet[columns].median()
            #which has highest range
            descriptive[columns]['Mode'] = dataSet[columns].mode()[0]
            #percentail
            descriptive[columns]['0%'] = np.percentile(dataSet[columns],0)
            descriptive[columns]['25%'] = dataSet.describe()[columns]['25%']
            descriptive[columns]['50%'] = dataSet.describe()[columns]['50%']
            descriptive[columns]['75%'] = dataSet.describe()[columns]['75%']
            descriptive[columns]['99%'] = np.percentile(dataSet[columns],99)
            descriptive[columns]['100%'] = dataSet.describe()[columns]['max']
            #lesser outliner and highest outliner
            descriptive[columns]['IQR'] = descriptive[columns]['75%'] - descriptive[columns]['25%']
            descriptive[columns]['1.5rules'] = 1.5 * descriptive[columns]['IQR']
            descriptive[columns]['Lesser'] = descriptive[columns]['25%'] - descriptive[columns]['1.5rules']
            descriptive[columns]['Greater'] = descriptive[columns]['75%'] + descriptive[columns]['1.5rules']
            descriptive[columns]['Min'] = dataSet[columns].min()
            descriptive[columns]['Max'] = dataSet[columns].max()
            descriptive[columns]['skewness'] = dataSet[columns].skew()
            descriptive[columns]['kurtosis'] = dataSet[columns].kurtosis()
        return descriptive
    
    def OutLier(quan, descriptive):
        lesser = []
        greater = []
        for columns in quan:
            if(descriptive[columns]["Min"] < descriptive[columns]['Lesser']):
                lesser.append(columns)
            if(descriptive[columns]["Max"] > descriptive[columns]['Greater']):
                greater.append(columns)
        return lesser, greater
                
        
    def ReplaceOutlier(lesser, greater, dataSet, descriptive, quan):
        for columns in lesser:
            dataSet[columns][dataSet[columns] < descriptive[columns]['Lesser']] = descriptive[columns]['Lesser']
        for columns in greater:
            dataSet[columns][dataSet[columns] > descriptive[columns]['Greater']] = descriptive[columns]['Greater']
        descriptive = Univariate.Descriptive(quan, dataSet)
        lesser,greater = Univariate.OutLier(quan, descriptive)
        return descriptive,lesser,greater
        
    
    