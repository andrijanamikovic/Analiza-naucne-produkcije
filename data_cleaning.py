import pickle

import pandas as pd
import matplotlib.pyplot as plt
import  numpy as np
import networkx as nx

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

def input_data():
    autori = pd.read_excel("./data/autori.xlsx")
    epidem = pd.read_excel("./data/epidemiologija.xlsx")
    imun = pd.read_excel("./data/imunologija.xlsx")
    infek = pd.read_excel("./data/infektivne_bolesti.xlsx")
    mikro = pd.read_excel("./data/mikrobiologija.xlsx")
    return autori, epidem, imun,infek,mikro

autori, epidem, imun, infek, mikro = input_data()
print(autori.head())
autori['id'] = autori.index
print(f"Tipovi kolona za autore: {autori.dtypes}")
autori['H indeks'] = pd.to_numeric(autori['H indeks'], errors='coerce')
# uklanjanje autora za koje nemam podataka o broju radova i H indeksu
autori_null_rows = autori[pd.DataFrame(autori).isnull().any(axis=1)]
print(f"Redovi koje sadrze null vrednosti autori: \n {autori_null_rows}")
print(f'Broj autora pre izbacivanja: {autori.shape[0]}')
autori = autori.dropna()
print(f"Da li sada sadrze null vrednosti autori: {pd.DataFrame(autori).isnull().any()}")
autori['H indeks'] = autori['H indeks'].astype('int64')
autori['Broj radova'] = autori['Broj radova'].astype('int64')

print(f'Broj autora nakon izbacivanja: {autori.shape[0]}')
print(f'Tipovi nakon promene autori: {autori.dtypes}')

# provera da li su ime i prezime jedinstveni kao celina
full_name_authors_duplicated = autori.duplicated(subset=['Ime', 'Prezime'], keep=False)
print(f"Redovi sa dupliranim imenom i prezimenom: {autori[full_name_authors_duplicated]}")

autori['Ime'] = autori['Ime'].str.lower()
autori['Prezime'] = autori['Prezime'].str.lower()
autori['Katedra'] = autori['Katedra'].str.lower()
autori['Puno ime'] = autori['Ime'].str.cat(autori['Prezime'], sep=' ', na_rep='')
autori['Skraceno'] = autori['Prezime']+' ' + autori['Ime'].str[0]+'.'
#ako prezime ima crticu jasmina simonovic babic ona je skraceno napisana koa babic j.s. ili kao simonovic-babic j.???
#two_last_names = autori[autori['Prezime'].str.contains('-')]
#print(f'Dva prezimena imaju \n {two_last_names}')
#Proveri za ovo

with open('./data/autori_cleaned', 'wb') as file:
    pickle.dump(autori, file)

#prikaz raspodele broja radova po katedrama
department_pappers = autori.groupby('Katedra')['Broj radova'].sum().reset_index()
print("Broj radova po razlicitim katedrama")
print(department_pappers)
print("Infektivne iz fajla: ", infek.shape)
print("Epidemiologija iz fajla: ", epidem.shape)
print("Imunologija iz fajla: ", imun.shape)
print("Mikrobiologija iz fajla: ", mikro.shape)
#Vidim da potencijalno imam ponovljen rad u fajlu za infektivne i za imunologiju


good_articles_format = ['Article', 'Article in Press', 'Review', 'Book Chapter', 'Letter', 'Note']
#Izbaceni radovi objavljeni u ne validnim formatima
infek = infek[infek['Document Type'].isin(good_articles_format)]
epidem = epidem[epidem['Document Type'].isin(good_articles_format)]
imun = imun[imun['Document Type'].isin(good_articles_format)]
mikro = mikro[mikro['Document Type'].isin(good_articles_format)]
print("Infektivne iz fajla: ", infek.shape)
print("Epidemiologija iz fajla: ", epidem.shape)
print("Imunologija iz fajla: ", imun.shape)
print("Mikrobiologija iz fajla: ", mikro.shape)

#infektivno
print(infek.head())
infek_null_rows = pd.DataFrame(infek).isnull().any(axis=0)
print(f"Kolone koje sadrze null vrednosti infek: \n {infek_null_rows}")
for column in ['Volume', 'Art. No.', 'Page start','Page end','Page count','Link','Source']:
    if column  in infek.columns:
        infek = infek.drop([column], axis=1)
    if column in epidem.columns:
        epidem = epidem.drop([column], axis=1)
    if column in imun.columns:
        imun = imun.drop([column], axis=1)
    if column in mikro.columns:
        mikro = mikro.drop([column], axis=1)
# infek['id'] = infek.index
# epidem['id'] = epidem.index
# imun['id'] = imun.index
# mikro['id'] = mikro.index
print(f"Infektivne kolone = {infek.columns}")
print(f"Epidemiologija kolone = {epidem.columns}")
print(f"Imunologija kolone = {imun.columns}")
print(f"Mikrobiologija kolone = {mikro.columns}")
for column in ['Author', 'Authors','Source title', 'Title']:
    if column in infek.columns:
        infek[column] = infek[column].str.lower()
    if column in epidem.columns:
        epidem[column] = epidem[column].str.lower()
    if column in imun.columns:
        imun[column] = imun[column].str.lower()
    if column in mikro.columns:
        mikro[column] = mikro[column].str.lower()

print(infek.head())
print(f"Infektivno dataTypes: {infek.dtypes}")
print(f"Epidemiologija dataTypes: {epidem.dtypes}")
print(f"Imuno dataTypes: {imun.dtypes}")
print(f"Mikro dataTypes: {mikro.dtypes}")

#u autori mi pise autor rada kome je pridruzen sa faksa
infektivno_authors = infek.assign(AllAuthors=infek['Authors'].str.split(',')).explode('Authors')
print('Ovde vise autora: ', infektivno_authors)
author_counts_whole = infektivno_authors['AllAuthors'].value_counts()

radovi_po_autoru_pridruzeni = infek.groupby('Author').size()
print(f'Radovi po autoru pridruzeni {radovi_po_autoru_pridruzeni}')
print(f'Tip? {infektivno_authors} ')
#ne znam kako da proverim da li mi ima ime u listi koautora
# for author in radovi_po_autoru_pridruzeni.index:
#     shortName = autori[(autori['Puno ime'] == author)]['Skraceno']
#     print(infektivno_authors['AllAuthors'].apply(type))
#     print(type(shortName))
#     print('Skraceno? ', shortName)
#     with_author = infektivno_authors[infektivno_authors["AllAuthors"].str.contains(shortName)]
#     print('Sa autorom? ')
#     print(with_author)
# print(f'Radovi po autoru pridruzeni {radovi_po_autoru_pridruzeni}')

infek['Katedra'] = 'infektivne bolesti'
epidem['Katedra'] = 'katedra za epidemiologiju'
imun['Katedra']='katedra za imunologiju'
mikro['Katedra']='katedra za mikrobiologiju'

data = pd.concat([infek, epidem,imun,mikro], ignore_index=True)
print(data.head())

radovi_po_autoru_broj = data.groupby('Author').size()
print(f'Radovi po autoru pridruzeni {radovi_po_autoru_broj}')

for author in radovi_po_autoru_broj.index:
    if not autori['Puno ime'].eq(author).any():
        print(f"U pocetnom fajlu nema autora: {author}")

