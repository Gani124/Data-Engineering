import pandas as pd
import matplotlib. pyplot as mp
import seaborn as sb
# ======================county_info data============================================
df = pd.read_csv('acs2017_census_tract_data.csv', usecols = [1,2,3,15,17])

df['Total income'] = df['IncomePerCap'] * df['TotalPop']
df['poverty population'] = round((df['Poverty'] * df['TotalPop'])/100)

df = df.groupby(['County', 'State'])[['TotalPop','Total income','poverty population']].sum()

df['poverty percentage'] = round((df['poverty population']*100) / df['TotalPop'])
df['percapitalincome'] = round((df['Total income']/df['TotalPop']))

df.reset_index(inplace=True)
df.insert(0,'ID',range(1, len(df) + 1))
df['County'] = df['County'].str.replace(' County', '', case=False)
# myfile = df.to_csv('county_info.csv', index=False)
#print(df)
#========Most populous county in the USA and Least populous county in the USA========
# high_val = df['TotalPop'].max()
# less_val = df['TotalPop'].min()
# df1 = df.loc[df['TotalPop'] == high_val]
# df2 = df.loc[df['TotalPop'] == less_val]
# print('Most populous county in the USA is', df1['County'].iloc[0])
# print('Less populous county in the USA is', df2['County'].iloc[0])
#============================County_monthly===========================================
df1 = pd.read_csv('COVID_county_data.csv',usecols=[0,1,2,4,5])
df1['date'] = pd.to_datetime(df1['date'])  #-- converting in to date, time and month
df1['Month'] = df1['date'].dt.month #--taking only month out of it and adding as new column
df1['Year'] = df1['date'].dt.year #-- taking only year out of it and adding as new column
df1 = df1.groupby(['County','State','Month','Year']).sum()
df1.reset_index(inplace=True)
df1.insert(0,'ID',range(1, len(df1) + 1))
# myfile = df1.to_csv('COVID_monthly.csv',index=False)
# print(df1)
#==============================Integrated Database======================================
df2 = df1.groupby(['County','State'])[['cases','deaths']].sum()
df2.reset_index(inplace=True)
df2.insert(0,'ID',range(1, len(df2) + 1))
df3 = pd.merge(df, df2, on=['State','County'], how='inner')
df3 = df3.drop(columns=['Total income','poverty population','ID_x','ID_y'])
df3.insert(0,'ID',range(1, len(df3) + 1))
df3['TotalCasesPer100K'] = df3['cases'] / (df3['TotalPop'] / 100000)
df3['TotalDeathsPer100K'] = df3['deaths'] / (df3['TotalPop'] / 100000)
# myfile = df3.to_csv('covid_summary.csv',index=False)
# print(df3)
#======================corelation coefficient==========================================
state_name = 'Oregon'
res_df = df3.loc[df3['State'] == state_name]
#===================COVID total cases vs. % population in poverty======================
correlation1 = res_df['cases'].corr(res_df['poverty percentage'])
#===================COVID total deaths vs. % population in poverty=====================
correlation2 = res_df['deaths'].corr(res_df['poverty percentage'])
#==================COVID total cases vs. Per Capita Income level=======================
correlation3 = res_df['cases'].corr(res_df['percapitalincome'])
#==================COVID total deaths vs. Per Capita Income level======================
correlation4 = res_df['deaths'].corr(res_df['percapitalincome'])
#===================COVID total cases vs. % population in poverty=======================
correlation5 = df3['cases'].corr(df3['poverty percentage'])
#===================COVID total deaths vs. % population in poverty======================
correlation6 = df3['deaths'].corr(df3['poverty percentage'])
#===================COVID total cases vs. Per Capita Income level=======================
correlation7 = df3['cases'].corr(df3['percapitalincome'])
#===================COVID total deaths vs. Per Capita Income level======================
correlation8 = df3['deaths'].corr(df3['percapitalincome'])
#===================correlation between population and COVID cases======================
correlation9 = df3['TotalPop'].corr(df3['cases'])
#===================correlation between cases and deaths================================
correlation10 = df3['cases'].corr(df3['deaths'])

# print(f"The correlation for covid cases in {state_name} is: {correlation1},{correlation3}")
# print(f"The correlation for covid deaths in {state_name} is: {correlation2},{correlation4}")
# print(f"The correlation for covid cases in USA is: {correlation5},{correlation7}")
# print(f"The correlation for covid deaths in USA is: {correlation6},{correlation8}")
# print(f"The correlation for total population for covid deaths in USA is: {correlation9}")
# print(f"The correlation for covid cases and deaths in USA is: {correlation10}")
#==============================Data Visualization=======================================
plot = df3.plot.scatter(x = 'cases',y='deaths',c='DarkBlue')
mp.show()

plot2 = df3.plot.scatter(x = 'TotalPop',y='cases',c='Red')
mp.show()
#=======================================================================================



    