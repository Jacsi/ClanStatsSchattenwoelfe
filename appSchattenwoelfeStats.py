# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 16:27:55 2022

@author: Jacsi
"""

import time
import pandas as pd
import numpy as np
from datetime import timedelta
import plotly.express as px
import plotly.express as px
import plotly

import requests
from io import StringIO

import streamlit as st

clanname = "Die_Schattenwölfe"
url = requests.get('https://www.dieschattenwoelfe.de/Data/DailyClanStatsDieSchattenwoelfe_2.txt')
csv_raw = StringIO(url.text)
df = pd.read_csv(csv_raw, header=None)

print(df)


df[3] = df[3].map(lambda x: x.replace('.', ''))

df[3] = pd.to_numeric(df[3])

gesamtxpClanperday = pd.DataFrame(df.groupby([7]).sum())
gesamtxpClanperday[1] = clanname
gesamtxpClanperday[6] = gesamtxpClanperday.index.tolist()
gesamtxpClanperday[7] = gesamtxpClanperday.index.tolist()

df = df.append(gesamtxpClanperday , ignore_index=True)


##################################Get Active Member####################

gesamtxpClanperday = pd.DataFrame(df.groupby([7]).sum())


df[8] = pd.to_datetime(df[7]).dt.dayofweek

df[7] = pd.to_datetime(df[7]).dt.date

lastday = df[df[7] == max(df[7])]

activemeber = np.array(lastday[1])


#print(activemeber)

##################################END Active Member####################

################################## XP Calculation######################

#df[3] = df[3].map(lambda x: x.replace('.', ''))

#df[3] = pd.to_numeric(df[3])

st.title('Mitgliederstatistiken von Die_Schattenwoelfe')

filtername = st.selectbox( "Wähle ein Mitglied aus", activemeber, index =len(activemeber)-1)

dffilter = df[df[1] == filtername]

questteilnahmedf = dffilter[dffilter[8] == 2]
anzahlNichtTeilgenommenerQuests = 0
for questactivated in questteilnahmedf[2]:
    if questactivated == 1:
        anzahlNichtTeilgenommenerQuests = 0
    else:
        anzahlNichtTeilgenommenerQuests = anzahlNichtTeilgenommenerQuests+1

week = timedelta(days=7)

if (dffilter[7].max()- week ) < (dffilter[7].min()) :
    startdatedefault = dffilter[7].min()
else:
    startdatedefault = dffilter[7].max() - week
    
enddatedefault = dffilter[7].max()



startdate = st.date_input("Start Date", value=startdatedefault, min_value = dffilter[7].min(), max_value = enddatedefault)
enddate = st.date_input("End Date", value = enddatedefault,min_value = dffilter[7].min(), max_value = enddatedefault)



if (startdate >= enddate):
    st.text("Das Startdatum muss vor dem Enddatum liegen")
else:
    dffilter = dffilter[(dffilter[7] >= startdate) & (dffilter[7] <= enddate)] 

    
       
    xpbardiagram = np.diff(dffilter[3])
    
    #set values smaller than 0 to 0
    counterbd = 0
    for xyz in xpbardiagram:
        if xyz < 0:
            xyz = 0
            xpbardiagram[counterbd] = xyz
        counterbd = counterbd+1

    xpbardiagramsum = xpbardiagram.sum()

    dffilter = dffilter[(dffilter[7] > startdate)]

    # initialize data of lists.
    data = {'date':dffilter[7],
            'xp':xpbardiagram}

    # Creates pandas DataFrame.
    dfbardiagram = pd.DataFrame(data) 

    fig = px.bar(dfbardiagram, x='date' , y='xp')

    st.plotly_chart(fig, use_container_width=False)

    #print(xpbardiagram)
    #print(dffilter[7])

    st.text("Im ausgewähltem Zeitraum wurden: " + str(xpbardiagramsum) + " XP gesammelt.")
    ###################Calculate Xp while Quest#########



    #dffiltername = df[df[1] == filtername]

    #if (df[7].max()- week ) < (df[7].min()) :
    #    startdatefilter = df[7].min()
    #else:
    #    enddatefilter = df[7].max() - week

    #dffilterxpquest = dffiltername[(df[7] >= startdatefilter) & (dffiltername[7] <= enddatefilter)] 

    #max(df[8]) =2 Bis hier müssen XP gesammelt werden

    #max(df[8]) =3  ist der Erste Questtag vorbei


    ####################END XP Calc Quest################################


    ###################################### END XP Calculation#################
    t = (dffilter[dffilter[7] == max(dffilter[7])][2])

    if (filtername != clanname):
        if (t.item() ) :
               st.text("Derzeit hat " + filtername + " die Questteilnahme aktiviert!")
        else:
              st.text("Derzeit nimmt " + filtername + " NICHT an Quests teil! \nBitte aktiviere den Questharken, wenn du teilnehmen möchtest.")
                
        if (anzahlNichtTeilgenommenerQuests > 2):
            st.text("Die letzten " + str(anzahlNichtTeilgenommenerQuests) +" male hat " + filtername + " nicht an Clan Quests teilgenommen! \nBitte beachte, dass euch die Anführer ab unabgemeldeten 3 Quests kicken können!")


st.text("Die letzte Aktualisierung der Daten erfolgte am: " + str(df[7].max()) + "\nIn der Regel werden die Daten um 18:30 Uhr aktualisiert.")


