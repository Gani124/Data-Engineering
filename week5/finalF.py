import pandas as pd
import datetime
# df = pd.read_csv('trimetS.csv',usecols = [0,2,3,4,5,6,7])
# df = pd.read_csv('trimetFP.csv',usecols = [0,2,3,4,5,6,7])
df = pd.read_csv('trimetGP.csv', usecols = [0,2,3,4,5,6,7])
# ----------------------------- OPD_DATE,ACT_TIME CONVERSION AS TIMESTAMP IN TO NEW COLUMN-----------------------------------------------------
def combine_datetime(opd_date, act_time):
    dateTime = datetime.datetime.strptime(opd_date, '%d%b%Y:%H:%M:%S') + datetime.timedelta(seconds=int(act_time))
    return dateTime
df['TIMESTAMP'] = df.apply(lambda x: combine_datetime(x['OPD_DATE'], x['ACT_TIME']), axis=1)
df = df.drop(columns=['OPD_DATE','ACT_TIME'])
#-------------------------------------------------SPEED CONVERSIONS--------------------------------------------------------------
df['dMETERS'] = df.groupby('EVENT_NO_TRIP')['METERS'].diff()
df['dTIMESTAMP'] = df.groupby('EVENT_NO_TRIP')['TIMESTAMP'].diff()
df['SPEED'] = df.apply(lambda x : x['dMETERS']/x['dTIMESTAMP'].total_seconds(),axis=1)
df = df.drop(columns=['dMETERS','dTIMESTAMP'])
#filling NaN with 0
df['SPEED'] = df['SPEED'].fillna(0)
# print(df)
#------------------------------------------------- F,G section Q/A ----------------------------------------------------------------
#1) getting max value of 4223 bus without grouping event trip
maxspeed=df['SPEED'].max()
print('Maximum speed of the bus', df.loc[df['SPEED'] == maxspeed, 'VEHICLE_ID'].values[0], 'is', maxspeed)

#2) getting GPS latitude and longitude of that max value
maxspeed_row = df.loc[df['SPEED'] == maxspeed] #-- to get all the rows with all other required row values
print('Below are the full details where speed will be maximum speed: \n' ,maxspeed_row)

#3) median speed of the vehicle
medianspeed = df['SPEED'].median()
print('Median speed of the bus', df.loc[df['SPEED'] == medianspeed, 'VEHICLE_ID'].values[0], 'is', medianspeed)

#4) which vehicle has fastest mean speed for any single trip on this day
meanspeed = df.groupby(['VEHICLE_ID','EVENT_NO_TRIP'])['SPEED'].describe()
only_mean_speed = meanspeed['mean']
fast_mean_speed = only_mean_speed.max()
mean_speed_row = meanspeed.loc[only_mean_speed == fast_mean_speed]
print(mean_speed_row)