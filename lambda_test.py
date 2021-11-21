import boto3
import json
import sys
import os
import boto3
from io import StringIO
import logging
#import pandas as pd

# set up logging
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler.setFormatter(formatter)
LOG.addHandler(logHandler)

def create_table():
    # TODO implement
    dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
    
    LOG.info(list(dynamodb.tables.all()))
    print("here")
    
    table = dynamodb.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


def add_item (data):
    dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
    table = dynamodb.Table('Movies')
    response = table.put_item(
       Item= data
    )
    return response

    
if __name__ == "__main__":
    # movie_table = create_table()
    # print("Table status:", movie_table.table_status)
    data= {
           "year" : 2013,
           "title" : "Turn It Down, Or Else!",
            }
    response = add_item(data)
    print(response)
        

    

