import pandas as pd
import sqlite3
from sqlite3 import Error

from preprocessing import preprocess_data, need_date, uppertacion, table_empresas, table_transactions
#import sys
#sys.path.insert(1, '/home/ladiv/Github/RestAPI/basemodel')
#from . import companies
#from basemodel.models import Companies, Transactions

# Preprocesamiento de los datos
#data = pd.read_csv("/home/ladiv/Github/RestAPI/LoadData/test_database.csv")
#data = preprocess_data(data)
#df_empresas = table_empresas(data)
#df_transactions = table_transactions(data, df_empresas)

table_empresas = pd.read_csv("/home/ladiv/Github/Api_P/plerk/LoadData/Table_Empresas.csv")
table_transactions = pd.read_csv("/home/ladiv/Github/Api_P/plerk/LoadData/Table_Transactions.csv")


#for indice_fila, fila in table_empresas.iterrows():
  #print(fila.nombre)
  # Instanciamos el registro 
  #companie = companies.models.Companies(name=fila.nombre, status=fila.status, ID = fila.ID)
  # Guardamos el registro en la base de datos
  #companie.save()

#print(True)
#from basemodel.models import Companies

conector = sqlite3.connect('../db.sqlite3')
#table_empresas.to_sql('companies_companies', con=conector, if_exists='append', index=False)
table_transactions.to_sql('transactions_transactions',con=conector, if_exists='append', index=False)
