from django.shortcuts import redirect, render
import pandas as pd
import joblib
from .models import Contact, OrderUpdate, authenticator, Claimed
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User

model = joblib.load('Crop_Recommendation/model.pkl')

df = pd.read_csv('Data/final_df.csv')

prod_dict = {'Absolute': 0, 'Absolute-Maxx': 1, 'Adament': 2, 'Aliette': 3, 'Delaro': 4, 'Delaro Complete': 5, 'Flint Extra': 6, 'Luna': 7, 'Minuet': 8, 'Previcur Flex': 9, 'Proline': 10, 'Propulse': 11, 'Prosaro': 12, 'Provost Silver': 13, 'Scala': 14, 'Serenade ASO': 15, 'Serenade Opti': 16, 'Stratego': 17, 'Stratego YLD': 18, 'Finish 6 Pro': 19, 'Ginstar': 20, 'Stance': 21, 'Admire Pro': 22, 'Baythroid XL': 23, 'Leverage 360': 24, 'Movento': 25, 'Movento MPC': 26, 'Oberon': 27, 'Sivanto': 28, 'Velum': 29, 'Velum One': 30, 'Velum Prime': 31, 'Velum Total': 32, 'Wolverine': 33, 'Wolverine Advanced': 34, 'Warrant Ultra': 35, 'Warrant': 36, 'Varro': 37, 'TripleFLEX II': 38, 'RT 3': 39, 'Roundup WeatherMAX': 40, 'Roundup PowerMAX II': 41, 'Roundup PowerMAX 3': 42, 'Rimfire Max': 43, 'Ricestar HT': 44, 'Osprey': 45, 'Olympus': 46, 'Nortron SC': 47, 'Luxxur': 48, 'Laudis': 49, 'Huskie FX': 50, 'Huskie Complete': 51, 'Huskie': 52, 'Harness Xtra': 53, 'Harness MAX': 54, 'DiFlexx DUO': 55, 'DiFlexx': 56, 'Degree Xtra': 57, 'Corvus': 58, 'Capreno': 59, 'Balance Flexx': 60, 'Axiom': 61, 'Autumn Super': 62, 'Alion': 63}

state_dict = {'AL': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32, 35, 36, 38, 40, 41, 42, 45, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'AR': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 35, 36, 38, 40, 41, 42, 44, 45, 46, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'CO': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 33, 34, 36, 37, 38, 39, 40, 42, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'DE': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 36, 38, 40, 42, 45, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'FL': [0, 1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32, 40, 41, 42, 49, 52, 55, 56, 59, 61, 63], 'GA': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32, 35, 36, 38, 40, 41, 42, 45, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'ID': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 33, 34, 36, 37, 39, 40, 42, 45, 46, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 59, 61, 62, 63], 'IL': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 35, 36, 38, 40, 42, 45, 46, 47, 49, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'IN': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 35, 36, 38, 40, 42, 45, 46, 49, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'KS': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 35, 36, 38, 39, 40, 42, 44, 45, 46, 47, 49, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'KY': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 17, 18, 20, 22, 23, 24, 25, 27, 28, 29, 31, 35, 38, 40, 41, 42, 45, 46, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'LA': [0, 1, 3, 4, 6, 8, 9, 10, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 35, 36, 38, 40, 41, 42, 44, 45, 46, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'MD': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 27, 28, 31, 35, 36, 38, 40, 42, 45, 49, 50, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'MI': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 35, 36, 38, 40, 42, 45, 46, 47, 49, 50, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'MN': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'MO': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 35, 36, 38, 40, 41, 42, 44, 45, 46, 47, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'MS': [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 35, 36, 38, 40, 41, 42, 44, 45, 46, 49, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'MT': [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 33, 34, 36, 37, 39, 40, 42, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'NC': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 35, 36, 38, 40, 41, 42, 45, 47, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'ND': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'NE': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 35, 36, 38, 39, 40, 42, 45, 46, 47, 49, 50, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'NM': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 36, 38, 39, 40, 42, 45, 46, 47, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62], 'NY': [0, 3, 4, 6, 7, 9, 10, 11, 12, 14, 15, 18, 23, 24, 25, 31, 35, 36, 38, 40, 42, 45, 47, 49, 52, 53, 54, 55, 56, 57, 59, 63], 'OH': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 35, 36, 38, 40, 42, 45, 46, 47, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'OK': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 35, 36, 38, 39, 40, 42, 45, 46, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'OR': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 33, 34, 37, 39, 40, 42, 45, 46, 47, 48, 49, 52, 53, 55, 56, 59, 61, 62, 63], 'PA': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 35, 36, 38, 40, 42, 45, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 'SC': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 35, 36, 38, 40, 41, 42, 45, 49, 50, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'SD': [0, 1, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'TN': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 35, 36, 38, 40, 41, 42, 44, 45, 46, 49, 50, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'TX': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 35, 36, 38, 39, 40, 42, 44, 45, 46, 47, 49, 50, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'UT': [0, 1, 3, 4, 6, 7, 8, 9, 10, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 33, 35, 36, 39, 40, 42, 45, 46, 47, 49, 52, 53, 54, 55, 56, 57, 59, 61, 62, 63], 'VA': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 35, 36, 38, 40, 41, 42, 45, 49, 50, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'WA': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 33, 34, 37, 39, 40, 42, 45, 46, 47, 48, 49, 52, 55, 56, 59, 61, 62, 63], 'WI': [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 33, 34, 35, 36, 38, 40, 42, 43, 47, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'WY': [0, 1, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 22, 23, 24, 25, 27, 28, 31, 33, 34, 36, 37, 38, 39, 40, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'IA': [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 35, 36, 38, 39, 40, 42, 45, 46, 47, 49, 50, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'CA': [2, 3, 6, 7, 8, 9, 14, 15, 17, 18, 19, 20, 21, 23, 24, 25, 27, 28, 30, 40, 45, 47, 49, 56, 59, 63], 'AK': [3, 8, 9, 10, 14, 15, 16, 22, 24, 25, 27, 28, 40, 42, 50, 52, 55], 'AZ': [3, 4, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 30, 32, 36, 40, 42, 45, 49, 55, 59, 61, 62], 'CT': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 35, 36, 40, 42, 49, 50, 52, 53, 54, 55, 56, 57, 59, 61, 62, 63], 'HI': [3, 6, 8, 9, 10, 14, 15, 16, 22, 23, 24, 25, 27, 28, 30, 36, 42, 46, 49, 54, 55, 56, 59, 61, 63], 'MA': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 35, 40, 42, 45, 49, 50, 52, 54, 55, 56, 59, 61, 62, 63], 'ME': [3, 4, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 35, 40, 42, 47, 49, 52, 53, 54, 55, 56, 59, 61, 62, 63], 'NH': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 42, 49, 50, 52, 55, 56, 59, 61, 62, 63], 'NJ': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 35, 36, 38, 40, 42, 45, 49, 50, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'NV': [3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 39, 40, 42, 45, 47, 49, 50, 52, 53, 54, 55, 56, 57, 61, 63], 'RI': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 35, 36, 40, 49, 52, 53, 54, 55, 56, 59, 61, 62, 63], 'VT': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 27, 28, 31, 35, 36, 38, 40, 42, 49, 50, 52, 53, 54, 55, 56, 57, 59, 61, 62, 63], 'WV': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 27, 28, 31, 35, 36, 38, 40, 42, 45, 49, 50, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63], 'PR': [7, 8, 9, 14, 15, 16, 19, 22, 23, 25, 27, 40, 49], 'DC': [8, 9, 10, 14, 15, 16, 25, 28, 31, 40, 45, 49, 53, 54, 55, 57, 61], 'AS': [33, 46], 'FM': [33, 46], 'GU': [33, 46], 'MH': [33, 46], 'MP': [33, 46], 'PW': [33, 46], 'VI': [33, 46]}

pest_dict = {'Anthracnose': [0, 2, 4, 5, 6, 7, 10, 11, 12, 14, 15, 16, 17, 18], 'Blight, Leaf': [0, 6, 7, 15], 'Blotch, Glume': [0, 4, 10, 17, 18], 'Blotch, Leaf': [0, 4, 7, 17, 18], 'Blotch, Net': [0, 4, 10, 12, 17, 18], 'Blotch, Spot': [0, 4, 10, 12, 17, 18], 'Blotch, Web': [0, 13, 15], 'Powdery Mildew': [0, 4, 5, 6, 7, 10, 11, 12, 14, 15, 16, 17, 18, 29, 30, 31], 'Rot, Limb': [0], 'Rust': [0, 1, 4, 5, 6, 7, 10, 11, 12, 15, 17, 18], 'Scab, Pecan': [0, 15, 17, 22], 'Scald': [0, 4, 10, 12, 17, 18], 'Spot, Early Leaf': [0, 10, 11, 13, 15, 29, 32], 'Spot, Late Leaf': [0, 10, 11, 13, 15, 29, 32], 'Spot, Tan': [0, 4, 5, 10, 12, 15, 17, 18], 'Anthracnose leaf blight': [1], 'Eyespot': [1], 'Gray leaf spot': [1], 'Northern/Southern corn leaf blight': [1], 'Leaf blight': [1], 'Powdery mildew': [1], 'Tan spot': [1], 'Glume blotch': [1], 'Alternaria': [2, 6, 7, 14], 'Blight, Alternaria Late': [2, 6, 7], 'Blight, Blossom': [2, 6, 7, 14], 'Blight, Botryosphaeria Panicle': [2, 6, 7], 'Blight, Botryosphaeria': [2, 14, 15], 'Blight, Brown Rot Blossom': [2, 6, 7, 14, 15, 16], 'Blight, Eastern Filbert': [2, 6, 7, 17], 'Shoot': [2], 'Blight, Shoot': [2, 7, 14], 'Bacteria, Ice-Nucleating': [3], 'Blight, Alternaria Leaf': [3, 6, 7, 15, 16], 'Blight, Fire': [3, 15, 16], 'Blight, Phytophthora Raceme': [3], 'Blotch, Purple': [3, 7, 14, 15, 16], 'Canker, Citrus': [3, 15, 16, 22, 28], 'Canker, Phomopsis': [3, 7, 10], 'Canker, Phytophthora': [3], 'Canker, Pruning-Wound': [3], 'Damping Off, Pythium': [3, 9], 'Disease, Citrus Greening': [3], 'Disease, Huanglongbing': [3], 'Disease, Root': [3], 'Downy Mildew': [3, 6, 7, 9, 15], 'Gummosis': [3], 'Mold, Blue': [3, 15], 'Red Stele': [3], 'Rot, Alternaria Fruit': [3, 7, 10, 11, 15, 16], 'Rot, Anthracnose Fruit': [3, 15, 16], 'Rot, Crown': [3, 4, 10, 15], 'Rot, Heart': [3, 15], 'Rot, Leather': [3], 'Rot, Phytophthora Brown': [3], 'Rot, Phytophthora Collar': [3], 'Rot, Phytophthora Foliar': [3], 'Rot, Phytophthora Foot': [3], 'Rot, Phytophthora Fruit': [3], 'Rot, Phytophthora Root': [3, 9, 15], 'Rot, Root': [3, 10], 'Rust, White': [3, 15], 'Sigatoka, Black': [3], 'Sigatoka, Yellow': [3], 'Spear Slime': [3], 'Spot, Alternaria Brown': [3, 7, 29, 31], 'Spot, Alternaria Leaf': [3, 4, 5, 6, 7, 10, 11, 14, 15, 16, 17, 18], 'Spot, Bacterial': [3, 15, 16], 'Spot, Blister': [3], 'Blight, Anthracnose Leaf': [4, 5, 10, 11, 17, 18], 'Blight, Ascochyta': [4, 10, 11, 18], 'Blight, Cercospora': [4, 5, 10, 17, 18], 'Blight, Helminthosporium Leaf': [4, 5, 10, 11, 12, 17, 18], 'Blight, Mycosphaerella': [4, 11, 18], 'Blight, Northern Corn Leaf': [4, 5, 10, 11, 12, 17, 18], 'Blight, Pod': [4, 10, 15, 17, 18], 'Blight, Rhizoctonia Aerial': [4, 5, 10, 17, 18], 'Blight, Southern Corn Leaf': [4, 5, 10, 11, 12, 17, 18], 'Blight, Stem': [4, 10, 15, 17, 18], 'Blotch, Septoria': [4, 5, 18], 'Blotch, Stagonospora': [4, 5, 10, 12, 18], 'Canker, Rhizoctonia Stem': [4, 6, 10], 'Mold, Gray': [4, 6, 7, 11, 14, 15, 16, 18], 'Mold, White': [4, 5, 7, 10, 11, 13, 15, 16, 18, 29, 31, 32], 'Pasmo': [4], 'Rot, Sclerotinia Stem': [4, 5, 7, 10, 11, 15, 16, 18], 'Rust, Asian Soybean': [4, 5, 10, 11, 15, 17, 18], 'Spot, Ascochyta Leaf': [4, 7, 18], 'Spot, Ascochyta Pod': [4, 18], 'Spot, Brown': [4, 5, 7, 10, 11, 14, 15, 17, 18], 'Spot, Cercospora Leaf': [4, 6, 7, 10, 11, 15], 'Spot, Eye': [4, 5, 10, 11, 12, 17, 18], 'Spot, Frogeye Leaf': [4, 5, 10, 11, 17, 18], 'Spot, Gray Leaf': [4, 5, 6, 7, 10, 11, 12, 17, 18], 'Spot, Northern Corn Leaf': [4, 5, 10, 11, 12, 17, 18], 'Spot, Physoderma Brown': [4, 5, 18], 'Spot, Tar': [4, 5], 'Spot, Target': [4, 7, 10, 11, 14, 15, 16, 32], 'Blight, Pod and Stem': [5], 'Blast, Rice': [6], 'Blight, Botryosphaeria Shoot': [6, 7], 'Blight, Early': [6, 7, 9, 14, 15, 16, 31], 'Blight, Late': [6, 7, 9, 15, 16], 'Blight, Phomopsis Leaf': [6, 7], 'Blight, Plectosporium': [6], 'Blight, Sheath': [6, 15, 17], 'Blotch, Sooty': [6, 7, 15, 16], 'Flyspeck': [6, 7, 15, 16], 'Fruit Drop, Post-Bloom': [6, 7, 15, 16], 'Melanose': [6, 7, 15, 16], 'Rot, Bitter': [6, 7, 15, 16], 'Rot, Black': [6, 7, 15, 16], 'Rot, Botrytis Bunch': [6, 7], 'Rot, Phomopsis Soft': [6], 'Rot, Rhizoctonia Crown': [6], 'Rot, White': [6, 7, 16], 'Rust, Cedar Apple': [6, 7, 15, 16], 'Scab': [6, 7, 8, 14, 15], 'Shot Hole': [6, 7, 14, 15, 16], 'Spot, Cherry Leaf': [6, 7, 15], 'Spot, Greasy': [6, 7, 15, 16], 'Spot, Leaf': [6, 7, 15], 'Spot, Phomopsis Cane': [6, 7], 'Spot, Phomopsis Leaf': [6, 7], 'Spot, Ramularia Leaf': [6, 7], 'Spot, Septoria Leaf': [6, 7, 10, 11, 30], 'Spot, Stemphylium Purple': [6], 'Black Dot': [7, 15], 'Blight, Alternaria': [7, 14], 'Blight, Botrytis': [7, 10, 11, 14, 15, 16], 'Blight, Botrytis Leaf': [7, 14, 15, 16], 'Blight, Botrytis Shoot': [7], 'Blight, Gummy Stem': [7, 10, 11, 15], 'Blight, Monilinia': [7, 10, 11], 'Blight, Phomopsis': [7], 'Blight, Southern': [7, 8, 10, 11, 13, 15], 'Blight, Stemphylium Leaf': [7], 'Blotch, Cladosporium Leaf': [7], 'Blotch, Septoria Glume': [7, 12], 'Blotch, Septoria Leaf': [7, 10, 12, 17], 'Early Dying': [7, 31], 'Leaf Curl, Peach': [7], 'Lettuce Drop': [7, 29], 'Mold, Black': [7], 'Mold, Botrytis Gray': [7], 'Mummy Berry': [7, 16], 'Nematode': [7, 11, 22, 25, 26, 29, 30, 31, 32], 'Rot, Alternaria': [7], 'Rot, Aspergillus': [7, 10], 'Rot, Belly': [7], 'Rot, Botrytis Neck': [7, 15, 16], 'Rot, Cottony': [7], 'Rot, Fruit': [7, 10, 15], 'Rot, Green Fruit': [7, 14], 'Rot, Hull': [7], 'Rot, Jacket': [7, 14], 'Rot, Monilinia Brown': [7], 'Rot, Penicillium': [7, 14], 'Rot, Phomopsis Fruit': [7], 'Rot, Rhizoctonia Bottom': [7], 'Rot, Rhizopus Fruit': [7], 'Rot, Ripe Fruit': [7], 'Rot, Sclerotinia Head': [7], 'Rot, Sour': [7, 15, 16], 'Rot, Stemphylium Stalk': [7], 'Rust, Quince': [7], 'Scurf, Silver': [7], 'Spot, Alternaria Black': [7, 11], 'Spot, Alternaria Fruit': [7], 'Spot, Botrytis Leaf': [7, 14], 'Spot, Brooks Fruit': [7], 'Spot, Brown Leaf': [7], 'Spot, Citrus Black': [7], 'Spot, Ring': [7], 'Spot, Rusty': [7, 15], 'Spot, Septoria': [7], 'Wilt, Sclerotinia': [7], 'Wilt, Verticillium': [7, 8, 15, 25, 31], 'Clubroot': [8, 15], 'Colletotrichum': [8, 15], 'Fusarium': [8, 10, 15, 29, 32], 'Phytophthora': [8, 15], 'Pythium': [8, 15], 'Rhizoctonia': [8, 11, 15], 'Sclerotinia': [8, 15, 16], 'Sclerotium Rolfsii': [8, 15], 'Verticillium': [8, 15], 'Damping Off, Phytophthora': [9], 'Disease, Pythium Seedling': [9], 'Rot, Pod': [9], 'Rot, Pythium Root': [9], 'Blackleg': [10], 'Blight, Fusarium': [10, 11], 'Blight, Fusarium Head': [10, 12], 'Blight, Head': [10], 'Blight, Phomopsis Twig': [10], 'Blight, Rhizoctonia Foliar': [10], 'Blotch, Speckled': [10], 'Canker, Pitch': [10], 'Damping Off': [10], 'Rot, Cylindrocladium Black': [10, 11, 13, 15], 'Rot, Gibberella Ear': [10], 'Rot, Rhizoctonia': [10, 11], 'Rot, Rhizoctonia Limb': [10, 11, 13], 'Rot, Rhizoctonia Root': [10], 'Rot, Rhizoctonia Stalk': [10], 'Rot, Sclerotinia': [10], 'Rot, Southern Stem': [10, 11, 13], 'Rust, Fusiform': [10], 'Rust, Leaf': [10, 11, 13, 15], 'Rust, White Pine Blister': [10, 11], 'Scab, Head': [10], 'Spot, Chlorotic Leaf': [10], 'Spot, Phoma Leaf': [10], 'Spot, Valdensinia Leaf': [10, 11], 'Spot, Yellow Leaf': [10], 'Wilt, Fusarium': [10, 11, 30], 'Blight, Phomopsis Stem': [11], 'Blight, Sclerotinia': [11], 'Rot, Charcoal': [11, 30], 'Rot, Rhizoctonia Peg': [11, 13], 'Rot, Rhizoctonia Pod': [11, 13], 'Rot, Sclerotium': [11, 13], 'Spot, Corynespora Leaf': [11], 'Scorch, Leaf': [13], 'Spot, Pepper': [13], 'Rot, Brown Fruit': [14, 15, 16], 'Rot, Neck': [14], 'Aphanomyces': [15], 'Aspergillus': [15], 'Bacterial Pustule': [15], 'Bakanae Disease': [15], 'Black Shank': [15], 'Black Stem, Spring': [15], 'Blast': [15], 'Blast, Bacterial': [15], 'Blight, Bacterial': [15], 'Blight, Northern Leaf': [15], 'Blight, Southern Leaf': [15], 'Blight, Walnut': [15], 'Blight, Xanthomonas': [15], 'Blotch, Bacterial Fruit': [15], 'Botrytis': [15, 16], 'Canker, Bacterial': [15, 16], 'Disease, Coffee Berry': [15], 'Erwinia': [15], 'Eutypa': [15], 'Gumming Disease': [15], 'Head Drop, Sclerotinia': [15, 16], 'Leaf Drop, Sclerotinia': [15, 16], 'Macrophomina': [15], 'Mold, Sooty': [15], 'Monosporascus cannonballus': [15], 'Oak Root Fungus': [15], 'Olive Knot': [15], 'Phomopsis': [15, 16], 'Pink Root': [15, 29], 'Ramularia': [15], 'Rot, Aerial Stem': [15, 16], 'Rot, Armillaria Root': [15], 'Rot, Bacterial': [15], 'Rot, Black Crown': [15, 16], 'Rot, Black Root': [15], 'Rot, Bot': [15, 16], 'Rot, Botrytis Fruit': [15, 16], 'Rot, Brown': [15, 16], 'Rot, Buckeye': [15, 16], 'Rot, Bulls-Eye': [15, 16], 'Rot, Pin': [15], 'Rot, Pink': [15, 16], 'Rot, Stem': [15, 17], 'Rust, Common': [15], 'Scab, Common Seedborne': [15], 'Sclerotinia Sclerotiorum': [15], 'Sigatoka': [15], 'Smut': [15], 'Speck, Bacterial': [15, 16], 'Spot, Alternaria': [15, 16], 'Spot, Angular Leaf': [15, 16], 'Spot, Bacterial Leaf': [15, 16], 'Spot, Brooks': [15, 16], 'Spot, Common Leaf': [15], 'Spot, Sheath': [15, 17], 'Spot, Xanthomonas Leaf': [15], 'Streak, Bacterial': [15], 'Streak, Bacterial Leaf': [15], 'Wilt, Bacterial': [15, 22], 'Monilinia': [16], 'Blast, Leaf': [17], 'Blast, Neck': [17], 'Blight, Septoria Leaf': [17], 'Blight, Yellow Leaf': [17], 'Blotch, Brown': [17], 'Rot, Black Sheath': [17], 'Rust, Crown': [17], 'Smut, False': [17], 'Smut, Kernel': [17], 'Smut, Leaf': [17], 'Spot, Aggregate Sheath': [17], 'Spot, Narrow Brown Leaf': [17], 'NA': [19, 20, 21], 'Adelgid': [22, 23, 25, 26], 'Aphid': [22, 23, 24, 25, 26, 28, 32], 'Aphid, Black Peach': [22], 'Aphid, Black Pecan': [22, 24], 'Aphid, Cotton': [22, 23, 24, 32], 'Aphid, Woolly Apple': [22, 25, 26, 28], 'Bean Common Mosaic Virus': [22], 'Bean Golden Mosaic Virus': [22], 'Beet Curly Top Hybrigeminivirus': [22], 'Beetle Larva, Asiatic Garden': [22], 'Beetle Larva, Japanese': [22], 'Beetle Larva, Oriental': [22], 'Beetle, Bean Leaf': [22, 23, 24], 'Beetle, Colorado Potato': [22, 23, 24, 28], 'Beetle, Cottonwood Leaf': [22], 'Beetle, Cucumber': [22, 23, 24], 'Beetle, Flea': [22, 23, 24], 'Beetle, Green June': [22, 24], 'Beetle, Japanese': [22, 23, 24], 'Beetle, Multicolored Asian Lady': [22], 'Bollworm': [22], 'Borer, Banana Corm': [22], 'Borer, Rednecked Cane': [22], 'Budworm': [22, 23], 'Chafer Larva, European': [22], 'Chafer Larva, Masked': [22], 'Chafer, Rose': [22, 24], 'Citrus Tristeza Virus': [22], 'Citrus Yellows': [22], 'Complex, Root Weevil Larva': [22, 24], 'Complex, White Grub': [22], 'Cricket, Mole': [22], 'Curculio, Plum': [22, 23, 24], 'Cutworm': [22, 23, 24], 'Disease, Pierces': [22], 'Fleahopper, Cotton': [22, 23], 'Fly, Black': [22, 24], 'Fly, Cherry Fruit': [22, 23, 24, 25, 26], 'Grub, Root': [22], 'Grub, White': [22, 23], 'Lace Bug, Avocado': [22], 'Leaf Silvering': [22], 'Leafhopper': [22, 23, 24, 25, 26, 28, 32], 'Leafminer': [22, 23, 24, 25, 26], 'Leafminer, Citrus': [22, 25, 26, 28], 'Lygus Bug': [22, 23, 24], 'Maggot, Apple': [22, 23, 24], 'Maggot, Blueberry': [22, 25, 26, 28], 'Mealybug': [22, 24, 25, 26], 'Midge, Swede': [22, 25, 26], 'Nematode, Citrus': [22], 'Net Necrosis': [22], 'Phylloxera': [22, 24, 25, 26], 'Phylloxerina popularia': [22], 'Plant Bug': [22, 24, 32], 'Planthopper': [22], 'Potato Leaf Roll Virus': [22, 25], 'Potato Yellows': [22], 'Psylla, Asian Citrus': [22], 'Psylla, Pear': [22, 25, 26, 28], 'Psylla, Potato': [22, 27], 'Rootworm': [22], 'Sawfly': [22], 'Scale': [22, 24, 25, 26], 'Scale, European Fruit Lecanium': [22, 25, 26], 'Scale, San Jose': [22, 24, 25, 26, 28], 'Sharpshooter': [22, 24, 28], 'Skeletonizer, Grapeleaf': [22, 23], 'Spittlebug': [22, 23, 24], 'Spot, Bacterial Citrus': [22], 'Stinkbug': [22, 23, 24], 'Stinkbug, Green': [22], 'Stinkbug, Southern Green': [22], 'Termite': [22], 'Thrips': [22, 23, 25, 28, 32], 'Thrips, Foliage-Feeding': [22, 24], 'Thrips, Foliage-Feeding Citrus': [22], 'Tomato Mottle Virus': [22], 'Tomato Spotted Wilt Virus': [22], 'Tomato Yellow Leaf Curl Virus': [22, 28], 'Weevil, Black Vine': [22], 'Weevil, Pepper': [22, 23, 24], 'Western Yellows': [22], 'Whitefly': [22, 23, 24, 25, 26, 27, 28, 32], 'Whitefly, Banded Wing': [22], 'Wireworm': [22, 23, 25, 26], 'Ant': [23, 24], 'Aphid, Bird Cherry-Oat': [23], 'Aphid, Black Cherry': [23], 'Aphid, Blue Pea': [23], 'Aphid, Cowpea': [23], 'Aphid, English Grain': [23], 'Aphid, Hop': [23, 24, 25, 26], 'Aphid, Pea': [23], 'Aphid, Potato': [23], 'Aphid, Russian Wheat': [23], 'Aphid, Soybean': [23], 'Appleworm, Lesser': [23, 24], 'Armyworm': [23, 24], 'Armyworm, Beet': [23, 24], 'Armyworm, Fall': [23], 'Armyworm, Southern': [23, 24], 'Armyworm, True': [23], 'Armyworm, Western Yellowstriped': [23, 24], 'Armyworm, Yellowstriped': [23], 'Bagworm': [23], 'Beetle, Blister': [23], 'Beetle, Cabbage Flea': [23], 'Beetle, Cereal Leaf': [23], 'Beetle, Click': [23], 'Beetle, Fuller Rose': [23, 24], 'Beetle, Grape Bud': [23, 24], 'Beetle, Grape Colaspis': [23], 'Beetle, Grape Flea': [23, 24], 'Beetle, Hop Flea': [23, 24], 'Beetle, June': [23, 24], 'Beetle, Mexican Bean': [23, 24], 'Beetle, Palestriped Flea': [23], 'Beetle, Pine Shoot': [23], 'Beetle, Southern Corn Leaf': [23], 'Beetle, Sunflower': [23], 'Beetle, Whitefringed': [23], 'Bollworm Egg, Cotton': [23], 'Bollworm, Cotton': [23, 24], 'Bollworm, Pink': [23, 24], 'Borer, American Plum': [23, 24], 'Borer, European Corn': [23, 24], 'Borer, Lesser Cornstalk': [23], 'Borer, Lesser Peach Tree': [23, 24], 'Borer, Peach Twig': [23, 24], 'Borer, Rice Stalk': [23], 'Borer, Southwestern Corn': [23], 'Borer, Stalk': [23], 'Borer, Sugarcane': [23], 'Budworm Egg, Tobacco': [23], 'Budworm, Tobacco': [23], 'Bug, Leaffooted': [23, 24], 'Cabbageworm, Imported': [23, 24], 'Cabbageworm, Southern': [23, 24], 'Casebearer, Pecan Nut': [23, 24], 'Caterpillar, Alfalfa': [23], 'Caterpillar, Black Woolly Bear': [23], 'Caterpillar, Saltmarsh': [23, 24], 'Caterpillar, Velvet Bean': [23, 24], 'Caterpillar, Woolly Bear': [23, 24], 'Chafer, Masked': [23], 'Chinch Bug': [23], 'Chinch Bug, False': [23], 'Cicada, Periodical': [23, 24], 'Cloverworm, Green': [23, 24], 'Complex, Root Weevil': [23, 24], 'Corn Earworm': [23, 24], 'Cricket': [23], 'Curculio, Cowpea': [23, 24], 'Cutworm, Army': [23], 'Cutworm, Black': [23], 'Cutworm, Climbing': [23, 24], 'Cutworm, Foliar-Feeding': [23, 24], 'Cutworm, Granulate': [23], 'Cutworm, Pale Western': [23], 'Cutworm, Sandhill': [23], 'Cutworm, Variegated': [23, 24], 'Cutworm, Western Bean': [23], 'Drosophila, Spotted Wing': [23, 24, 25, 26], 'Earwig': [23, 24], 'Earwig, Common': [23, 24], 'Filbertworm': [23, 24], 'Fly, Corn Silk': [23], 'Fly, Hessian': [23], 'Fly, Walnut Husk': [23, 24], 'Fly, Western Cherry Fruit': [23, 24], 'Fruitworm, Green': [23, 24], 'Fruitworm, Tomato': [23, 24], 'Gallmaker, Grape Cane': [23, 24], 'Grasshopper': [23, 24], 'Headworm, Sorghum': [23], 'Hornworm, Tomato': [23, 24], 'Katydid': [23, 24], 'Leaffolder, Grape': [23, 24], 'Leafhopper, Aster': [23], 'Leafhopper, Grape': [23], 'Leafhopper, Potato': [23, 24], 'Leafhopper, Southern Garden': [23, 24], 'Leafhopper, Variegated': [23], 'Leafhopper, White Apple': [23, 25, 26], 'Leafminer, Blotch': [23], 'Leafminer, Cotton': [23], 'Leafminer, Spotted Tentiform': [23, 24], 'Leafminer, Western Tentiform': [23, 24], 'Leafperforator, Cotton': [23, 24], 'Leafroller, Apple': [23, 24], 'Leafroller, Grape': [23, 24], 'Leafroller, Oblique-Banded': [23, 24], 'Leafroller, Omnivorous': [23, 24], 'Leafroller, Pandemis': [23, 24], 'Leafroller, Red-Banded': [23, 24], 'Leafroller, Variegated': [23, 24], 'Leaftier, Celery': [23], 'Leafworm, Cotton': [23, 24], 'Looper': [23], 'Looper, Alfalfa': [23, 24], 'Looper, Cabbage': [23, 24], 'Looper, Hop': [23, 24], 'Looper, Soybean': [23], 'Maggot, Cabbage': [23, 24], 'Maggot, Seedcorn': [23, 24], 'Mealybug, Grape': [23], 'Melonworm': [23], 'Midge': [23], 'Midge, Sorghum': [23], 'Midge, Sunflower': [23], 'Moth Larva, Diamondback': [23], 'Moth Larva, Gypsy': [23], 'Moth Larva, Tussock': [23], 'Moth, Banded Sunflower': [23], 'Moth, Codling': [23, 24, 25, 26], 'Moth, Ermine': [23, 24], 'Moth, Grape Berry': [23, 24], 'Moth, Oriental Fruit': [23, 24], 'Moth, Pine Shoot': [23], 'Moth, Pine Tip': [23], 'Moth, Sunflower': [23], 'Moth, Sunflower Bud': [23], 'Moth, Tufted Apple Bud': [23, 24], 'Navel Orangeworm': [23, 24], 'Peanutworm, Rednecked': [23, 24], 'Pickleworm': [23], 'Pinworm, Tomato': [23, 24], 'Plant Bug, Alfalfa': [23], 'Plant Bug, Hop': [23], 'Plant Bug, Tarnished': [23, 24, 28], 'Psyllid, Asian Citrus': [23, 24, 25, 26, 28], 'Psyllid, Potato': [23, 24, 27, 28], 'Rindworm': [23], 'Rootworm, Corn': [23, 24], 'Sawfly Larva': [23], 'Sawfly, European Apple': [23, 24], 'Sawfly, Grass': [23], 'Sawfly, Pear': [23, 24], 'Scale Crawler': [23], 'Scale Crawler, San Jose': [23, 24], 'Sharpshooter, Glassy-Winged': [23, 24], 'Shuckworm, Hickory': [23, 24], 'Skeletonizer, Western Grapeleaf': [23, 24], 'Skipper, Silver-Spotted': [23, 24], 'Slug, Pear': [23, 24], 'Spider': [23, 24], 'Spittlebug, Meadow': [23, 24], 'Spittlebug, Two-Lined': [23], 'Stinkbug, Brown Marmorated': [23, 24], 'Symphylan, Garden': [23, 24], 'Threecornered Alfalfa Hopper': [23, 24, 28], 'Thrips, Citrus': [23, 25, 26, 28], 'Thrips, Grass': [23], 'Tortrix, Orange': [23, 24], 'Tuberworm, Potato': [23, 24], 'Webber, Bean Leaf': [23, 24], 'Webworm': [23, 24], 'Webworm, Alfalfa': [23], 'Webworm, Cabbage': [23, 24], 'Webworm, Garden': [23, 24], 'Webworm, Sorghum': [23], 'Weevil': [23], 'Weevil, Alfalfa': [23], 'Weevil, Boll': [23, 24], 'Weevil, Carrot': [23, 24], 'Weevil, Egyptian Alfalfa': [23], 'Weevil, Head-Clipper': [23], 'Weevil, Pea': [23, 24], 'Weevil, Pea Leaf': [23], 'Weevil, Pecan': [23, 24], 'Weevil, Sugarcane Rootstock': [23], 'Weevil, Sunflower Seed': [23], 'Weevil, Sunflower Stem': [23], 'Weevil, Sweet Potato': [23, 24], 'Weevil, Vegetable': [23, 24], 'Beetle Larva, Fuller Rose': [24], 'Beetle, Leaf': [24], 'Borer, Dectes Stem': [24], 'Borer, Stem': [24], 'Fleahopper': [24, 28], 'Leafminer, Dipterous': [24], 'Mealybug Crawler': [24], 'Podworm': [24], 'Skeletonizer, Leaf': [24], 'Stink Bug': [24], 'Thrips, Chilli': [24, 28], 'Thrips, Palm': [24], 'Whitefly, Sweetpotato': [24, 27], 'Aphid, Bean': [25, 26], 'Aphid, Root': [25, 26], 'Corky Ringspot Virus': [25], 'Disease, Zebra Chip': [25], 'Gallmaker, Grape Tumid': [25, 26], 'Leafminer, Microlepidoptera': [25, 26], 'Maggot, Root': [25, 26], 'Midge, Apple Gall': [25, 26], 'Midge, Gall': [25], 'Midge, Pear Leaf': [25, 26], 'Mite, Apple Rust': [25, 26], 'Mite, Avocado Brown': [25, 26], 'Mite, Broad': [25, 26, 27], 'Mite, Citrus Bud': [25, 26], 'Mite, Citrus Red': [25, 26], 'Mite, Citrus Rust': [25, 26], 'Mite, European Red': [25, 26], 'Mite, Leaf Edge Roller Papaya': [25, 26], 'Mite, Pear Rust': [25, 26], 'Mite, Persea': [25, 26], 'Mite, Pink Citrus Rust': [25, 26], 'Mite, Silver': [25, 26], 'Mite, Texas Citrus': [25, 26], 'Mite, Tomato Russet': [25, 26, 27], 'Moth, Diamondback': [25, 26], 'Nematode, Sugar Beet Cyst': [25, 26], 'Potato Virus YPsylla': [25], 'Psyllid': [25, 26, 28], 'Scale, Black': [25, 26], 'Scale, Brown': [25, 26], 'Scale, California Red': [25, 26], 'Scale, Citricola': [25, 26, 28], 'Scale, Citrus Snow': [25, 26], 'Scale, Cottony Cushion': [25, 26], 'Scale, Florida Red': [25, 26], 'Scale, Green': [25, 26], 'Scale, Olive': [25, 26], 'Scale, Purple': [25, 26], 'Scale, Walnut': [25, 26], 'Scale, White Peach': [25, 26], 'Spider Mite, Pacific': [25, 26, 27], 'Spider Mite, Two-Spotted': [25, 26, 27], 'Spider Mite, Willamette': [25, 26], 'Thrips Nymph, Onion': [25, 26], 'Thrips, Avocado': [25, 26, 28], 'Thrips, Melon': [25], 'Thrips, Onion': [25], 'Thrips, Western Flower': [25], 'Tipworm, Cranberry': [25, 26], 'Midge, Blueberry Gall': [26], 'Spider Mite, False': [26], 'Thrips Nymph': [26], 'Thrips Nymph, Melon': [26], 'Thrips Nymph, Western Flower': [26], 'Weevil, Diaprepes Root': [26], 'Mite, Banks Grass': [27], 'Psylla, Tomato': [27], 'Psyllid, Tomato': [27], 'Spider Mite, Carmine': [27], 'Spider Mite, Desert': [27], 'Spider Mite, Strawberry': [27], 'Whitefly, Greenhouse': [27], 'Whitefly, Silverleaf': [27], 'Aphid, Green Peach': [28], 'Aphid, Sugarcane': [28], 'Bug, Squash': [28], 'Cucurbit Yellow Stunting Disorder Virus': [28], 'Katydid Nymph': [28], 'Lygus': [28], 'Mealybug, Citrus': [28], 'Mealybug, Vine': [28], 'Plant Bug, Western': [28], 'Scale, Barnacle': [28], 'Scale, Frosted': [28], 'Scale, Oystershell': [28], 'Thrips, Blueberry': [28], 'Wasp, Blueberry Stem Gall': [28], 'Rot, Aspergillus Crown': [29], 'Nematode, Root-Knot': [30], 'Amaranth, Palmer': [33, 34, 35, 38, 40, 49, 50, 51, 52, 54, 55, 56, 58, 59, 60], 'Artichoke, Jerusalem': [33, 34, 39, 40, 41, 42, 50, 51, 52, 55, 56], 'Barnyardgrass': [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 47, 48, 49, 51, 55, 57, 58, 59, 60, 61], 'Bedstraw, Catchweed': [33, 37, 43, 48, 50, 51, 52, 55, 56], 'Bindweed, Field': [33, 34, 39, 40, 41, 42, 50, 51, 52, 55, 56], 'Bittercress, Smallflowered': [33, 34, 50, 51, 52], 'Blackgrass': [33, 34, 45, 61], 'Buckwheat, Wild': [33, 34, 37, 38, 39, 40, 41, 42, 46, 47, 48, 49, 50, 51, 52, 54, 55, 56, 59], 'Canarygrass, Hood': [33, 34, 45, 46, 61], 'Canarygrass, Littleseed': [33, 34, 45, 46, 51], 'Canola, Volunteer': [33, 34, 37, 43, 45, 48, 50, 51, 52, 62], 'Catchfly, Cone': [33, 34, 50, 51, 52], 'Catchfly, Conical': [33, 34, 50, 51, 52], 'Catchfly, Nightflowering': [33, 34, 50, 51, 52, 55, 56], 'Chamomile, False': [33, 34, 50, 51, 52], 'Chamomile, Mayweed': [33, 34, 50, 52, 61], 'Chickweed, Common': [33, 34, 37, 38, 43, 45, 47, 48, 49, 50, 51, 52, 54, 55, 56, 58, 59, 60, 61, 62], 'Cleaver': [33], 'Cleavers': [33, 34, 50, 51, 52], 'Cockle, Cow': [33, 34, 50, 51, 52, 55, 56], 'Cockle, White': [33, 34, 50, 51, 52, 55, 56], 'Cocklebur, Common': [33, 34, 35, 38, 49, 50, 51, 52, 54, 55, 56, 59, 61], 'Corn, Volunteer': [33, 34, 39, 40, 41, 42], 'Cupgrass, Woolly': [33, 34, 38, 40, 41, 42, 49, 55, 58, 59, 60, 61], 'Dandelion': [33, 34, 39, 40, 41, 42, 49, 50, 51, 52, 55, 56, 59, 61], 'Dandelion, Seedling': [33, 34, 50, 52, 54, 58, 60], 'Dock, Curly': [33, 34, 39, 40, 41, 42, 49, 50, 51, 52, 54, 55, 56, 59], 'Dogfennel': [33, 34, 41, 43, 50, 52, 56], 'Fiddleneck, Coast': [33, 34, 50, 52, 61], 'Fiddleneck, Tarweed': [33, 34, 50, 52, 61], 'Filaree, Redstem': [33, 34, 50, 52], 'Flax, Volunteer': [33, 34, 50, 51, 52], 'Flixweed': [33, 34, 46, 50, 51, 52, 55, 56], 'Foxtail, Green': [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 47, 48, 49, 51, 55, 58, 59, 60, 61], 'Foxtail, Yellow': [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 47, 48, 49, 51, 55, 58, 59, 60, 61], 'Gromwell, Corn': [33, 34, 50, 51, 52], 'Hawksbeard, Narrowleaf': [33, 34, 50, 51, 52], 'Hempnettle, Common': [33, 34, 50, 51, 52], 'Henbit': [33, 34, 35, 36, 38, 39, 40, 41, 42, 43, 45, 46, 49, 50, 51, 52, 55, 56, 57, 58, 59, 60, 61, 62], 'Horseweed': [33, 34, 38, 39, 40, 41, 42, 49, 50, 51, 52, 54, 55, 56, 59], 'Jacobs Ladder': [33, 34, 50, 52, 55, 56], 'Knotweed, Prostrate': [33, 34, 49, 50, 52, 54, 55, 56, 59], 'Kochia': [33, 34, 38, 39, 40, 41, 42, 47, 49, 50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 61], 'Lambsquarters, Common': [33, 34, 35, 37, 38, 42, 47, 48, 49, 50, 51, 52, 54, 55, 56, 58, 59, 60, 61], 'Lentil, Volunteer': [33, 34, 50, 52], 'Lettuce, Chinese': [33, 34, 50, 52], 'Lettuce, Prickly': [33, 34, 39, 40, 41, 42, 50, 51, 52, 55, 56, 61], 'Mallow, Common': [33, 34, 50, 51, 52, 55, 56], 'Marestail': [33, 34, 38, 39, 40, 41, 42, 49, 50, 51, 52, 54, 55, 56, 58, 59, 60, 61, 62], 'Marestail, Common': [33], 'Marshelder': [33, 34, 49, 50, 51, 52, 55], 'Millet, Foxtail': [33, 35, 36, 38], 'Millet, Proso': [33, 57], 'Millet, Volunteer Common Foxtail': [33, 34], 'Millet, Volunteer German Foxtail': [33, 34], 'Millet, Volunteer Hungarian Foxtail': [33, 34], 'Millet, Volunteer Proso': [33, 34], 'Millet, Volunteer Siberian Foxtail': [33, 34], 'Millet, Wild Proso': [33, 34, 38, 39, 40, 41, 42, 49, 55, 58, 59, 60, 61], 'Mustard, Birdsrape': [33, 34, 50, 51, 52], 'Mustard, Black': [33, 34, 43, 46, 50, 51, 52, 55, 56], 'Mustard, Blue': [33, 34, 39, 40, 41, 42, 43, 46, 50, 51, 52, 55, 56, 61, 62], 'Mustard, Jim Hill': [33, 34, 50, 51, 52], 'Mustard, Tansy': [33, 34, 39, 40, 41, 42, 43, 46, 50, 51, 52, 55, 56, 62], 'Mustard, Tumble': [33, 34, 39, 40, 41, 42, 43, 45, 46, 50, 51, 52, 55, 56, 61], 'Mustard, Wild': [33, 34, 35, 37, 38, 39, 40, 41, 42, 43, 45, 46, 48, 49, 50, 51, 52, 54, 55, 56, 58, 59, 60, 62], 'Nightshade, Cutleaf': [33, 34, 50, 51, 52, 55, 56], 'Nightshade, Eastern Black': [33, 34, 35, 49, 50, 51, 52, 54, 55, 58, 59, 60, 61], 'Nightshade, Hairy': [33, 34, 35, 36, 39, 40, 41, 42, 49, 50, 51, 52, 54, 55, 57, 58, 59, 60], 'Oat, Wild': [33, 34, 35, 36, 37, 39, 40, 41, 42, 43, 45, 46, 47, 48, 51, 57, 58, 59, 61], 'Pennycress, Field': [33, 34, 37, 39, 40, 41, 42, 43, 45, 46, 48, 50, 51, 52, 55, 56, 58, 60, 62], 'Pepperweed, Virginia': [33, 34, 40, 41, 42, 50, 51, 52, 55, 56, 58, 60], 'Pigweed, Palmer': [33, 34, 39, 41, 42, 50, 51, 52], 'Pigweed, Prostrate': [33, 34, 50, 51, 52, 55, 56, 58, 60], 'Pigweed, Redroot': [33, 34, 35, 37, 38, 42, 43, 45, 46, 47, 48, 49, 50, 51, 52, 54, 55, 56, 58, 59, 60, 62], 'Pineapple Weed': [33, 34, 50, 52, 55, 56], 'Radish, Wild': [33, 34, 43, 45, 50, 51, 52, 55, 56, 58, 60, 61, 62], 'Ragweed, Common': [33, 34, 35, 38, 39, 40, 41, 42, 49, 50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 61], 'Ragweed, Giant': [33, 34, 35, 38, 39, 40, 41, 42, 49, 50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 61], 'Rocket, London': [33, 34, 40, 41, 42, 43, 50, 51, 52, 55, 56], 'Sage, Lanceleaf': [33, 34, 50, 51, 52], 'Salsify, Western': [33, 34, 50, 51, 52], 'Sandbur, Field': [33, 34, 38, 39, 40, 41, 42, 49, 55, 57, 58, 59, 60, 61], 'Shepherdspurse': [33, 34, 37, 38, 39, 40, 41, 42, 43, 46, 47, 48, 49, 50, 51, 52, 55, 56, 58, 59, 60, 61, 62], 'Smartweed, Pale': [33, 34, 49, 50, 51, 52, 54, 59], 'Smartweed, Pennsylvania': [33, 34, 35, 37, 38, 40, 41, 42, 47, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 61], 'Soybean, Volunteer': [33, 34, 50, 51, 52], 'Storksbill': [33, 34, 50, 52], 'Sunflower, Annual': [33, 34, 50, 51, 52], 'Swinecress': [33, 34, 39, 40, 41, 42, 43, 50, 51, 52], 'Thistle, Annual Sow': [33, 34, 39, 40, 41, 42, 47, 50, 51, 52, 55, 56], 'Thistle, Canada': [33, 34, 38, 39, 40, 41, 42, 49, 50, 51, 52, 54, 55, 56, 59, 62], 'Thistle, Perennial Sow': [33, 34, 40, 41, 42, 50, 51, 52, 55, 56], 'Thistle, Russian': [33, 34, 37, 39, 40, 41, 42, 47, 48, 49, 50, 51, 52, 55, 56, 58, 59, 60], 'Thistle, Spiny Sow': [33, 34, 50, 51, 52, 55, 56], 'Turnip, Wild': [33, 34, 43, 46, 50, 51, 52], 'Velvetleaf': [33, 34, 38, 39, 40, 41, 42, 49, 50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 61], 'Wallflower, Bushy': [33, 34, 46, 50, 51, 52], 'Waterhemp, Tall': [33, 34, 35, 49, 50, 51, 52, 54, 55, 59, 60, 61], 'Windgrass': [33, 34, 45, 46, 61], 'Wormwood, Absinth': [33, 34, 50, 51, 52], 'Wormwood, Biennial, Seedling': [33, 34, 50, 52], 'Bedstraw': [34], 'Catchweed': [34], 'Amaranth, Spiny': [35, 49, 54, 55, 56, 59], 'Anoda, Spurred': [35, 40, 41, 42], 'Beggarweed, Florida': [35, 36, 38, 40, 41, 42, 55, 56, 57, 61], 'Carelessweed': [35, 36, 56], 'Carpetweed': [35, 36, 38, 39, 40, 41, 42, 49, 50, 52, 54, 55, 56, 58, 59, 60, 61], 'Citronmelon': [35], 'Copperleaf, Hophornbeam': [35, 40, 41, 42, 55, 56, 58, 60], 'Copperleaf, Virginia': [35, 40, 41, 42], 'Crabgrass': [35, 36, 38, 39, 40, 41, 42], 'Crotalaria, Showy': [35], 'Croton, Tropic': [35, 55, 56], 'Crowfootgrass': [35, 36, 38, 40, 41, 42], 'Cucumber, Volunteer': [35], 'Cupgrass, Prairie': [35, 36, 38], 'Cupgrass, Southwestern': [35, 38], 'Eclipta': [35, 40, 41, 42], 'Foxtail, Giant': [35, 36, 38, 39, 40, 41, 42, 49, 55, 58, 59, 60, 61], 'Foxtail, Robust Purple': [35, 36, 38, 58, 60], 'Foxtail, Robust White': [35, 36, 38, 58, 60], 'Galinsoga': [35, 36, 38, 49, 54, 55, 57, 58, 59, 60, 61], 'Goosegrass': [35, 36, 38, 40, 41, 42, 49, 55, 57, 58, 59, 60, 61], 'Grassbur': [35, 36], 'Ground Cherry, Cutleaf': [35, 36, 57], 'Horsenettle': [35, 39, 40, 41, 42, 54, 62], 'Jimsonweed': [35, 38, 40, 41, 42, 49, 54, 55, 56, 57, 58, 59, 60, 61], 'Johnsongrass, Seedling': [35, 36, 38, 39, 40, 41, 42, 44, 49, 55, 57, 58, 59, 60, 61], 'Ladysthumb': [35, 38, 47, 49, 55, 56, 59, 61], 'Lambsquarters': [35, 36, 39, 40, 41, 42, 57, 61], 'Mallow, Venice': [35, 38, 49, 50, 52, 55, 56, 58, 59, 60, 61], 'Mexicanweed': [35], 'Moonflower, Purple': [35], 'Morningglory': [35, 61], 'Morningglory, Common': [35], 'Morningglory, Cypressvine': [35], 'Morningglory, Entireleaf': [35, 54], 'Morningglory, Ivyleaf': [35, 38, 49, 50, 52, 54, 55, 56, 59], 'Morningglory, Palmleaf': [35], 'Morningglory, Pitted': [35, 49, 50, 52, 54, 55, 59], 'Morningglory, Red': [35], 'Morningglory, Scarlet': [35], 'Morningglory, Small White': [35], 'Morningglory, Smallflower': [35], 'Morningglory, Tall': [35, 38, 50, 52, 55, 56], 'Morningglory, Willow Leaf': [35], 'Nightshade, Black': [35, 36, 39, 40, 41, 42, 47, 49, 54, 55, 56, 57, 58, 59, 60], 'Panicum, Browntop': [35, 36, 38, 40, 41, 42, 57, 61], 'Panicum, Fall': [35, 36, 38, 39, 40, 41, 42, 44, 57, 58, 59, 60, 61], 'Panicum, Texas': [35, 36, 38, 39, 40, 41, 42, 49, 55, 57, 58, 59, 60, 61], 'Pigweed': [35, 36, 39, 40, 41, 42, 57, 61, 63], 'Pigweed, Smooth': [35, 38, 49, 54, 55, 56, 58, 59, 60], 'Poinsettia, Wild': [35, 38], 'Purslane': [35, 36, 39, 40, 41, 42, 57], 'Purslane, Common': [35, 38, 42, 47, 49, 54, 55, 56, 58, 59, 60, 61], 'Pusley, Florida': [35, 36, 38, 40, 41, 42, 49, 55, 56, 57, 59, 61], 'Rice, Red': [35, 36, 38, 39, 40, 41, 42, 57], 'Rocket, Yellow': [35, 39, 40, 41, 42, 55, 56], 'Sandbur': [35, 36], 'Sesbania, Hemp': [35, 39, 40, 41, 42, 49, 50, 52, 54, 55, 56, 58, 59], 'Shattercane': [35, 36, 38, 39, 40, 41, 42, 49, 55, 57, 58, 59, 60, 61], 'Sida, Prickly': [35, 36, 38, 39, 40, 41, 42, 49, 55, 56, 57, 58, 59, 61], 'Signalgrass, Broadleaf': [35, 36, 38, 39, 40, 41, 42, 44, 49, 54, 55, 57, 58, 59, 60, 61], 'Smartweed': [35, 36, 57], 'Sprangletop, Red': [35, 36, 38, 57], 'Starbur, Bristly': [35, 36, 55, 56], 'Teaweed': [35, 36, 39, 40, 41, 42, 49, 55, 56, 57, 59], 'Waterhemp, Common': [35, 49, 50, 52, 54, 55, 58, 59, 60, 61], 'Watermelon, Wild': [35], 'Wheat, Volunteer': [35, 36, 39, 42, 47, 57], 'Wildcane': [35, 36, 57], 'Witchgrass': [35, 36, 38, 39, 40, 41, 42, 50, 52, 57, 58, 60, 61], 'Witchweed': [35], 'Waterhemp': [36, 38, 39, 40, 41, 42, 49, 55, 56, 57, 61], 'Brome, Japanese': [37, 39, 40, 41, 42, 43, 45, 46, 48, 51], 'Darnel, Persian': [37, 43, 45, 48, 51], 'Hempnettle': [37, 48, 55, 56, 62], 'Clover, Red': [38, 39, 40, 41, 42, 43, 58, 60], 'Foxtail, Bristly': [38, 39, 40, 41, 42, 58, 60], 'Nightshade': [38, 61], 'Nutsedge, Yellow': [38, 39, 40, 41, 42, 47, 54, 57, 58, 59, 61], 'Puncturevine': [38, 47, 50, 52, 55, 56, 58], 'Sicklepod': [38, 39, 40, 41, 42, 49, 55, 56, 57, 58, 59, 61], 'Spurge, Nodding': [38], 'Spurge, Prostrate': [38, 39, 40, 41, 42, 55, 56], 'Spurge, Spotted': [38, 39, 40, 41, 42, 61], 'Sunflower, Common': [38, 49, 54, 55, 56, 57, 59, 61], 'Wormwood, Biennial': [38, 49, 51], 'Alder': [39, 40, 41, 42], 'Alfalfa': [39, 40, 41, 42, 55, 56, 62], 'Bahiagrass': [39, 40, 41, 42], 'Barley': [39, 40, 41, 42], 'Barley, Little': [39, 40, 41, 42, 43, 62], 'Bermudagrass': [39, 40, 41, 42], 'Bittercress': [39, 40, 41, 42], 'Bluegrass, Annual': [39, 40, 41, 42, 45, 47, 58, 60, 61, 62], 'Bluegrass, Bulbous': [39, 40, 41, 42, 45, 46], 'Bluegrass, Kentucky': [39, 40, 41, 42, 45], 'Blueweed, Texas': [39, 40, 41, 42, 55, 56], 'Brome, Downy': [39, 40, 41, 42, 43, 45, 46, 47, 61, 62], 'Brome, Smooth': [39, 40, 41, 42, 43], 'Burcucumber': [39, 40, 41, 42, 49, 50, 52, 54, 55, 56, 58, 59, 60, 62], 'Bursage, Woollyleaf': [39, 40, 41, 42, 55, 56], 'Buttercup': [39, 40, 41, 42, 62], 'Canarygrass, Reed': [39, 40, 41, 42], 'Cattail': [39, 40, 41, 42], 'Cheat': [39, 40, 41, 42, 43, 45, 46], 'Cheatgrass': [39, 42], 'Chickweed': [39, 40, 41, 42], 'Clover, White': [39, 40, 41, 42, 58, 60], 'Cocklebur': [39, 40, 41, 42, 58, 60], 'Coreopsis, Plains': [39, 40, 41, 42], 'Dandelion, Dwarf': [39, 40, 41, 42], 'Devilsclaw': [39, 40, 41, 42, 50, 52], 'Dogbane, Hemp': [39, 40, 41, 42, 55, 56], 'Eucalyptus': [39, 40, 41, 42], 'Falseflax, Smallseed': [39, 40, 41, 42, 46, 55, 56], 'Fescue': [39, 40, 41, 42], 'Fescue, Fine': [39, 41, 42], 'Fescue, Tall': [39, 40, 41, 42], 'Filaree': [39, 40, 41, 42], 'Fleabane, Annual': [39, 40, 41, 42, 55, 56], 'Fleabane, Hairy': [39, 40, 41, 42], 'Fleabane, Rough': [39, 40, 41, 42], 'Foxtail': [39, 42, 61], 'Foxtail, Carolina': [39, 40, 41, 42, 62], 'Goatgrass, Jointed': [39, 40, 41, 42, 45, 46], 'Ground Cherry': [39, 40, 41, 42, 61], 'Groundsel, Common': [39, 40, 41, 42, 50, 52], 'Hemlock, Poison': [39, 40, 41, 42, 62], 'Horseradish': [39, 40, 41, 42], 'Itchgrass': [39, 40, 41, 42], 'Johnsongrass': [39, 40, 41, 42], 'Junglerice': [39, 40, 41, 42, 49, 55, 59], 'Kikuyugrass': [39, 40, 41, 42], 'Knapweed': [39, 40, 41, 42], 'Knotweed': [39, 40, 41, 42], 'Madrone': [39, 41, 42], 'Milkweed, Common': [39, 40, 41, 42, 55, 56], 'Milo': [39, 41, 42], 'Morningglory, Annual': [39, 40, 41, 42, 57, 58, 60, 61], 'Mullein, Common': [39, 40, 41, 42], 'Napiergrass': [39, 40, 41, 42], 'Nightshade, Silverleaf': [39, 40, 41, 42, 55, 56], 'Nutsedge, Purple': [39, 40, 41, 42, 47], 'Oak': [39, 41, 42], 'Oat': [39, 40, 41, 42], 'Orchardgrass': [39, 40, 41, 42], 'Paragrass': [39, 40, 41, 42], 'Peppertree, Brazilian': [39, 40, 41, 42], 'Pine, Australian': [39], 'Pokeweed, Common': [39, 40, 41, 42, 49, 54, 59, 62], 'Potato, Wild Sweet': [39, 40, 41, 42], 'Quackgrass': [39, 40, 41, 42, 43, 45, 46], 'Reed, Giant': [39, 40, 41, 42], 'Rye, Cereal': [39, 40, 41, 42], 'Rye, Volunteer': [39, 40, 41, 42], 'Ryegrass': [39, 40, 41, 42], 'Saltcedar': [39, 40, 41, 42], 'Sandbur, Longspine': [39, 40, 41, 42], 'Sorghum, Grain': [39, 40, 41, 42], 'Speedwell, Purslane': [39, 40, 41, 42], 'Sprangletop': [39, 40, 41, 42, 44], 'Spurge, Leafy': [39, 40, 41, 42, 55, 56], 'Spurry, Umbrella': [39, 40, 41, 42], 'Stinkgrass': [39, 40, 41, 42], 'Sunflower': [39, 40, 41, 42, 61], 'Sweetgum': [39, 40, 41, 42], 'Tan Oak': [39, 41, 42], 'Thistle, Artichoke': [39, 40, 41, 42], 'Thistle, Yellow Star': [39, 40, 41, 42, 55, 56], 'Timothy': [39, 40, 41, 42], 'Torpedograss': [39, 40, 41, 42], 'Trumpet Creeper': [39, 40, 41, 42, 55, 56], 'Unicorn Plant': [39, 41, 42], 'Weed': [39, 42, 47, 57, 61], 'Wheat': [39, 40, 41, 42], 'Wheat, Overwintered': [39, 40, 41, 42], 'Wheatgrass, Crested': [39, 42], 'Wheatgrass, Tall': [39, 42], 'Wheatgrass, Western': [39, 40, 41, 42], 'Willow': [39, 40, 41, 42], 'Alligatorweed': [40, 41, 42], 'Ammannia, Purple': [40, 41, 42], 'Anise': [40, 41, 42], 'Ash': [40, 41, 42], 'Aspen, Quaking': [40, 41, 42], 'Bassia, Fivehook': [40, 41, 42], 'Bearclover': [40, 41, 42], 'Bearmat': [40, 41, 42], 'Beech': [40, 41, 42], 'Bentgrass': [40, 41, 42], 'Bermudagrass, Water': [40, 41, 42], 'Birch': [40, 41, 42], 'Black Gum': [40, 41, 42], 'Blackberry': [40, 41, 42], 'Bracken': [40, 41, 42], 'Broom, French': [40, 41, 42], 'Broom, Scotch': [40, 41, 42], 'Buckwheat, California': [40, 41, 42], 'Cascara': [40, 41, 42], 'Catsclaw': [40, 41, 42], 'Ceanothus': [40, 41, 42], 'Chamise': [40, 41, 42], 'Cherry, Bitter': [40, 41, 42], 'Cherry, Black': [40, 41, 42], 'Cherry, Pin': [40, 41, 42], 'Chervil': [40, 41, 42], 'Cogongrass': [40, 41, 42], 'Coyote Brush': [40, 41, 42], 'Dallisgrass': [40, 41, 42], 'Dandelion, False': [40, 41, 42], 'Dogwood': [40, 41, 42], 'Elderberry': [40, 41, 42], 'Elm': [40, 41, 42], 'Evening Primrose, Cutleaf': [40, 41, 42, 56], 'Fennel': [40, 41, 42], 'Fern, Bracken': [40, 41, 42, 55, 56], 'Fern, Sword': [40, 41, 42], 'Fiddleneck': [40, 41, 42], 'Geranium, Carolina': [40, 41, 42, 55, 56], 'Gorse': [40, 41, 42], 'Groundsel, Cressleaf': [40, 41, 42, 62], 'Guineagrass': [40, 41, 42], 'Hawthorn': [40, 41, 42], 'Hazardia': [40, 41, 42], 'Hazel': [40, 41, 42], 'Hickory': [40, 41, 42], 'Holly, Florida': [40, 41, 42], 'Honeysuckle': [40, 41, 42], 'Hornbeam, American': [40, 41, 42], 'Ice Plant': [40, 41, 42], 'Ivy, Poison': [40, 41, 42], 'Knotgrass': [40, 41, 42], 'Kudzu': [40, 41, 42], 'Lantana': [40, 41, 42], 'Lespedeza': [40, 41, 42], 'Locust, Black': [40, 41, 42], 'Madrone, Resprout': [40, 41, 42], 'Manna Grass, Eastern': [40, 41, 42], 'Manzanita': [40, 41, 42], 'Maple, Red': [40, 41, 42], 'Maple, Sugar': [40, 41, 42], 'Maple, Vine': [40, 41, 42], 'Mayweed': [40, 41, 42, 55, 56], 'Monkey-Flower': [40, 41, 42], 'Muhly, Wirestem': [40, 41, 42], 'Myrtle, Southern Wax': [40, 41, 42], 'Oak, Black': [40, 41, 42], 'Oak, Northern': [40, 41, 42], 'Oak, Poison': [40, 41, 42], 'Oak, Post': [40, 41, 42], 'Oak, Southern Red': [40, 41, 42], 'Oak, White': [40, 41, 42], 'Olive, Russian': [40, 41, 42], 'Pampasgrass': [40, 41, 42], 'Persimmon': [40, 41, 42], 'Phragmites': [40, 41, 42], 'Pine': [40, 41, 42], 'Poplar, Yellow': [40, 41, 42], 'Redbud, Eastern': [40, 41, 42], 'Redvine': [40, 41, 42, 55, 56], 'Rose, Multiflora': [40, 41, 42], 'Ryegrass, Perennial': [40, 41, 42], 'Sage, Black': [40, 41, 42], 'Sage, White': [40, 41, 42], 'Sagebrush, California': [40, 41, 42], 'Salmonberry': [40, 41, 42], 'Sassafras': [40, 41, 42], 'Smartweed, Ladysthumb': [40, 41, 42, 54, 58], 'Smartweed, Swamp': [40, 41, 42, 55, 56], 'Sourwood': [40, 41, 42], 'Spanish Needles': [40, 41, 42, 55, 56], 'Speedwell, Corn': [40, 41, 42, 58, 60], 'Sumac, Poison': [40, 41, 42], 'Sumac, Smooth': [40, 41, 42], 'Sumac, Winged': [40, 41, 42], 'Tallowtree, Chinese': [40, 41, 42], 'Tan Oak, Resprout': [40, 41, 42], 'Tassel': [40, 41, 42], 'Thimbleberry': [40, 41, 42], 'Tree Tobacco': [40, 41, 42], 'Vasey Grass': [40, 41, 42], 'Velvetgrass': [40, 41, 42, 47], 'Virginia Creeper': [40, 41, 42], 'Dodder': [41, 42], 'Milkweed': [41], 'Pine, Austrian': [41, 42], 'Seedhead': [41, 42], 'Banana Bunchy Top Virus': [42], 'Canola, Non-Glyphosate Tolerant': [42], 'Cheeseweed, Common': [42], 'Goatweed': [42], 'Groundsel': [42], 'Johnsongrass, Rhizome': [42], 'Malva': [42], 'Medusahead': [42], 'Nettle, Stinging': [42, 55, 56], 'Nutsedge': [42], 'Resprout': [42], 'Ryegrass, Common': [42], 'Tree': [42], 'Weed, Annual': [42, 61], 'Woody Brush': [42], 'Bachelor Button': [43, 56], 'Barley, Foxtail': [43, 46, 61], 'Beet, Wild': [43], 'Chickweed, Mouseear': [43, 46, 55, 56, 61, 62], 'Cornflower': [43, 55, 56], 'Speedwell, Ivyleaf': [43], 'Watergrass': [44], 'Bluegrass, Roughstalk': [45, 61], 'Brome, Ripgut': [45, 46, 61], 'Brome, Soft': [45, 61], 'Chess, Hairy': [45], 'Fescue, Rattail': [45, 46, 47, 61], 'Ryegrass, Annual': [45, 61], 'Ryegrass, Italian': [45, 61, 62], 'Ventenata': [45, 61], 'Brome': [46, 61], 'Buttercup, Bur': [46], 'Chess, Soft': [46, 47], 'Rapeseed, Volunteer': [46], 'Rescuegrass': [46], 'Wormseed': [46], 'Barley, Volunteer': [47], 'Barley, Volunteer (Preemergence)': [47], 'Barnyardgrass (Preemergence)': [47, 53, 54], 'Bluegrass, Annual (Preemergence)': [47], 'Brome, Downy (Preemergence)': [47], 'Buckwheat, Wild (Preemergence)': [47], 'Canarygrass': [47], 'Canarygrass (Preemergence)': [47], 'Chess, Soft (Preemergence)': [47], 'Chickweed, Common (Preemergence)': [47, 54], 'Crabgrass, Large': [47, 49, 54, 55, 58, 59, 60, 61], 'Crabgrass, Large (Preemergence)': [47, 54], 'Fescue, Rattail (Preemergence)': [47], 'Foxtail, Green (Preemergence)': [47, 53, 54], 'Foxtail, Yellow (Preemergence)': [47, 53, 54], 'Knotweed, Prostrate (Preemergence)': [47], 'Ladysthumb (Preemergence)': [47], 'Lambsquarters, Common (Preemergence)': [47, 54], 'Manna Grass': [47], 'Manna Grass (Preemergence)': [47], 'Nutsedge, Purple (Preemergence)': [47], 'Nutsedge, Yellow (Preemergence)': [47, 53, 54], 'Oat, Wild (Preemergence)': [47, 53, 54], 'Pigeongrass': [47], 'Pigeongrass (Preemergence)': [47], 'Pigweed, Redroot (Preemergence)': [47, 54], 'Potato, Volunteer': [47, 49, 54, 55, 59], 'Potato, Volunteer (Preemergence)': [47], 'Puncturevine (Preemergence)': [47], 'Purslane, Common (Preemergence)': [47, 54], 'Shepherdspurse (Preemergence)': [47, 54], 'Smartweed, Pale (Preemergence)': [47, 54], 'Smartweed, Pennsylvania (Preemergence)': [47, 53, 54], 'Thistle, Annual Sow (Preemergence)': [47, 54], 'Thistle, Russian (Preemergence)': [47], 'Velvetgrass (Preemergence)': [47], 'Vetch, Common': [47], 'Vetch, Common (Preemergence)': [47, 54], 'Wheat, Volunteer (Preemergence)': [47, 53, 54], 'Amaranth, Powell': [49, 54, 55, 56, 59], 'Buffalobur': [49, 50, 52, 54, 55, 56, 58, 59, 60], 'Crabgrass, Smooth': [49, 55, 58, 59, 60, 61], 'Deadnettle, Purple': [49, 55, 58, 59, 60, 62], 'Hemp': [49, 54, 55, 59], 'Lovegrass, Tufted': [49], 'Morningglory, Cotton': [49, 55, 59], 'Sorghum, Volunteer': [49, 55, 59], 'Tumbleweed, Amaranth': [49, 55, 59], 'Chickpea, Volunteer': [50, 52], 'Cotton, Volunteer': [50, 52], 'Fluvellin, Sharppoint': [50], 'Fumitory': [50, 52, 55, 56], 'Melon, Smell': [50, 52, 59], 'Pea, Volunteer': [50, 52], 'Pigweed, Tumble': [50, 52, 54, 55, 56, 58], 'Purslane, Horse': [50, 52], 'Vetch, Hairy': [50, 52], 'Fluellin, Sharp-Leaved': [52], 'Beggarweed, Florida (Preemergence)': [53, 54], 'Buttonweed (Preemergence)': [53], 'Carelessweed (Preemergence)': [53], 'Carpetweed (Preemergence)': [53, 54], 'Cocklebur (Preemergence)': [53], 'Crabgrass (Preemergence)': [53], 'Cupgrass, Woolly (Preemergence)': [53, 54], 'Foxtail, Giant (Preemergence)': [53, 54], 'Foxtail, Robust Purple (Preemergence)': [53, 54], 'Foxtail, Robust White (Preemergence)': [53, 54], 'Galinsoga (Preemergence)': [53, 54], 'Goosegrass (Preemergence)': [53, 54], 'Grassbur (Preemergence)': [53], 'Ground Cherry, Annual (Preemergence)': [53], 'Ground Cherry, Cutleaf (Preemergence)': [53, 54], 'Henbit (Preemergence)': [53, 54], 'Jimsonweed (Preemergence)': [53, 54], 'Johnsongrass, Seedling (Preemergence)': [53, 54], 'Kochia (Preemergence)': [53, 54], 'Lambsquarters (Preemergence)': [53], 'Millet, Proso (Preemergence)': [53], 'Morningglory, Annual (Preemergence)': [53], 'Mustard (Preemergence)': [53, 54], 'Nightshade, Black (Preemergence)': [53, 54], 'Nightshade, Hairy (Preemergence)': [53, 54], 'Panicum, Browntop (Preemergence)': [53, 54], 'Panicum, Fall (Preemergence)': [53, 54], 'Panicum, Texas (Preemergence)': [53, 54], 'Pigweed (Preemergence)': [53], 'Purslane (Preemergence)': [53], 'Pusley, Florida (Preemergence)': [53], 'Ragweed, Common (Preemergence)': [53, 54], 'Ragweed, Giant (Preemergence)': [53, 54], 'Rice, Red (Preemergence)': [53, 54], 'Sandbur (Preemergence)': [53], 'Sedge (Preemergence)': [53], 'Shattercane (Preemergence)': [53, 54], 'Sicklepod (Preemergence)': [53, 54], 'Sida, Prickly (Preemergence)': [53, 54], 'Signalgrass, Broadleaf (Preemergence)': [53, 54], 'Smartweed (Preemergence)': [53], 'Sprangletop, Red (Preemergence)': [53, 54], 'Sunflower, Common (Preemergence)': [53, 54], 'Teaweed (Preemergence)': [53], 'Velvetleaf (Preemergence)': [53, 54], 'Waterhemp (Preemergence)': [53], 'Wildcane (Preemergence)': [53], 'Witchgrass (Preemergence)': [53, 54], 'Amaranth, Palmer (Preemergence)': [54], 'Amaranth, Powell (Preemergence)': [54], 'Amaranth, Spiny (Preemergence)': [54], 'Atriplex': [54], 'Buffalobur (Preemergence)': [54], 'Burclover, California (Preemergence)': [54], 'Carrot, Wild': [54, 55, 56, 62], 'Carrot, Wild (Preemergence)': [54], 'Chamomile, Mayweed (Preemergence)': [54], 'Chickweed, Mouseear (Preemergence)': [54], 'Cocklebur, Common (Preemergence)': [54], 'Crowfootgrass (Preemergence)': [54], 'Cupgrass, Prairie (Preemergence)': [54], 'Cupgrass, Southwestern (Preemergence)': [54], 'Dandelion, Common': [54, 62], 'Dandelion, Common (Preemergence)': [54], 'Dandelion, Seedling (Preemergence)': [54], 'Deadnettle, Purple (Preemergence)': [54], 'Dock, Curly (Preemergence)': [54], 'Evening Primrose, Cutleaf (Preemergence)': [54], 'Fiddleneck, Coast (Preemergence)': [54], 'Filaree, Redstem (Preemergence)': [54], 'Filaree, Whitestem (Preemergence)': [54], 'Fleabane, Hairy (Preemergence)': [54], 'Geranium, Carolina (Preemergence)': [54], 'Ground Cherry, Smooth (Preemergence)': [54], 'Groundsel, Common (Preemergence)': [54], 'Horsenettle (Preemergence)': [54], 'Horseweed (Preemergence)': [54], 'Lettuce, Prickly (Preemergence)': [54], 'Mallow, Common (Preemergence)': [54], 'Marestail (Preemergence)': [54], 'Millet, Foxtail (Preemergence)': [54], 'Millet, Wild Proso (Preemergence)': [54], 'Morningglory, Entireleaf (Preemergence)': [54], 'Morningglory, Ivyleaf (Preemergence)': [54], 'Morningglory, Pitted (Preemergence)': [54], 'Morningglory, Smallflower (Preemergence)': [54], 'Morningglory, Tall (Preemergence)': [54], 'Nettle, Burning (Preemergence)': [54], 'Nightshade, Eastern Black (Preemergence)': [54], 'Pansy, Field (Preemergence)': [54], 'Pigweed, Smooth (Preemergence)': [54], 'Pigweed, Tumble (Preemergence)': [54], 'Pineapple Weed (Preemergence)': [54], 'Puncturevine, Common (Preemergence)': [54], 'Pusley': [54], 'Pusley (Preemergence)': [54], 'Redmaid (Preemergence)': [54], 'Rocket, London (Preemergence)': [54], 'Sandbur, Field (Preemergence)': [54], 'Smartweed, Ladysthumb (Preemergence)': [54], 'Spanish Needles (Preemergence)': [54], 'Starbur, Bristly (Preemergence)': [54], 'Swinecress (Preemergence)': [54], 'Tasselflower, Red (Preemergence)': [54], 'Vetch, Purple (Preemergence)': [54], 'Waterhemp, Common (Preemergence)': [54], 'Waterhemp, Tall (Preemergence)': [54], 'Willowherb, Panicle (Preemergence)': [54], 'Alkanet': [55, 56], 'Aster, Slender': [55, 56], 'Aster, Spiny': [55, 56], 'Aster, White Heath': [55, 56], 'Bedstraw, Smooth': [55, 56], 'Bindweed, Hedge': [55, 56], 'Broomweed, Common': [55, 56], 'Buckwheat, Tartary': [55, 56], 'Buffaloweed': [55, 56], 'Burclover, California': [55, 56], 'Burdock, Common': [55, 56], 'Buttercup, Corn': [55, 56], 'Buttercup, Creeping': [55, 56], 'Buttercup, Roughseed': [55, 56], 'Buttercup, Tall': [55, 56], 'Buttercup, Western Field': [55, 56], 'Campion, Bladder': [55, 56], 'Chamomile, Corn': [55, 56], 'Chervil, Bur': [55, 56], 'Chickweed, Field': [55, 56], 'Chicory': [55, 56], 'Clover': [55, 56], 'Clover, Hop': [55, 56], 'Clover, Sweet': [55, 56], 'Cockle, Corn': [55, 56], 'Croton, Woolly': [55, 56], 'Daisy, English': [55, 56], 'Dock, Broadleaf': [55, 56], 'Dragonhead, American': [55, 56], 'Evening Primrose, Common': [55, 56], 'Garlic, Wild': [55, 56, 62], 'German Moss': [55, 56], 'Goldenrod, Canada': [55, 56], 'Goldenrod, Missouri': [55, 56], 'Goldenweed, Common': [55, 56], 'Goosefoot, Nettleleaf': [55, 56], 'Gromwell': [55, 56], 'Hawkweed': [55, 56], 'Henbane, Black': [55], 'Horsenettle, Carolina': [55, 56], 'Ironweed': [55, 56], 'Knapweed, Diffuse': [55, 56], 'Knapweed, Dwarf': [55], 'Knapweed, Spotted': [55, 56], 'Knawel': [55, 56], 'Lespedeza, Sericea': [55, 56], 'Lettuce, Miners': [55, 56], 'Lovegrass': [55], 'Milkweed, Honeyvine': [55, 56], 'Milkweed, Western Whorled': [55, 56], 'Mustard, Treacle': [55, 56], 'Mustard, Yellowtops': [55, 56], 'Onion, Wild': [55, 56], 'Pigweed, Rough': [55, 56], 'Plantain, Bracted': [55, 56], 'Plantain, Broadleaf': [55, 56, 58, 60, 62], 'Plantain, Buckhorn': [55, 56], 'Pokeweed': [55, 56], 'Poorjoe': [55, 56], 'Poppy, Red-Horned': [55, 56], 'Queen Annes Lace': [55, 56], 'Ragweed, Lanceleaf': [55, 56], 'Ragweed, Western': [55, 56], 'Ragwort, Tansy': [55, 56], 'Rubberweed, Bitter': [55, 56], 'Salsify': [55, 56], 'Senna, Coffee': [55, 56], 'Smartweed, Green': [55, 56], 'Snakeweed, Broom': [55, 56], 'Sneezeweed, Bitter': [55, 56], 'Soda Apple, Tropical': [55, 56], 'Sorrel, Red': [55, 56], 'Spikeweed, Common': [55, 56], 'Spurry, Corn': [55, 56], 'Starwort, Little': [55, 56], 'Sumpweed, Rough': [55, 56], 'Sundrops': [55], 'Sunflower, Volunteer': [55, 56], 'Teasel': [55, 56], 'Thistle, Bull': [55, 56], 'Thistle, Milk': [55, 56], 'Thistle, Musk': [55, 56], 'Thistle, Plumeless': [55, 56], 'Thistle, Scotch': [55, 56], 'Toadflax, Dalmatian': [55, 56], 'Vetch': [55, 56], 'Violet, Wild': [55, 56], 'Water Hemlock': [55], 'Water Hemlock, Spotted': [55, 56], 'Water Primrose, Winged': [55, 56], 'Woodsorrel, Creeping': [55, 56], 'Woodsorrel, Yellow': [55, 56], 'Wormwood': [55, 56], 'Wormwood, Common': [55, 56], 'Wormwood, Louisiana': [55, 56], 'Yankeeweed': [55, 56], 'Yarrow, Common': [55, 56], 'Bitterdock': [56], 'Bitterweed': [56], 'Buckvine': [56], 'Cypressweed': [56], 'Evening Primrose': [56], 'Fanweed': [56], 'Frenchweed': [56], 'Henbane': [56], 'Horsenettle, White': [56], 'Knapweed, Black': [56], 'Knapweed, Russian': [56], 'Mallow, Dwarf': [56], 'Milkweed, Climbing': [56], 'Peppergrass': [56], 'Povertyweed': [56], 'Ragweed, Bur': [56], 'Sorrel, Sheep': [56], 'Stinkweed': [56], 'Sundrops, Halfshrub': [56], 'Sunflower, Wild': [56, 58, 60], 'Water Primrose, Creeping': [56], 'Buttonweed': [57], 'Ground Cherry, Annual': [57], 'Mustard': [57, 61], 'Buttercup, Smallflower': [58, 60], 'Chamomile': [58, 60], 'Medic, Black': [58, 60], 'Millet, Browntop': [58], 'Oat, Tame': [58], 'Puncturevine, Common': [58], 'Spurge, Toothed': [58, 60], 'Vetch, Bird': [58], 'Violet, Field': [58, 60], 'Waterhemp,Tall': [58], 'Plantain, Blackseed': [59], 'Bluegrass, Rough': [61], 'Brome, California': [61], 'Dandelion, Falsealseflax, Smallseed': [61], 'Fescue, Fine, Volunteer': [61], 'Fescue, Tall, Volunteer': [61], 'Lovegrass, Indian': [61], 'Orchardgrass, Volunteer': [61], 'Ryegrass, Annual, Volunteer': [61], 'Ryegrass, Perennial, Volunteer': [61], 'Weed, Perennial': [61], 'Weed, Triazine Resistant': [61], 'Burdock': [62], 'Chamomile, Scentless': [62], 'Marestail, Glyphosate Resistant': [62], 'Pansy, Field': [62], 'Turnip Weed': [62], 'Redstem filaree': [63], 'Marestail (horseweed)': [63]}

crop_dict = {'Barley': [0, 1, 4, 8, 10, 12, 15, 17, 18, 23, 28, 33, 34, 39, 40, 41, 42], 'Grass, For Seed': [0, 6, 15, 23, 39, 40, 41, 42], 'Peanut': [0, 1, 10, 11, 13, 15, 16, 22, 23, 24, 28, 29, 32, 36, 40, 41, 42], 'Pecan': [0, 1, 2, 6, 7, 15, 16, 17, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Wheat': [0, 1, 4, 5, 8, 10, 12, 15, 17, 18, 23, 28, 33, 34, 39, 40, 41, 42, 45], 'Corn, Field': [1, 4, 5, 8, 10, 11, 12, 15, 17, 18, 23, 27, 28, 29, 36, 39, 42, 49, 53, 54, 55, 56, 57, 58, 59, 60, 61], 'Corn, Field, For Seed': [1, 4, 5, 10, 11, 17, 18, 22, 29], 'Corn, Sweet': [1, 4, 5, 8, 10, 11, 12, 15, 17, 18, 23, 27, 28, 29, 39, 40, 41, 42, 49, 53, 57, 59], 'Corn, Sweet, For Seed': [1, 4, 5, 17, 18], 'Grass, Grown for Seed': [1], 'Popcorn': [1, 4, 5, 8, 10, 11, 12, 15, 17, 18, 23, 27, 28, 29, 39, 40, 41, 42, 49, 53, 54, 55, 56, 57], 'Almond': [2, 6, 7, 14, 15, 16, 23, 25, 26, 30, 40, 41, 42, 63], 'Beechnut': [2, 6, 7, 15, 16, 22, 23, 24, 25, 26, 28, 30, 40, 41, 42, 63], 'Brazil Nut': [2, 6, 7, 22, 23, 24, 25, 26, 28, 30, 40, 41, 42, 63], 'Butternut': [2, 6, 7, 15, 16, 22, 23, 24, 25, 26, 28, 30, 40, 41, 42, 63], 'Cashew': [2, 6, 7, 15, 16, 22, 23, 24, 25, 26, 28, 30, 40, 41, 42, 63], 'Chinquapin': [2, 6, 7, 22, 23, 24, 25, 26, 28, 30, 40, 41, 42, 63], 'Filbert': [2, 6, 7, 15, 16, 17, 22, 23, 24, 25, 26, 28, 30, 40, 41, 42, 63], 'Hickory Nut': [2, 6, 7, 22, 23, 24, 25, 26, 28, 30, 40, 41, 42, 63], 'Macadamia Nut': [2, 3, 6, 7, 22, 23, 24, 25, 26, 28, 30, 41, 63], 'Pistachio': [2, 6, 7, 14, 15, 16, 22, 23, 24, 25, 26, 28, 30, 40, 41, 42, 63], 'Walnut': [2, 6, 7, 15, 16, 28, 63], 'Almond, Non-Bearing': [3], 'Amaranth': [3, 6, 7, 8, 22, 23, 24, 25, 27, 28, 29, 40, 41, 42], 'Apple': [3, 6, 7, 14, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Apple, Non-Bearing': [3], 'Apricot, Non-Bearing': [3], 'Arugula, Roquette': [3, 6, 7, 8, 22, 23, 24, 25, 26, 28, 29, 41, 42], 'Asparagus': [3, 6, 15, 16, 40, 41, 42], 'Avocado': [3, 15, 22, 25, 26, 28, 40, 41, 42], 'Avocado, Non-Bearing': [3], 'Balsam Apple': [3, 7, 8, 9, 10, 22, 23, 27, 28, 29, 30, 40, 41, 42], 'Balsam Pear': [3, 7, 8, 9, 10, 22, 23, 27, 28, 29, 30, 40, 41, 42], 'Banana': [3, 15, 22, 25, 26, 28, 40, 41, 42], 'Blackberry': [3, 7, 15, 16, 22, 28, 29, 31, 40, 41, 42, 63], 'Blueberry': [3, 15, 16, 22, 28], 'Broccoli': [3, 6, 7, 8, 10, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Broccoli, Cavalo': [3, 8, 22, 23, 24, 25, 26, 27, 28, 30, 31, 40, 41], 'Broccoli, Chinese Gai Lon': [3, 6, 7, 8, 22, 23, 24, 25, 26, 27, 28, 29, 30, 41, 42], 'Broccoli, Raab': [3, 6, 7, 8, 10, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Brussels Sprout': [3, 6, 7, 8, 10, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Cabbage': [3, 6, 7, 8, 10, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Cabbage, Chinese Bok Choy': [3, 6, 7, 8, 10, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Cabbage, Chinese Mustard': [3, 6, 7, 8, 22, 23, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Cabbage, Chinese Napa': [3, 6, 7, 8, 10, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Cardoon': [3, 6, 7, 8, 22, 23, 25, 26, 28, 29, 40, 41, 42], 'Cauliflower': [3, 6, 7, 8, 10, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Celery': [3, 6, 7, 8, 15, 16, 22, 23, 25, 26, 28, 29, 40, 41, 42], 'Celery, Chinese': [3, 6, 7, 8, 23, 25, 26, 28, 29, 40, 41, 42], 'Celtuce': [3, 6, 7, 8, 22, 23, 25, 26, 28, 29, 40, 41, 42], 'Chard, Swiss': [3, 6, 7, 8, 9, 22, 23, 25, 26, 28, 29, 40, 41, 42], 'Cherry, Sour, Non-Bearing': [3], 'Cherry, Sweet, Non-Bearing': [3], 'Chervil': [3, 6, 7, 8, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Chicory, Red': [3, 6, 7, 8, 22, 23, 24, 25, 26, 28, 29, 41, 42], 'Chrysanthemum, Edible-Leaved': [3, 6, 7, 8, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Chrysanthemum, Garland': [3, 6, 7, 8, 9, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Citrus': [3, 15, 16, 22, 25, 26, 30, 31, 63], 'Citrus, Non-Bearing': [3], 'Collard': [3, 6, 7, 8, 10, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Corn Salad': [3, 6, 7, 8, 9, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Crabapple': [3, 6, 7, 14, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Crabapple, Non-Bearing': [3], 'Cranberry': [3, 10, 15, 16, 22, 25, 26, 27, 29, 40, 41, 42], 'Cress, Garden': [3, 6, 7, 8, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Cress, Upland': [3, 6, 7, 8, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Cucumber': [3, 6, 7, 8, 9, 10, 11, 15, 16, 22, 23, 27, 28, 29, 30, 31, 40, 41, 42], 'Cucumber, Chinese': [3, 7, 8, 9, 10, 22, 23, 27, 28, 29, 30, 40, 41, 42], 'Cucurbit': [3, 9, 15, 16], 'Dandelion': [3, 6, 7, 8, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Dock': [3, 6, 7, 8, 9, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Endive': [3, 6, 7, 8, 9, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Escarole': [3, 6, 7, 8, 9, 22, 23, 24, 25, 26, 29, 41, 42], 'Fennel, Florence': [3, 6, 7, 8, 15, 22, 23, 25, 26, 28, 29, 40, 41, 42], 'Gai Choy': [3, 6, 7, 8, 23, 24, 25, 26, 28, 29, 30, 41, 42], 'Gherkin': [3, 6, 7, 8, 9, 10, 11, 22, 23, 27, 28, 29, 30, 31, 40, 41, 42], 'Ginseng': [3, 6, 7, 14, 15, 16, 22, 28, 40, 41, 42], 'Gourd, Edible': [3, 6, 7, 8, 9, 10, 11, 22, 23, 27, 28, 29, 30, 31, 40, 41, 42], 'Grape': [3, 6, 7, 14, 15, 16, 22, 23, 24, 25, 26, 28, 40, 41, 42, 63], 'Hop': [3, 6, 7, 15, 22, 23, 24, 25, 26, 28, 31, 40, 41, 42, 63], 'Kale': [3, 6, 7, 8, 10, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Kohlrabi': [3, 6, 7, 8, 10, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Lettuce, Head': [3, 6, 7, 8, 9, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Lettuce, Leaf': [3, 6, 7, 8, 9, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Loganberry': [3, 7, 15, 16, 22, 28, 29, 31, 40, 41, 42, 63], 'Loquat': [3, 6, 7, 14, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Loquat, Non-Bearing': [3], 'Mayhaw': [3, 6, 7, 14, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Mayhaw, Non-Bearing': [3], 'Melon, Bitter': [3, 7, 8, 9, 10, 22, 23, 27, 28, 29, 30, 40, 41, 42], 'Melon, Citron': [3, 6, 7, 8, 9, 10, 11, 22, 23, 27, 28, 29, 30, 31, 40, 41, 42], 'Mizuna': [3, 6, 7, 8, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Momordica': [3, 6, 7, 8, 9, 10, 11, 22, 27, 28, 29, 30, 31, 41, 42], 'Muskmelon': [3, 6, 7, 8, 9, 10, 11, 15, 16, 22, 23, 27, 28, 29, 30, 31, 40, 41, 42], 'Mustard Greens': [3, 6, 7, 8, 10, 15, 16, 22, 23, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Nectarine, Non-Bearing': [3], 'Onion, Dry Bulb': [3, 14, 47], 'Orach': [3, 6, 7, 8, 9, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Parsley': [3, 6, 7, 8, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Peach, Non-Bearing': [3], 'Pear': [3, 6, 7, 14, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Pear, Non-Bearing': [3], 'Pear, Oriental': [3, 14, 22, 23, 24, 25, 28, 63], 'Pear, Oriental, Non-Bearing': [3], 'Pineapple': [3, 15, 25, 26, 40, 41, 42], 'Plantain': [3, 15, 22, 25, 26, 28, 40, 41, 42], 'Plum, Chickasaw, Non-Bearing': [3], 'Plum, Damson, Non-Bearing': [3], 'Plum, Japanese, Non-Bearing': [3], 'Plum, Non-Bearing': [3], 'Plumcot, Non-Bearing': [3], 'Prune, Non-Bearing': [3], 'Pumpkin': [3, 6, 7, 8, 9, 10, 11, 22, 23, 27, 28, 29, 30, 31, 40, 41, 42], 'Purslane, Garden': [3, 6, 7, 8, 9, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Purslane, Winter': [3, 6, 7, 8, 9, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Quince': [3, 6, 7, 14, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Quince, Non-Bearing': [3], 'Radicchio': [3, 6, 7, 8, 9, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Rape Greens': [3, 6, 7, 8, 10, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Rapini': [3, 6, 7, 8, 23, 24, 26, 28, 29, 30, 41, 42], 'Raspberry, Black': [3, 7, 22, 28, 29, 31, 40, 41, 42, 63], 'Raspberry, Red': [3, 7, 22, 28, 29, 31, 40, 41, 42, 63], 'Rhubarb': [3, 6, 7, 8, 22, 23, 25, 26, 28, 29, 40, 41, 42], 'Sorrel': [3, 6, 7, 8, 22, 23, 24, 25, 26, 28, 29, 41, 42], 'Spinach': [3, 6, 7, 8, 9, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Spinach, Mustard': [3, 6, 7, 8, 10, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Spinach, New Zealand': [3, 6, 7, 8, 9, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Spinach, Vine': [3, 6, 7, 8, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42], 'Squash, Summer': [3, 6, 7, 8, 9, 10, 11, 22, 23, 27, 28, 29, 30, 31, 40, 41, 42], 'Squash, Winter': [3, 6, 7, 8, 9, 10, 11, 22, 23, 27, 28, 29, 30, 31, 40, 41, 42], 'Strawberry': [3, 6, 7, 8, 14, 15, 16, 22, 27, 28, 29, 30, 31, 40, 41, 42], 'Tobacco, Field': [3], 'Tobacco, Greenhouse': [3], 'Tobacco, Transplant': [3], 'Tomato': [3, 6, 7, 8, 9, 14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Watermelon': [3, 6, 7, 8, 9, 10, 11, 15, 16, 22, 23, 27, 28, 29, 30, 31, 40, 41, 42], 'Waxgourd, Chinese': [3, 6, 7, 8, 9, 10, 11, 22, 23, 27, 28, 29, 30, 31, 40, 41, 42], 'Bean': [4, 15, 16, 22, 24, 28, 40], 'Bean, Adzuki': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Dry Broad': [4, 10, 11, 23, 24, 29], 'Bean, Dry Lima': [4, 10, 11, 23, 24, 29], 'Bean, Fava': [4, 8, 22, 25, 26, 28, 39, 41, 42], 'Bean, Field': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Garbanzo': [4, 8, 15, 16, 22, 23, 25, 26, 28, 39, 41, 42], 'Bean, Guar': [4, 10, 22, 26, 28], 'Bean, Hyacinth': [4, 8, 22, 25, 26, 28], 'Bean, Kidney': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Lablab': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Lupin': [4, 8, 11, 22, 25, 26, 28, 39, 41, 42], 'Bean, Moth': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 39, 40, 41, 42], 'Bean, Mung': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Navy': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Phaseolus': [4, 8, 11, 24, 26, 28, 39, 41, 42], 'Bean, Pinto': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Rice': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Tepary': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Urd': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Vigna': [4, 8, 11, 25, 26, 28, 39, 41, 42], 'Beet, Sugar': [4, 6, 8, 10, 11, 22, 25, 26, 36, 41, 42, 47], 'Catjang': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Chickpea': [4, 8, 10, 11, 15, 16, 18, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Cotton': [4, 10, 15, 16, 19, 20, 21, 22, 23, 24, 27, 28, 32, 35, 36, 39, 41, 42], 'Cowpea': [4, 8, 10, 22, 23, 24, 25, 26, 28, 39, 40, 41, 42], 'Flax': [4, 10, 15, 16, 39, 40, 41, 42], 'Lentil': [4, 8, 10, 11, 15, 16, 18, 22, 23, 25, 26, 28, 29, 39, 40, 41, 42], 'Lupin, Grain': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Lupin, Sweet': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Lupin, White': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Lupin, White Sweet': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Pea': [4, 15, 16, 24, 28, 40], 'Pea, Black-Eyed': [4, 8, 10, 11, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Pea, Crowder': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Pea, Field': [4, 8, 10, 22, 23, 24, 25, 26, 28, 39, 40, 41, 42], 'Pea, Pigeon': [4, 8, 10, 22, 23, 25, 26, 28, 39, 40, 41, 42], 'Pea, Pisum': [4, 8, 26, 28, 39, 42], 'Pea, Southern': [4, 8, 10, 11, 22, 23, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Soybean': [4, 5, 10, 11, 15, 16, 17, 18, 22, 23, 24, 25, 26, 28, 35, 36, 39, 41, 42], 'Amaranth, Leafy': [6, 8, 9, 22, 24, 25, 26, 28], 'Angelica': [6, 7, 22, 40, 41, 42], 'Apricot': [6, 7, 14, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Arracacha': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Arrowroot': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Artichoke, Chinese': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Artichoke, Globe': [6, 7, 22, 25, 26, 40, 41, 42], 'Artichoke, Jerusalem': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Balm': [6, 7, 22, 40, 41, 42], 'Basil': [6, 7, 22, 40, 41, 42], 'Bay, Sweet': [6, 7, 22, 40, 41, 42], 'Bearberry': [6, 7, 10, 14, 25, 26, 27, 28, 29, 31, 40, 41, 42], 'Beet, Garden': [6, 7, 22, 28, 40, 41, 42, 47], 'Bilberry': [6, 7, 10, 14, 25, 26, 27, 28, 29, 31, 40, 41, 42], 'Blueberry, Lowbush': [6, 7, 10, 11, 14, 22, 25, 26, 27, 28, 29, 31, 40, 41, 42], 'Borage': [6, 7, 10, 22, 40, 41, 42], 'Broccolo, Cavalo': [6, 7, 8, 28, 29, 42], 'Burdock, Edible': [6, 7, 22, 28], 'Burnet': [6, 7, 22, 40, 41, 42], 'Calamondin': [6, 7, 8, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Camomile': [6, 7, 41, 42], 'Canistel': [6, 22, 25, 26, 28, 40, 41, 42], 'Canna, Edible': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28], 'Carrot': [6, 7, 8, 15, 16, 22, 23, 24, 25, 26, 28, 40, 41, 42, 47], 'Cassava, Bitter': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Cassava, Sweet': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Catnip': [6, 7, 22, 40, 41, 42], 'Celeriac': [6, 7, 22, 40, 41, 42], 'Chayote, Fruit': [6, 7, 8, 9, 10, 11, 22, 27, 28, 29, 30, 31, 40, 41, 42], 'Chayote, Root': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Cherry': [6, 15, 16, 22, 24, 28, 30, 63], 'Cherry, Sweet': [6, 7, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Cherry, Tart': [6, 7, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Chervil, Dried': [6, 7, 22, 40, 41, 42], 'Chervil, Turnip-Rooted': [6, 7, 22, 28, 40, 41, 42], 'Chestnut': [6, 7, 15, 16, 22, 23, 24, 25, 26, 28, 30, 40, 41, 42, 63], 'Chicory': [6, 7, 22, 28, 40, 41, 42], 'Chironja': [6, 8, 22, 23, 24, 25, 26, 40, 41, 42, 63], 'Chive': [6, 7, 22, 40, 41, 42], 'Chive, Chinese': [6, 7, 22, 40, 41, 42], 'Chufa': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Cilantro': [6, 7], 'Citron': [6, 7, 8, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Clary': [6, 7, 22, 40, 41, 42], 'Cloudberry': [6, 7, 10, 14, 25, 26, 27, 28, 29, 31, 40, 41, 42], 'Coriander, Leaf': [6, 7, 40, 41, 42], 'Costmary': [6, 7, 22, 40, 41, 42], 'Cress, Winter': [6, 22, 24, 25, 26, 28], 'Culantro, Leaf': [6, 7, 22, 40, 41, 42], 'Curry, Leaf': [6, 7, 22, 40, 41, 42], 'Daikon': [6, 10, 22, 28], 'Dasheen': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Dill, Seed': [6, 7, 40, 41, 42], 'Dillweed': [6, 7, 9, 22, 40, 41, 42], 'Eggplant': [6, 7, 8, 9, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Ginger': [6, 7, 9, 14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Gooseberry': [6, 7, 10, 11, 14, 15, 16, 22, 25, 26, 28, 29, 40, 41, 42], 'Grape, Amur River': [6, 7, 14, 25, 26, 28, 40, 41, 42], 'Grapefruit': [6, 7, 8, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Ground Cherry': [6, 7, 8, 9, 14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Hazelnut': [6, 7, 17, 24, 25, 26, 28, 30, 41, 42, 63], 'Horehound': [6, 7, 22, 40, 41, 42], 'Horseradish': [6, 7, 15, 16, 22, 28, 40, 41, 42], 'Hyssop': [6, 7, 22, 40, 41, 42], 'Kiwifruit, Hardy': [6, 7, 14, 25, 26, 28, 40, 41, 42], 'Kumquat': [6, 7, 8, 14, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Lavender': [6, 7, 22, 40, 41, 42], 'Lemon': [6, 7, 8, 14, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Lemon Balm': [6, 7, 22], 'Lemongrass': [6, 7, 22, 40, 41, 42], 'Leren': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Lime': [6, 7, 8, 14, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Lingonberry': [6, 7, 10, 11, 14, 22, 25, 26, 27, 28, 29, 31, 40, 41, 42], 'Lovage, Leaf': [6, 7, 22, 40, 41, 42], 'Mandarin': [6, 7, 8, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Mango': [6, 15, 22, 25, 26, 28, 40, 41, 42], 'Marigold': [6, 7, 22, 40, 41, 42], 'Marjoram': [6, 7, 22, 40, 41, 42], 'Marjoram, Annual': [6, 7], 'Marjoram, Pot': [6, 7], 'Marjoram, Sweet': [6, 7], 'Marjoram, Wild': [6, 7], 'Maypop': [6, 7, 14, 25, 26, 28, 40, 41, 42], 'Muntries': [6, 7, 10, 14, 25, 26, 27, 28, 29, 31, 40, 41, 42], 'Nasturtium': [6, 7, 22, 40, 41, 42], 'Nectarine': [6, 7, 14, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Orange, Sour': [6, 7, 8, 22, 23, 24, 25, 26, 28, 29, 30, 31, 63], 'Orange, Sweet': [6, 7, 8, 22, 23, 24, 25, 26, 28, 29, 30, 31, 63], 'Oregano': [6, 7, 40, 41, 42], 'Papaya': [6, 15, 22, 25, 26, 28, 40, 41, 42], 'Parsley, Chinese': [6, 7, 22, 42], 'Parsley, Dried': [6, 7, 22, 40, 41, 42], 'Parsley, Turnip-Rooted': [6, 7, 22, 28, 40, 41, 42], 'Parsnip': [6, 7, 22, 28, 40, 41, 42], 'Partridgeberry': [6, 7, 10, 14, 25, 26, 27, 28, 29, 31, 40, 41, 42], 'Peach': [6, 7, 14, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Pennyroyal': [6, 7, 22, 40, 41, 42], 'Pepino': [6, 7, 8, 9, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Pepper': [6, 8, 9, 15, 16, 22, 23, 24, 25, 27, 28, 40, 41, 42], 'Pepper, Bell': [6, 7, 8, 9, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Pepper, Chili': [6, 8, 22, 23, 24, 25, 26, 27, 40, 41, 42], 'Pepper, Cooking': [6, 8, 22, 23, 24, 25, 27, 40, 41, 42], 'Pepper, Sweet': [6, 8, 22, 23, 24, 25, 27, 28, 40, 41, 42], 'Pimento': [6, 8, 22, 23, 24, 25, 26, 27, 40, 41, 42], 'Plum': [6, 7, 14, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Plum, Chickasaw': [6, 7, 14, 22, 23, 24, 25, 26, 28, 29, 30, 31, 63], 'Plum, Damson': [6, 7, 14, 22, 23, 24, 25, 26, 28, 29, 30, 31, 63], 'Plum, Japanese': [6, 7, 14, 22, 23, 24, 25, 26, 28, 29, 30, 31, 63], 'Plumcot': [6, 7, 14, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Potato': [6, 7, 8, 9, 14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 31, 40, 41, 42], 'Potato, Sweet': [6, 7, 9, 14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Prune, Fresh': [6, 7, 22, 23, 24, 25], 'Pummelo': [6, 7, 8, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 42, 63], 'Radish': [6, 7, 10, 15, 16, 22, 23, 24, 28, 40, 41, 42], 'Radish, Oriental': [6, 7, 22, 28, 40, 41, 42], 'Rice': [6, 8, 15, 17, 39, 40, 41, 42, 44], 'Rosemary': [6, 7, 22, 40, 41, 42], 'Rue': [6, 7, 22, 40, 41, 42], 'Rutabaga': [6, 7, 10, 22, 28, 40, 41, 42], 'Sage': [6, 7, 22, 40, 41, 42], 'Salsify': [6, 7, 22, 28, 40, 41, 42], 'Salsify, Black': [6, 7, 22, 28, 40, 41, 42], 'Salsify, Spanish': [6, 7, 22, 28, 40, 41, 42], 'Sapodilla': [6, 22, 25, 26, 40, 41, 42], 'Sapote, Black': [6, 22, 25, 26, 28, 40, 41, 42], 'Sapote, Mamey': [6, 22, 25, 26, 40, 41, 42], 'Satsuma Mandarin': [6, 7, 8, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Savory, Summer': [6, 7, 22, 40, 41, 42], 'Savory, Winter': [6, 7, 22, 40, 41, 42], 'Schisandra Berry': [6, 7, 14, 25, 26, 28, 40, 41, 42], 'Skirret': [6, 7, 22, 28, 40, 41, 42], 'Spinach, Chinese': [6, 7, 8, 22, 23, 24, 25, 26, 28, 29, 41, 42], 'Spinach, Indian': [6, 22, 24, 25, 26, 28], 'Spinach, Malabar': [6, 9, 22, 24, 25, 26, 28], 'Star Apple': [6, 22, 25, 26, 28, 40, 41, 42], 'Tampala': [6, 8, 22, 24, 25, 26, 28], 'Tangelo': [6, 7, 8, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Tangerine': [6, 7, 8, 15, 16, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Tangor': [6, 7, 8, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Tanier': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Tansy': [6, 7, 22, 40, 41, 42], 'Taro': [6, 7, 9, 22, 24, 25, 26, 28, 41, 42], 'Tarragon': [6, 7, 22, 40, 41, 42], 'Thyme': [6, 7, 22, 40, 41, 42], 'Tomatillo': [6, 7, 8, 9, 14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 40, 41, 42], 'Turmeric': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Turnip': [6, 7, 10, 15, 16, 22, 28, 40, 41, 42], 'Walnut, Black': [6, 7, 22, 23, 24, 25, 26, 28, 30, 40, 41, 42, 63], 'Walnut, English': [6, 7, 22, 23, 24, 25, 26, 28, 30, 40, 41, 42, 63], 'Wintergreen': [6, 7, 22, 40, 41, 42], 'Woodruff': [6, 7, 22, 40, 41, 42], 'Wormwood': [6, 7, 22, 40, 41, 42], 'Yam Bean': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Yam, True': [6, 7, 9, 14, 22, 23, 24, 25, 26, 27, 28, 40, 41, 42], 'Yellow Rocket': [6], 'African Nut-Tree': [7, 25, 26, 28, 30, 63], 'Almond, Tropical': [7, 25, 26, 28, 30, 63], 'Apricot, Japanese': [7, 14, 25, 26, 28, 29, 30, 31, 63], 'Aronia Berry': [7, 10, 11, 25, 26, 28, 29, 40, 41, 42], 'Arugula': [7, 8, 10, 27, 29, 40], 'Azarole': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Barberry, European': [7, 10, 11, 25, 26, 28, 29, 40, 41, 42], 'Bean, Dry': [7, 10, 15, 16, 23, 41], 'Bean, Succulent': [7], 'Blueberry, Highbush': [7, 10, 11, 22, 25, 26, 28, 29, 40, 41, 42, 63], 'Broccoli, Chinese': [7, 10, 29, 30, 31, 40], 'Bunya Pine': [7, 25, 26, 28, 30, 63], 'Bush Nut': [7, 25], 'Bush Tomato': [7, 9, 14, 25, 26, 28, 29, 30, 31], 'Cajou Nut': [7, 25, 26, 28, 30, 63], 'Calabaza': [7, 8, 9, 10, 22, 23, 27, 28, 29, 30, 40, 41, 42], 'Candlenut': [7, 25, 26, 28, 30, 63], 'Cantaloupe': [7, 8, 9, 10, 11, 15, 16, 22, 23, 27, 28, 29, 30, 31, 40, 41, 42], 'Cantaloupe, True': [7, 9, 10, 11, 22, 23, 28, 29, 30, 31], 'Capulin': [7, 14, 25, 26, 28, 29, 30, 31, 63], 'Casaba': [7, 9, 10, 11, 22, 23, 28, 29, 30, 31, 40, 41, 42], 'Cherry, Black': [7, 25, 26, 28, 29, 30, 31, 63], 'Cherry, Nanking': [7, 25, 26, 28, 29, 30, 31, 63], 'Chestnut, Guiana': [7, 25, 26, 28, 30, 63], 'Chestnut, Japanese Horse': [7, 25, 26, 28, 30, 63], 'Chive, Chinese, Fresh Leaf': [7, 14, 22, 25, 26, 29], 'Chive, Fresh Leaf': [7, 14, 22, 25, 26, 29], 'Citrus, Hybrid': [7, 8, 22, 23, 24, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Cocona': [7, 9, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Coconut': [7, 16, 25, 26, 28, 30, 40, 41, 42, 63], 'Coquito Nut': [7, 25, 26, 28, 30, 63], 'Cranberry, Highbush': [7, 10, 11, 25, 26, 29, 40, 41, 42], 'Cucuzza': [7, 8, 9, 10, 22, 23, 27, 28, 29, 30, 40, 41, 42], 'Currant Tomato': [7, 9, 14, 25, 26, 28, 29, 30, 31], 'Currant, Black': [7, 10, 11, 25, 26, 28, 29, 40, 41, 42], 'Currant, Buffalo': [7, 10, 11, 25, 26, 28, 29, 40, 41, 42], 'Currant, Native': [7, 10, 11, 25, 26, 28, 29, 40, 41, 42], 'Currant, Red': [7, 10, 11, 25, 26, 28, 29, 40, 41, 42], 'Daikon, Oriental': [7], 'Daylily, Bulb': [7, 14, 22, 25, 26, 29], 'Dika Nut': [7, 25, 26, 28, 30, 63], 'Eggplant, African': [7, 9, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Eggplant, Scarlet': [7, 9, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Elderberry': [7, 10, 11, 15, 16, 22, 25, 26, 28, 29, 40, 41, 42], 'Fritillaria, Bulb': [7, 14, 22, 25, 26, 29, 40, 41, 42], 'Fritillaria, Leaf': [7, 14, 22, 25, 26, 29], 'Garden Huckleberry': [7, 9, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Garlic, Bulb': [7, 14, 25, 26, 29], 'Garlic, Great Headed, Bulb': [7, 14, 25, 26, 29], 'Garlic, Serpent Bulb': [7, 14, 22, 25, 26, 29, 40, 41, 42], 'Ginkgo': [7, 25, 26, 28, 30, 63], 'Goji Berry': [7, 9, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Grapefruit, Japanese Summer': [7, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Guava, Chilean': [7, 10, 11, 25, 26, 28, 29, 40, 41, 42], 'Heartnut': [7, 25, 26, 28, 30, 63], 'Hechima': [7, 8, 9, 10, 22, 23, 27, 28, 29, 30, 40, 41, 42], 'Honeysuckle, Edible': [7, 10, 11, 25, 26, 28, 29, 40, 41, 42], 'Hosta, Elegans': [7, 14, 22, 25, 26, 29, 40, 41, 42], 'Huckleberry': [7, 10, 11, 15, 16, 22, 25, 26, 28, 29, 40, 41, 42], 'Hyotan': [7, 8, 9, 10, 22, 23, 27, 28, 29, 30, 40, 41, 42], 'Jostaberry': [7, 10, 11, 25, 26, 28, 29, 40, 41, 42], 'Jujube, Chinese': [7, 14, 25, 26, 28, 29, 30, 31, 63], 'Juneberry': [7, 10, 11, 22, 25, 26, 28, 29, 40, 41, 42], 'Kurrat': [7, 14, 22, 25, 26, 29, 40, 41, 42], 'Leek': [7, 14, 22, 25, 26, 29, 40, 41, 42], 'Leek, Ladys': [7, 14, 22, 25, 26, 29, 40, 41, 42], 'Leek, Wild': [7, 14, 22, 25, 26, 29, 40, 41, 42], 'Lily, Bulb': [7, 14, 22, 25, 26, 29], 'Lime, Australian Desert': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Lime, Australian Finger': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Lime, Australian Round': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Lime, Brown River Finger': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Lime, Mount White': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Lime, New Guinea Wild': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Lime, Russell River': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Lime, Sweet': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Lime, Tahiti': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Mandarin, Mediterranean': [7, 25, 26, 28, 29, 30, 31, 40, 63], 'Martynia': [7, 9, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Medlar': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Melon, Chinese Preserving': [7, 8, 9, 10, 28, 29, 30, 41, 42], 'Melon, Crenshaw': [7, 9, 10, 11, 22, 23, 28, 29, 30, 31, 40, 41, 42], 'Melon, Golden Pershaw': [7, 9, 10, 11, 22, 23, 28, 29, 30, 31, 40, 41, 42], 'Melon, Honey Ball': [7, 9, 10, 11, 22, 23, 28, 29, 30, 31, 40, 41, 42], 'Melon, Honeydew': [7, 9, 10, 11, 22, 23, 28, 29, 30, 31, 40, 41, 42], 'Melon, Mango': [7, 9, 10, 11, 22, 23, 28, 29, 30, 31, 40, 41, 42], 'Melon, Persian': [7, 9, 10, 11, 22, 23, 28, 29, 30, 31, 40, 41, 42], 'Melon, Pineapple': [7, 9, 10, 11, 22, 23, 28, 29, 30, 31, 40, 41, 42], 'Melon, Santa Claus': [7, 9, 10, 11, 22, 23, 28, 29, 30, 31, 40, 41, 42], 'Melon, Snake': [7, 9, 10, 11, 22, 23, 28, 29, 30, 31, 40, 41, 42], 'Mongongo Tree': [7, 25, 26, 28, 30, 63], 'Monkey Pot': [7, 25, 26, 28, 30, 63], 'Monkey Puzzle Tree': [7, 25, 26, 28, 30, 63], 'Naranjilla': [7, 9, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Oak, Bur': [7, 25, 26, 28, 30, 63], 'Okari Nut': [7, 25, 26, 28, 30, 63], 'Okra': [7, 9, 15, 16, 22, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Okra, Chinese': [7, 8, 9, 10, 22, 23, 27, 28, 29, 30, 40, 41, 42], 'Onion, Beltsville Bunching': [7, 14, 22, 25, 26, 29, 30, 31, 40, 41, 42], 'Onion, Bulb': [7, 14, 22, 25, 26, 29, 30, 31, 40, 41, 42], 'Onion, Chinese Bulb': [7, 14, 22, 25, 26, 29, 30, 31, 40, 41, 42], 'Onion, Fresh': [7, 14, 22, 25, 26, 29, 30, 31, 40, 41, 42], 'Onion, Green': [7, 14, 22, 25, 26, 29, 30, 31, 40, 41, 42], 'Onion, Macrostem': [7, 14, 22, 25, 26, 29, 30, 31, 40, 41, 42], 'Onion, Pearl': [7, 14, 22, 25, 26, 29, 30, 31, 40, 41, 42], 'Onion, Potato, Bulb': [7, 14, 25, 26, 29, 30, 31], 'Onion, Tree, Top': [7, 14, 22, 25, 26, 29, 30, 31], 'Onion, Welsh, Top': [7, 14, 22, 25, 26, 29, 30, 31], 'Orange, Tachibana': [7, 25, 26, 28, 29, 30, 31, 63], 'Orange, Trifoliate': [7, 25, 26, 28, 29, 30, 31, 63], 'Pea Eggplant': [7, 9, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Peach Palm': [7, 25, 26, 28, 30, 63], 'Pear, Asian': [7, 14, 26, 28, 29, 30, 31, 40, 41, 42], 'Pepper, Non-Bell': [7, 9, 24, 25, 26, 28, 29, 30, 31], 'Pequi': [7, 25, 26, 28, 30, 63], 'Pili Nut': [7, 25, 26, 28, 30, 63], 'Pine Nut': [7, 25, 26, 28, 30, 40, 41, 42, 63], 'Pine, Brazilian': [7, 25, 26, 28, 30, 63], 'Plum, American': [7, 14, 25, 26, 28, 29, 30, 31, 63], 'Plum, Beach': [7, 14, 25, 26, 28, 29, 30, 31, 63], 'Plum, Canada': [7, 14, 25, 26, 28, 29, 30, 31, 63], 'Plum, Cherry': [7, 14, 25, 26, 28, 29, 30, 31, 63], 'Plum, Klamath': [7, 14, 25, 26, 28, 29, 30, 31, 63], 'Prune-Plum': [7, 14, 25, 26, 28, 29, 30, 31, 63], 'Quince, Chinese': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Quince, Japanese': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Raspberry, Wild': [7, 28, 29, 31, 40, 41, 42, 63], 'Roselle': [7, 9, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Salal': [7, 10, 11, 22, 25, 26, 28, 29, 40, 41, 42], 'Sapucaia Nut': [7, 25, 26, 28, 30, 63], 'Sea-Buckthorn': [7, 10, 11, 25, 26, 28, 29, 40, 41, 42], 'Serviceberry, Saskatoon': [7, 10, 25, 26, 28, 29, 40, 41, 42], 'Shallot, Bulb': [7, 14, 25, 26, 29, 30, 31, 47], 'Shallot, Fresh Leaf': [7, 14, 25, 26, 29, 30, 31], 'Sloe': [7, 14, 25, 26, 28, 29, 30, 31, 63], 'Squash, Acorn': [7, 8, 9, 10, 22, 23, 27, 28, 29, 30, 40, 41, 42], 'Squash, Butternut': [7, 8, 9, 10, 22, 23, 27, 28, 29, 30, 40, 41, 42], 'Squash, Hubbard': [7, 8, 9, 10, 22, 23, 27, 28, 29, 30, 40, 41, 42], 'Squash, Spaghetti': [7, 8, 9, 10, 22, 23, 27, 28, 29, 30, 40, 41, 42], 'Sunberry': [7, 9, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42], 'Sunflower': [7, 15, 16, 23, 39, 40, 42], 'Tejocote': [7, 14, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Tomato Tree': [7, 9, 14, 25, 26, 28, 29, 30, 31], 'Turnip Greens': [7, 23, 24, 28], 'Uniq Fruit': [7, 25, 26, 28, 29, 30, 31, 40, 41, 42, 63], 'Vegetable, Brassica Leafy': [7, 15, 23, 26], 'Walnut, Persian': [7, 25], 'Yellowhorn': [7, 25, 26, 28, 30, 63], 'Bean, Asparagus': [8, 22, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Broad': [8, 23, 25, 26, 28, 39, 40, 41, 42], 'Bean, Chinese Long': [8, 22, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Jack': [8, 22, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Lima': [8, 9, 10, 15, 16, 22, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Runner': [8, 22, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Snap': [8, 15, 16, 22, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Sword': [8, 22, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Wax': [8, 22, 25, 26, 28, 29, 39, 40, 41, 42], 'Bean, Yardlong': [8, 22, 25, 26, 28, 29, 39, 40, 41, 42], 'Bluegrass': [8, 15, 39, 40, 41, 42], 'Buckwheat': [8, 10, 23, 28, 39, 40, 41, 42], 'Fennel, Finocchio': [8, 22, 25, 26, 28], 'Fescue': [8, 15, 39, 40, 41, 42], 'Grass, Fodder': [8, 28], 'Grass, Forage': [8, 28], 'Grass, Gramineal': [8, 28, 39, 41, 42], 'Grass, Hay': [8, 23, 28], 'Grass, Pasture': [8, 28], 'Grass, Seed': [8], 'Grass, Silage': [8, 28], 'Guar': [8, 11, 23, 24, 25, 28, 29, 39, 40, 41, 42], 'Millet, Pearl': [8, 10, 23, 28, 39, 40, 41, 42], 'Millet, Proso': [8, 10, 23, 28, 39, 40, 41, 42], 'Milo': [8, 28, 39, 41, 42, 57], 'Oat': [8, 10, 15, 17, 23, 28, 39, 40, 41, 42], 'Orchardgrass': [8, 15, 39, 40, 41, 42, 50, 52], 'Pea, Dwarf': [8, 22, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Pea, Edible-Podded': [8, 22, 25, 26, 28, 29, 39, 40, 41, 42], 'Pea, English': [8, 22, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Pea, Garden': [8, 22, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Pea, Green': [8, 22, 24, 25, 26, 28, 29, 39, 40, 41, 42], 'Pea, Snow': [8, 22, 25, 26, 28, 29, 39, 40, 41, 42], 'Pea, Sugar Snap': [8, 22, 25, 26, 28, 29, 39, 40, 41, 42], 'Range Grass': [8, 28], 'Rice, Wild': [8, 39, 40, 41, 42], 'Rye': [8, 10, 15, 23, 28, 39, 40, 41, 42, 52], 'Seakale': [8], 'Sorghum': [8, 15, 23, 28], 'Soybean, Immature Seed': [8, 22, 25, 26, 28, 39], 'Teosinte': [8, 23, 28, 39, 40, 41, 42], 'Triticale': [8, 10, 15, 17, 23, 28, 39, 40, 41, 42, 45, 46, 52], 'Vegetable, Legume': [8, 15, 26], 'Amaranth, Chinese': [9], 'Aster, Indian': [9], 'Black Jack': [9], 'Cats Whisker': [9], 'Cham-Chwi': [9], 'Chamnamul': [9], 'Chervil, Fresh Leaf': [9], 'Chipilin': [9], 'Cilantro, Leaf': [9, 22, 28, 41, 42], 'Cockscomb, Feather': [9], 'Cosmos': [9, 61], 'Cucurbit, Greenhouse': [9], 'Dandelion, Leaf': [9], 'Dang-Gwi, Leaf': [9], 'Dol-Namul': [9], 'Ebolo': [9], 'Fameflower': [9], 'Good-King-Henry': [9], 'Guava': [9, 22, 25, 26, 40, 41, 42], 'Huauzontle': [9], 'Jute, Leaf': [9], 'Lettuce, Bitter': [9], 'Lettuce, Leaf, Greenhouse': [9], 'Marrow Vegetable': [9, 10, 22, 23, 28, 40, 41, 42], 'Parsley, Fresh Leaf': [9], 'Pepper, Greenhouse': [9], 'Plantain, Buckhorn': [9], 'Primrose, English': [9], 'Squash, Crookneck': [9, 10, 22, 23, 28, 40, 41, 42], 'Squash, Scallop': [9, 10, 22, 23, 28, 40, 41, 42], 'Squash, Straightneck': [9, 10, 22, 23, 28, 40, 41, 42], 'Starfruit': [9, 22, 25, 26, 41, 42], 'Tanier Spinach': [9], 'Tomato, Greenhouse': [9], 'Violet, Chinese Leaf': [9], 'Zucchini': [9, 10, 22, 23, 28, 40, 41, 42], 'Beet, Table, For Seed': [10, 47], 'Brassica, For Seed': [10], 'Canola': [10, 11, 15, 16, 39, 41, 42], 'Chard, Swiss, For Seed': [10, 47], 'Conifer': [10], 'Crambe': [10, 11, 39, 40, 41, 42], 'Cuphea': [10, 40, 41, 42], 'Durum': [10, 12, 33, 34, 37, 43, 46, 48, 51], 'Echium': [10, 40, 41, 42], 'Gold-of-Pleasure': [10, 40, 41, 42], 'Hardwood Plantation': [10], 'Lesquerella': [10, 39, 40, 41, 42], 'Lunaria': [10], 'Meadowfoam': [10, 39, 40, 41, 42], 'Milkweed': [10, 40, 41, 42], 'Mustard': [10], 'Mustard, Ethiopian': [10], 'Mustard, Hares Ear': [10, 40, 41, 42], 'Mustard, Seed': [10, 40, 41, 42], 'Mustard, White': [10], 'Mustard, Yellow': [10], 'Pine': [10, 40, 41, 42], 'Pine, Loblolly': [10], 'Pine, Longleaf': [10], 'Pine, Shortleaf': [10], 'Pine, Slash': [10], 'Poppy, Seed': [10, 40, 41, 42], 'Radish, Oil': [10, 40, 41, 42], 'Rapeseed': [10, 11, 15, 16], 'Rapeseed, Indian': [10], 'Sesame': [10, 15, 16, 39, 40, 41, 42], 'Spinach, For Seed': [10, 47], 'Sweet Rocket': [10, 40, 41, 42], 'Wheat, Spring-Seeded': [10, 12, 50], 'Wheat, Winter': [10, 12, 37, 43, 45, 46, 48, 50, 51, 52], 'Cottonseed': [11, 28, 29], 'Cucumis melo': [11, 22, 28, 29, 30, 31], 'Serviceberry,Saskatoon': [11], 'Corn, For Seed': [12, 36, 53], 'Cucumber, Greenhouse': [14], 'Garlic, Great Headed': [14, 22, 25, 40, 41, 42], 'Onion, Welsh': [14, 40, 41, 42], 'Plum, Stanley': [14], 'Prune': [14, 15, 16, 23, 40, 41, 42, 63], 'Shallot': [14, 15, 16, 22, 40, 41, 42], 'Alfalfa': [15, 23, 28, 36, 41, 42], 'Animal Feed, Non-Grass': [15], 'Artichoke': [15, 16], 'Bean, Green': [15, 16, 29], 'Bean, Shell': [15, 16], 'Beet': [15, 16], 'Berry': [15, 16, 26], 'Cassava': [15], 'Castor': [15, 16, 40, 41, 42], 'Cereal Grain': [15], 'Clover': [15, 28, 40, 41, 42], 'Coffee': [15, 22, 25, 26, 40, 41, 42, 63], 'Corn': [15], 'Corn, Seed': [15, 23, 28, 39, 40, 41, 49, 54, 55, 56, 57, 58, 59, 60, 61], 'Corn, Silage': [15, 39, 40, 41, 42, 49, 53, 55, 56, 57, 58, 60, 61], 'Currant': [15, 16, 22], 'Fruit, Pome': [15, 16, 23, 26], 'Fruit, Stone': [15, 16, 23, 26], 'Garlic': [15, 16, 22, 40, 41, 42], 'Herb': [15, 16], 'Kiwifruit': [15, 16], 'Lettuce': [15, 16, 24, 29], 'Macadamia': [15, 16, 40, 42], 'Melon': [15, 16, 30, 40, 41, 42], 'Millet': [15], 'Mint': [15, 27], 'Nut Tree': [15, 16, 26], 'Oil Seed Crop': [15, 16], 'Olive': [15, 16, 40, 41, 42, 63], 'Onion': [15, 16, 22, 41, 42], 'Orange': [15, 16, 29, 40, 41, 42, 63], 'Pea, Split': [15, 16], 'Pomegranate': [15, 22, 25, 26, 28, 40, 41, 42], 'Raspberry': [15, 16, 22, 29], 'Ryegrass': [15, 39, 40, 41, 42], 'Safflower': [15, 16, 39, 40, 42], 'Spice': [15, 16], 'Squash': [15, 16, 28, 30], 'Sugarcane': [15, 23, 40, 41, 42], 'Tobacco': [15, 22, 29, 31], 'Vegetable, Bulb': [15, 16, 26], 'Vegetable, Fruiting': [15, 16, 26], 'Vegetable, Leafy': [15, 16, 23, 26], 'Vegetable, Legume, Dried': [15], 'Vegetable, Legume, Succulent': [15], 'Watercress': [15, 22, 25, 26, 42], 'Brassica': [16], 'Bushberry': [16, 22, 26], 'Caneberry': [16], 'Legume': [16], 'Palm, Oil': [16], 'Vegetable': [16], 'Vegetable, Corm': [16, 26], 'Vegetable, Root': [16], 'Vegetable, Tuber': [16], 'Pea, Dry': [18, 23, 41], 'Acerola': [22, 25, 26, 40, 41, 42], 'Anise, Sweet': [22, 28], 'Arrowroot, Queensland': [22], 'Atemoya': [22, 40, 41, 42], 'Bay, Sweet Leaf': [22], 'Bean, Black Eyed': [22], 'Berry, Black Satin': [22, 40, 41, 42], 'Berry, Dirksen Thornless': [22, 40, 41, 42], 'Berry, Oregon Evergreen': [22, 40, 41, 42], 'Biriba': [22, 40, 41, 42], 'Blackberry, Cherokee': [22, 40, 41, 42], 'Blackberry, Cheyenne': [22, 40, 41, 42], 'Blackberry, Mammoth': [22, 40, 41, 42], 'Blackberry, Marion': [22], 'Blackberry, Shawnee': [22, 40, 41, 42], 'Boysenberry': [22, 40, 41, 42], 'Celery, Chinese Fresh Leaf': [22], 'Celery, Chinese Stalk': [22], 'Chamomile': [22, 40], 'Cherimoya': [22, 40, 41, 42], 'Chesterberry': [22, 40, 41, 42], 'Christmas Tree': [22, 23, 40, 41, 42], 'Citrullus': [22], 'Cocoyam': [22, 28], 'Coriander': [22], 'Coryberry': [22, 40, 41, 42], 'Cottonwood': [22], 'Cress, Yellow Rocket': [22, 24, 25, 26, 28], 'Custard Apple': [22, 40, 41, 42], 'Darrowberry': [22, 40, 41, 42], 'Dewberry': [22, 40, 41, 42], 'Feijoa': [22, 25, 26, 40, 41, 42], 'Fennel, Sweet': [22, 28], 'Grape, American Bunch': [22], 'Grape, Muscadine': [22, 23, 24], 'Grape, Vinifera': [22], 'Himalayaberry': [22, 40, 41, 42], 'Hullberry': [22, 40, 41, 42], 'Ilama': [22, 40, 42], 'Jaboticaba': [22, 25, 26, 40, 41, 42], 'Jambu, Wax': [22, 25, 26, 40, 41, 42], 'Jicama': [22, 28], 'Kava': [22, 28, 40], 'Lavacaberry': [22, 40, 41, 42], 'Longan': [22, 25, 26, 40, 41, 42], 'Lowberry': [22, 40, 41, 42], 'Lucretiaberry': [22, 40, 41, 42], 'Lychee': [22, 25, 26, 40, 41, 42], 'Manoic Pea': [22, 28], 'Marionberry': [22, 40, 41, 42], 'Melon, Winter': [22], 'Nectarberry': [22, 40, 41, 42], 'Olallieberry': [22, 40, 41, 42], 'Onion, Potato': [22, 25, 40, 41, 42], 'Oyster Plant': [22, 28], 'Passion Fruit': [22, 25, 26, 40, 41, 42], 'Persimmon': [22, 25, 26, 28, 40, 41, 42], 'Phenomenalberry': [22, 40, 41, 42], 'Poplar': [22, 40, 41, 42], 'Prune, Dried': [22, 23, 25], 'Pulasan': [22, 25, 26, 28, 40, 41, 42], 'Pumpkin, Cuban': [22], 'Rambutan': [22, 25, 26, 40, 41, 42], 'Rangerberry': [22, 40], 'Ravenberry': [22, 40, 41, 42], 'Rossberry': [22, 40, 41, 42], 'Sapote, White': [22, 23, 24, 25, 26, 28, 40, 41, 42], 'Soursop': [22, 40, 41, 42], 'Spanish Lime': [22, 25, 26, 40, 41, 42], 'Strawberry, Annual': [22], 'Strawberry, Perennial': [22], 'Sugar Apple': [22, 40, 41, 42], 'Watercress, Upland': [22, 40, 41, 42], 'Youngberry': [22, 40, 41, 42], 'Chayote': [23], 'Cole Crop': [23, 26], 'Grape, Raisin': [23, 24], 'Grape, Table': [23, 24], 'Grape, Wine': [23, 24], 'Grass, Alfalfa Mixture': [23], 'Pasture': [23, 40, 41], 'Rangeland': [23, 39, 40, 41, 42], 'Bean, Dry Shelled': [24, 25, 26, 28], 'Lentil, Dry': [24], 'Lupine': [24, 40, 41, 42], 'Pea, Dry Pigeon': [24], 'Pea, Dry Shelled': [24, 25, 26, 28], 'Pisum': [24, 41], 'Vigna': [24], 'Allium': [25], 'Bean, Edible-Podded': [25, 26, 28], 'Bean, Succulent Shelled': [25, 26, 28], 'Christmas Tree Plantation': [25, 26], 'Onion, Bentsville Bunching': [25], 'Pea, Succulent Shelled': [25, 26, 28], 'Pepper, Cayenne': [25, 26], 'Pepper, Habanero': [25, 26], 'Pepper, Jalapeno': [25, 26], 'Pepper, Poblano': [25, 26], 'Pepper, Serrano': [25, 26], 'Taro, Leaf': [25, 26, 28], 'Fruit, Small': [26], 'Vegetable, Tuberous': [26], 'Carrot, For Seed': [27], 'Yam': [27], 'Abiu': [28], 'Akee Apple': [28], 'Bacuri': [28], 'Binjai': [28], 'Celeriac, Celery Root': [28], 'Clover, For Seed': [28], 'Cupuacu': [28], 'Cushaw': [28], 'Imbe': [28, 40, 41, 42], 'Jatoba': [28], 'Kava, Turnip-Rooted': [28, 41, 42], 'Kei Apple': [28], 'Langsat': [28], 'Lanjut': [28], 'Lucuma': [28], 'Mabolo': [28], 'Mandarin Orange': [28], 'Mandarin, Clementine': [28, 63], 'Mangosteen': [28, 40, 41, 42], 'Paho': [28], 'Pawpaw': [28, 40, 41, 42], 'Pepper, Hot': [28], 'Poshte': [28], 'Quandong': [28], 'Quinoa': [28, 39, 40, 41, 42], 'Sapote, Green': [28], 'Sataw': [28], 'Screw Palm': [28], 'Sorghum, Sweet': [28], 'Squash, Summer Crookneck': [28], 'Squash, Summer Scallop': [28], 'Squash, Summer Straightneck': [28], 'Tamarind': [28, 40, 41, 42], 'Bean, Lupin, Dry': [29], 'Bean, Moth, Dry Shelled': [29], 'Bean, Moth, Edible-Podded': [29], 'Bean, Phaseolus, Dry Shelled': [29], 'Bean, Phaseolus, Edible-Podded': [29], 'Bean, Succulent Broad': [29], 'Bean, Succulent Phaseolus': [29], 'Bean, Succulent Vigna': [29], 'Bean, Vigna, Dry Shelled': [29], 'Bean, Vigna, Edible-Podded': [29], 'Pea, Pigeon, Edible-Podded': [29], 'Pea, Pisum, Edible-Podded': [29], 'Pea, Succulent Pigeon': [29], 'Pea, Succulent Pisum': [29], 'Soybean 2, Roundup Ready': [35, 36, 40, 41, 42], 'Soybean, Roundup Ready': [35, 36, 40, 41, 42], 'Alfalfa, Roundup Ready': [36, 40, 41, 42], 'Corn 2, Hybrid, Roundup Ready': [36], 'Cotton, Flex, Roundup Ready': [36, 40, 41, 42], 'Cotton, Roundup Ready': [36, 40, 41, 42], 'Sorghum, Forage': [36, 50, 52], 'Sorghum, Grain': [36, 39, 40, 41, 42, 50, 52, 57], 'Wheat, Spring': [37, 43, 46, 48, 51, 52], 'Corn 2, Roundup Ready': [38, 41, 42, 53, 57], 'Corn, Field, Conventional Tillage': [38, 54, 57], 'Corn, Field, Herbicide Tolerant': [38], 'Corn, Field, Liberty Link': [38], 'Corn, Field, No-Till': [38, 54], 'Corn, Field, Reduced Tillage': [38, 57], 'Corn, Silage, Conventional Tillage': [38, 57], 'Corn, Silage, Herbicide Tolerant': [38], 'Corn, Silage, Liberty Link': [38], 'Corn, Silage, No-Till': [38], 'Corn, Silage, Reduced Tillage': [38, 57], 'Bahiagrass': [39, 40, 41, 42], 'Bermudagrass': [39, 40, 41, 42], 'Borage, Oil Seed': [39, 41, 42], 'Bromegrass': [39, 40, 41, 42], 'Building, Foundation': [39, 40, 41, 42], 'Canal, Dry': [39, 41, 42], 'Conservation Reserve Program': [39, 40, 41, 42, 50, 52], 'Ditch, Dry': [39, 40, 41, 42], 'Ditchbank, Along': [39, 40, 41, 42], 'Equipment Storage Area': [39, 40, 41, 42], 'Fallow System': [39, 40, 41, 42], 'Farm Road': [39, 40, 41, 42], 'Farmstead': [39, 40, 41, 42, 63], 'Fence': [39, 40, 41, 42], 'Fence, Along': [39, 40, 41, 42], 'Gourd, Buffalo, Oil Seed': [39, 41, 42], 'Grass, For Sod': [39, 40, 41, 42], 'Guineagrass': [39, 40, 41, 42], 'Habitat Management': [39, 40, 41, 42], 'Jojoba': [39, 40, 41, 42], 'Kikuyugrass': [39, 40, 41, 42], 'Landscape Planting': [39, 42], 'Mustard, Oil Seed': [39, 41, 42], 'Pangola Grass': [39, 40, 41, 42], 'Rape': [39, 40, 41, 42], 'Ryegrass, Annual': [39, 41, 42, 47, 50, 52], 'Shelterbelt': [39, 40, 41, 42], 'Storage Area': [39, 41, 42], 'Teff': [39, 40, 41, 42], 'Timothy': [39, 40, 41, 42, 50, 52], 'Wheatgrass': [39, 40, 41, 42], 'Wildlife Food Plot': [39, 40, 41, 42], 'Alfalfa, Conventional': [40], 'Allspice': [40, 41, 42], 'Aloe, Vera': [40, 41, 42], 'Ambarella': [40, 41, 42], 'Anise, Star': [40, 41, 42], 'Annatto': [40], 'Aster, Stokes': [40, 41, 42], 'Bamboo Shoot': [40, 41, 42], 'Bayberry': [40, 41, 42], 'Beet Greens': [40, 41, 42], 'Beet, Sugar, Conventional': [40], 'Beet, Sugar, Roundup Ready': [40, 41, 42], 'Betelnut': [40, 41, 42], 'Bingleberry': [40, 41, 42], 'Blackberry, Andean': [40, 41, 42], 'Blackberry, Arctic': [40, 41, 42], 'Blackberry, California': [40, 41, 42], 'Blackberry, Common': [40, 41, 42], 'Blackberry, Evergreen': [40, 41, 42], 'Blimbe': [40, 41, 42], 'Breadfruit': [40, 41, 42], 'Brombeere': [40, 41, 42], 'Buffaloberry': [40, 41, 42], 'Burdock': [40, 41, 42], 'Cacao': [40, 41, 42], 'Cactus': [40, 41, 42], 'Calendula': [40, 41, 42], 'Canal': [40], 'Canna': [40, 41, 42], 'Canola, Conventional': [40], 'Canola, Spring, Roundup Ready': [40, 41, 42], 'Canola, Tru': [40, 41], 'Flex, Roundup Ready': [40, 41], 'Canola, Winter, Roundup Ready': [40, 41, 42], 'Caper Bud': [40, 41, 42], 'Carambola': [40, 41, 42], 'Caraway': [40, 41, 42], 'Caraway, Black': [40, 41, 42], 'Cardamom': [40, 41, 42], 'Cassia Bark': [40, 41, 42], 'Cassia Bud': [40, 41, 42], 'Celery, Seed': [40, 41, 42], 'Chaya': [40, 41, 42], 'Che': [40, 41, 42], 'Cherry, Pin': [40, 41, 42], 'Chokecherry': [40, 41, 42], 'Cinnamon': [40, 41, 42], 'Clove Bud': [40, 41, 42], 'Coriander, Seed': [40, 41, 42], 'Corn 2, Field Hybrid, Roundup Ready': [40, 41, 42], 'Corn 2, Sweet, Roundup Ready': [40, 41, 42], 'Corn, Agrisure GTCorn, Field': [40, 41], 'Cotton, Conventional': [40], 'Culantro, Seed': [40, 41, 42], 'Cumin': [40, 41, 42], 'Daylily': [40, 41, 42], 'Dewberry, Northern': [40, 41, 42], 'Dewberry, Southern': [40, 41, 42], 'Dill': [40, 41, 42], 'Dokudami': [40, 41, 42], 'Dragon Fruit': [40, 41, 42], 'Durian': [40, 41, 42], 'Epazote': [40, 41, 42], 'Eucalyptus': [40, 41, 42], 'Evening Primrose': [40, 41, 42], 'Fennel, Common, Seed': [40, 41, 42], 'Fennel, Florence, Seed': [40, 41, 42], 'Fenugreek': [40, 41, 42], 'Fig': [40, 41, 42], 'Galangal': [40, 41, 42], 'Ginger, White': [40, 41, 42], 'Gourd, Buffalo': [40], 'Governors Plum': [40, 41, 42], 'Gow Kee': [40, 41, 42], 'Grains of Paradise': [40, 41, 42], 'Greenhouse': [40, 41, 42], 'Imbu': [40, 41, 42], 'Jackfruit': [40, 41, 42], 'Juniper Berry': [40, 41, 42], 'Kenaf': [40, 41, 42], 'Kiwifruit, Fuzzy': [40, 41, 42], 'Kudzu': [40, 41, 42], 'Landscape Plant': [40], 'Lespedeza': [40, 41, 42], 'Leucaena': [40, 41, 42], 'Lovage, Seed': [40, 41, 42], 'Mace': [40, 41, 42], 'Mamey Apple': [40, 41, 42], 'Marmaladebox': [40, 41, 42], 'Mora Berry': [40, 41, 42], 'Mulberry': [40, 41, 42], 'Mures Deronce': [40, 41, 42], 'Myoga': [40, 41, 42], 'Niger, Seed': [40, 41, 42], 'Non-Crop Area': [40], 'Noni': [40, 41, 42], 'Nutmeg': [40, 41, 42], 'Onion, Tree': [40, 41, 42], 'Oregano, Mexican': [40, 41, 42], 'Palm': [40, 41, 42], 'Palm, Date': [40], 'Papaya, Mountain': [40, 41, 42], 'Pepper, Black': [40, 41, 42], 'Pepper, Leaf': [40, 41, 42], 'Pepper, White': [40, 41, 42], 'Pepperberry, Mountain': [40, 41, 42], 'Peppermint': [40, 41, 42], 'Perilla': [40, 41, 42], 'Phalsa': [40, 41, 42], 'Poppy': [40], 'Prickly Pear, Cactus': [40, 41, 42], 'Riberry': [40, 41, 42], 'Rose Apple': [40, 41, 42], 'Rose Hip': [40, 41, 42], 'Saffron': [40, 41, 42], 'Sainfoin': [40, 41, 42], 'Serviceberry': [40, 41, 42], 'Shadehouse': [40, 41, 42], 'Soybean, Conventional': [40], 'Soybean, Enlist E3Soybean, GT 27Soybean, Immature Seed': [40, 41, 42], 'Spearmint': [40, 41, 42], 'Spinach, Water': [40, 41, 42], 'Stevia, Leaf': [40, 41, 42], 'Surinam Cherry': [40, 41, 42], 'Tallow Tree, Chinese': [40, 41, 42], 'Tallowwood': [40, 41, 42], 'Tayberry': [40, 41, 42], 'Tea': [40, 41, 42], 'Tea Oil Plant': [40, 41, 42], 'Ti': [40, 41, 42], 'Tree, Ornamental': [40], 'Trefoil': [40, 41, 42], 'Vanilla': [40, 41, 42], 'Velvetbean': [40, 41, 42], 'Vernonia': [40, 41, 42], 'Vetch': [40, 41, 42], 'Wasabi': [40, 41, 42], 'Yacon': [40, 41, 42], 'Zarzamora': [40, 41, 42], 'Annatto, Seed': [41, 42], 'Barbados Cherry': [41, 42], 'Cilantro, Seed': [41, 42], 'Cocoa Bean': [41, 42], 'Corn, Sweet, Roundup Ready': [41], 'Date': [41, 42], 'Driveway': [41, 42], 'Euphorbia': [41, 42], 'Farmyard': [41, 42], 'Fence Row': [41, 42], 'Fruit, Ugli': [41, 42], 'Genip': [41, 42], 'Ginseng, Non-Bearing': [41, 42], 'Landscape Ornamental': [41], 'Llama': [41], 'Mulberry, Indian': [41, 42], 'Non-Food Crop': [41], 'Parking Area': [41, 42], 'Parsley, Chinese Leaf': [41], 'Poppy, Oil Seed': [41, 42], 'Pummello': [41], 'Rangeberry': [41, 42], 'Right-of-Way': [41, 42], 'Safflower, Oil Seed': [41], 'Sunflower, Oil Seed': [41], 'Terrestrial Site': [41, 42], 'Cherry, Sour': [42], 'Corn 2, Field Hybrid Seed, Roundup Ready': [42], 'Corn, Field, Agrisure GTCorn, Seed': [42], 'Cotton, Gly': [42], 'Tol': [42], 'Fallow Land, Rice': [42], 'Legume, Forage': [42], 'Soybean, Roundup Ready 2 Xtend': [42], 'Spring Canola, Truflex, Roundup Ready': [42], 'Tillage System': [42], 'Tree Crop, Non-Food': [42], 'Triticale, Fall-Seeded': [45], 'Wheat, Fall-Seeded': [45], 'Beet, Table': [47], 'Bentgrass': [47], 'Bluegrass, Kentucky': [47, 50, 52], 'Fescue, Tall': [47, 50, 52], 'Fescue, Tall, For Sod': [47], 'Ryegrass, Perennial': [47, 50, 52], 'Ryegrass, Perennial, For Sod': [47], 'Corn, Glyphosate-Tolerant': [49], 'Barley, Spring-Seeded': [50], 'Barley, Winter': [50, 52], 'Durum, Spring-Seeded': [50, 52], 'Fescue, Fine': [50, 52], 'Rye, Spring-Seeded': [50], 'Triticale, Spring-Seeded': [50], 'Barley, Spring': [52], 'Miscanthus': [53, 57], 'Non-Food Perennial Bioenergy Crop': [53, 57], 'Corn, Field, Conservation Tillage': [54, 57], 'Corn, Seed, Conservation Tillage': [54], 'Corn, Seed, Conventional Tillage': [54, 57], 'Corn, Seed, No-Till': [54], 'Popcorn, Conservation Tillage': [54, 57], 'Popcorn, Conventional Tillage': [54, 57], 'Popcorn, No-Till': [54], 'Crop Stubble': [56, 62], 'Fallow Land': [56, 58, 62], 'Corn, For Seed, Conservation Tillage': [57], 'Corn, Seed, Reduced Tillage': [57], 'Corn, Silage, Conservation Tillage': [57], 'Corn, Sweet, Conservation Tillage': [57], 'Corn, Sweet, Conventional Tillage': [57], 'Corn, Sweet, Reduced Tillage': [57], 'Popcorn, Reduced Tillage': [57], 'Eco-Fallow': [58], 'Corn, Field, For Silage': [59], 'Corn, White': [59, 61], 'Corn, Field, Glyphosate-Tolerant': [60], 'Baby Blue Eyes': [61], 'Bermudagrass, For Seed': [61], 'Blackeyed Susan': [61], 'Catchfly': [61], 'Coreopsis, Lance Leaved': [61], 'Coreopsis, Plains': [61], 'Cosmos, Sulfur': [61], 'Daisy, Gloriosa': [61], 'Daisy, Oxeye': [61], 'Dames-Rocket': [61], 'Fescue, Fine, For Seed': [61], 'Fescue, Tall, For Seed': [61, 63], 'Fir, Douglas, Plantation': [61], 'Fir, Fraser, Plantation': [61], 'Fir, Grand, Plantation': [61], 'Fir, Noble, Plantation': [61], 'Fir, Nordmann, Plantation': [61], 'Fir, True, Plantation': [61], 'Orchardgrass, For Seed': [61], 'Poppy, California': [61], 'Fallow Land, Corn, For Seed': [62], 'Fallow Land, Field Corn': [62], 'Fallow Land, Soybean': [62], 'Fallow Land, Wheat': [62], 'Fallow Land, White Corn': [62], 'Blueberry, Rabbiteye': [63], 'Bromegrass, Smooth, For Seed': [63], 'Ryegrass, Perennial, For Seed': [63], 'Timothy, For Seed': [63], 'Wheatgrass, For Seed': [63]}

# Create your views here.
def home(request):
    return render(request, 'app1/home.html')

def explore(request):
    states = ['AL',
            'AR',
            'CO',
            'DE',
            'FL',
            'GA',
            'ID',
            'IL',
            'IN',
            'KS',
            'KY',
            'LA',
            'MD',
            'MI',
            'MN',
            'MO',
            'MS',
            'MT',
            'NC',
            'ND',
            'NE',
            'NM',
            'NY',
            'OH',
            'OK',
            'OR',
            'PA',
            'SC',
            'SD',
            'TN',
            'TX',
            'UT',
            'VA',
            'WA',
            'WI',
            'WY',
            'IA',
            'CA',
            'AK',
            'AZ',
            'CT',
            'HI',
            'MA',
            'ME',
            'NH',
            'NJ',
            'NV',
            'RI',
            'VT',
            'WV',
            'PR',
            'DC',
            'AS',
            'FM',
            'GU',
            'MH',
            'MP',
            'PW',
            'VI']
    types = ['F', 'HE', 'HA', 'I']
    data = {
        'states': states,
        'types': types,
    }

    return render(request, 'app1/explore_prod.html', data)

def filterproduct(request):
    if request.method == 'POST':
        index = [i for i in range(64)]
        result = "NOT NIL"
        productname = ''
        f_product_name = []
        f_product_type = []
        f_product_crop = []
        f_product_state = []
        f_product_pest = []
        f_key_benefit = []
        f_product_description = []
        f_use_mix = []
        input1, input2, input3, input4, input5 = '', '', '', '', ''
        crop_flag = 0
        state_flag = 0
        pest_flag = 0
        try:
            productname = request.POST['productname']
            input1 = productname
        except:
            pass
        cropname = ''
        try:
            cropname = request.POST['cropname']
            input2 = cropname
        except:
            pass
        state = ''
        try:
            state = request.POST['state']
            input3 = state
        except:
            pass
        pests = ''
        try:
            pests = request.POST['pests']
            input4 = pests
        except:
            pass
        producttype = ''
        try:
            producttype = request.POST['producttype']
            if(producttype == 'F'):
                input5 = 'Fungicides'
            elif(producttype == 'HE'):
                input5 = 'Herbicides'
            elif(producttype == 'HA'):
                input5 = 'Harvest Aids'
            else:
                input5 = 'Insecticides'
        except: 
            pass

        input_parameters = []
        flag = 0
        if(input1!=''):
            input_parameters.append("Product Name: " + input1)
        if(input2!=''):
            input_parameters.append("Crop Name: " + input2)
        if(input3!=''):
            input_parameters.append("State: " + input3)
        if(input4!=''):
            input_parameters.append("Pest: " + input4)
        if(input5!=''):
            input_parameters.append("Product Type: " + input5)
        if(len(input_parameters)):
            flag = 1
        if productname:
            try:
                current_index = [prod_dict[productname]]
                index = list(set(index) & set(current_index))
            except:
                result = "NIL"
                pass
        if cropname:
            try:
                current_index = crop_dict[cropname]
                index = list(set(index) & set(current_index))
                f_product_crop.append(cropname)
            except:
                result = "NIL"
                pass
        if state:
            try:
                current_index = state_dict[state]
                index = list(set(index) & set(current_index))
                f_product_state.append(state)
            except:
                result = "NIL"
                pass
        if pests:
            try:
                current_index = pest_dict[pests]
                index = list(set(index) & set(current_index))
                f_product_pest.append(pests)
            except:
                result = "NIL"
                pass
        if producttype:
            try:
                current_index = []
                for i in range(len(df)):
                    if producttype == df.iloc[i]['product_type']:
                        current_index.append(i)
                index = list(set(index) & set(current_index))
            except:
                result = "NIL"
                pass
        
        if result == 'NIL' or len(index) == 0:
            index = ['No Result Found']
            length = []
        else:
            for val in index:
                f_product_name.append(df.iloc[val]['product_name'])
                productType = df.iloc[val]['product_type']
                if(productType == 'F'):
                    f_product_type.append('Fungicides')
                elif(productType == 'HE'):
                    f_product_type.append('Herbicides')
                elif(productType == 'HA'):
                    f_product_type.append('Harvest Aids')
                else:
                    f_product_type.append('Insecticides')
                #f_product_type.append(df.iloc[val]['product_type'])
                f_key_benefit.append(df.iloc[val]['key_benefits'])
                f_product_description.append(df.iloc[val]['safety_ins'])
                f_use_mix.append(df.iloc[val]['use&mix'])
            if(len(f_product_crop) == 0):
                crop_flag = 0
                for val in index:
                    f_product_crop.append(df.iloc[val]['registered_crops'])
            else:
                crop_flag = 1
            if(len(f_product_state) == 0):
                state_flag = 0
                for val in index:
                    f_product_state.append(df.iloc[val]['geo_location'])
            else:
                state_flag = 1
            if(len(f_product_pest) == 0):
                pest_flag = 0
                for val in index:
                    f_product_pest.append(df.iloc[val]['effective_against'])
            else:
                pest_flag = 1
            length = [i for i in range(len(f_product_name))]
        for i in range(len(f_key_benefit)):
            f_key_benefit[i] = f_key_benefit[i][1:-1]
            f_key_benefit[i] = f_key_benefit[i].split(",")
            print(f_key_benefit[i])
        for i in range(len(f_product_crop)):
            f_product_crop[i] = f_product_crop[i][1:-1]
            f_product_crop[i] = f_product_crop[i].split("',")
        for i in range(len(f_product_pest)):
            f_product_pest[i] = f_product_pest[i][1:-1]
            f_product_pest[i] = f_product_pest[i].split("',")
        for i in range(len(f_product_state)):
            f_product_state[i] = f_product_state[i][1:-1]
            f_product_state[i] = f_product_state[i].split(',')
        length_length = len(length)
        data = {
            'indexes':index,
            'product_name':f_product_name,
            'product_type':f_product_type,
            'registered_crops':f_product_crop,
            'geo_location':f_product_state,
            'effective_against':f_product_pest,
            'key_benefits':f_key_benefit,
            'safety_ins':f_product_description,
            'use_mix':f_use_mix,
            'length':length,
            'inputs':input_parameters,
            'flag':flag,
            'length_length':length_length,
            'crop_flag':crop_flag,
            'state_flag':state_flag,
            'pest_flag':pest_flag,
        }
        return render(request, 'app1/prod_result.html', data)

def crop_recommend(request):
    return render(request, 'app1/crop_recommend.html')

def result(request):
    if request.method == 'POST':
        prediction = ''
        try:
            nitrogen = float(request.POST['nitrogen'])
            phosphorus = float(request.POST['phosphorus'])
            potassium = float(request.POST['potassium'])
            temperature = float(request.POST['temperature'])
            humidity = float(request.POST['humidity'])
            ph = float(request.POST['ph'])
            rainfall = float(request.POST['rainfall'])

            data = [[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]]
            prediction = model.predict(data)[0]
        except:
            prediction = 'Sorry, Failed to recommend!!'
        
        data = {
            'prediction':prediction,
        }
        return render(request, 'app1/crop_recommend.html', data)

def feedback(request):
    if request.method == 'POST':
        first = request.POST['first']
        last = request.POST['last']
        email = request.POST['email']
        message = request.POST['message']
        """ print("first_name:", first)
        print("last_name:", last)
        print("email:", email)
        print("message:", message) """

        contact = Contact(first_name=first, last_name=last, email=email, message=message)

        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email

        send_mail(
                'New Feedback',
                'You have a new inquiry, ' + 'Please login to your admin panel for more info.',
                'bharadwajshreenath@gmail.com',
                [admin_email],
                fail_silently=True,
            )

        contact.save()
        messages.success(request, "Thank you for your feedback, we will get back to you shortly!!")
        return redirect('/feedback')
    return render(request, 'app1/feedback.html')

def trace(request):
    if request.method == 'POST':
        message = ''
        orderid = int(request.POST['orderId'])
        print("orderid:", orderid)
        try:
            order = OrderUpdate.objects.all().filter(order_id=orderid)
            #print(order.values_list('update_desc'))
            update = list(order.values_list('update_desc'))[0][0].split(',')
            arrived = list(order.values_list('arrived'))[0][0].split(',')
            dispatched = list(order.values_list('dispatched'))[0][0].split(',')
            arrived_date = list(order.values_list('arrived_date'))[0][0].split(',')
            dispatched_date = list(order.values_list('dispatched_date'))[0][0].split(',')
            arrived_time = list(order.values_list('arrived_time'))[0][0].split(',')
            dispatched_time = list(order.values_list('dispatched_time'))[0][0].split(',')
            """ print("update:", update)
            print("arrived:", arrived)
            print("arrived_date:",arrived_date)
            print("arrived_time:", arrived_time) """
            length = len(update)
            updations = []
            for i in range(length):
                sub = []
                if(i == 0):
                    sub.append(update[i])
                    sub.append('')
                    if(dispatched[i] == 'Y'):
                        sub.append('Dispatched on '+ dispatched_date[i]+ ' at '+ dispatched_time[i])
                elif(i!=length-1):
                    sub.append(update[i])
                    if(arrived[i] == 'Y'):
                        sub.append('Arrived on '+ arrived_date[i]+ ' at '+ arrived_time[i])
                    else:
                        sub.append('')
                    if(dispatched[i] == 'Y'):
                        sub.append('Dispatched on '+ dispatched_date[i]+ ' at '+ dispatched_time[i])
                    else:
                        sub.append('')
                else:
                    sub.append('Dest.')
                    if(arrived[i] == 'Y'):
                        sub.append('Arrived at '+ arrived_date[i]+ ' on '+ arrived_time[i])
                    else:
                        sub.append('')
                    sub.append('')
                updations.append(sub)
            #print("updations:", updations)
            message = "Your order has been placed!!"
            data = {
                'updations': updations,
                'message':message,
                'length':[0, 1, 2],
            }

        except:
            message = "No order with this order id exist"
            #print("qwerty")
            data = {
                'message':message,
            }

        return render(request, 'app1/trace.html', data)
    return render(request, 'app1/trace.html')

def authenticate(request):

    if request.method == 'POST':
        auth = request.POST['code']
        auth_secret = list(authenticator.objects.values_list('auth_secret'))
        claimed = list(Claimed.objects.values_list('auth_secret'))
        codes = []
        claimed_codes = []
        for secret in auth_secret:
            codes.append(secret[0])
        for secret in claimed:
            claimed_codes.append(secret[0])
        ''' print("secret:", codes)
        print("claimed:", claimed[0][0]) '''
        index = -1
        claimed = -1
        for i in range(len(codes)):
            if auth == codes[i]:
                index = i
        for i in range(len(claimed_codes)):
            if auth == claimed_codes[i]:
                claimed = 1
                break
        if(index == -1):
            message = "This code is not authenticated!!"
        elif(claimed == 1):
            message = "This code is already claimed!!"
        else:
            message = 'This product is authenticated!!'
        claimed = Claimed(auth_secret = auth)
        claimed.save()
        data = {
            'message':message,
        }
        return render(request, 'app1/authenticate.html', data)

    return render(request, 'app1/authenticate.html')

def absolute(request):
    index = [0]
    f_product_name = []
    f_product_type = []
    f_product_crop = []
    f_product_state = []
    f_product_pest = []
    f_key_benefit = []
    f_product_description = []
    f_use_mix = []
    for val in index:
        f_product_name.append(df.iloc[val]['product_name'])
        productType = df.iloc[val]['product_type']
        if(productType == 'F'):
            f_product_type.append('Fungicides')
        elif(productType == 'HE'):
            f_product_type.append('Herbicides')
        elif(productType == 'HA'):
            f_product_type.append('Harvest Aids')
        else:
            f_product_type.append('Insecticides')
        #f_product_type.append(df.iloc[val]['product_type'])
        f_key_benefit.append(df.iloc[val]['key_benefits'])
        f_product_description.append(df.iloc[val]['safety_ins'])
        f_use_mix.append(df.iloc[val]['use&mix'])
    if(len(f_product_crop) == 0):
        crop_flag = 0
        for val in index:
            f_product_crop.append(df.iloc[val]['registered_crops'])
    else:
        crop_flag = 1
    if(len(f_product_state) == 0):
        state_flag = 0
        for val in index:
            f_product_state.append(df.iloc[val]['geo_location'])
    else:
        state_flag = 1
    if(len(f_product_pest) == 0):
        pest_flag = 0
        for val in index:
            f_product_pest.append(df.iloc[val]['effective_against'])
    else:
        pest_flag = 1
    length = [i for i in range(len(f_product_name))]
    for i in range(len(f_key_benefit)):
        f_key_benefit[i] = f_key_benefit[i][1:-1]
        f_key_benefit[i] = f_key_benefit[i].split(",")
        print(f_key_benefit[i])
    for i in range(len(f_product_crop)):
        f_product_crop[i] = f_product_crop[i][1:-1]
        f_product_crop[i] = f_product_crop[i].split("',")
    for i in range(len(f_product_pest)):
        f_product_pest[i] = f_product_pest[i][1:-1]
        f_product_pest[i] = f_product_pest[i].split("',")
    for i in range(len(f_product_state)):
        f_product_state[i] = f_product_state[i][1:-1]
        f_product_state[i] = f_product_state[i].split(',')
    length_length = len(length)
    data = {
        'indexes':index,
        'product_name':f_product_name,
        'product_type':f_product_type,
        'registered_crops':f_product_crop,
        'geo_location':f_product_state,
        'effective_against':f_product_pest,
        'key_benefits':f_key_benefit,
        'safety_ins':f_product_description,
        'use_mix':f_use_mix,
        'length':length,
        'length_length':length_length,
        'crop_flag':crop_flag,
        'state_flag':state_flag,
        'pest_flag':pest_flag,
    }
    
    return render(request, 'app1/product.html', data) 

def wolverine(request):
    index = [33]
    f_product_name = []
    f_product_type = []
    f_product_crop = []
    f_product_state = []
    f_product_pest = []
    f_key_benefit = []
    f_product_description = []
    f_use_mix = []
    for val in index:
        f_product_name.append(df.iloc[val]['product_name'])
        productType = df.iloc[val]['product_type']
        if(productType == 'F'):
            f_product_type.append('Fungicides')
        elif(productType == 'HE'):
            f_product_type.append('Herbicides')
        elif(productType == 'HA'):
            f_product_type.append('Harvest Aids')
        else:
            f_product_type.append('Insecticides')
        #f_product_type.append(df.iloc[val]['product_type'])
        f_key_benefit.append(df.iloc[val]['key_benefits'])
        f_product_description.append(df.iloc[val]['safety_ins'])
        f_use_mix.append(df.iloc[val]['use&mix'])
    if(len(f_product_crop) == 0):
        crop_flag = 0
        for val in index:
            f_product_crop.append(df.iloc[val]['registered_crops'])
    else:
        crop_flag = 1
    if(len(f_product_state) == 0):
        state_flag = 0
        for val in index:
            f_product_state.append(df.iloc[val]['geo_location'])
    else:
        state_flag = 1
    if(len(f_product_pest) == 0):
        pest_flag = 0
        for val in index:
            f_product_pest.append(df.iloc[val]['effective_against'])
    else:
        pest_flag = 1
    length = [i for i in range(len(f_product_name))]
    for i in range(len(f_key_benefit)):
        f_key_benefit[i] = f_key_benefit[i][1:-1]
        f_key_benefit[i] = f_key_benefit[i].split(",")
        print(f_key_benefit[i])
    for i in range(len(f_product_crop)):
        f_product_crop[i] = f_product_crop[i][1:-1]
        f_product_crop[i] = f_product_crop[i].split("',")
    for i in range(len(f_product_pest)):
        f_product_pest[i] = f_product_pest[i][1:-1]
        f_product_pest[i] = f_product_pest[i].split("',")
    for i in range(len(f_product_state)):
        f_product_state[i] = f_product_state[i][1:-1]
        f_product_state[i] = f_product_state[i].split(',')
    length_length = len(length)
    data = {
        'indexes':index,
        'product_name':f_product_name,
        'product_type':f_product_type,
        'registered_crops':f_product_crop,
        'geo_location':f_product_state,
        'effective_against':f_product_pest,
        'key_benefits':f_key_benefit,
        'safety_ins':f_product_description,
        'use_mix':f_use_mix,
        'length':length,
        'length_length':length_length,
        'crop_flag':crop_flag,
        'state_flag':state_flag,
        'pest_flag':pest_flag,
    }
    
    return render(request, 'app1/product.html', data) 

def alion(request):
    index = [63]
    f_product_name = []
    f_product_type = []
    f_product_crop = []
    f_product_state = []
    f_product_pest = []
    f_key_benefit = []
    f_product_description = []
    f_use_mix = []
    for val in index:
        f_product_name.append(df.iloc[val]['product_name'])
        productType = df.iloc[val]['product_type']
        if(productType == 'F'):
            f_product_type.append('Fungicides')
        elif(productType == 'HE'):
            f_product_type.append('Herbicides')
        elif(productType == 'HA'):
            f_product_type.append('Harvest Aids')
        else:
            f_product_type.append('Insecticides')
        #f_product_type.append(df.iloc[val]['product_type'])
        f_key_benefit.append(df.iloc[val]['key_benefits'])
        f_product_description.append(df.iloc[val]['safety_ins'])
        f_use_mix.append(df.iloc[val]['use&mix'])
    if(len(f_product_crop) == 0):
        crop_flag = 0
        for val in index:
            f_product_crop.append(df.iloc[val]['registered_crops'])
    else:
        crop_flag = 1
    if(len(f_product_state) == 0):
        state_flag = 0
        for val in index:
            f_product_state.append(df.iloc[val]['geo_location'])
    else:
        state_flag = 1
    if(len(f_product_pest) == 0):
        pest_flag = 0
        for val in index:
            f_product_pest.append(df.iloc[val]['effective_against'])
    else:
        pest_flag = 1
    length = [i for i in range(len(f_product_name))]
    for i in range(len(f_key_benefit)):
        f_key_benefit[i] = f_key_benefit[i][1:-1]
        f_key_benefit[i] = f_key_benefit[i].split(",")
        print(f_key_benefit[i])
    for i in range(len(f_product_crop)):
        f_product_crop[i] = f_product_crop[i][1:-1]
        f_product_crop[i] = f_product_crop[i].split("',")
    for i in range(len(f_product_pest)):
        f_product_pest[i] = f_product_pest[i][1:-1]
        f_product_pest[i] = f_product_pest[i].split("',")
    for i in range(len(f_product_state)):
        f_product_state[i] = f_product_state[i][1:-1]
        f_product_state[i] = f_product_state[i].split(',')
    length_length = len(length)
    data = {
        'indexes':index,
        'product_name':f_product_name,
        'product_type':f_product_type,
        'registered_crops':f_product_crop,
        'geo_location':f_product_state,
        'effective_against':f_product_pest,
        'key_benefits':f_key_benefit,
        'safety_ins':f_product_description,
        'use_mix':f_use_mix,
        'length':length,
        'length_length':length_length,
        'crop_flag':crop_flag,
        'state_flag':state_flag,
        'pest_flag':pest_flag,
    }
    
    return render(request, 'app1/product.html', data) 

def scala(request):
    index = [14]
    f_product_name = []
    f_product_type = []
    f_product_crop = []
    f_product_state = []
    f_product_pest = []
    f_key_benefit = []
    f_product_description = []
    f_use_mix = []
    for val in index:
        f_product_name.append(df.iloc[val]['product_name'])
        productType = df.iloc[val]['product_type']
        if(productType == 'F'):
            f_product_type.append('Fungicides')
        elif(productType == 'HE'):
            f_product_type.append('Herbicides')
        elif(productType == 'HA'):
            f_product_type.append('Harvest Aids')
        else:
            f_product_type.append('Insecticides')
        #f_product_type.append(df.iloc[val]['product_type'])
        f_key_benefit.append(df.iloc[val]['key_benefits'])
        f_product_description.append(df.iloc[val]['safety_ins'])
        f_use_mix.append(df.iloc[val]['use&mix'])
    if(len(f_product_crop) == 0):
        crop_flag = 0
        for val in index:
            f_product_crop.append(df.iloc[val]['registered_crops'])
    else:
        crop_flag = 1
    if(len(f_product_state) == 0):
        state_flag = 0
        for val in index:
            f_product_state.append(df.iloc[val]['geo_location'])
    else:
        state_flag = 1
    if(len(f_product_pest) == 0):
        pest_flag = 0
        for val in index:
            f_product_pest.append(df.iloc[val]['effective_against'])
    else:
        pest_flag = 1
    length = [i for i in range(len(f_product_name))]
    for i in range(len(f_key_benefit)):
        f_key_benefit[i] = f_key_benefit[i][1:-1]
        f_key_benefit[i] = f_key_benefit[i].split(",")
        print(f_key_benefit[i])
    for i in range(len(f_product_crop)):
        f_product_crop[i] = f_product_crop[i][1:-1]
        f_product_crop[i] = f_product_crop[i].split("',")
    for i in range(len(f_product_pest)):
        f_product_pest[i] = f_product_pest[i][1:-1]
        f_product_pest[i] = f_product_pest[i].split("',")
    for i in range(len(f_product_state)):
        f_product_state[i] = f_product_state[i][1:-1]
        f_product_state[i] = f_product_state[i].split(',')
    length_length = len(length)
    data = {
        'indexes':index,
        'product_name':f_product_name,
        'product_type':f_product_type,
        'registered_crops':f_product_crop,
        'geo_location':f_product_state,
        'effective_against':f_product_pest,
        'key_benefits':f_key_benefit,
        'safety_ins':f_product_description,
        'use_mix':f_use_mix,
        'length':length,
        'length_length':length_length,
        'crop_flag':crop_flag,
        'state_flag':state_flag,
        'pest_flag':pest_flag,
    }
    
    return render(request, 'app1/product.html', data) 

def movento(request):
    index = [25]
    f_product_name = []
    f_product_type = []
    f_product_crop = []
    f_product_state = []
    f_product_pest = []
    f_key_benefit = []
    f_product_description = []
    f_use_mix = []
    for val in index:
        f_product_name.append(df.iloc[val]['product_name'])
        productType = df.iloc[val]['product_type']
        if(productType == 'F'):
            f_product_type.append('Fungicides')
        elif(productType == 'HE'):
            f_product_type.append('Herbicides')
        elif(productType == 'HA'):
            f_product_type.append('Harvest Aids')
        else:
            f_product_type.append('Insecticides')
        #f_product_type.append(df.iloc[val]['product_type'])
        f_key_benefit.append(df.iloc[val]['key_benefits'])
        f_product_description.append(df.iloc[val]['safety_ins'])
        f_use_mix.append(df.iloc[val]['use&mix'])
    if(len(f_product_crop) == 0):
        crop_flag = 0
        for val in index:
            f_product_crop.append(df.iloc[val]['registered_crops'])
    else:
        crop_flag = 1
    if(len(f_product_state) == 0):
        state_flag = 0
        for val in index:
            f_product_state.append(df.iloc[val]['geo_location'])
    else:
        state_flag = 1
    if(len(f_product_pest) == 0):
        pest_flag = 0
        for val in index:
            f_product_pest.append(df.iloc[val]['effective_against'])
    else:
        pest_flag = 1
    length = [i for i in range(len(f_product_name))]
    for i in range(len(f_key_benefit)):
        f_key_benefit[i] = f_key_benefit[i][1:-1]
        f_key_benefit[i] = f_key_benefit[i].split(",")
        print(f_key_benefit[i])
    for i in range(len(f_product_crop)):
        f_product_crop[i] = f_product_crop[i][1:-1]
        f_product_crop[i] = f_product_crop[i].split("',")
    for i in range(len(f_product_pest)):
        f_product_pest[i] = f_product_pest[i][1:-1]
        f_product_pest[i] = f_product_pest[i].split("',")
    for i in range(len(f_product_state)):
        f_product_state[i] = f_product_state[i][1:-1]
        f_product_state[i] = f_product_state[i].split(',')
    length_length = len(length)
    data = {
        'indexes':index,
        'product_name':f_product_name,
        'product_type':f_product_type,
        'registered_crops':f_product_crop,
        'geo_location':f_product_state,
        'effective_against':f_product_pest,
        'key_benefits':f_key_benefit,
        'safety_ins':f_product_description,
        'use_mix':f_use_mix,
        'length':length,
        'length_length':length_length,
        'crop_flag':crop_flag,
        'state_flag':state_flag,
        'pest_flag':pest_flag,
    }
    
    return render(request, 'app1/product.html', data)