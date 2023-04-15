# importing required modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as matp
import seaborn as sbr
import regex as re
from pylab import rcParams
from urllib.request import urlopen
from bs4 import BeautifulSoup

# connecting required URL to the url library where we pull out the data
# Dataset1
url = "http://www.hubertiming.com/results/2017GPTR10K"
# Dataset2
# url = "https://www.hubertiming.com/results/2023WyEasterLong"
html = urlopen(url)

# beautiful soup is to extract data from the html and xml files.
soup = BeautifulSoup(html, 'lxml')

# taking all the tr=table rows
rows = soup.find_all('tr')

# empty array for result
Final_rows = []

# loop through the table data in cells and take the string text value using bs4
for row in rows:
    td = row.find_all("td")
    text = str(td)
    Final_text = BeautifulSoup(text, 'lxml').get_text()
    Final_rows.append(Final_text)

# converting the result in to dataframe
df = pd.DataFrame(Final_rows)

# splitting the columns
df1 = df[0].str.split(',', expand=True)

# getting table headers using beautiful soup
header = soup.find_all("th")

# empty array for result
Final_header = []

# fetching text from header using soup
Header_text = str(header)
Final_Header_text = BeautifulSoup(Header_text, 'lxml').get_text()
Final_header.append(Final_Header_text)

# dataframe for header
df2 = pd.DataFrame(Final_header)

# splitting the header
df3 = df2[0].str.split(',', expand=True)

# remvoing square brackets from header without using column names
df3 = df3.apply(lambda x: x.str.strip('[]'))

# concatinating the both data data frames header followed by data
frames = [df3, df1]
df4 = pd.concat(frames)

# reconfig the data frame
df5 = df4.rename(columns=df4.iloc[0])

# removing null values
df6 = df5.dropna(axis=0, how='any')

# remvoing duplicate header entry
df7 = df6.drop(df6.index[0])

# remvoing square brackets from data
df7 = df7.apply(lambda x: x.str.strip('[]'))

# removing \r \n characters from data frame
df7 = df7.replace(r'\n', ' ', regex=True)
df7 = df7.replace(r'\r', ' ', regex=True)
df7 = df7.replace(r'  ', '', regex=True)

# visualization part
time = df7[' Time'].tolist()

# empty array
converted_time = []

# converting time in to mins


def converting(s):
    t = 0
    for u in s.split(':'):
        t = 60 * t + int(u)
    return t / 60


# appending to empty array
for i in time:
    converted_time.append(converting(i))

# New column to the data frame
df7['Runner_mins'] = converted_time
print(df7)

# visualization using pylab
# 1st question
rcParams['figure.figsize'] = 10, 5
df7.boxplot(column='Runner_mins')
matp.grid(True)
matp.ylabel(' Time')
matp.xticks([1], ['Runners'])
matp.show()

# 2nd question visualization
plot = df7['Runner_mins']
sbr.distplot(plot, hist=True, kde=True, color='m',
             hist_kws={'edgecolor': 'Black'}, bins=20)
matp.show()

# 3rd question visualization
f = df7.loc[df7[' Gender'] == ' F']['Runner_mins']
m = df7.loc[df7[' Gender'] == ' M']['Runner_mins']
sbr.distplot(f, hist=True, kde=True, label='Female',
             hist_kws={'edgecolor': 'Black'})
sbr.distplot(m, hist=False, kde=True, label='Male')
matp.title('Performance')
matp.legend()
matp.show()

# Visualization based on gender
df7.boxplot(column='Runner_mins', by=' Gender')
matp.ylabel('Chip Time')
matp.suptitle("")
matp.show()

# visualization code for gender O
# o= df7.loc[df7[' Gender']==' O']['Runner_mins']
# sbr.distplot(o, hist=True, kde=True, label='Female', hist_kws={'edgecolor':'Black'})=0)
# matp.show()

# Groupby Stats
group = df7.groupby(" Gender", as_index=True).describe()
print(group)
