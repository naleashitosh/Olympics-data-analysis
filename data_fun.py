import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


def medal(data):
    # Remove duplicated associated with the players in the team
    medal_data = data.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'])
    # groupby medal count by NOC
    medal_data = medal_data.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold', ascending=False).reset_index()
    # convert float to int
    #medal_data[['Gold','Silver','Bronze']] = medal_data[['Gold','Silver','Bronze']].astype(int)
    # add total medal column
    medal_data['total'] = medal_data.Gold + medal_data.Silver + medal_data.Bronze

    return medal_data

def year_country_list(data):
    years = sorted((data.Year.unique()))
    years.insert(0,'Overall')
    country = list(data.region.unique())
    country.remove(np.nan)
    country.sort()
    country.insert(0,'Overall')
    return years,country

def medalwise(data,year,country):
    medals = data.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'])
    y = 0
    if year == 'Overall' and country == 'Overall':
        medals_new = medals
    if year == 'Overall' and country != 'Overall':
        y = 1
        medals_new = medals[medals.region == country]
    if year != 'Overall' and country == 'Overall':
        medals_new = medals[medals.Year == year]
    if year != 'Overall' and country != 'Overall':
        medals_new = medals[(medals.Year == year) & (medals.region == country)]
    if y == 1:
        medals_new = medals_new.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year', ascending=True).reset_index()
    else:medals_new = medals_new.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold', ascending=False).reset_index()
    #medals_new[['Gold','Silver','Bronze']] = medals_new[['Gold','Silver','Bronze']].astype(int)
    medals_new['total'] = medals_new.Gold + medals_new.Silver + medals_new.Bronze
    return medals_new

def participated_countries(data):
    part_countries = data.groupby('Year')['region'].unique().reset_index()
    part_countries.region = part_countries.region.apply(lambda x:len(x))
    part_countries.columns = ['Year','No of countries']
    return part_countries

def no_of_events_fun(data):
    no_of_events = data.groupby('Year')['Event'].unique().reset_index()
    no_of_events.Event = no_of_events.Event.apply(lambda x:len(x))
    no_of_events.columns = ['Year','No of Events']
    return no_of_events

def no_of_athletes_fun(data):
    no_of_athletes = data.groupby('Year')['Name'].unique().reset_index()
    no_of_athletes.Name = no_of_athletes.Name.apply(lambda x:len(x))
    no_of_athletes.columns = ['Year','No of Athletes']
    return no_of_athletes

def medals_on_athletes(data1):
    data1 = data1.dropna(subset=['Medal'])
    data = data1.groupby('Name').sum()[['Gold','Silver','Bronze']]
    data = data.merge(data1[['Name','Sport']],on = 'Name',how ='left').drop_duplicates('Name')
    data['Total'] = data.Gold + data.Silver + data.Bronze
    data.sort_values('Total',ascending=False,inplace=True)
    data.index = np.arange(1, len(data) + 1)
    data = data[['Name','Sport', 'Gold', 'Silver', 'Bronze', 'Total']]
    return data

def countryWiseMedals(data):
    data = data.dropna(subset='Medal')
    data.drop_duplicates(subset= ['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'],inplace=True)
    data = pd.concat([data,pd.get_dummies(data.Year)],axis=1)
    data = data.groupby('region').sum()[sorted(data.Year.unique())]
    data['Total'] = data.sum(axis = 1)
    data.sort_values('Total',ascending=False,inplace=True)
    data = data.reset_index()
    data.index = np.arange(1, len(data) + 1)
    return data

def sportWiseMedals(data,country):
    data = data.dropna(subset='Medal')
    data.drop_duplicates(subset= ['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'],inplace=True)
    data = pd.concat([data,pd.get_dummies(data.Year)],axis=1)
    data = data[data.region == country]
    data = data.groupby('Sport').sum()[sorted(data.Year.unique())]
    return data

def athletesCountrywise(data1, country):
    data1 = data1.dropna(subset=['Medal'])
    data = data1.groupby('Name').sum()[['Gold','Silver','Bronze']]
    data = data.merge(data1[['Name','region','Sport']],on = 'Name',how ='left').drop_duplicates('Name')
    data['Total'] = data.Gold + data.Silver + data.Bronze
    data.sort_values('Total',ascending=False,inplace=True)
    data = data[['Name','region','Sport', 'Gold', 'Silver', 'Bronze', 'Total']]
    data = data[data.region == country].drop('region',axis = 1)
    data.index = np.arange(1, len(data) + 1)
    return data

def scatter(df,sport):
    # plt.figure(figsize=(13,10))
    data1 = df[df.Sport == sport]
    fig = sns.scatterplot(data = data1,x = 'Weight',y = 'Height',hue = data1.Medal,style=data1.Sex)
    return fig

def lineplot(df):
    df.drop_duplicates(subset=['Name'],inplace=True)
    men = df[df.Sex == 'M'].groupby('Year')['Sex'].count().reset_index()
    women = df[df.Sex == 'F'].groupby('Year')['Sex'].count().reset_index()
    athlete = men.merge(women,on = 'Year',how = 'left').fillna(0)
    athlete.columns = ['Year', 'Men', 'Women']
    fig = px.line(athlete, x = 'Year', y = ['Men', 'Women'])
    return fig