from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers

from rest_framework import viewsets

from .serializers import Post1Serializer, Post2Serializer
from transactions.models import Transactions
from companies.models import Companies
import pandas as pd
import json
# Create your views here.

class ShowData(APIView):
    def to_pandas_t(self, data):
        self.data = data

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

    def to_pandas_c(self, data):
        self.data = data

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

    def get(self, request, format = None):
        transactions = Transactions.objects.all()

        transactions= serializers.serialize('json', transactions)
        
        #print(type(transactions_json))
        transactions = json.loads(transactions)
        #print(type(transactions))
        #print(transactions[0:10]) 
        # Compuesta por una lista con un diccionario anidado y pk como el id
        # de la compañia
        df_transactions = self.to_pandas_t(transactions)

        companies = Companies.objects.all()
        companies = serializers.serialize('json', companies)
        companies = json.loads(companies)
        df_companies = self.to_pandas_c(companies)
        
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

"""
class PostMergeViewSet(viewsets.ModelViewSet):
    serializer_class =Post1Serializer
    queryset = Transactions.objects.all()
    serializer_class =Post2Serializer
    queryset = Companies.objects.all()  
    print(queryset)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
"""