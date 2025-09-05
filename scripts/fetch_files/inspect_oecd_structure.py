import pandas as pd
import requests
from io import StringIO

# OECD Time Use dataset API (CSV)
url = "https://sdmx.oecd.org/public/rest/data/OECD.WISE.INE,DSD_TIME_USE@DF_TIME_USE,1.0/?dimensionAtObservation=AllDimensions&format=csvfilewithlabels"

# Add headers so server accepts the request
headers = {"User-Agent": "Mozilla/5.0"}

# Fetch CSV text
resp = requests.get(url, headers=headers)
resp.raise_for_status()  # will raise error if request fails

# Load into pandas
df = pd.read_csv(StringIO(resp.text))
df.head()
