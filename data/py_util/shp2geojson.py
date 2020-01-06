
# source:https://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/1270.0.55.003July%202016?OpenDocument
# directory: work from the directory where shape file downloaded
# export to directory above

import shapefile
import json
import os ,re 
import pandas as pd 


# read the shapefile
reader = shapefile.Reader("1270055003_poa_2016_aust_shape/POA_2016_AUST.shp")

feature = reader.shapeRecords()[0]

fields = reader.fields[1:]
fields_df = pd.DataFrame(fields,columns=['name','format','length','unknown'])


aaa = [sr.record for sr in reader.shapeRecords()]

buffer = []
for idx,sr in enumerate(reader.shapeRecords()):
    poa_name = sr.record[1]
    if re.match("2\d{3}",poa_name) is None :
        continue
    print('POA name: "{p}"'.format(p=poa_name))
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature", \
    geometry=geom, properties=atr)) 

# write the GeoJSON file

geojson = open("POA_2016_NSW.geojson", "w")
geojson.write(dumps({"type": "FeatureCollection", "features": buffer}) )
geojson.close()
