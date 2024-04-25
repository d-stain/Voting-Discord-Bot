import ast
import math
from discord import ui
import traceback
import discord
from discord.ext import commands
import logging
import random
import base64
import asyncio
import json
from discord.ext import tasks
from datetime import datetime
import time
from dotenv import load_dotenv
import os
from algosdk.v2client import indexer
from algosdk.v2client import algod
import requests
import re
import copy
import io
import pandas as pd
import os

#Discord set-up
load_dotenv('example_token.env')
TOKEN = os.getenv('TOKEN')
intents = discord.Intents().default()
client = commands.Bot(command_prefix='.', intents=intents)
intents=discord.Intents.default()
intents.message_content = True

#Indexer on Voi tesnet
indexer_address = "https://testnet-idx.voi.nodly.io"
indexer_token = ""
headers = {"X-API-Key": indexer_token,}
voi_index = indexer.IndexerClient(indexer_token, indexer_address,headers)

#Algod on Voi tesnet
algod_address = "https://testnet-api.voi.nodly.io"
algod_token = ""
headers = {
    "X-API-Key": algod_token,
}
voi_algod_client = algod.AlgodClient(algod_token, algod_address,headers)

# Configure logger for error logging
logging.basicConfig(filename= 'voibot_log.txt', filemode = 'w', format = '%(asctime)s - %(levelname)s - %(message)s', level = logging.INFO)
logging.info('Start of the log')
logger = logging.getLogger()
 
#filepath to all database files
filepath = "C:/Users/"

#HolderDB
filename = "holder_database.json"
path_hdb = filepath + filename
with open(path_hdb,'r') as file:
    holder_database = json.load(file)

#user DB
filename2 = "user_database.json"
path_udb = filepath + filename2
with open(path_udb,'r') as file:
    user_database = json.load(file)

# Group DB
filename3 = "Voting_Group_database.json"
path_ddb = filepath + filename3
with open(path_ddb,'r') as file:
     Voting_Group_database = json.load(file)

#Creator DB
filename4 = "creator_database.json"
path_cdb = filepath + filename4
with open(path_cdb,'r') as file:
    creator_database = json.load(file)

#Active props DB
filename5 = "active_proposals.json"
path_ap = filepath + filename5
with open(path_ap,'r') as file:
    active_proposals = json.load(file)

#Active props DB
filename6 = "completed_proposals.json"
path_cp = filepath + filename6
with open(path_cp,'r') as file:
    completed_proposals = json.load(file)
    