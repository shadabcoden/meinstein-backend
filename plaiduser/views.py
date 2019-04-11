from __future__ import absolute_import

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from plaiduser.models import MeAccounts, MeUserdetail, MePlaidUserItem, MePlaidUserItemAccounts
from plaiduser.serializers import MeAccountsSerializer, MeUserdetailSerializer

from rest_framework import generics

import json
import requests

from plaid import Client
from plaid.errors import APIError, ItemError

@api_view(['GET', 'POST'])
def accounts_list(request, format=None):
    """
    List all Items, or create a new ME Account.
    """
    if request.method == 'GET':
        items = MeAccounts.objects.all()
        serializer = MeAccountsSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MeAccountsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def account_detail(request, pk, format=None):
    """
    Retrieve, update or delete a ME Account.
    """
    try:
        item = MeAccounts.objects.get(account_id=pk)
    except MeAccounts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MeAccountsSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MeAccountsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def users_list(request, format=None):
    """
    List all Items, or create a new ME Account.
    """
    if request.method == 'GET':
        items = MeUserdetail.objects.all()
        serializer = MeUserdetailSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MeUserdetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk, format=None):
    """
    Retrieve, update or delete a ME Account.
    """
    try:
        item = MeUserdetail.objects.get(user_id=pk)
    except MeUserdetail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MeUserdetailSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MeUserdetailSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def call_api(request, format=None):
    # public_token = "public-sandbox-b15afb50-4f4e-48e7-a9ba-57351a810176" # 30 minutes expiry, got from plaid link ios
    client = Client(client_id='5c8159a33f8cdc0012224a84', secret='ed1c07b6c1b947e11d8d5c0cd6d384',
        public_key='7552cbcb11c6fa47dc533dc69bee73', environment='sandbox', api_version='2018-05-22')
    
    # response = client.Item.public_token.exchange(public_token)
    # access_token = response['access_token']

    access_token = "access-sandbox-234fa568-7417-4a4e-a34e-641b41d4ab64" #no expiry

    output = getAuthData(client, access_token)

    # headers = {}
    # url = 'http://jsonplaceholder.typicode.com/users/'
    # method = request.method.lower()
    # method_map = {
    #     'get': requests.get,
    #     'post': requests.post
    # }
    #return Response(method_map[method](url))
    return Response(data= output)


# same way create such method to dump data for other Plaid Endpoints
def getAuthData(client, access_token):
    output = []

    try:
        response = client.Auth.get(access_token)
        
        numbers = response['numbers']

        accounts = response['accounts']

        output = response

        plaid_user_item = MePlaidUserItem()
        plaid_user_item.item_id =  "ins_40" # data got from API
        plaid_user_item.item_name = "Morganstanley"
        plaid_user_item.accesstoken = access_token
        item = MeUserdetail.objects.get(user_id=2)
        plaid_user_item.user = item # MeUserdetail 1 getid
        plaid_user_item.save()


        for account in accounts:
            account_id = account['account_id']
            account_mask = account['mask']
            account_name = account['name']
            account_type = account['type']
            account_subtype = account['subtype']
            account_official_name = account['official_name']
            account_balance = account['balances']['available']
            account_currency = account['balances']['iso_currency_code']
            user_item_id = 1

            plaid_user_item_accounts = MePlaidUserItemAccounts()
            plaid_user_item_accounts.account_id = account_id
            plaid_user_item_accounts.name = account_name
            plaid_user_item_accounts.mask =  account_mask
            plaid_user_item_accounts.accounts_type = account_type
            plaid_user_item_accounts.subtype = account_subtype
            plaid_user_item_accounts.official_name = account_official_name
            plaid_user_item_accounts.available_balance = account_balance
            plaid_user_item_accounts.iso_currency_code = account_currency
            item = MePlaidUserItem.objects.get(user_item_id= user_item_id)
            plaid_user_item_accounts.user_item = item  # MePlaidUserItem id
            plaid_user_item_accounts.save()


    except:
        output = "error code"

    return output
