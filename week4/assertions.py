import pandas as pd
import numpy as np
# df = pd.read_csv('Participantonly.csv')
# df = df.iloc[:,[0,1]]
# # df = df.head(15)
# df = df.dropna(subset=['Crash ID','Participant ID'])
# print(df)
#---------------------------------------------------------------------------
#existance assertion
# df = pd.read_csv('Crashonly.csv')
# df = df.iloc[:,[2,3,4]]
# # df = df.head(15)
# df = df.dropna(subset=['Crash Month','Crash Day','Crash Year'])
# # print(df)
# if(df['Crash Year'] == 2019).all():
#     for i in range(1,13):
#         if((df['Crash Month'] == i)).any():
#             counts = df['Crash Month'].value_counts().sort_index()
#             total = counts.sum()
#             print('Success. It has month',i ,'and the total count is',counts[i])
#         else:
#             print("Failed. It don't have month",i)
#------------------------------------------------------------------------------
#Limit assertion
# df = pd.read_csv('Crashonly.csv')
# df = df.iloc[:,[12,49]]
# df = df.dropna(subset=['Highway Number','Weather Condition'])
# # print(df)
# if(df['Highway Number'] == 26).all():
#     if(df['Weather Condition'] == 3).any():
#         counts = df['Weather Condition'].value_counts().sort_index().rename_axis('Rainy Crashes')
#         # print(counts)
#         print('Rainy conditions on Mount hood highway with code number',counts.index[3],'count of',counts[3])
#-------------------------------------------------------------------------------
#intra record assertions
# df = pd.read_csv('Vehicleonly.csv')
# df = df.iloc[:,[0,1]]
# df = df.dropna(subset=['Crash ID','Vehicle ID'])
# # print(df)
# if not df['Crash ID'].isnull().all():
#     if not df['Vehicle ID'].isnull().all():
#         print('There is a crash ID for every single vehicle ID')
#     else:
#         print('fail')
# else:
#     print('fail')
#-----------------------------------------------------------------------------
#inter-record assertions(1)
# df = pd.read_csv('Crashonly.csv')
# df = df.iloc[:,[3]]
# df = df.dropna(subset=['Crash Day'])
# # print(df)
# df2 = pd.read_csv('Participantonly.csv')
# df2 = df2.iloc[:,[0,1]]
# df2 = df2.dropna(subset=['Crash ID','Participant ID'])
# # print(df2)
# final_df = df.join(df2, how='outer')
# # print(final_df)

# if not final_df['Participant ID'].isnull().all():
#     if not final_df['Crash ID'].isnull().all():
#         if not final_df['Crash Day'].isnull().all():
#             print('success')
#         else:
#             print('fail')
#     else:
#         print('fail')
# else:
#     print('fail')
#-------------------------------------------------------------
#inter-record assertions(2)
# df = pd.read_csv('Crashonly.csv')
# df = df.iloc[:,[0,7]]
# df = df.dropna(subset=['County Code'])
# # print(df)
# if not df['Crash ID'].isnull().all():
#     if not df['County Code'].isnull().all():
#         print('Success')
#     else:
#         print('fail')
# else:
#     print('fail')
#-------------------------------------------------------------------
#inter-record assertions(3)
# df = pd.read_csv('Vehicleonly.csv')
# df = df.iloc[:,[0,4]]
# df = df.dropna(subset=['Vehicle Type Code','Crash ID'])
# # print(df)
# if not df['Vehicle Type Code'].isnull().all():
#     if not df['Crash ID'].isnull().all():
#         print('Success')
#     else:
#         print('fail')
# else:
#     print('fail')
#---------------------------------------------------------------------
#summary assertion(1)
# df = pd.read_csv('Crashonly.csv')
# df = df.iloc[:,[0,36]]
# count = 0
# for index,row in df.iterrows():
#     if row['Road Character'] == 1:
#         count += 1
# print(count)
#-----------------------------------------------------------------------
#summary assertion(2)
# df = pd.read_csv('Crashonly.csv')
# df = df[['Alcohol-Involved Flag']].copy()
# df = df.dropna(subset=['Alcohol-Involved Flag'])
# df2 = df[df['Alcohol-Involved Flag'] == 1]
# sub_size = len(df2)
# total_size = len(df)
# percentage = sub_size/total_size * 100 
# print('Total Percentage that participant had found drinking is',round(percentage))
#-----------------------------------------------------------------------------------------------
#summary assertion(3)
# df = pd.read_csv('Vehicleonly.csv')
# df = df[['Vehicle Hit & Run Flag']].copy()
# df = df.dropna(subset=['Vehicle Hit & Run Flag'])
# df2 = df[df['Vehicle Hit & Run Flag'] == 1]
# hit_size = len(df2)
# total_size = len(df)
# percentage = hit_size/total_size * 100
# print('Total percentage of vehicle Hit and Run is',round(percentage))
#------------------------------------------------------------------------------------------------
#statistical assertion(1)
# df = pd.read_csv('Crashonly.csv')
# df = df[['Crash Month']].copy()
# df = df.dropna(subset=['Crash Month'])
# count = df.value_counts().sort_index()
# mean = df.shape[0]/12
# stnd = count.std()
# threshold = 1.0
# score = (count -mean)/stnd
# if (score > threshold).any():
#     print('Crashes are evenly distributed')
# else:
#     print('crashes are not evenly distributed')
#--------------------------------------------------------------
#statistical assertion(2)
# df = pd.read_csv('Crashonly.csv')
# df = df.iloc[:,[0,49]]
# df = df.dropna(subset=['Crash ID','Weather Condition'])
# total_crashes = len(df['Crash ID'])
# cause_counts = df['Weather Condition'].value_counts().sort_index()
# expected_crash = total_crashes/len(cause_counts)
# difference = expected_crash - cause_counts
# root_measure = ((difference ** 2).sum() / len(cause_counts)) ** 0.5
# if root_measure > 10:
#     print('yes, evenly distributed')
# else:
#     print('No, not evenly distributed')
#----------------------------------------------------------------------------------


