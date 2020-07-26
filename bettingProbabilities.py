import pandas as pd
import numpy as np

pred = pd.read_csv('./poissonPredictionMeans.csv', encoding = "ISO-8859-1")
odds = pd.read_csv('./bigboy.csv', encoding = "ISO-8859-1")
dict = {"Date":[],"Home":[],"Away":[],"Home Score":[],"Away Score":[]}
for col in odds.columns:
    if ("1" == col or "X" == col or "2" == col or "AH" in col or "Over" in col or "Under" in col):
        dict[col] = []
        dict["P(" + col + ")"] = []
dict["P(AH 0.0 (1))"] = []
dict["P(AH 0.0 (2))"] = []

curIndex = 0
goalDiffs = [-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6]
ouList = [0,1,2,3,4,5,6,7,8,9]
while (curIndex < len(pred.index)):
    print (curIndex)
    table = [[],[],[],[],[],[],[],[],[],[],[]]
    for col in pred.columns:
        if ("Goal Prob" in col):
            for col2 in pred.columns:
                if ("Goal Prob" in col2):
                    table[int(col.split(" Goal Prob")[0])].append(float(pred.at[curIndex, col]) * float(pred.at[curIndex + 1, col2]))
    for key in dict:
        if ("P(" in key):
            dict[key].append(0)
    for home in range(11):
        for away in range(11):
            if (home > away):
                dict["P(1)"][-1] = dict["P(1)"][-1] + table[home][away]
            elif (away > home):
                dict["P(2)"][-1] = dict["P(2)"][-1] + table[home][away]
            else:
                dict["P(X)"][-1] = dict["P(X)"][-1] + table[home][away]
    for diff in goalDiffs:
        pHome = 0
        pAway = 0
        pDraw = 0
        if (diff == -6):
            for home in range(11):
                for away in range(11):
                    if (home - 6 > away):
                        pHome += table[home][away]
                    elif (home - 6 < away):
                        pAway += table[home][away]
                    else:
                        pDraw += table[home][away]
            dict["P(AH -6.0 (1))"][-1] = pHome / (pHome + pAway)
            dict["P(AH -6.0 (2))"][-1] = pAway / (pHome + pAway)
            dict["P(AH -5.75 (1))"][-1] = ((1/2)*pDraw + pHome)/(1-(1/2)*pDraw)
            dict["P(AH -5.75 (2))"][-1] = pAway / (1-(1/2)*pDraw)
        elif (diff != 6):
            for home in range(11):
                for away in range(11):
                    if (home + diff > away):
                        pHome += table[home][away]
                    elif (home + diff < away):
                        pAway += table[home][away]
                    else:
                        pDraw += table[home][away]
            dict["P(AH " + str(float(diff)) + " (1))"][-1] = pHome / (pHome + pAway)
            dict["P(AH " + str(float(diff)) + " (2))"][-1] = pAway / (pHome + pAway)
            dict["P(AH " + str(float(diff) + 0.25) + " (1))"][-1] = ((1/2)*pDraw + pHome)/(1-(1/2)*pDraw)
            dict["P(AH " + str(float(diff) + 0.25) + " (2))"][-1] = pAway / (1-(1/2)*pDraw)
            dict["P(AH " + str(float(diff) - 0.25) + " (1))"][-1] = pHome / (1-(1/2)*pDraw)
            dict["P(AH " + str(float(diff) - 0.25) + " (2))"][-1] = ((1/2)*pDraw + pAway)/(1-(1/2)*pDraw)
            dict["P(AH " + str(float(diff) - 0.5) + " (1))"][-1] = pHome
            dict["P(AH " + str(float(diff) - 0.5) + " (2))"][-1] = pAway + pDraw
        else:
            for home in range(11):
                for away in range(11):
                    if (home + 6 > away):
                        pHome += table[home][away]
                    elif (home + 6 < away):
                        pAway += table[home][away]
                    else:
                        pDraw += table[home][away]
            dict["P(AH 6.0 (1))"][-1] = pHome / (pHome + pAway)
            dict["P(AH 6.0 (2))"][-1] = pAway / (pHome + pAway)
            dict["P(AH 5.75 (1))"][-1] = pHome / (1-(1/2)*pDraw)
            dict["P(AH 5.75 (2))"][-1] = ((1/2)*pDraw + pAway)/(1-(1/2)*pDraw)
    for total in ouList:
        pOver = 0
        pUnder = 0
        pDraw = 0
        if (total == 0):
            for home in range(11):
                for away in range(11):
                    if (home + away > total):
                        pOver += table[home][away]
                    elif (home + away < total):
                        pUnder += table[home][away]
                    else:
                        pDraw += table[home][away]
            dict["P(Over 0.25)"][-1] = pOver / (1-(1/2)*pDraw)
            dict["P(Under 0.25)"][-1] = ((1/2)*pDraw + pUnder)/(1-(1/2)*pDraw)
        elif (total != 9):
            for home in range(11):
                for away in range(11):
                    if (home + away > total):
                        pOver += table[home][away]
                    elif (home + away < total):
                        pUnder += table[home][away]
                    else:
                        pDraw += table[home][away]
            dict["P(Over " + str(float(total)) + ")"][-1] = pOver / (pOver + pUnder)
            dict["P(Under " + str(float(total)) + ")"][-1] = pUnder / (pOver + pUnder)
            dict["P(Over " + str(float(total) + 0.25) + ")"][-1] = pOver / (1-(1/2)*pDraw)
            dict["P(Under " + str(float(total) + 0.25) + ")"][-1] = ((1/2)*pDraw + pUnder)/(1-(1/2)*pDraw)
            dict["P(Over " + str(float(total) - 0.25) + ")"][-1] = ((1/2)*pDraw + pOver)/(1-(1/2)*pDraw)
            dict["P(Under " + str(float(total) - 0.25) + ")"][-1] = pUnder / (1-(1/2)*pDraw)
            dict["P(Over " + str(float(total) - 0.5) + ")"][-1] = pOver + pDraw
            dict["P(Under " + str(float(total) - 0.5) + ")"][-1] = pUnder
        else:
            for home in range(11):
                for away in range(11):
                    if (home + away > total):
                        pOver += table[home][away]
                    elif (home + away < total):
                        pUnder += table[home][away]
                    else:
                        pDraw += table[home][away]
            dict["P(Over 9.0)"][-1] = pOver / (pOver + pUnder)
            dict["P(Under 9.0)"][-1] = pUnder / (pOver + pUnder)
            dict["P(Over 8.75)"][-1] = ((1/2)*pDraw + pOver)/(1-(1/2)*pDraw)
            dict["P(Under 8.75)"][-1] = pUnder / (1-(1/2)*pDraw)
            dict["P(Over 8.5)"][-1] = pOver + pDraw
            dict["P(Under 8.5)"][-1] = pUnder
    for index, row in odds.iterrows():
        if (row["Home"] == pred.at[curIndex, "Team"] and row["Away"] == pred.at[curIndex+1, "Team"] and row["Date"] == pred.at[curIndex, "Date"]):
            for col in odds.columns:
                if ("1" == col or "X" == col or "2" == col or "AH" in col or "Over" in col or "Under" in col or "Date" == col or "Home Score" == col or "Away Score" == col):
                    dict[col].append(row[col])
            dict["Home"].append(pred.at[curIndex, "Team"])
            dict["Away"].append(pred.at[curIndex+1, "Team"])
    curIndex += 2
for key in dict:
    print (key, len(dict[key]))
dfFinal = pd.DataFrame.from_dict(dict)
dfFinal.to_csv("./bettingPredictions.csv")
