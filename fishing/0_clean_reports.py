import pandas as pd
import numpy as np

imputation = True #Set to False to not use AIS data to impute

file = pd.read_csv(r'./result.csv')

# Select only the potero vessels
ceibe = file[file['Barco Lote (Descripción)']=='CEIBE DOUS']
luis = file[file['Barco Lote (Descripción)']=='DON LUIS I']
mateo = file[file['Barco Lote (Descripción)']=='SAN MATEO']
orion3 = file[file['Barco Lote (Descripción)']=='ORION 3']
francisco = file[file['Barco Lote (Descripción)']=='DON FRANCISCO I']
orion5 = file[file['Barco Lote (Descripción)']=='ORION 5']

result = ceibe.append([luis,mateo,orion3,orion5,francisco])

result = result[['Barco Lote (Descripción)','Fecha','KN','KB','LAT','LONG']]
result['KN'] = result['KN'].str.replace(",", "")
result['KN'] = pd.to_numeric(result['KN'])
result['KB'] = result['KB'].str.replace(",", "")
result['KB'] = pd.to_numeric(result['KB'])
result.Fecha = pd.to_datetime(result.Fecha,format="%d/%m/%y")
result = result[result.LAT !='S/C']
result = result[result.LAT !='A PTO']

result.LAT = result.LAT.str.replace('\'','')
result.LONG = result.LONG.str.replace('\'','').str.replace('´','')

# Change coordinates to decimal degrees
result['Latitude'] = pd.to_numeric(result.LAT.str[0:2]) + pd.to_numeric(result.LAT.str[-2:])/60
result['Longitude'] = pd.to_numeric(result.LONG.str[0:2]) + pd.to_numeric(result.LONG.str[-2:])/60

result = result[['Barco Lote (Descripción)','Fecha','KN','Latitude','Longitude']]
result.columns = ['Embarcacion','Day','KN','Latitude','Longitude']

# Map into Predefined Grid
result['Latitude'] = [np.ceil(x)-0.25 if abs(x-np.ceil(x))<0.5 else np.ceil(x)-0.75 for x in result['Latitude']]
result['Longitude'] = [np.ceil(x)-0.25 if abs(x-np.ceil(x))<0.5 else np.ceil(x)-0.75 for x in result['Longitude']]

# Aggregate the different kg caught per size by boat,day and Grid
result = result.groupby(['Embarcacion','Day','Latitude','Longitude']).sum().reset_index()

# Imputation

if imputation:
    ############ DATA ###############

    quadrants = pd.read_csv(r'fishing_quadrants.csv')

    ############## PROCESS ##############

    #Split impute vs no impute

    keep = result.dropna()
    impute  =result[result.isna().any(axis=1)]

    # Keep quadrant with more daily fishing hours
    quadrants = quadrants.sort_values(by=['Embarcacion','Day','Duration'],ascending=[True,True,False])
    quadrants = quadrants.drop_duplicates(['Embarcacion','Day'],keep= 'first')

    # Impute
    impute = pd.merge(impute,quadrants)
    impute = impute[[['Embarcacion','Day','KN','GridLat','GritLon']]]
    impute.columns = ['Embarcacion','Day','KN','Latitude','Longitude']

    # Merge datasets
    data = pd.concat([keep,impute])


result.to_csv(r'./fishing_result.csv',index=False)