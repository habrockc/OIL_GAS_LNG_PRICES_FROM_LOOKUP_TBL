# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 10:40:14 2021

@author: cdhabro
"""

import pandas as pd
import numpy as np
import seaborn as sns

sns.set_style("darkgrid")


### create a time-series dataframe

startDate = "1/1/2021"
print(f"Begin table date: {startDate}")
#endDate = dt.date.today()
endDate = "5/15/2021"
print(f"Today: {endDate}")



dfCal = pd.DataFrame({"DATE": pd.date_range(start=startDate, end=endDate, freq="d")})

print(dfCal)
print("\n"*2)







### create a lookup table for 2-stream oil and gas
### for all lookup tables, create a list of 2-element tuples with first element being a string date and second a float value

lookupOil = []
lookupOil = [("12/23/2020", 40.00), ("12/28/2020", 43.34), ("1/21/2021", 45.27), ("5/3/2021", 57.99), ("7/17/2021", 99.99)]


dfOil = pd.DataFrame(data=lookupOil, columns=["DATE", "OIL"])
dfOil["DATE"] = pd.to_datetime(dfOil["DATE"])
print(dfOil)
print("\n"*2)



lookupGas = [("12/29/2020", 3.39), ("1/23/2021", 3.27), ("2/10/2021", 2.79), ("7/21/2021", 333.33)]

dfGas = pd.DataFrame(data=lookupGas, columns=["dat", "GAS"])
dfGas["dat"] = pd.to_datetime(dfGas["dat"])
print(dfGas)
print("\n"*2)



lookupLNG = [("12/29/2020", 6.50), ("1/23/2021", 5.75), ("5/13/2021", 5.99), ("2/10/2021", 4.79)]

dfLNG = pd.DataFrame(data=lookupLNG, columns=["date", "LNG"])
dfLNG["date"] = pd.to_datetime(dfLNG["date"])
print(dfLNG)
print("\n"*2)








### write a function that can take any lookup table and add values to the main table based on dates


def match_values(mainTable, lookupTable, mainTableDate, lookupTableDate, lookupTableValueColumn):
    
    ### checking to see if at least one row (date and value) exist, if not then quit and return nothing
    if lookupTable.shape[0] == 0:
        print(f"CAUTION: {lookupTable} is length of 0, continuing to next lookup table.")
        return None

    
    df = pd.merge(left=mainTable, right=lookupTable, how="left", left_on=[mainTableDate], right_on=[lookupTableDate])
    df[lookupTableValueColumn] = df[lookupTableValueColumn].ffill()
    print(df[0:30])
    print("\n"*2)
    
    ### get all dates in lookup table that are not in main table
    lookupDatesNotInCal = lookupTable[lookupTable[lookupTableDate].isin(mainTable[mainTableDate]) == False] 
    
    ### get min date in main table
    minCalenderTableDate = mainTable[mainTableDate].min()
    
    ### remove dates not in main table but that are after the min date of main table (bullet proof errors)
    lookupDatesNotInCal = lookupDatesNotInCal[lookupDatesNotInCal[lookupTableDate] < minCalenderTableDate]
    
    ### now get max date of all dates not in main table to get most recent date before main table dates begin
    maxLookupDateNotInCal = lookupDatesNotInCal.max()
    #print(maxLookupDateNotInCal)
    #print("\n"*2)
    
    ### need to work on logic above to ensure only getting max values that are less than min calendar val
    backfillDate = maxLookupDateNotInCal[lookupTableDate]
    backfillValue = maxLookupDateNotInCal[lookupTableValueColumn]
    
    print(f"Last date in lookup: {backfillDate}")
    print(f"Last value in lookup: {backfillValue}")
    print("\n"*2)
    
    df[lookupTableValueColumn] = np.where((df[lookupTableValueColumn].isna() == True), backfillValue, df[lookupTableValueColumn])
    print(df)
    print("\n"*2)

    df.rename(columns={lookupTableDate:"DATE"}, inplace=True)
    print(df)
    print("\n"*2)
    return df


### call function and assign to new dataframe for each lookup item
newDfO = match_values(dfCal, dfOil, "DATE", "DATE", "OIL")
newDfG = match_values(dfCal, dfGas, "DATE", "dat", "GAS")
newDfLNG = match_values(dfCal, dfLNG, "DATE", "date", "LNG")
### add new dataframes above from function call to list for later concatenation
listOfDataFrames = [newDfO, newDfG, newDfLNG]
### concatenate all dataframes in list by columns (axis=1)
dfConcat = pd.concat(listOfDataFrames, axis=1)
print(dfConcat[0:60])
print("\n"*2)

### due to concatenation, drop duplicated columns
dfWant = dfConcat.loc[:, ~dfConcat.columns.duplicated()]
print(dfWant)
print("\n"*2)


dfWant.plot(x="DATE", kind="line", figsize=(10,8))
