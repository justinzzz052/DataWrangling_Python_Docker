#Import packages
import pandas as pd
import numpy as np
from sklearn import linear_model

#Load the training data
df_train=pd.read_csv('train.csv')

#Confirmed inputs
df_train_num=df_train[['OverallQual', 'YearBuilt', 'TotalBsmtSF', 'GrLivArea','FullBath', 'GarageArea','Id','SalePrice']]

#Normalise Area
df_train_num['GrLivArea']=np.log(df_train_num['GrLivArea'])
df_train_num['SalePrice']=np.log(df_train_num['SalePrice'])

#Remove outliers
df_train_num = df_train_num[df_train_num['TotalBsmtSF']<3000]
df_train_num = df_train_num[df_train_num['GrLivArea']<4500]
df_train_num = df_train_num[df_train_num['GarageArea']<1250]

#Build the model
ls = linear_model.LassoCV()

#Split the input and output
df_train_num_x=df_train_num.drop(['SalePrice','Id'],axis=1) 
df_train_num_y=df_train_num['SalePrice']

#Train the model
ls.fit(df_train_num_x, df_train_num_y)

#Check the model coefficients
print('Coefficients: \n', ls.coef_)

#Load the test data
df_test=pd.read_csv('test.csv')
df_test_num=df_test[['OverallQual', 'YearBuilt', 'TotalBsmtSF', 'GrLivArea','FullBath', 'GarageArea','Id']]

#IMPORTANT: All the feature engineering & data cleaning steps we have done to the testing variables, we have to do the same for the test dataset!!
#Normalise Area
df_test_num['GrLivArea']=np.log(df_test_num['GrLivArea'])

#Before we can feed the data into our model, we have to check missing values again. Otherwise the code will give you an error.
df_test_num.isnull().sum()
df_test_num['TotalBsmtSF']=df_test_num['TotalBsmtSF'].fillna(np.mean(df_test_num['TotalBsmtSF']))
df_test_num['GarageArea']=df_test_num['GarageArea'].fillna(np.mean(df_test_num['GarageArea']))


#Predict the results for test dataset
submit= pd.DataFrame()
submit['Id'] = df_test_num.Id
#select features 
preds_out = ls.predict(df_test_num[['OverallQual', 'YearBuilt', 'TotalBsmtSF', 'GrLivArea','FullBath', 'GarageArea']])
submit['SalePrice'] = np.exp(preds_out)
#final submission  
submit.to_csv('LassoCV_submission.csv', index=False)

