"""
This code aims to find the 66 optimized fire stations based on the fire interventation data.
"""

import pandas as pd
import time
import numpy as np
from sklearn.cluster import KMeans
import gzip

# from IPython.core.display import display, HTML
# display(HTML("<style>.container { width:90% !important; }</style>"))
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_colwidth', 150)
currenttime = time.time()

# Read the Montreal Fire Interventation data downloaded from http://donnees.ville.montreal.qc.ca/
with gzip.open('FireInterventionData_All_20190312_Update.csv.gz') as f:
    FireDataAll = pd.read_csv(f)
# FireDataAll = pd.read_csv('FireInterventionData_All_20190312_Update.csv')
FireDataAll = FireDataAll.loc[FireDataAll.latitude != 0]
FireDataAll = FireDataAll.loc[FireDataAll.year >=2018]
FireDataAll = FireDataAll[["longitude","latitude"]]

# Since the longitude and latitude per degree are not the same length of arc, here we
# need to correct the length difference.
lonmin = FireDataAll.longitude.min()
latmin = FireDataAll.latitude.min()
FireDataAll.longitude = (FireDataAll.longitude - lonmin) * 79/111
FireDataAll.latitude = (FireDataAll.latitude - latmin)


# Extrace the corrected longitude and the latitude value from the original data.
X = FireDataAll[["longitude","latitude"]].values
# np.where(np.isnan(X))

# Fit the model based on the X
kmeans = KMeans(n_clusters=66)  
kmeans.fit(X) 


result2009 = pd.DataFrame(kmeans.cluster_centers_)
result2009.columns = ["longitude","latitude"]
# Transform the longitude and latitude back to the original arc distance.
result2009.longitude = 111/79 * result2009.longitude + lonmin
result2009.latitude =  result2009.latitude + latmin


# Write the result into the csv file. Which are the oprimized location.
result2009.to_csv("Results/KmeansResult2009_WithDeformCorrection_result.csv")
print("Total time elapsed =", time.time() -currenttime)