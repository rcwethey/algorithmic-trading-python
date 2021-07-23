from secrets import IEX_CLOUD_API_TOKEN
import numpy as np
from scipy import stats
import math
import pandas as pd
import requests
import xlsxwriter
import os
import sys

# Helper functions


def chunks(lst, n):
    """Yield successive n-sized chunks from list"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


stocks = pd.read_csv(os.path.join(
    os.path.dirname(sys.argv[0]), "sp_500_stocks.csv"))
