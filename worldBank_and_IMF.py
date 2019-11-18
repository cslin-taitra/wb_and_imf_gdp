# !pip install wbdatab

import pandas as pd
import wbdata as wb

# WorldBank資料來源
## http://blogs.worldbank.org/opendata/new-country-classifications-income-level-2017-2018
    
## 國家資料，收入水平
countries = wb.get_country(display=False)  
df_country = pd.DataFrame(countries)

def get_income(x):
    return x['value']

df_country['incomeLevel'] = df_country.incomeLevel.apply(get_income)
df_country[df_country.id == 'TWN']

## GDP (current US$)
## https://data.worldbank.org/indicator/NY.GDP.MKTP.CD

gdp = wb.get_data("NY.GDP.MKTP.CD")
list_gdp = []
for i in gdp:
    if  i['date'] == '2018':
        list_gdp = list_gdp + [[i['country']['id'], i['country']['value'], i['value']]]
df_gdp = pd.DataFrame(list_gdp, columns = ['iso2Code','name','value'])

## GDP growth (annual %)
## GDP 成長
## https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG

gdp_growth = wb.get_data("NY.GDP.MKTP.KD.ZG")
list_gdp_growth = []
for i in gdp_growth:
    if  i['date'] == '2018':
        list_gdp_growth = list_gdp_growth + [[i['country']['id'], i['country']['value'], i['value']]]
df_gdp_growth = pd.DataFrame(list_gdp_growth, columns = ['iso2Code','name','value'])

## GDP per capita (current US$)  
## 人均 GDP
## https://data.worldbank.org/indicator/NY.GDP.PCAP.CD

gdp_per_capita = wb.get_data("NY.GDP.PCAP.CD")

list_gdp_per_capita = []
for i in gdp_per_capita:
    if  i['date'] == '2018':
        list_gdp_per_capita = list_gdp_per_capita + [[i['country']['id'], i['country']['value'], i['value']]]
df_gdp_per_capita = pd.DataFrame(list_gdp_per_capita, columns = ['iso2Code','name','value'])

## GDP per capita growth (annual %)
## https://data.worldbank.org/indicator/NY.GDP.PCAP.KD.ZG

gdp_per_capita_growth = wb.get_data("NY.GDP.PCAP.KD.ZG")

list_gdp_per_capita_growth = []
for i in gdp_per_capita_growth:
    if  i['date'] == '2018':
        list_gdp_per_capita_growth = list_gdp_per_capita_growth + [[i['country']['id'], i['country']['value'], i['value']]]
df_gdp_per_capita_growth = pd.DataFrame(list_gdp_per_capita_growth, columns = ['iso2Code','name','value'])

df_wb_mg = df_country[['id','incomeLevel','iso2Code','name']].merge(
    df_gdp, how='left').merge(
    df_gdp_growth[['iso2Code','value']],
        left_on='iso2Code', right_on='iso2Code', how='left', suffixes=['_gdp','_gdp_growth']).merge(
    df_gdp_per_capita[['iso2Code','value']], 
        left_on='iso2Code', right_on= 'iso2Code', how='left').merge(
    df_gdp_per_capita_growth[['iso2Code','value']], 
        left_on='iso2Code', right_on='iso2Code', how='left', suffixes=['_per_capita','_per_capita_growth'])
        
# IMF 資料來源
## https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/download.aspx
## https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls

df_imf = pd.read_csv(
    'https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls',
    sep='\t',
 encoding='latin-1')

keys = [i for i in range(0,9)] + [i for i in range(47,55)]

df_imf_mg = df_imf[
    (df_imf.Units == 'U.S. dollars') &
    (df_imf['WEO Subject Code'] == 'NGDPD')].iloc[:,keys]
df_imf_mg[df_imf_mg.ISO=='TWN']


# 存為 Excel 檔案
df_wb_mg.merge(df_imf_mg.iloc[:,[1,9,10,6,7]],
              right_on = 'ISO', 
              left_on = 'id').to_excel('Country_from_WB_IMF.xlsx', index=False)
