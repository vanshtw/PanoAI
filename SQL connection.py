import pyodbc
import json

# Define connection parameters
server = 'OR1DRA862' 
database = 'UDA_ProfServices'

# Establish connection
conn = pyodbc.connect(f'DRIVER={{SQL Server}};'
                      f'SERVER={server};'
                      f'DATABASE={database};'
                      f'Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()

# Execute a query
cursor.execute("SELECT * FROM UDA_ProfServices.PS.vw_td_RevenueCategory")

# Fetch and print results
rows = cursor.fetchall()
a=[]
# Process and print results
for row in rows:
    a.append(row)  # Each row is a tuple
        
#print(rows)
print(a)
print((a))

# Close the connection
cursor.close()
conn.close()