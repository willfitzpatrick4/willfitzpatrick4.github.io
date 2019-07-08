---

title: "Investigating International Energy Datasets"
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

Outputting the first 5 elements of the GDP data set:

<img src="/images/2nddataset.JPG">


### Dataset 3

The last dataset containing published records of countries' contribution to renewable and sustainable projects was then imported.

It was then reorganised and filtered in the following way:

- The country column was indexed

- The top 15 ranked countries were then queried


```python

ScimEn = pd.read_excel('scimagojr-3.xlsx')
ScimEn = ScimEn.set_index(['Country'])
ScimEn = ScimEn[(ScimEn['Rank'] < 16)]

```

With the first 15 elements of the Scimajr dataset as follows:

<img src="/images/thetop15rankedfinalset.JPG">


## Merging the Data Sets

To execute beneficial analysis on the data it was necessary to merge all three of the sets to yield data cohesive for all three of the files, this was achieved using pandas merge function sequentially.

Firstly the energy dataset was merged to output the intersection of both the datasets (using pandas pd.merge and setting 'how' to 'inner') the 'Country' index was.

This was then repeated. The first merged set was combined with the scimajr set to yield a combination of all three sets.


``` python
Merged = pd.merge(Energy, GDP, how='inner', left_index=True, right_index=True)

secondMerged = pd.merge(Merged, ScimEn, how='inner', left_index=True, right_index=True)

columns_to_include = ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '%Renewable', '2006', '2007', '2008', '2009',
'2010', '2011', '2012', '2013', '2014', '2015']

Combined = secondMerged[columns_to_include]
Combined = Combined.rename(index=str, columns={' ': 'Country'})
Combined = Combined[(Combined['Rank'] < 16)]
A1 = Combined[(Combined['Rank'] < 16)]

```

The first 15 countries of the merged set, in order of rank, were as follows:

<img src="/images/finalmergedset.JPG">

# Data Investigation

## Q1 How Many Countries Were lost in the Creation of the New Data Set?

This can be calculated by creating a new set with the union of all the data (by using 'how' and 'outer' sequentially).

The length of this set is calculated, and the length of the 1st merged set (containing the intersection of all three datasets) is subtracted.

```HTML

<svg width="800" height="300">
  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />
  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />
  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />
  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>
  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>
</svg>

```

``` python
Merged2 = pd.merge(Energy, GDP, how='outer', left_index=True, right_index=True)
Merged3 = pd.merge(Merged2, ScimEn, how='outer', left_index=True, right_index=True)

Merged4 = pd.merge(GDP, Energy, how='inner', left_index=True, right_index=True)
Merged5 = pd.merge(Merged4, ScimEn, how='inner', left_index=True, right_index=True)

A2 = len(Merged3)-len(Merged5)

```

Outputting a value of 173.

## Q2 What is the Average GDP over the past 10 Years for each country?

Here it was necessary to output a panda series including the average GDP of the 15 countries over the last 10 years.

Within Iran's '2015' GDP data there existed a NaN output. To exclude this from the calculations the median GDP (based on other values) was taken for '2015' and the mean GDP was calculated.

```python
Top15 = A1
Col = ['2015']
Top15[Col] = Top15[Col].fillna(Top15[Col].median())
```

The necessary calculation was then computed and outputted to a new column.

This was then converted to a pandas series and ordered from highest to lowest.

```python
Top15['avgGDP'] = ((Top15['2006'] + Top15['2007'] + Top15['2008'] + Top15['2009'] + Top15['2010'] + Top15['2011'] + Top15['2012'] + Top15['2013'] + Top15['2014'] + Top15['2015']) / 10)

[columns_to_keep] = ['avgGDP']

A3 = Top15[columns_to_keep]
A3 = pd.Series(Top15['avgGDP'])

A3.sort('avgGDP', ascending=False)
```
Outputting the following series:


<img src="/images/averageGDPover10years.JPG">
