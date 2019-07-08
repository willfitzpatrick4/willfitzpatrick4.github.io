---

title: "Cleaning/Merging of International Energy Datasets"
date: 2018-02-21
tags: [Data Science]
header:
  image: "/images/worldwideenergy.jpg"
excerpt: "Data Science, Data Cleaning , Data Analysis"

---

# Introduction

This project looked at 3 publically available datasets associated with international energy consumption.

The first dataset contains a list of indicators for energy supply and renewable electricity production from the United Nations from the year 2013.

The second dataset is an international record from the World Bank containing countries' GDP from 1960 to 2015.

The third contains records of the Sciamgo Journal and Country Rank for Energy Engineering and Power Technology. This ranks countries based on their journal contributions with regards to areas mentioned in the previous sets.

## Reorganisation and Cleaning

### Dataset 1

The first dataset was imported and the header and footer of the file were removed.  

```python

import pandas as pd
import numpy as np

Energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skipfooter=38)

```
The first 10 countries in the list were as follows:

<img src="/images/dataset1first10countries.JPG">

To achieve this extra lines of code were implemented:

- The columns were  renamed to the relevant subcategories

- The country column was set as the index

- The columns were  renamed to the relevant subcategories and the redundant columns were deleted


```python

Energy = Energy.rename(index=str, columns={"Unnamed: 2": "Countries", "Petajoules": "Energy Supply", "Gigajoules": "Energy Supply per Capita", "%": "%Renewable"})
Energy = Energy.set_index(['Countries'])
Energy = Energy.drop(Energy.columns[[0, 1]], axis=1)

```

- Next the data was cleaned to ensure the country names were coherent to the other datasets.


### Dataset 2

The second dataset from the world bank was imported containing international GDP levels.

Likewise as with the first set:

- The header was bypassed

- Inconsistencies in the country labels were rectified

- The country column was set as the index

- NaN cells were then dropped from the dataset 

```python

import pandas as pd
GDP = pd.read_csv('world_bank.csv', skiprows=4)
GDP = GDP.rename({"Hong Kong SAR, China": "Hong Kong", "Iran, Islamic Rep.": "Iran", "Korea, Rep.": "South Korea"})
GDP = GDP.set_index(['Country Name'])
GDP = GDP.dropna()


```

<img src="/images/2nddataset.JPG">


### Dataset 3

The last dataset containing published records of countries' contribution to renewable and sustainable projects was then imported.

It was then reorganised in the following way:

- The country column was indexed
- The top 15 ranked countries were then queried


```python

ScimEn = pd.read_excel('scimagojr-3.xlsx')
ScimEn = ScimEn.set_index(['Country'])
ScimEn = ScimEn[(ScimEn['Rank'] < 16)]

```


<img src="/images/thetop15rankedfinalset.JPG">
