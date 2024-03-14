import pandas as pd
import streamlit as st
import data_fun,preprocessor
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.figure_factory as ff

data = pd.read_csv('athlete_events.csv')
reg = pd.read_csv('noc_regions.csv')

df = preprocessor.processor(data,reg)

ich_bin_ashutosh = 'https://github.com/naleashitosh'

st.sidebar.markdown(ich_bin_ashutosh, unsafe_allow_html=True)

st.sidebar.image('https://olympics.com/images/static/b2p-images/logo_color.svg')

st.sidebar.header('Olympics Analysis')

sidemenu = st.sidebar.radio('Select option',
              ('Medal wise Analysis','Overall Analysis',
                'Country wise Analysis', 'Athlete wise Analysis'))


if sidemenu == 'Medal wise Analysis':
    st.header('Medal wise Analysis')
    years,country = data_fun.year_country_list(df)
    country_1 = st.sidebar.selectbox('Select Country',country)
    if country_1 == 'Overall': year_1 = st.sidebar.selectbox('Select Year',years)
    else: 
        years = sorted(df[df.region==country_1].Year.unique().tolist())
        years.insert(0,'Overall')
        year_1 = st.sidebar.selectbox('Select Year',years)
    if year_1 == 'Overall' and country_1 == 'Overall':
        st.subheader('Overall Performance')
    if year_1 == 'Overall' and country_1 != 'Overall':
        st.subheader(country_1 +'Performance')
    if year_1 != 'Overall' and country_1 == 'Overall':
        st.subheader('Overall performance in year '+str(year_1))
    if year_1 != 'Overall' and country_1 != 'Overall':
        st.subheader('Performance of '+country_1+' in '+str(year_1))
    medal_df = data_fun.medalwise(df,year_1,country_1)
    st.table(medal_df)

if sidemenu == 'Overall Analysis': 
    editions = len(df.Year.unique())-1 # -1 is because of 1906 Intercalated Games
    city = len(df.City.unique())
    sports = len(df.Sport.unique())
    events = len(df.Event.unique())
    athletes = len(df.Name.unique())
    countries = len(df.region.unique())
    col1,col2,col3 = st.columns(3)
    with col1:
        st.subheader('Editions')
        st.title(editions)
    with col2:
            st.subheader('Cities')
            st.title(city)
    with col3:
            st.subheader('Sports')
            st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.subheader('Events')
        st.title(events)
    with col2:
            st.subheader('Athletes')
            st.title(athletes)
    with col3:
            st.subheader('Countries')
            st.title(countries)

    # Participation of countries over the years
    part_nations = data_fun.participated_countries(df)
    st.header(' ')
    _, col2, _ = st.columns([1, 25, 1])
    with col2:
        st.header('Participation of countries over the years')
    plot1 = px.line(part_nations,x = 'Year',y = 'No of countries')
    st.plotly_chart(plot1)

    # No of Events over the years
    part_events = data_fun.no_of_events_fun(df)
    st.header(' ')
    _, col2, _ = st.columns([1, 25, 1])
    with col2:
        st.header('No of Events over the years')
    plot2 = px.line(part_events,x = 'Year',y = 'No of Events')
    st.plotly_chart(plot2)

    # No of Athletes over the years
    part_athletes = data_fun.no_of_athletes_fun(df)
    st.header(' ')
    _, col2, _ = st.columns([1, 25, 1])
    with col2:
        st.header('No of Athletes over the years')
    plot3 = px.line(part_athletes,x = 'Year',y = 'No of Athletes')
    st.plotly_chart(plot3)

    # No of Events of each sport over the years
    st.header('No of Events of each sport over the years')
    xc = df[['Year','Sport','Event']].drop_duplicates(['Year','Sport','Event'])
    xc.drop('Event',axis = 1,inplace= True)
    xc = pd.concat([xc,pd.get_dummies(xc.Year)],axis=1)
    xc = xc.groupby('Sport').sum()[sorted(xc.Year.unique())].astype(int)
    xc = xc.sort_values('Sport')
    fig,ax = plt.subplots(figsize=(19,21))
    ax = sns.heatmap(xc,annot= True,cmap = 'PuBuGn')
    st.pyplot(fig)

    # Most successful athletes
    st.header('Succesfull Athletes')
    selected_sport = sorted(df.Sport.unique())
    selected_sport.insert(0,'Overall')
    selected_sport = st.selectbox('Select the Sport',selected_sport)
    xn = data_fun.medals_on_athletes(df)
    if selected_sport != 'Overall':
        xn = xn[xn.Sport == selected_sport]
        xn.drop('Sport',inplace=True,axis =1)
        xn.index = np.arange(1, len(xn) + 1)
        st.table(xn)
    else:
        _, col2, _ = st.columns([1, 25, 1])
        with col2:
            st.dataframe(xn,width=1400)

if sidemenu == 'Country wise Analysis':
    data = data_fun.countryWiseMedals(df)
    st.header('Medals Won by countries over the years ')
    st.dataframe(data)
    _, col2, _ = st.columns([1, 1, 1])
    with col2:
        st.header('Medal Trend')
    country = st.sidebar.selectbox('Select the Country',list(data.region))
    st.subheader('Medals won by '+country+' over the years')
    plt.figure(figsize = (10,20))
    plot1 = px.line(data[data.region==country].drop(['region','Total'],axis = 1).T,labels={'index':'Year','value':'Medals'})
    plot1.update_layout(showlegend=False)
    st.plotly_chart(plot1)

    tab = data_fun.sportWiseMedals(df,country)
    plt.figure(figsize=(20,20))
    fig,ax = plt.subplots(figsize=(19,21))
    ax = sns.heatmap(tab,annot= True,cmap = 'PuBuGn')
    st.pyplot(fig)

    topAthletes = data_fun.athletesCountrywise(df,country)
    st.subheader('Top Athletes of ' + country)
    st.dataframe(topAthletes)

if sidemenu == 'Athlete wise Analysis':
    data1 = df.dropna(subset=['Name','region'])
    data1 = data1.dropna(subset=['Medal','Age'])
    data2 = data1[data1.Medal == 'Gold'].dropna(subset= ['Age'])
    data3 = data1[data1.Medal == 'Silver'].dropna(subset= ['Age'])
    data4 = data1[data1.Medal == 'Bronze'].dropna(subset= ['Age'])
    fig = ff.create_distplot([data1.Age,data2.Age,data3.Age,data4.Age],['All','Gold','Silver','Bronze'],show_hist=False,show_rug=False)
    st.header('Distribution of AGE')
    st.plotly_chart(fig)


    data1 = df.dropna(subset=['Name','region'])
    sportx = []
    name = list(data1.Sport.unique())
    for n,i in enumerate(name):
        if len(data1[data1.Sport == i]) > 162:
            sportx.append(i)
    xv = []
    name = []
    medal_list = ['Overall','Gold', 'Bronze', 'Silver']
    medal = st.selectbox('Select the Medal',medal_list)
    for i in sportx:
        data2 = data1[data1.Sport ==  i]
        if medal != 'Overall':
            xv.append(list(data2[data2.Medal == medal]['Age'].dropna()))
        if medal == 'Overall':
            xv.append(list(data2.Age.dropna()))
        name.append(i)
    st.header('Distrubution of age ('+medal+')')
    fig = ff.create_distplot(xv,name,show_hist=False,show_rug=False)
    st.plotly_chart(fig)

    st.header('Height Vs Weight')
    sportv = st.selectbox('Select the Sport',df.Sport.unique())
    sc_fig, ax = plt.subplots(figsize = (10,7))
    ax = data_fun.scatter(df,sportv)
    st.pyplot(sc_fig) 

    st.header('Men and Women Participation')
    ax = data_fun.lineplot(df)
    ax.update_layout(autosize = False,width = 800, height = 500)
    st.plotly_chart(ax)