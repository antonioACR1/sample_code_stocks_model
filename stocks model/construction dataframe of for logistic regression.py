import pandas as pd
from datetime import timedelta

#read sentiment dataset
df=pd.read_csv("C:/Users/USUARIO/Documents/sentimentCounts.csv",header=0)
columns=df.columns.values
fechasAcciones=[]
for i in range(1,columns.size):
        fechasAcciones.append(pd.to_datetime(columns[i].replace("count",""),format="%Y-%m-%d"))
dateColumns=columns[1:(columns.size-1)]
countsPerDate=[]
for i in dateColumns:
    countsPerDate.append(df[i].tolist())
dictionaryCountDate=dict(zip(fechasAcciones,countsPerDate))

#read get stock prices 
acciones=pd.read_csv("C:/Users/USUARIO/Documents/volarisAcciones.csv",header=0)
acciones['FechaString']=acciones['Fecha'].astype(str).str.replace('.','-')
acciones['FechaDate']=pd.to_datetime(acciones['FechaString'],format='%d-%m-%Y')
accionesOrdered=acciones.sort_values(by="FechaDate")
	
fecha=accionesOrdered['FechaDate'].tolist()
precioCierre=accionesOrdered['Cierre'].tolist()
fecha=fecha[1:]
precioCierre=precioCierre[1:]
dictionaryPriceDate=dict(zip(fecha, precioCierre))
	#get all dates including missing ones
fechaFull=[min(fecha)]
i=min(fecha)
while(i<max(fecha)):
    i=i+timedelta(days=1)
    fechaFull.append(i)	
for i in fechaFull:
    if i in dictionaryPriceDate:
        print("date is in the dictionary")
    else:
        iSaturday=i
        iFriday=iSaturday-timedelta(days=1)
        iMonday=iSaturday+timedelta(days=2)
        dictionaryPriceDate[iSaturday]=(dictionaryPriceDate[iFriday]+dictionaryPriceDate[iMonday])/2
        iSunday=iSaturday+timedelta(days=1)
        dictionaryPriceDate[iSunday]=(dictionaryPriceDate[iSaturday]+dictionaryPriceDate[iMonday])/2
dictionaryStatusDateFull={}
for i in list(dictionaryPriceDate.keys()):
    if i+timedelta(days=1) not in list(dictionaryPriceDate.keys()):
        print("next not available")
    elif dictionaryPriceDate[i]<=dictionaryPriceDate[i+timedelta(days=1)]:
        dictionaryStatusDateFull[i]=1.0
    else:
        dictionaryStatusDateFull[i]=0.0
dateDF=[]
countDF=[]
statusDF=[]

for i in list(dictionaryCountDate.keys()):
    dateDF.append(i)
    countDF.append(dictionaryCountDate[i])
    statusDF.append(dictionaryStatusDateFull[i])		
DF=pd.DataFrame({'date':dateDF,'Count':countDF,'status':statusDF})
DF[['sentiment1','sentiment2','sentiment3']] = pd.DataFrame(DF.Count.values.tolist(), index= DF.index)
DF.to_csv("C:/Users/USUARIO/Documents/stockDF.csv",index=False)
		