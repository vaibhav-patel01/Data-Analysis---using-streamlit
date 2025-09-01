import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib as plt

df = pd.read_csv("olympics_cleaned5.csv")
st.set_page_config(layout= "wide" ,page_title="Olympics Dashboard")
# st.markdown("<h1 style='margin-top: -60px; text-align: center;' >Summer Olympics<h1/>",unsafe_allow_html = True)
st.sidebar.image("pngegg.png")
years = []
for i in range(1896,2025):
    if (i %4) == 0 :
        years.append(i)
years.append("1896 - 2024")
years.reverse()

def clear_other_selections(changed_key):
    if st.session_state[changed_key] is not None:
        all_keys = ['sb_year', 'sb_country', 'sb_sport', 'sb_athlete']
        for key in all_keys:
            if key != changed_key:
                st.session_state[key] = None

st.sidebar.selectbox("Seasons",years,index=None,placeholder="Year",key='sb_year', on_change=clear_other_selections, args=('sb_year',) )
st.sidebar.selectbox("Select Country Wise",df["region"].sort_values().dropna().unique().tolist(),index=None,placeholder="Country",key='sb_country',on_change=clear_other_selections,args=('sb_country',))
st.sidebar.selectbox("Select Games",df["Sport"].sort_values().unique().tolist(),index=None,placeholder="Sport",key='sb_sport',on_change=clear_other_selections,args=('sb_sport',))
st.sidebar.selectbox("Select you favourite athlete",df[df["number_of_medals"] != 0]["Name"].drop_duplicates().sort_values().tolist(),index=None,placeholder="Athlete",key='sb_athlete',on_change=clear_other_selections,args=('sb_athlete',))

def load_overall():
    st.markdown("<h1 style='margin-top: -60px; text-align: center;' >Summer Olympics<h1/>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top: -50px; text-align: left;' >Top Statistics <h3/>",unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown("""<h4 style='margin-top: -60px; text-align: center;' >🗓️ Editions<h4/>""",unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin-top: -50px; text-align: center;'><strong>{str(len(df["Year"].unique()))}</strong></h3>",unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top: 0px; text-align: center;' >🏃 Sports<h4/>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin-top: -50px; text-align: center;'>{46}</h3>", unsafe_allow_html=True)
    with col2:
        st.markdown("<h4 style='margin-top: -60px; text-align: center;' >🌍 Nations<h4/>",unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin-top: -50px; text-align: center;'><strong>{len(df["region"].unique())}</strong></h3>",unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:   0px; text-align: center;' >🏅 Events<h4/>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin-top: -50px; text-align: center;'>{len(df["Event"].unique())}</h3>",unsafe_allow_html=True)
    with col3:
        st.markdown("<h4 style='margin-top: -60px; text-align: center;' >🏙️ Host Cities<h4/>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin-top: -50px; text-align: center;'>{len(df["City"].unique())}</h3>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top: 0px; text-align: center;' >🤸 Athletes <h4/>",unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin-top: -50px; text-align: center;'>{len(df["Name"].unique())}</h3>",unsafe_allow_html=True)
    col4,col5 = st.columns(2)
    with col4:
        st.subheader("Participation Over the Time")
        fig1 = px.line(df.groupby("Year")["Name"].count().reset_index(),"Year","Name",range_x = (1896,2024),labels = {"Name":"athlets"} )
        st.plotly_chart(fig1)
    with col5:
        st.subheader("Gender Wise participation")
        fig2 = px.line(df.groupby(["Sex","Year"])["Name"].count().reset_index(),"Year","Name",color = "Sex",labels = {"Name":"athlets"},color_discrete_map={'Male': 'dodgerblue','Female': 'magenta'})
        st.plotly_chart(fig2)

    st.subheader("Overall Medal Tally")
    with st.expander("Show medal tally"):
        st.dataframe(df.drop_duplicates(subset=["Team", "NOC", "Year", "Sport", "Event", "Medal"]).groupby("region")[['Gold', 'Silver', 'Bronze',"number_of_medals"]].sum().sort_values(by="number_of_medals", ascending=False).rename(columns = {"region":"Country","number_of_medals":"Total"}))
    st.subheader("Top Athletes performance")
    with st.expander("Show medal tally"):
        st.dataframe(df[df["Medal"] != "No medal"].groupby(["Name","region","Sport"])[["Gold","Silver","Bronze","number_of_medals"]].sum().reset_index().sort_values(ascending = False,by = "number_of_medals").reset_index(drop = True).rename(columns = {"region":"Country"}))

def load_yearwise(option):
    st.markdown(f"<h1 style='margin-top: -40px; text-align: center;' >{df[df["Year"] == option]["City"].values[0] + " Olympics"}<h1/>", unsafe_allow_html=True)
    st.header("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1 :
        st.metric('Nations participated', len(df[(df["Year"] == option)]["NOC"].unique()))
        with st.expander("Show Nations"):
            st.dataframe(df[(df["Year"] == option)][["region","NOC"]].drop_duplicates().dropna().reset_index().drop(columns = "index"))
        st.metric('Total Athletes', len(df[df["Year"] == option]["Name"].drop_duplicates()))
        with st.expander("Show Athletes"):
            st.dataframe(df[df["Year"] == option]["Name"].drop_duplicates().sort_values().reset_index().drop(columns = "index"))
    with col2 :
        st.metric('Total Sports', len(df[(df["Year"] == option)]["Sport"].drop_duplicates()))
        with st.expander("Show Sports"):
            st.dataframe(df[(df["Year"] == option)]["Sport"].drop_duplicates().sort_values().reset_index().drop(columns = "index").replace("Cycling Road","Cycling").reset_index(drop = True))
        st.metric('Female Athletes', len(df[(df["Year"] == option) & (df["Sex"] == "Female")]["Name"].drop_duplicates()))
        with st.expander("Show Athletes"):
            st.dataframe(df[(df["Year"] == option) & (df["Sex"] == "Female")]["Name"].drop_duplicates().sort_values().reset_index().drop(columns="index"))
    with col3 :
        st.metric('Total Events', len(df[(df["Year"] == option)]["Event"].drop_duplicates()))
        with st.expander("Show Events"):
            st.dataframe(df[(df["Year"] == option)]["Event"].drop_duplicates().sort_values().reset_index().drop(columns = "index"))
        st.metric('Female Athletes', len(df[(df["Year"] == option) & (df["Sex"] == "Male")]["Name"].drop_duplicates()))
        with st.expander("Show Athletes"):
            st.dataframe(df[(df["Year"] == option) & (df["Sex"] == "Male")]["Name"].drop_duplicates().sort_values().reset_index().drop(columns="index"))
    st.subheader("Medal Tally")
    with st.expander("Show medal tally"):
        st.dataframe(df.loc[(df['Year'] == option) & (df['Medal'].notna())].drop_duplicates(subset=['Year', 'Event', 'NOC', 'Medal']).groupby('region')['Medal'].value_counts().unstack(fill_value=0).reindex(columns=['Gold', 'Silver', 'Bronze'], fill_value=0).assign(Total=lambda d: d['Gold'] + d['Silver'] + d['Bronze']).sort_values(by=['Total', 'Gold', 'Silver'], ascending=[False, False, False]).head(50))
    st.subheader("Top Performing Athletes")
    with st.expander("Show medal tally"):
        st.dataframe(df[(df["Year"] == option) & (df["number_of_medals"] != 0)].groupby(["Name","region","Sport"])[["Gold","Silver","Bronze","number_of_medals"]].sum().reset_index().sort_values(ascending = False,by = "number_of_medals").reset_index(drop = True).rename(columns = {"region":"Country"}))

def load_athlete(name):
    st.markdown(f"<h1 style='margin-top: -50px; text-align: center;' >{"Athletes " + name }<h1/>",unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric('Country',df[df["Name"] == name]["region"].values[0])
        st.metric('Sport', df[df["Name"] == name]["Sport"].values[0])
    with col2:
        st.metric('Total Matches Played', len(df[df["Name"] == name]))
        st.metric('Gender', df[df["Name"] == name]["Sex"].values[0])
    with col3:
        st.metric('Total Medals',df[df["Name"] == name]["number_of_medals"].sum())
    st.subheader("Matches played")
    with st.expander("Show "):
        st.dataframe(df[df["Name"] == name][["player_id","Year","City","Event","Gold","Silver","Bronze"]].rename(columns = {"City":"Olympic"}).sort_values(ascending = False,by = "Year").reset_index(drop = True))

def load_country(country):
    st.markdown(f"<h1 style='margin-top: -50px; text-align: center;' >{country + " Statistics"} <h1/>", unsafe_allow_html=True)
    df_country = df[df["region"] == country]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total Athletes', f"🏃 {df_country['Name'].nunique()}")
    with col2:
        st.metric('Editions', f"🗓️ {df_country['Year'].nunique()}")
    with col3:
        st.metric('Total Medals', f"🏆 {df_country['Gold'].sum() + df_country['Silver'].sum() + df_country['Bronze'].sum()}")
    with col4:
        st.markdown(f"""<div style="text-align: center;"><strong>Medal Breakdown</strong><br>🥇 {df_country['Gold'].sum()} | 🥈 {df_country['Silver'].sum()} | 🥉 {df_country['Bronze'].sum()}</div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Performance over the years")
    st.plotly_chart(px.line(df[df["region"] == country].drop_duplicates(subset=['Year', 'Event', 'NOC', 'Medal']).groupby("Year")["number_of_medals"].sum().reset_index(),"Year","number_of_medals",labels = {"number_of_medals":"Medals"}))
    col1,col2 =  st.columns(2)
    with col1:
        st.header("Top games of the Country")
        st.plotly_chart(px.pie(df[df["region"] == country].drop_duplicates(subset=['Year', 'Event', 'NOC', 'Medal']).groupby("Sport")["number_of_medals"].sum().sort_values(ascending = False).reset_index().head(10),values = "number_of_medals",names = "Sport"))
    with col2:
        st.header("Top Athletes")
        st.dataframe(df[df["region"] == country][["Name","Sex","Gold","Silver","Bronze","number_of_medals"]].groupby(["Name","Sex"])[["Gold","Silver","Bronze","number_of_medals"]].sum().sort_values(ascending = False,by = "number_of_medals").reset_index().drop(columns = "number_of_medals"))
    st.subheader("Gender-Wise Performance Analysis")
    col21,col22 = st.columns(2)
    with col21:
        st.markdown("##### 🥇 Overall Medal Split")
        fig_donut = px.pie(df_country[df_country['number_of_medals'] > 0].groupby('Sex')['number_of_medals'].sum().reset_index(),names='Sex',values='number_of_medals',hole=0.4,color_discrete_map={'Male': 'dodgerblue', 'Female': 'magenta'})
        st.plotly_chart(fig_donut, use_container_width=True)
    with col22:
        st.markdown("##### 🏃 Athlete Participation Over Time")
        fig_line = px.line(df_country.groupby(['Year', 'Sex'])['Name'].nunique().reset_index(),x='Year',y='Name',color='Sex',labels={'Name': 'Number of Athletes'},markers=True,color_discrete_map={'Male': 'dodgerblue', 'Female': 'magenta'})
        st.plotly_chart(fig_line, use_container_width=True)
    st.subheader("Country vs. Country Rivalry")
    with st.expander("Show "):
        country1 = st.selectbox("Select the Rival", df["region"].sort_values().dropna().unique().tolist())
        if country1:
            st.subheader(f"Total Medals Over Time: {country} vs. {country}")
            fig_line = px.line(df[df['region'].isin([country, country1])].groupby(['Year', 'region'])["number_of_medals"].sum().reset_index(), x='Year', y='number_of_medals',color='region', title='Medal Count Comparison',
                               labels={'number_of_medals': 'Total Medals'}, markers=True)
            st.plotly_chart(fig_line, use_container_width=True)
            st.subheader("Top 5 Sports Comparison")
            col31, col32 = st.columns(2)
            with col31:
                st.markdown(f"##### Top Sports for {country}")
                st.dataframe(df[df['region'] == country].drop_duplicates(subset = ['Year', 'Event', 'NOC', 'Medal']).groupby('Sport')['number_of_medals'].sum().nlargest(5))
            with col32:
                st.markdown(f"##### Top Sports for {country1}")
                st.dataframe(df[df['region'] == country1].drop_duplicates(subset = ['Year', 'Event', 'NOC', 'Medal']).groupby('Sport')['number_of_medals'].sum().nlargest(5))

def load_sport(sport):
    st.markdown(f"<h1 style='margin-top: -50px; text-align: center;' >{sport+" Analysis" } <h1/>",
                unsafe_allow_html=True)
    col21,col22,col23,col24 = st.columns(4)
    with col21:
        st.metric('Total Events',len(df[df["Sport"] == sport]["Event"].drop_duplicates().sort_values()))
        with st.expander("Show Events"):
            st.dataframe(df[df["Sport"] == sport]["Event"].drop_duplicates().sort_values().reset_index().drop(columns = "index"))
    with col22:
        st.metric('Participating Nations',  len(df[df["Sport"] == sport]["region"].drop_duplicates().sort_values()))
        with st.expander("Show Nations"):
            st.dataframe(df[df["Sport"] == sport]["region"].drop_duplicates().sort_values().reset_index().drop(columns = "index"))
    with col23:
        st.metric('Total Female Athletes', len(df[(df["Sport"] == sport) & (df["Sex"] == "Female")]["Name"].drop_duplicates()))
        with st.expander("Show Athletes"):
            st.dataframe( df[(df["Sport"] == sport) & (df["Sex"] == "Female")]["Name"].drop_duplicates().sort_values().reset_index().drop(columns = "index"))
    with col24:
        st.metric('Total Male Athletes', len(df[(df["Sport"] == sport) & (df["Sex"] == "Male")]["Name"].drop_duplicates()))
        with st.expander("Show Athletes"):
            st.dataframe( df[(df["Sport"] == sport) & (df["Sex"] == "Male")]["Name"].drop_duplicates().sort_values().reset_index().drop(columns = "index"))
    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Number of events with Year")
        st.plotly_chart(px.line(df[df["Sport"] == sport].groupby("Year")["Event"].nunique().reset_index(),"Year","Event"))
    with col2:
        st.subheader("Participation over the Year")
        st.plotly_chart(px.line(df[df["Sport"] == sport][["Year","Name"]].groupby("Year")["Name"].count().reset_index(),"Year","Name", labels={"Name": "Number of Athletes"}))
    st.markdown("---")
    with col1:
        st.subheader("Top Dominating countries")
        st.plotly_chart(px.pie(df[(df["Sport"] == sport) & (df["number_of_medals"] != 0)].drop_duplicates(subset=['Year', 'Event', 'NOC', 'Medal']).groupby("region")["number_of_medals"].sum().sort_values(ascending = False).reset_index().head(10),values = "number_of_medals",names = "region"))
    with col2:
        st.dataframe(df[(df["Sport"] == sport) & (df["number_of_medals"] != 0)].drop_duplicates(subset=['Year', 'Event', 'NOC', 'Medal']).groupby("region")[["Gold","Silver","Bronze","number_of_medals"]].sum().sort_values(ascending = False,by = "number_of_medals").reset_index().drop(columns = "number_of_medals").rename(columns = {"region":"country"}))
    st.subheader("Top Athletes")
    with st.expander("Medal Tally"):
        st.dataframe(df[(df["Sport"] == sport) & (df["number_of_medals"] != 0)][["Name","Sex","region","Gold","Silver","Bronze","number_of_medals"]].groupby(["Name","Sex","region"])[["Gold","Silver","Bronze","number_of_medals"]].sum().sort_values(ascending = False,by = "number_of_medals").reset_index().drop(columns = "number_of_medals").rename(columns = {"region":"Country"}))

if st.session_state.sb_year:
    if st.session_state.sb_year == "1896 - 2024":
        load_overall()
    else:
        load_yearwise(st.session_state.sb_year)
elif st.session_state.sb_country:
    load_country(st.session_state.sb_country)
elif st.session_state.sb_sport:
    load_sport(st.session_state.sb_sport)
elif st.session_state.sb_athlete:
    load_athlete(st.session_state.sb_athlete)
else:
    load_overall()