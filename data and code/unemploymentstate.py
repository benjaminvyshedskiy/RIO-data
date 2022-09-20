import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
weeklyjobs = pd.read_csv('unemploymeny.csv', thousands=',')
# wockaflocka = weeklyjobs.pivot_table(index=["State"],columns=["Filed week ended"],values=["Initial Claims"]).transpose()
wockaflocka = weeklyjobs.pivot_table(index=["State"],columns=["Filed week ended"],values=["Initial Claims"]).transpose()
##set ,values="whatever"
print(wockaflocka)
heyyy = wockaflocka.droplevel(0)
heyyy.index = pd.to_datetime(heyyy.index)
print(heyyy)
heyyy = heyyy.reindex(sorted(heyyy.index))
heyyy = heyyy.iloc[1:262,:]
print(heyyy)
covidunemployment = heyyy.iloc[-53:,:]
#-------------------------------------------------------------------
weeklycovid = pd.read_csv('2020ODComp.csv')
weekly = weeklycovid.drop(weeklycovid.columns[[0,1]],axis=1)
weekly = weekly.iloc[-53:,:]
weekly.index = covidunemployment.index
print(weekly.columns.values)
covidunemployment = covidunemployment[covidunemployment.columns.intersection(list(weekly.columns))]
weekly = weekly[weekly.columns.intersection(list(covidunemployment.columns))]
print(covidunemployment)
print(weekly)
##----------------
##Todays unemployment is tommorows overdose--or five weeks from tommorow...
##----------------
class Corrobj:
    def __init__(self, ccf, state):
        self.ccf = ccf
        ccfweights = ccf.reset_index(level=0)
        ccfweights["weighted"] = ccfweights.apply(lambda x: (-1 * x[state] if x["index"] <0 else x[state]),axis=1)
        print(ccfweights)
        self.sum = ccfweights["weighted"].sum()
        self.state = state
        self.optimallag = self.ccf.idxmax()[0]
        self.maxcorr = self.ccf.loc[self.optimallag].values[0]

    def getcorr(self):
        return self.maxcorr
    def getlag(self):
        return self.optimallag
    def getweighted(self):
        finalweight = self.sum
        return finalweight

my_objects = []
dict = dict()
for state in list(weekly.columns.values):
    lagged_correlation = pd.DataFrame.from_dict(
        {state: [covidunemployment[state].corr(weekly[state].shift(t)) for t in range(-10,10,1)]})

    lagged_correlation.index = range(-10,10,1)
    obj = Corrobj(lagged_correlation,state)
    my_objects.append(obj)
    lagged_correlation[state].plot()
    dict[state] = obj.ccf
plt.show()
corrlist = []
print("----------")
lagsum = 0
corrsum = 0
weightsum = 0
statelist = []
corrlist = []
laglist = []
weightlist = []
for obj in my_objects:
    statelist.append(obj.state)
    lagsum+=obj.getlag()
    laglist.append(obj.getlag())
    corrsum+=obj.getcorr()
    corrlist.append(obj.getcorr())
    weightsum+=obj.getweighted()
    weightlist.append(obj.getweighted())
print("average lag is ")
print(lagsum/len(my_objects))
print(corrsum/len(my_objects))
print(weightsum/len(my_objects))

ccfresults = pd.DataFrame(list(zip(corrlist,laglist,weightlist)),index=statelist, columns=['Correlation','Optimal Lag',"WeightedCorr"]).sort_values(by=["Correlation"])
print(ccfresults)
ccfresults.to_csv("2020StateOptimalLagIC.csv")
print(dict[""])
dff = pd.DataFrame.from_dict(dict,orient="index")
