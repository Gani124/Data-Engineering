import pandas as pd
df = pd.read_csv('Crash.csv')
#--------------------------------------------------------------------------------------------------------
#crash only dataframe
#df1
# hcrash_df= df[['Crash ID']].copy()
#df2
# crash_df=df.iloc[:,7:106].copy()
#32,33,67,79,102
# fcrash_df = hcrash_df.join(crash_df,how='outer')
# Crash_DF = fcrash_df.to_csv('Crashonly',index=False)
# print(fcrash_df)

#----------------------------------------------------------------------------------------------------------
#vehicle only dataframe
# hvehicle_df = df.iloc[:,[0,2]].copy()
# print(hvehicle_df)
# vehicle_df = df.iloc[:,106:128]
# fvehicle_df = hvehicle_df.join(vehicle_df, how = 'outer')
# Vehicle_df = fvehicle_df.to_csv('Vehicleonly', index = False)
# print(fvehicle_df)
#-----------------------------------------------------------------------------------------------------------
#participate only dataframe
# hpart_df = df.iloc[:,[0,3]].copy()
# part_df = df.iloc[:,128:159]
# fpart_df = hpart_df.join(part_df, how = 'outer')
# Part_df = fpart_df.to_csv('Participantonly', index= False)
# print(fpart_df)

