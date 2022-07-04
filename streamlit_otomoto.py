# -*- coding: utf-8 -*-
"""
Created on Sat Jul  11:40:29 2022

@author: pawel lipinski
"""

import streamlit as st
import joblib
import pickle
from datetime import date
import pandas as pd
import os


st.set_page_config(layout="wide")

current_year = date.today().year


st.title("Wyceń swój samochód")

model_nested_values = {
    'Abarth': ['500', '595'], 'Alfa Romeo': ['147', '156', '159', 'Brera', 'Giulia', 'Giulietta', 'GT', 'Mito', 'Stelvio', 'Tonale'], 'Aston Martin': ['DB9'], 'Audi': ['80', '100', 'A1', 'A2', 'A3', 'A4', 'A4 Allroad', 'A5', 'A6', 'A6 Allroad', 'A7', 'A8', 'Cabriolet', 'e-tron', 'e-tron GT', 'Q2', 'Q3', 'Q4', 'Q4 Sportback', 'Q5', 'Q7', 'Q8', 'R8', 'RS Q3', 'RS Q8', 'RS3', 'RS4', 'RS5', 'RS6', 'RS7', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'SQ5', 'SQ7', 'SQ8', 'TT', 'TT S'], 'BMW': ['3GT', '5GT', '6GT', 'i3', 'i8', 'Inny', 'iX', 'M2', 'M3', 'M4', 'M5', 'M6', 'M8', 'Seria 1', 'Seria 2', 'Seria 3', 'Seria 4', 'Seria 5', 'Seria 6', 'Seria 7', 'Seria 8', 'X1', 'X2', 'X3', 'X3 M', 'X4', 'X5', 'X5 M', 'X6', 'X6 M', 'X7', 'Z3', 'Z4'], 'BMW-ALPINA': ['B5'], 'Bentley': ['Continental Flying Spur', 'Continental GT'], 'Cadillac': ['CTS', 'Escalade', 'SRX'], 'Chevrolet': ['Aveo', 'Camaro', 'Captiva', 'Corvette', 'Cruze', 'Epica', 'Kalos', 'Lacetti', 'Malibu', 'Matiz', 'Nubira', 'Orlando', 'Silverado', 'Spark', 'Tahoe', 'Trailblazer', 'Trax'], 'Chrysler': ['200', '300C', '300s', 'Grand Voyager', 'Pacifica', 'PT Cruiser', 'Sebring', 'Stratus', 'Town & Country', 'Voyager'], 'Citroën': ['Berlingo', 'C1', 'C2', 'C3', 'C3 Aircross', 'C3 Picasso', 'C3 Pluriel', 'C4', 'C4 Aircross', 'C4 Cactus', 'C4 Grand Picasso', 'C4 Picasso', 'C4 SpaceTourer', 'C5', 'C5 Aircross', 'C5X', 'C6', 'C8', 'C-Crosser', 'C-ElysÃ©e', 'DS3', 'DS4', 'DS5', 'Jumper', 'Jumpy Combi', 'Nemo', 'Saxo', 'SpaceTourer', 'Xsara', 'Xsara Picasso'], 'Cupra': ['Ateca', 'Formentor'], 'DFSK': ['Seres 3'], 'DS Automobiles': ['DS 4', 'DS 4 Crossback', 'DS 5', 'DS 7 Crossback'], 'Dacia': ['Dokker', 'Duster', 'Jogger', 'Lodgy', 'Logan', 'Sandero', 'Sandero Stepway'], 'Daewoo': ['Kalos', 'Lanos', 'Matiz'], 'Daihatsu': ['Cuore', 'Materia', 'Sirion', 'Terios'], 'Dodge': ['Caliber', 'Challenger', 'Charger', 'Durango', 'Grand Caravan', 'Journey', 'Nitro', 'RAM'], 'Fiat': ['126', '500', '500L', '500X', 'Bravo', 'Cinquecento', 'Croma', 'Doblo', 'Ducato', 'Fiorino', 'Freemont', 'Grande Punto', 'Idea', 'Linea', 'Panda', 'Punto', 'Punto 2012', 'Punto Evo', 'Qubo', 'Scudo', 'Sedici', 'Seicento', 'Stilo', 'Talento', 'Tipo'], 'Ford': ['B-MAX', 'C-MAX', 'EcoSport', 'EDGE', 'Escape', 'Escort', 'Explorer', 'F150', 'Fiesta', 'Focus', 'Focus C-Max', 'Fusion', 'Galaxy', 'Grand C-MAX', 'KA', 'Ka+', 'Kuga', 'Maverick', 'Mondeo', 'Mustang', 'Mustang Mach-E', 'Puma', 'Ranger', 'Ranger Raptor', 'S-Max', 'Tourneo Connect', 'Tourneo Courier', 'Tourneo Custom', 'Transit', 'Transit Connect', 'Transit Courier', 'Transit Custom'], 'Honda': ['Accord', 'City', 'Civic', 'CR-V', 'CR-Z', 'e', 'FR-V', 'HR-V', 'Insight', 'Jazz', 'Legend', 'Odyssey'], 'Hummer': ['H2', 'H3'], 'Hyundai': ['Accent', 'Atos', 'Bayon', 'Coupe', 'Elantra', 'Galloper', 'Genesis', 'Genesis Coupe', 'Getz', 'i10', 'i20', 'I30', 'i30 N', 'i40', 'IONIQ', 'ix20', 'ix35', 'Kona', 'Matrix', 'Santa Fe', 'Sonata', 'Terracan', 'Tucson', 'Veloster'], 'Infiniti': ['FX', 'G', 'Q30', 'Q50', 'Q60', 'Q70', 'QX30', 'QX50', 'QX60', 'QX70'], 'Isuzu': ['D-Max'], 'Iveco': ['Daily'], 'Jaguar': ['E-Pace', 'F-Pace', 'F-Type', 'I-Pace', 'S-Type', 'XE', 'XF', 'XJ', 'XK', 'XK8', 'X-Type'], 'Jeep': ['Cherokee', 'Commander', 'Compass', 'Gladiator', 'Grand Cherokee', 'Liberty', 'Patriot', 'Renegade', 'Wrangler'], 'Kia': ['Carens', 'Carnival', 'Ceed', 'EV6', 'Magentis', 'Niro', 'Optima', 'Picanto', "Pro_cee'd", 'Rio', 'Sorento', 'Soul', 'Sportage', 'Stinger', 'Stonic', 'Venga', 'XCeed'], 'Lada': ['Niva'], 'Lancia': ['Delta', 'Musa', 'Phedra', 'Voyager', 'Ypsilon'], 'Land Rover': ['Defender', 'Discovery', 'Discovery Sport', 'Freelander', 'Range Rover', 'Range Rover Evoque', 'Range Rover Sport', 'Range Rover Velar'], 'Lexus': ['CT', 'ES', 'GS', 'IS', 'LC', 'LS', 'LX', 'NX', 'RC', 'RX', 'SC', 'UX'], 'Lincoln': ['Navigator', 'Town Car'], 'MINI': ['Clubman', 'Cooper', 'Cooper S', 'Countryman', 'John Cooper Works', 'ONE'], 'Maserati': ['Ghibli', 'GranTurismo', 'Levante', 'Quattroporte'], 'Mazda': ['2', '3', '5', '6', 'CX-3', 'CX-30', 'CX-5', 'CX-60', 'CX-7', 'CX-9', 'MX-5', 'RX-8'], 'Mercedes-Benz': ['AMG GT', 'Citan', 'CL', 'CLA', 'CLC', 'CLK', 'CLS', 'EQB', 'EQC', 'EQE', 'EQS', 'EQV', 'GL', 'GLA', 'GLB', 'GLC', 'GLE', 'GLK', 'GLS', 'Klasa A', 'Klasa B', 'Klasa C', 'Klasa E', 'Klasa G', 'Klasa R', 'Klasa S', 'Klasa T', 'Klasa V', 'Klasa X', 'ML', 'SL', 'SLK', 'Sprinter', 'Vaneo', 'Viano', 'Vito', 'W124 (1984-1993)', 'W201 (190)'], 'Mitsubishi': ['ASX', 'Carisma', 'Colt', 'Eclipse Cross', 'Grandis', 'L200', 'Lancer', 'Lancer Evolution', 'Outlander', 'Pajero', 'Pajero Pinin', 'Space Star'], 'Nissan': ['350 Z', '370 Z', 'Almera', 'Altima', 'GT-R', 'Juke', 'Leaf', 'Micra', 'Murano', 'Navara', 'Note', 'NV200', 'Pathfinder', 'Patrol', 'Pixo', 'Primera', 'Pulsar', 'Qashqai', 'Qashqai+2', 'Rogue', 'Terrano', 'Tiida', 'Townstar', 'X-Trail'], 'Opel': ['Adam', 'Agila', 'Ampera', 'Antara', 'Astra', 'Combo', 'Corsa', 'Crossland X', 'Frontera', 'Grandland X', 'Insignia', 'Karl', 'Meriva', 'Mokka', 'Movano', 'Omega', 'Signum', 'Tigra', 'Vectra', 'Vivaro', 'Zafira'], 'Peugeot': ['106', '107', '108', '206', '207', '207', '207', '207', '208', '208', '208', '208', '208', '301', '301', '301', '301', '307', '307', '307', '308', '308', '308', '308', '308', '308', '308', '308', '406', '406', '406', '407', '407', '407', '407', '407', '407', '407', '508', '508', '508', '508', '508', '508', '508', '607', '607', '607', '607', '807', '807', '807', '807', '1007', '1007', '1007', '1007', '1007', '1007', '2008', '2008', '2008', '2008', '2008', '2008', '2008', '2008', '2008', '2008', '2008', '3008', '3008', '3008', '3008', '3008', '4007', '5008', '206 CC', '206 CC', '206 CC', '206 CC', '206 CC', '206 CC', '206 plus', '206 plus', '206 plus', '207 CC', '207 CC', '207 CC', '207 CC', '207 CC', '307 CC', '307 CC', '307 CC', '307 CC', '307 CC', '307 CC', '308 CC', '308 CC', '308 CC', '308 CC', 'Bipper', 'Boxer', 'Expert', 'Partner', 'RCZ', 'Rifter', 'Traveller'], 'Polonez': ['Atu', 'Caro'], 'Porsche': ['911', '718 Boxster', '718 Cayman', 'Boxster', 'Cayenne', 'Cayman', 'Macan', 'Panamera', 'Taycan'], 'RAM': ['1500'], 'Renault': ['Arkana', 'Captur', 'Clio', 'Espace', 'Fluence', 'Grand Espace', 'Grand Scenic', 'Kadjar', 'Kangoo', 'Koleos', 'Laguna', 'Master', 'Megane', 'Modus', 'Scenic', 'Talisman', 'Thalia', 'Trafic', 'Twingo', 'Twizy', 'Vel Satis', 'Zoe'], 'Rover': ['75'], 'Saab': ['900', '9-3', '9-5'], 'Seat': ['Alhambra', 'Altea', 'Altea XL', 'Arona', 'Arosa', 'Ateca', 'Cordoba', 'Exeo', 'Ibiza', 'Leon', 'Mii', 'Tarraco', 'Toledo'], 'Smart': ['Forfour', 'Fortwo'], 'SsangYong': ['Korando', 'REXTON', 'Tivoli', 'Tivoli Grand'], 'Subaru': ['BRZ', 'Forester', 'Impreza', 'Justy', 'Legacy', 'Levorg', 'OUTBACK', 'WRX', 'XV'], 'Suzuki': ['Alto', 'Baleno', 'Grand Vitara', 'Ignis', 'Jimny', 'Kizashi', 'Liana', 'Samurai', 'Splash', 'Swace', 'Swift', 'SX4', 'SX4 S-Cross', 'Vitara', 'XL7'], 'Tesla': ['Model 3', 'Model S', 'Model X'], 'Toyota': ['4-Runner', 'Auris', 'Avensis', 'Aygo', 'Camry', 'Celica', 'C-HR', 'Corolla', 'Corolla Verso', 'GT86', 'Highlander', 'Hilux', 'iQ', 'Land Cruiser', 'Prius', 'Prius+', 'ProAce', 'Proace City Verso', 'Proace Verso', 'RAV4', 'Sienna', 'Tundra', 'Urban Cruiser', 'Verso', 'Verso S', 'Yaris', 'Yaris Verso'], 'Volkswagen': ['Amarok', 'Arteon', 'Atlas', 'Beetle', 'Bora', 'Caddy', 'California', 'Caravelle', 'CC', 'Crafter', 'Eos', 'Fox', 'Golf', 'Golf Plus', 'Golf Sportsvan', 'ID.3', 'ID.4', 'ID.5', 'Jetta', 'Lupo', 'Multivan', 'New Beetle', 'Passat', 'Passat CC', 'Phaeton', 'Polo', 'Scirocco', 'Sharan', 'Taigo', 'T-Cross', 'Tiguan', 'Tiguan Allspace', 'Touareg', 'Touran', 'Transporter', 'T-Roc', 'up!'], 'Volvo': ['C30', 'C70', 'S40', 'S60', 'S80', 'S90', 'V40', 'V50', 'V60', 'V70', 'V90', 'XC 40', 'XC 60', 'XC 70', 'XC 90'], 'Škoda': ['Citigo', 'Enyaq', 'Fabia', 'Felicia', 'Kamiq', 'Karoq', 'Kodiaq', 'Octavia', 'RAPID', 'Roomster', 'Scala', 'Superb', 'Yeti']}

# =============================================================================
#model_nested_values obtained via below script:
#    
#import pandas as pd
# 
# df=pd.read_csv("model_results.csv", usecols=["brand","model"])
# 
# df.drop_duplicates(inplace=True)
# model_nested_values = df.groupby('brand')['model'].apply(list).to_dict()
# 
# print(model_nested_values)
# 
# =============================================================================

col1, col2, col3, col4 = st.columns(4)

fuel = col1.selectbox("Rodzaj paliwa:",['Benzyna','Benzyna+CNG',  'Benzyna+LPG', 'Diesel', 'Elektryczny','Hybryda', 'Wodór'])
power = col2.number_input("Podaj moc w KM:", value=0, min_value=0, step=1)
cylinder_capacity = col3.number_input("Pojemność skokowa w cm3:", value=0, min_value=0, step=1)
transmission = col4.selectbox("Skrzynia biegów:", ['Automatyczna', 'Manualna'])
mileage = col1.number_input("Podaj przebieg w km:", value=0, min_value=0, step=1)
age = col2.number_input("Rok produkcji:", value=2022, min_value=0, step=1) #tranform into age
brand = col3.selectbox("Marka samochodu:", ['Abarth',	'Alfa Romeo',	'Aston Martin',	'Audi',	'Bentley',	'BMW',	'BMW-ALPINA',	'Cadillac',	'Chevrolet',	'Chrysler',	'Citroën',	'Cupra',	'Dacia',	'Daewoo',	'Daihatsu',	'DFSK',	'Dodge',	'DS Automobiles',	'Fiat',	'Ford',	'Honda',	'Hummer',	'Hyundai',	'Infiniti',	'Isuzu',	'Iveco',	'Jaguar',	'Jeep',	'Kia',	'Lada',	'Lancia',	'Land Rover',	'Lexus',	'Lincoln',	'Maserati',	'Mazda',	'Mercedes-Benz',	'MINI',	'Mitsubishi',	'Nissan',	'Opel',	'Peugeot',	'Polonez',	'Porsche',	'RAM',	'Renault',	'Rover',	'Saab',	'Seat',	'Škoda',	'Smart',	'SsangYong',	'Subaru',	'Suzuki',	'Tesla',	'Toyota',	'Volkswagen',	'Volvo'])
model = col4.selectbox("Model samochodu:", model_nested_values[brand] )
no_crash = col1.selectbox("Bezwypadkowy:", ['Tak', 'Nie'])
color = col2.selectbox("Kolor:", ['Beżowy', 'Biały', 'Bordowy', 'Brązowy', 'Czarny', 'Czerwony', 'Fioletowy', 'Inny kolor', 'Niebieski', 'Srebrny', 'Szary', 'Zielony', 'Złoty', 'Żółty'])

colour_type_choices = {"matt":"Mat", "metallic":"Metalik", "pearl":"Perłowy"}

def format_func_colour_type(colour_type):
    return colour_type_choices[colour_type]

colour_type = col3.selectbox("Rodzaj koloru:", options=list(colour_type_choices.keys()), format_func=format_func_colour_type)
country = col4.selectbox("Kraj pochodzenia:",  ['Polska', 'Austria', 'Belgia', 'Białoruś', 'Bułgaria', 'Chorwacja', 'Czechy', 'Dania', 'Estonia', 'Finlandia', 'Francja', 'Grecja', 'Hiszpania', 'Holandia', 'Inny', 'Irlandia', 'Islandia', 'Japonia', 'Kanada', 'Liechtenstein', 'Litwa', 'Luksemburg', 'Łotwa', 'Monako', 'Niemcy', 'Norwegia', 'Rosja', 'Rumunia', 'Stany Zjednoczone', 'Szwajcaria', 'Szwecja', 'Słowacja', 'Słowenia', 'Turcja', 'Ukraina', 'Wielka Brytania', 'Węgry', 'Włochy'])
doors = col1.selectbox("Liczba drzwi:", [2, 3, 4, 5, 6])
seats = col2.selectbox("Liczba siedzeń:", [2, 3, 4, 5, 6, 7, 8, 9])

condition = col3.selectbox("Stan:", ["Nowe", "Używane"])
car_type = col4.selectbox("Typ samochodu:", ["Auta małe", "Auta miejsckie", "Coupe", "KAbriolet", "Kombi", "Kompakt", "Minivan", "Sedan", "SUV"])
district = col1.selectbox("district", ['dolnoslaskie',	'kujawsko-pomorskie',	'lodzkie',	'lubelskie',	'lubuskie',	'malopolskie',	'mazowieckie',	'opolskie',	'podkarpackie',	'podlaskie',	'pomorskie',	'slaskie',	'swietokrzyskie',	'warminsko-mazurskie',	'wielkopolskie',	'zachodniopomorskie'])
drive = col2.selectbox("Napęd:", ['4x4 (dołączany automatycznie)',	'4x4 (dołączany ręcznie)',	'4x4 (stały)',	'Na przednie koła',	'Na tylne koła'])
registered = col3.selectbox("Zarejestrowany w Polsce:", ["Tak", "Nie"])

col1, col2 = st.columns([4,1])

col1.title("Podaj wyposażenie:")


col1, col2, col3, col4 = st.columns(4)


equipment_choices = {0: "Nie", 1: "Tak"}


def format_func_equipment_zawieszenie(zawieszenie):
    return equipment_choices[zawieszenie]
zawieszenie = col1.selectbox("Zawieszenie regulowane:", options=list(equipment_choices.keys()), format_func=format_func_equipment_zawieszenie)

def format_func_equipment_startstop(startstop):
    return equipment_choices[startstop]
startstop = col2.selectbox("System StartStop:", options=list(equipment_choices.keys()), format_func=format_func_equipment_startstop)

def format_func_equipment_ogrzewane_siedzenie_tylne(ogrzewane_siedzenie_tylne):
    return equipment_choices[ogrzewane_siedzenie_tylne]
ogrzewane_siedzenie_tylne = col3.selectbox("Ogrzewane siedzenia tylne:", options=list(equipment_choices.keys()), format_func=format_func_equipment_ogrzewane_siedzenie_tylne)

def format_func_equipment_klimatyzacja_4strefowa(klimatyzacja_4strefowa):
    return equipment_choices[klimatyzacja_4strefowa]
klimatyzacja_4strefowa = col4.selectbox("Klimatyzacja automatyczna 4 lub więcej strefowa:", options=list(equipment_choices.keys()), format_func=format_func_equipment_klimatyzacja_4strefowa)

def format_func_equipment_kamera_parkowania(kamera_parkowania):
    return equipment_choices[kamera_parkowania]
kamera_parkowania = col1.selectbox("Kamera parkowania tył:", options=list(equipment_choices.keys()), format_func=format_func_equipment_kamera_parkowania)

def format_func_equipment_ogrzewanie_postojowe(ogrzewanie_postojowe):
    return equipment_choices[ogrzewanie_postojowe]
ogrzewanie_postojowe = col2.selectbox("Ogrzewanie postojowe:", options=list(equipment_choices.keys()), format_func=format_func_equipment_ogrzewanie_postojowe)

def format_func_equipment_czujnik_martwego_pola(czujnik_martwego_pola):
    return equipment_choices[czujnik_martwego_pola]
czujnik_martwego_pola = col3.selectbox("Asystent (czujnik) martwego pola:", options=list(equipment_choices.keys()), format_func=format_func_equipment_czujnik_martwego_pola)

def format_func_equipment_kamera_w_lusterku(kamera_w_lusterku):
    return equipment_choices[kamera_w_lusterku]
kamera_w_lusterku = col4.selectbox("Kamera w lusterku bocznym:", options=list(equipment_choices.keys()), format_func=format_func_equipment_kamera_w_lusterku)

def format_func_equipment_przyciemniane_szyby(przyciemniane_szyby):
    return equipment_choices[przyciemniane_szyby]
przyciemniane_szyby = col1.selectbox("Przyciemniane tylne szyby:", options=list(equipment_choices.keys()), format_func=format_func_equipment_przyciemniane_szyby)

def format_func_equipment_lane_assist(lane_assist):
    return equipment_choices[lane_assist]
lane_assist = col2.selectbox("Lane assist - kontrola zmiany pasa ruchu:", options=list(equipment_choices.keys()), format_func=format_func_equipment_lane_assist)

def format_func_equipment_tempomat_adaptacyjny(tempomat_adaptacyjny):
    return equipment_choices[tempomat_adaptacyjny]
tempomat_adaptacyjny = col3.selectbox("Tempomat adaptacyjny ACC:", options=list(equipment_choices.keys()), format_func=format_func_equipment_tempomat_adaptacyjny)

def format_func_equipment_wspomaganie_kierownicy(wspomaganie_kierownicy):
    return equipment_choices[wspomaganie_kierownicy]
wspomaganie_kierownicy = col4.selectbox("Wspomaganie kierownicy:", options=list(equipment_choices.keys()), format_func=format_func_equipment_wspomaganie_kierownicy)

def format_func_equipment_podgrzewana_przednia_szyba(podgrzewana_przednia_szyba):
    return equipment_choices[podgrzewana_przednia_szyba]
podgrzewana_przednia_szyba = col1.selectbox("Podgrzewana przednia szyba:", options=list(equipment_choices.keys()), format_func=format_func_equipment_podgrzewana_przednia_szyba)

def format_func_equipment_ogranicznik_predkosci(ogranicznik_predkosci):
    return equipment_choices[ogranicznik_predkosci]
ogranicznik_predkosci = col2.selectbox("Ogranicznik predkośći:", options=list(equipment_choices.keys()), format_func=format_func_equipment_ogranicznik_predkosci)

def format_func_equipment_tapicerka_skorzana(tapicerka_skorzana):
    return equipment_choices[tapicerka_skorzana]
tapicerka_skorzana = col3.selectbox("Tapicerka skórzana:", options=list(equipment_choices.keys()), format_func=format_func_equipment_tapicerka_skorzana)

def format_func_equipment_klimatyzacja_2strefowa(klimatyzacja_2strefowa):
    return equipment_choices[klimatyzacja_2strefowa]
klimatyzacja_2strefowa = col4.selectbox("Klimatyzacja automatyczna dwustrefowa:", options=list(equipment_choices.keys()), format_func=format_func_equipment_klimatyzacja_2strefowa)

def format_func_equipment_elektryczne_szyby_przednie(elektryczne_szyby_przednie):
    return equipment_choices[elektryczne_szyby_przednie]
elektryczne_szyby_przednie = col1.selectbox("Elektryczne szyby przednie:", options=list(equipment_choices.keys()), format_func=format_func_equipment_elektryczne_szyby_przednie)

def format_func_equipment_lusterka_boczne_elektryczne(lusterka_boczne_elektryczne):
    return equipment_choices[lusterka_boczne_elektryczne]
lusterka_boczne_elektryczne = col2.selectbox("Lusterka boczne ustawiane elektrycznie:", options=list(equipment_choices.keys()), format_func=format_func_equipment_lusterka_boczne_elektryczne)

def format_func_equipment_system_nawigacji_sat(system_nawigacji_sat):
    return equipment_choices[system_nawigacji_sat]
system_nawigacji_sat = col3.selectbox("System nawigacji satelitarnej:", options=list(equipment_choices.keys()), format_func=format_func_equipment_system_nawigacji_sat)

def format_func_equipment_podgrzewane_lusterka_boczne(podgrzewane_lusterka_boczne):
    return equipment_choices[podgrzewane_lusterka_boczne]
podgrzewane_lusterka_boczne = col4.selectbox("Podgrzewane lusterka boczne:", options=list(equipment_choices.keys()), format_func=format_func_equipment_podgrzewane_lusterka_boczne)

def format_func_equipment_elektryczny_fotel_kierowcy(elektryczny_fotel_kierowcy):
    return equipment_choices[elektryczny_fotel_kierowcy]
elektryczny_fotel_kierowcy = col1.selectbox("Elektrycznie ustawiany fotel kierowcy:", options=list(equipment_choices.keys()), format_func=format_func_equipment_elektryczny_fotel_kierowcy)


def format_func_equipment_elektryczny_fotel_pasazera(elektryczny_fotel_pasazera):
    return equipment_choices[elektryczny_fotel_pasazera]
elektryczny_fotel_pasazera = col2.selectbox("Elektrycznie ustawiany fotel pasażera:", options=list(equipment_choices.keys()), format_func=format_func_equipment_elektryczny_fotel_pasazera)

def format_func_equipment_podgrzewany_fotel_kierowcy(podgrzewany_fotel_kierowcy):
    return equipment_choices[podgrzewany_fotel_kierowcy]
podgrzewany_fotel_kierowcy = col3.selectbox("Podgrzewany fotel kierowcy:", options=list(equipment_choices.keys()), format_func=format_func_equipment_podgrzewany_fotel_kierowcy)


                             




        
df_pred=pd.DataFrame([[fuel,power,transmission,mileage, age, brand, model, no_crash, color, colour_type, country, doors, seats, cylinder_capacity, condition, car_type, district, drive, registered, zawieszenie, startstop, ogrzewane_siedzenie_tylne, klimatyzacja_4strefowa, kamera_parkowania, ogrzewanie_postojowe, czujnik_martwego_pola, kamera_w_lusterku, przyciemniane_szyby, lane_assist, tempomat_adaptacyjny, wspomaganie_kierownicy, podgrzewana_przednia_szyba, ogranicznik_predkosci, tapicerka_skorzana, klimatyzacja_2strefowa, elektryczne_szyby_przednie, lusterka_boczne_elektryczne, system_nawigacji_sat, podgrzewane_lusterka_boczne, elektryczny_fotel_kierowcy, elektryczny_fotel_pasazera, podgrzewany_fotel_kierowcy]], 
                     columns=['fuel','power','transmission', 'mileage', 'age', 'brand', 'model', 'no_crash', 'color', 'colour_type', 'country', 'doors', 'seats', 'cylinder_capacity', 'condition', 'car_type', 'district', 'drive', 'registered', 'Zawieszenie regulowane', 'System StartStop', 'Ogrzewane siedzenia tylne', 'Klimatyzacja automatyczna 4 lub wicej strefowa','Kamera parkowania tył', 'Ogrzewanie postojowe', 'Asystent (czujnik) martwego pola', 'Kamera w lusterku bocznym','Przyciemniane tylne szyby', 'Lane assist - kontrola zmiany pasa ruchu', 'Tempomat adaptacyjny ACC', 'Wspomaganie kierownicy','Podgrzewana przednia szyba', 'Ogranicznik prdkoci', 'Tapicerka skrzana', 'Klimatyzacja automatyczna dwustrefowa','Elektryczne szyby przednie', 'Lusterka boczne ustawiane elektrycznie', 'System nawigacji satelitarnej','Podgrzewane lusterka boczne', 'Elektrycznie ustawiany fotel kierowcy', 'Elektrycznie ustawiany fotel pasaera', 'Podgrzewany fotel kierowcy'])


df_pred["doors"]=df_pred["doors"].astype("category")
df_pred["seats"]=df_pred["seats"].astype("category")
df_pred["cylinder_capacity"]=df_pred["cylinder_capacity"].astype("int64")
df_pred["fuel"]=df_pred["fuel"].astype("category")
df_pred["power"]=df_pred["power"].astype("int64" )
df_pred["transmission"]=df_pred["transmission"].astype("category")
df_pred["mileage"]=df_pred["mileage"].astype("int64")
df_pred["age"]=df_pred["age"].astype("int64")
df_pred["age"]=current_year-df_pred["age"]
df_pred["brand"]=df_pred["brand"].astype("category")
df_pred["model"]=df_pred["model"].astype("category")
df_pred["no_crash"]=df_pred["no_crash"].astype("category")
df_pred["color"]=df_pred["color"].astype("category")
df_pred["country"]=df_pred["country"].astype("category")
df_pred["colour_type"]=df_pred["colour_type"].astype("category")
df_pred["condition"]=df_pred["condition"].astype("category")
df_pred["car_type"]=df_pred["car_type"].astype("category")
df_pred["district"]=df_pred["district"].astype("category")
df_pred["drive"]=df_pred["drive"].astype("category")
df_pred["registered"]=df_pred["registered"].astype("category")

df_pred["Zawieszenie regulowane"]=df_pred["Zawieszenie regulowane"].astype("int64")
df_pred["System StartStop"]=df_pred["System StartStop"].astype("int64")
df_pred["Ogrzewane siedzenia tylne"]=df_pred["Ogrzewane siedzenia tylne"].astype("int64")
df_pred["Klimatyzacja automatyczna 4 lub wicej strefowa"]=df_pred["Klimatyzacja automatyczna 4 lub wicej strefowa"].astype("int64")
df_pred["Kamera parkowania tył"]=df_pred["Kamera parkowania tył"].astype("int64")
df_pred["Ogrzewanie postojowe"]=df_pred["Ogrzewanie postojowe"].astype("int64")
df_pred["Asystent (czujnik) martwego pola"]=df_pred["Asystent (czujnik) martwego pola"].astype("int64")
df_pred["Kamera w lusterku bocznym"]=df_pred["Kamera w lusterku bocznym"].astype("int64")
df_pred["Przyciemniane tylne szyby"]=df_pred["Przyciemniane tylne szyby"].astype("int64")
df_pred["Lane assist - kontrola zmiany pasa ruchu"]=df_pred["Lane assist - kontrola zmiany pasa ruchu"].astype("int64")
df_pred["Tempomat adaptacyjny ACC"]=df_pred["Tempomat adaptacyjny ACC"].astype("int64")
df_pred["Wspomaganie kierownicy"]=df_pred["Wspomaganie kierownicy"].astype("int64")
df_pred["Podgrzewana przednia szyba"]=df_pred["Podgrzewana przednia szyba"].astype("int64")
df_pred["Ogranicznik prdkoci"]=df_pred["Ogranicznik prdkoci"].astype("int64")
df_pred["Tapicerka skrzana"]=df_pred["Tapicerka skrzana"].astype("int64")
df_pred["Klimatyzacja automatyczna dwustrefowa"]=df_pred["Klimatyzacja automatyczna dwustrefowa"].astype("int64")
df_pred["Elektryczne szyby przednie"]=df_pred["Elektryczne szyby przednie"].astype("int64")
df_pred["Lusterka boczne ustawiane elektrycznie"]=df_pred["Lusterka boczne ustawiane elektrycznie"].astype("int64")
df_pred["System nawigacji satelitarnej"]=df_pred["System nawigacji satelitarnej"].astype("int64")
df_pred["Podgrzewane lusterka boczne"]=df_pred["Podgrzewane lusterka boczne"].astype("int64")
df_pred["Elektrycznie ustawiany fotel kierowcy"]=df_pred["Elektrycznie ustawiany fotel kierowcy"].astype("int64")
df_pred["Elektrycznie ustawiany fotel pasaera"]=df_pred["Elektrycznie ustawiany fotel pasaera"].astype("int64")
df_pred["Podgrzewany fotel kierowcy"]=df_pred["Podgrzewany fotel kierowcy"].astype("int64")






def convert_df(df_pred):
   return df_pred.to_csv().encode('utf-8')

csv = convert_df(df_pred)

st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)

model_lgbm = joblib.load('lgbr_model.pkl')
prediction = model_lgbm.predict(df_pred)

if st.button('Wyceń'):

    st.write('Wycena:', prediction, unsafe_allow_html=False)
    
def download_model(model_lgbm):
    output_model = pickle.dumps(model_lgbm)
    href = f'<a href="data:file" download="myfile.pkl">Download Trained Model .pkl File</a>'
    st.markdown(href, unsafe_allow_html=True)


download_model(model_lgbm)