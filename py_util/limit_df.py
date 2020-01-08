#  set to directory the file is in

import pandas as pd 
import os 
import numpy as np

pd.options.display.max_columns = 100

df = pd.read_csv('20180304_final_df.csv')

## time cutoff
df = df.query("YYYYQ >=  20131 and YYYYQ <= 20174")

## column cutoff
columns = ["source","state",'postcode',"suburb","dateID",
'D_Sale_type','D_landSize',
"R_constructionStatus","sale_price",
"longitude","latitude",
"baths","propertyType","beds","parking"]

df = df[columns]

df.to_csv("20180304_property.csv")

### 
df.baths = df.baths.apply(lambda x: 5 if x > 5 else 0 if x < 0 else x  )
df.beds = df.beds.apply(lambda x: 4 if x > 4 else  0 if x < 0 else x  )
df.parking = df.parking.apply(lambda x: 3 if x > 3 else  0 if x < 0 else x  )



###  postcode summ 
baseID = ['postcode']
aggID = ['baths','beds','parking','propertyType']
poa_summ = df.groupby(baseID+aggID
    ).agg({'sale_price':[np.size,np.sum]})
poa_summ.columns = ['volume','sales']
poa_summ = poa_summ.reset_index()

poa_summ.postcode = poa_summ.postcode.astype(int) 
poa_summ.baths = poa_summ.baths.astype(int) 
poa_summ.beds = poa_summ.beds.astype(int) 
poa_summ.parking = poa_summ.parking.astype(int) 
poa_summ.volume = poa_summ.volume.astype(int) 

## put in overall
overall = poa_summ.groupby(aggID)[['volume','sales']].sum().reset_index()
overall['postcode'] = 9999

poa_summ = pd.concat([poa_summ,overall],axis=0)

poa_summ.to_csv("property_poa.csv")


