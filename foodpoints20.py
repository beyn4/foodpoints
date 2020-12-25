"""
Created on 11/17/2020

@author: nadia
"""

import pandas as pd
import datetime
import matplotlib.pyplot as plt

dukecard = {}
trans = {}


def makedataframe(f):
    frame = pd.DataFrame(f)
    return frame


def addtodict(dict,loc):
    if dict == dukecard:
        dict["Balance"] = 0
        dict["Spent"] = 0
    for x in loc:
        if "DukeCard" in x:
            pass
        else:
            dict[x] = 0
    return dict


def amounts(data):
    """
    return dollar amount in dataframe as float
    """
    usd = data['Amount']
    for x in usd:
        if isinstance(x,float):
            pass
        elif "(" in x:
            money = float(x[x.index("(")+1:x.index(")")])
            usd.replace(to_replace=x, value=money,inplace=True)
        elif "," in x:
            money = float(x[0:x.index(",")] + x[x.index(",")+1:x.index("USD")])
            usd.replace(to_replace=x,value=money,inplace=True)
        else:
            money = float(x[:x.index("USD")])
            usd.replace(to_replace=x, value=money,inplace=True)
    return data


def balances(data):
    """
    add credit to balance in dict, subtract credit from location unless dukecard
    add debit to location in dict, subtract from balance
    """
    k = amounts(data)
    for index, row in k.iterrows():
        if row.iloc[4] == "Credit":
            if "DukeCard" in row.iloc[3]:
                dukecard["Balance"] += row.iloc[5]
            else:
                dukecard["Balance"] += row.iloc[5]
                dukecard[row.iloc[3]] -= row.iloc[5]
                dukecard["Spent"] -= row.iloc[5]
        elif row.iloc[4] == "Debit":
            if "DukeCard" in row.iloc[3]:
                pass
            else:
                dukecard["Balance"] -= row.iloc[5]
                dukecard[row.iloc[3]] += row.iloc[5]
                dukecard["Spent"] += row.iloc[5]
    return dukecard

def convert_time(dt):
    """
    standardize datetime
    """
    t = pd.to_datetime(dt)
    return t


def checktime(t1,t2):
    """
    compare datetime for two transactions
    """
    time = t1 - t2
    diff = datetime.timedelta(minutes=2)
    if time < diff:
        return True
    else:
        return False


def count_transactions(data):
    """
    count number of transactions at location
    if datetime of subsequent transactions at same location are <2 minutes apart, return one trans
    """
    loc = data['Location']
    addtodict(trans,loc)
    for i in range(len(loc) - 2):
        if "DukeCard" in loc[i]:
            i += 1
        else:
            if loc[i] == loc[i+1]:
                ct = checktime(data['Date/Time'][i],data['Date/Time'][i+1])
                if ct == True:
                    trans[loc[i]] += 1
                    i += 1
                else:
                    pass
            else:
                trans[loc[i]] += 1
    return trans


def condense2(dict):
    final = {}
    places = {"Au Bon Pain": "Au Bon Pain", "Loop": "The Loop", "McD": "McDonald's", "Pitchfork": "Pitchfork's",
              "Pegram": "Pegram Vending", "Hollows": "Hollows Vending", "Carr": "Classroom Vending",
              "House BB": "Magnolia Vending", "Il Forno": "Il Forno", "Beyu": "Beyu Blue",
              "Marketplace": "Marketplace", "Trinity": "Trinity Cafe", "The Cafe": "Cafe",
              "Divinity": "Divinity Cafe", "Perk": "Vondy (Saladelia)", "Skillet": "Skillet"}
    if dict == dukecard:
        final["Balance"] = dict["Balance"]
        final["Spent"] = dict["Spent"]
    for k,v in dict.items():
        for p,l in places.items():
            if p in k:
                if places[p] not in final:
                    final[places[p]] = 0
                    final[places[p]] += v
                else:
                    final[places[p]] += v
    ret = {key: round(val,2) for key, val in final.items()}
    return ret


def bargraph(dict):
    d = condense2(dict)
    x = [k for k,v in d.items()]
    y = [v for k,v in d.items()]
    if dict == dukecard:
        x = x[2:]
        y = y[2:]
    plt.bar(x,y)
    plt.show()

# write func to match timestamp to standardized name of place
# correct graphs so labels fit
# make dict of dicts for each sem
# make function to read file so it can just be called in main block?
# add provision to carry over excess from fall to spring
# divide dicts by fall and spring?


if __name__ == '__main__':
    # fall 2020
    file = pd.read_csv("foodpointsfall20.csv")
    #  is it possible to iterate through files in a directory for later iterations?
    df = makedataframe(file)
    addtodict(dukecard,df['Location'])
    df['Date/Time'] = convert_time(df['Date/Time'])
    bal = condense2(balances(df))
    tra = condense2(count_transactions(df))
    print(bal,tra)