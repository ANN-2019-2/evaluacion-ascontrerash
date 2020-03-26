##
## Preparación
##
import pandas as pd
import numpy as np
import glob

filenames = glob.glob('datos\precios\*.xlsx')
filenamesx = glob.glob('datos\precios\*.xls')
filenames = filenames + filenamesx

data = pd.DataFrame()
ano=1995
for f in filenames:
    if ano<2000:
        aux = pd.read_excel(f,header=3)
    
    elif ano==2000 or ano==2005 or ano>=2010 :
        aux = pd.read_excel(f,header=2)
        aux = aux.drop(['Version'],axis=1)
        
    else:
        aux = pd.read_excel(f,header=2)
        
    ano+=1  
    data = data.append(aux,sort=False)
    #data = pd.concat([data,aux])
del ano, aux, f, filenames, filenamesx
data = data.dropna(subset=['Fecha'])
data = data[data.columns[:-2]] 
data = data.fillna(0)
data['promedio'] = data.mean(axis=1)
data = data.reset_index(drop=True)
data = data[['Fecha','promedio']]


ipc = pd.read_excel('datos/1.2.5.IPC_Serie_variaciones.xlsx',header =12)
ipc = ipc.iloc[:-6] 
ipc = ipc.iloc[:,0:2] 
ipc.columns = ['Corte', 'ipc']
ipc['Corte'] = ipc['Corte'].astype(str)
ipc['Corte'] = ipc['Corte'].apply(lambda x: x[:4] + '-' + x[4:])
ipc['Corte'] = pd.to_datetime(ipc['Corte']).dt.to_period('M')
indiceBase = ipc.tail(1).iloc[0,1]
data['Corte'] = pd.to_datetime(data['Fecha']).dt.to_period('M')

data = pd.merge(data, ipc[["Corte", "ipc"]], on="Corte", how="left")
data['promedioIPC'] =  data['promedio'] * (indiceBase / data['ipc'])


