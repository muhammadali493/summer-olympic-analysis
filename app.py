import streamlit as st
import pandas as pd
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data\\athlete_events.csv')
region_df = pd.read_csv('data\\noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Summer Olympic Analysis")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athelete-wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")

    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_country == 'Overall' and selected_year == 'Overall':
        st.title('Overall Medal Tally')
    if selected_country == 'Overall' and selected_year != 'Overall':
        st.title(f"Medal Tally in {selected_year}")
    if selected_country != 'Overall' and selected_year == 'Overall':
        st.title(f"{selected_country} Overall Performance")
    if selected_country != 'Overall' and selected_year != 'Overall':
        st.title(f"{selected_country} Performance in {selected_year}")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':

    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athelets = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Stats")
    col1,col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1,col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athelets")
        st.title(athelets)
    # Participating Nations' graph
    nations_over_time = helper.data_over_time(df, 'region')
    st.title("Participating Nations over time")
    fig, ax = plt.subplots()
    ax.plot(nations_over_time['Year'], nations_over_time['count'], marker='o')
    ax.set_title("Participating nations over time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Participating Nations")

    st.pyplot(fig)
    # Total Events over time
    events_over_time = helper.data_over_time(df, 'Event')
    st.title("No. of Events over time")
    fig, ax = plt.subplots()
    ax.plot(events_over_time['Year'], events_over_time['count'], marker='o')
    ax.set_title("No. of Events over time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Events")

    st.pyplot(fig)
    # Participating Atheletes over time
    athelets_over_time = helper.data_over_time(df, 'Name')
    st.title("No. of Participating Atheletes over time")
    fig, ax = plt.subplots()
    ax.plot(athelets_over_time['Year'], athelets_over_time['count'], marker='o')
    ax.set_title("No. of Participating Atheletes over time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Participating Atheletes")

    st.pyplot(fig)

    # Ploting heatmap 
    st.title("No. of Events per Sport over time")
    fig, ax = plt.subplots(figsize=(25,25))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)

    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select the Sport', sport_list)
    top_athletes = helper.most_successful(df,selected_sport)
    st.table(top_athletes)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select the country', country_list)
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig, ax = plt.subplots()
    ax.plot(country_df['Year'], country_df['Medal'], marker='o')
    ax.set_title(f"Medals Over Time - {selected_country}")
    ax.set_xlabel('Year')
    ax.set_ylabel('Medals Won')

    st.pyplot(fig)

    pt = helper.country_event_heatmap(df, selected_country)
    st.title(f"Performance in Each Sport over time - {selected_country}")
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    top_10 = helper.top_athletes_of_country(df, selected_country)
    st.title(f'Top 10 athletes of {selected_country}')
    st.table(top_10)