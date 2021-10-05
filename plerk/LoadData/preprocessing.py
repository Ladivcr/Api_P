# -*- coding: utf-8 -*-
"""PlerkData.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10b1vwzAIZ4qO4JlDQbdjnzxt-XGo9s69

Date of creation: Monday 04 October 2021

Author: Ladivcr


                                     /| /                     
                                   / |/ | .-/                
                               |\ /  |  |/  /                 
              /\               | \|  |  |  |.-~/              
             / |   /|       |\ |  |  l  |  |  /               
          |\ |  \ / |  /|   | \|  |   \ `  | /                
      __  | \|   \|  \/ | __l  \   \   `  _. |                
      \ ~-|  `\   `\  \  \\ ~\  \   `. .-~   |                
       \   ~-. "-.  `  \  ^._ ^. "-.  /  \   |                
     .--~-._  ~-  `  _  ~-_.-"-." ._ /._ ." ./                
      >--.  ~-.   ._  ~>-"    "\\   /   /   |                 
     <.___~"--._    ~-{  .-~ .  `\ | . /    |                 
      <__ ~"-.  ~       /_/   \   \|  /   : |                 
        ^-.__           ~(_/   \     _    | |______           
            ^--.,___.-~"  /_/   !  `-.~"--l_ /     ~"-.       
                   (_/ .  ~(   /'     "~"--,|      -. _)      
                    (_/ .  \  :           / |           \     
                     \ /    `.    .     .^   \_.-~"~--.  )    
                      (_/ .   `  /     /       !       )/     
                       / / _.   '.   .':      /              
                       ~(_/ .   /    _  `  .-\_                     oooO
                         /_/ . ' .-~" `.  / \  \          (>        (...)    Oooo
                         ~( /   '  :   | /   "-.~-.______//         ...(    (....)
                           "-,.    l   |/ \_    __{----._(>          ._)     )../
                            //(     \  |    ~"~"     //                      (_/
                           /' /\     \  \           ((        
                         .^. / /\     "  }__ //==>            
                        / / ' '  "-.,__ {---(=>              
                      .^ '       :  |  ~"               
                     / .  .  . : | :!                       
                    (_/  /   | | |-"                        
                      \-_|_(_.^-~"               

                        █   ▄▀█ █▀▄ █ █ █ █▀▀ █▀█
                        █▄▄ █▀█ █▄▀ █ ▀▄▀ █▄▄ █▀▄

# Tareas

- [X] Limpieza de datos
- [X] Construcción del modelo base
"""

import pandas as pd
#import seaborn as sns
import uuid


def uppertacion(comp_name): 
  """A function to capitalize each company name
  INPUT
  comp_name = str | string wth a company name
  OUTPUT 
  a upper string company name
  """
  return comp_name.upper()


def need_date (f_tran):
  """A function to select just necessary part from a string
  INPUT
  f_tran = str | date of each transfer
  OUTPUT 
  A string just with necessary date
  """ 
  return str(f_tran[0:19])


def preprocess_data(my_data):
  """Function to apply the whole data processing 
  INPUT 
  my_data = Pandas DataFrame with whole data
  OUPUT
  Pandas DataFrame with data, but clean data :D
  """

  # Eliminación de datos nulos
  my_data.dropna(inplace=True)

  # Uppertacion de los datos
  my_data["company"] = my_data["company"].apply(uppertacion)

  # Remplazo de los valores "duplicados"
  my_data.replace(to_replace="COMISIÓN FEDERAL DE ELECTRICIDAD", value='CFE', inplace=True)
  my_data.replace(to_replace="HBOMAX", value="HBO MAX", inplace=True)
  my_data.replace(to_replace="IZZY INTERNET", value="IZZI INTERNET", inplace=True)
  my_data.replace(to_replace="NEW YORK TIMES", value="THE NEW YORK TIMES", inplace=True)
  my_data.replace(to_replace="PARAMOUNT PLUSS", value="PARAMOUNT+", inplace=True)
  my_data.replace(to_replace="PEDIDOS YA", value="PEDIDOSYA", inplace=True)

  # Cambio del formato de la fecha
  my_data["date"] = my_data["date"].apply(need_date)  
  my_data['date'] = pd.to_datetime(my_data['date'], format="%Y-%m-%d %H:%M:%S")

  return my_data

def table_empresas(my_data):
  """Function to create the table for companies 
  INPUT 
  my_data = Pandas DataFrame with whole data
  OUPUT
  Pandas DataFrame where the DF is the table for our DB
  """
  nombre = list(data.company.unique())
  status = ["activa" for i in range(len(nombre))]
  ID = [str(uuid.uuid4()) for ID in range(len(nombre))]

  # TODO: Corroboramos que no haya IDs duplicados
  # Recordemos que va a una base de datos por lo tanto el nombre y el ID deben de ser únicos
  if len(nombre) != len(list(set(ID))):
    duplication = True
    while duplication:
      ID = [str(uuid.uuid4()) for ID in range(len(nombre))]
      if len(nombre) == len(list(set(ID))):
        duplication = False
        break
  else: 
    pass
        
  Empresa = {
    'name' : nombre,
    'status': status,
    'ID': ID
  }
  df_Empresa = pd.DataFrame(Empresa)

  return df_Empresa


def table_transactions(my_data, table_empresas): 
  """Function to create the table for transactions
  INPUT 
  my_data = Pandas DataFrame with whole data
  table_empresas = Pandas DataFrame with companies's data
  OUPUT
  Pandas DataFrame where the DF is the table for our DB
  """
  # Combinar dataframes para generar la nueva tabla
  tmp = pd.merge(table_empresas, data, left_on='name', right_on='company')
  # Renombrar las columnas 
  tmp.rename(columns={'ID':'ID_Company','date':'transaction_date'},inplace=True)
  # Eliminamos las columnas que no corresponden al modelo para la tabla de transacciones
  del(tmp["name"])
  del(tmp["company"])
  del(tmp["status"])
  # Generación de IDs para cada transacción en la tabla
  ID_Transaction = [str(uuid.uuid4()) for ID in range(len(tmp))]
  # Asignamos el ID a cada transacción 
  tmp = tmp.assign(ID=ID_Transaction)

  # Obtención de la tabla "cobro final"
  #TODO: Columna para Cobro final 
  #Cobro Final (Boolean)
  # Este punto es una combinación de "Estatus de transacción y estatus de aprobación"
  # Sólo se deben cobrar aquellas combinaciones que sean: status_transaction = closed & status_approved = true

  # 1 si fue cobrado 
  # 0 si no fue cobrado
  ultimo_cobro = []
  # Iteración por filas del DataFrame:
  for indice_fila, fila in tmp.iterrows():
    Stransaction = fila.status_transaction
    Sapproved = fila.status_approved
    #print(indice_fila)
    #print(fila.status_transaction)
    #print(fila.status_approved)
    if Stransaction == "closed" and Sapproved == True:
      ultimo_cobro.append(1)
    else:
      ultimo_cobro.append(0)

  # añadimos la columna 
  tmp = tmp.assign(final_pay=ultimo_cobro)

  # Retornamos la nueva tabla
  return tmp