import pandas as pd

df_serverdetails = pd.read_excel("C:\Vansh\OneDrive - Adobe\Work\#Cloud Journey\Gen AI Bot Files\Datapoints\RevenueMapping.xlsx", sheet_name= "SQL Server Details")  
df_data          = pd.read_excel("C:\Vansh\OneDrive - Adobe\Work\#Cloud Journey\Gen AI Bot Files\Datapoints\RevenueMapping.xlsx", sheet_name= "Views and Columns")  

#print(df_serverdetails, df_data)

df_json = df_data.to_json(orient="records")
print(df_json)  # Send this to the chatbot