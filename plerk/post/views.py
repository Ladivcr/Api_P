from os import name
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializers import Post1Serializer, Post2Serializer
from transactions.models import Transactions
from companies.models import Companies
import pandas as pd
import json
# Create your views here.
def to_pandas_t(data):
        #self.data = data

        tmp_df = {"ID": [], "ID_Company": [], "price": [], "transaction_date": [],
        "status_transaction": [], "status_approved": [], "final_pay": []}

        for element in data:          
            element = (dict(element))
            for key, value in element.items():
                #print("key", key,"value", value)
                if key == "pk":
                    tmp_df["ID"].append(value)
                elif key == "fields":
                    tmp_df["ID_Company"].append(element["fields"]["ID_Company"])
                    tmp_df["price"].append(element["fields"]["price"])
                    tmp_df["transaction_date"].append(element["fields"]["transaction_date"])
                    tmp_df["status_transaction"].append(element["fields"]["status_transaction"])
                    tmp_df["status_approved"].append(element["fields"]["status_approved"])
                    tmp_df["final_pay"].append(element["fields"]["final_pay"])
                    
        df = pd.DataFrame (tmp_df)
        return (df)

def to_pandas_c(data):
        

        tmp_df = {"ID": [], "name": [], "status": []}

        for element in data:          
            element = (dict(element))
            for key, value in element.items():
                #print("key", key,"value", value)
                if key == "pk":
                    tmp_df["ID"].append(value)
                elif key == "fields":
                    tmp_df["name"].append(element["fields"]["name"])
                    tmp_df["status"].append(element["fields"]["status"])
                    
        df = pd.DataFrame (tmp_df)
        return (df)

class ShowData(APIView):

    def get(self, request, format = None):
        transactions = Transactions.objects.all()
        transactions= serializers.serialize('json', transactions)
        
        #print(type(transactions_json))
        transactions = json.loads(transactions)
        #print(type(transactions))
        #print(transactions[0:10]) 
        # Compuesta por una lista con un diccionario anidado y pk como el id
        # de la compañia
        #df_transactions = self.to_pandas_t(transactions)
        df_transactions = to_pandas_t(transactions)

        companies = Companies.objects.all()
        companies = serializers.serialize('json', companies)
        companies = json.loads(companies)
        #df_companies = self.to_pandas_c(companies)
        df_companies = to_pandas_c(companies)
        
        # TODO: La empresa con más ventas
        #print(df_transactions.columns)
        result = df_transactions.groupby(['ID_Company'])['final_pay'].count().sort_values().tail(1).reset_index()
        aux = str(result.ID_Company[0])
        #result = result.ID_Company[0] 
        max_sales = df_companies.loc[(df_companies["ID"] == aux)]
        
        # TODO: Empresa con menos ventas
        result = df_transactions.groupby(['ID_Company'])['final_pay'].count().sort_values().head(1).reset_index()
        aux = str(result.ID_Company[0])
        #result = result.ID_Company[0] 
        min_sales = df_companies.loc[(df_companies["ID"] == aux)]
        
        # TODO: El precio total de las transacciones que SI se cobraron
        whole_price = df_transactions.loc[(df_transactions.status_transaction == "closed") & (df_transactions.status_approved == True)]["price"].sum()
        #whole_price = df_transactions.loc[(df_transactions.final_pay == 1)]["price"].sum()


        # TODO: El precio total de las transacciones que NO se cobraron
        Lost_price = df_transactions.loc[(df_transactions.status_transaction != "closed") & (df_transactions.status_approved != True)]["price"].sum()
        

        # TODO: Empresa más rechazada 
        tmp = df_transactions.loc[(df_transactions.status_transaction != "closed") & (df_transactions.status_approved != True)]
        tmp = tmp.groupby(['ID_Company'])['final_pay'].count().sort_values().tail(1).reset_index()
        reject = str(tmp.ID_Company[0])
        reject = df_companies.loc[(df_companies["ID"] == reject)].name
        
        #reject = 1
        return Response({'Servicio de resumen':{
                            'Empresa con mas ventas': max_sales,
                            'Empresa con menos ventas':min_sales,
                            'Precio total de transacciones cobradas (pesos)' : whole_price,
                            'Precio total de transacciones no cobradas (pesos)' : Lost_price,
                            'Empresa mas rechazada': reject}
        })

class FilterData(APIView):

    def get(self, request, id, format=None):
        print(id)
        print(request)
        print("\nENTRE\n")
        transactions = Transactions.objects.all()
        transactions= serializers.serialize('json', transactions)
        transactions = json.loads(transactions)
        df_transactions = to_pandas_t(transactions)
    
        companies = Companies.objects.all()
        companies = serializers.serialize('json', companies)
        companies = json.loads(companies)
        df_companies = to_pandas_c(companies)

        # TODO: Nombre de la empresa
        name_companie = df_companies.loc[(df_companies.ID == str(id))].name
        #print(name_companie)

        # TODO: Total de transacciones que SI se cobraron 
        aux = list(df_transactions.loc[(df_transactions.ID_Company == str(id))].final_pay)
        total_yes = aux.count("1")
        #print(aux)

        # TODO: Total de transacciones que NO se cobraron
        aux = list(df_transactions.loc[(df_transactions.ID_Company == str(id))].final_pay)
        total_no = aux.count("0")

        # TODO: El día que se registraron más transacciones
        fechas=list(df_transactions.loc[(df_transactions.ID_Company == str(id))].transaction_date)
        short_fechas = [i[:10] for i in fechas]
        filter = set(short_fechas)
        conteo = 0
        fecha = ""
        for fec in filter:
            tmp = short_fechas.count(fec)
            if tmp > conteo:
                conteo = tmp
                fecha = fec
    
        #print(fecha, conteo)
        tmp = pd.Timestamp(fecha)
        #day_week = tmp.dayofweek
        day_week_name = tmp.day_name()

        # * TODO: El més con más ventas
        short_fechas = [pd.Timestamp(i[:10]) for i in fechas]

        aux = {}
        for month in short_fechas:
            month_na = month.month_name()
            if month_na in aux:
                aux[month_na] += 1
            else:
                aux[month_na] = 1
        
        max_sales_month = max(aux.values())
        max_sales_month = list(aux.keys())[list(aux.values()).index(max_sales_month)]


        return Response({"Servicio de empresa": {
            "ID": id,
            "Nombre": name_companie,
            "Total de transacciones que SI se cobraron": total_yes,
            "Total de transacciones que NO se cobraron": total_no,
            f"El día que se registraron más transacciones {fecha} ({day_week_name})": conteo,
            "El mes en el que se ha vendido más": max_sales_month
        }})