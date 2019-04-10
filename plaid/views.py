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

from plaid.models import MeAccounts, MeUserdetail
from plaid.serializers import MeAccountsSerializer, MeUserdetailSerializer

from rest_framework import generics

import json
import requests


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
        item = MeAccounts.objects.get(id=pk)
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
        item = MeUserdetail.objects.get(id=pk)
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
    headers = {}
    url = 'http://jsonplaceholder.typicode.com/users/'
    method = request.method.lower()
    method_map = {
        'get': requests.get,
        'post': requests.post
    }
    return Response(method_map[method](url))

