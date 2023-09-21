import pandas as pd
import streamlit as st
import numpy as np
import time 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

plt.style.use('dark_background')

st.set_page_config(
    page_title="Test Dashboard",
    page_icon="✅",
    layout="wide",
)

# sample sales data
data = pd.read_csv('gamesync_sales_data_transformed.csv').iloc[:,1:]
data['monday_of_week']=pd.to_datetime(data['monday_of_week'])

# sample game interaction data
gi_data = pd.read_csv('gi_data_transformed.csv').iloc[:,1:]
weekly_gi_events = gi_data.groupby(['event', 'week_start']).agg(
    total_interactions=('player_address', 'count'),
    Unique_users=('player_address', 'nunique'),
    ).reset_index().round({'total_interactions': 2, 'Unique_users': 2}).sort_values(by='week_start', ascending=True)

weekly_gi_game = gi_data.groupby(['week_start']).agg(
    total_interactions=('player_address', 'count'),
    Unique_users=('player_address', 'nunique'),
    ).reset_index().round({'total_interactions': 2, 'Unique_users': 2}).sort_values(by='week_start', ascending=True)



# dashboard title
st.title("Game Collection Dashboard")





### ----- weekly data as table 
weekly_data = data.groupby(['game', 'monday_of_week']).agg(
    NFTs_Sold=('number_of_nft_token_id', 'sum'),
    Sales_volume=('value', 'sum'),
    Unique_buyers=('buyer_address', 'nunique'),
    ).reset_index().round({'NFTs_Sold': 2, 'Sales_volume': 2, 'Unique_buyers': 2}).sort_values(by='game', ascending=False)

weekly_data_table = weekly_data.loc[weekly_data.monday_of_week=='2023-08-21'][['game', 'NFTs_Sold', 'Sales_volume', 'Unique_buyers']]


### ------- filtered data plots 


tab1, tab2, tab3, tab4 = st.tabs(["Sales Summary", "Game sales comparison", "Collection Sales", "Game interactions"])

with tab1:
    st.header("Sales data")
    st.markdown("Past weeks sales for each game + sales trends week on week with mean sales price, floor and ceiling")
    
    st.markdown("### Last week Sales")

    

    st.dataframe(weekly_data_table)

    # plot game sales data 
    st.markdown("---")
    st.markdown("### Weekly sales trend")

    # sns.set_style("darkgrid")
    fig_2 = sns.relplot(x="monday_of_week", y="value_per_nft_USD",
        hue="game",
        data=data,  
        col="game",  
        kind="line", 
        errorbar = 'sd',
        col_wrap=4, 
        legend=False)
    fig_2.set(ylim=(0, 1400))
    fig_2.set_xlabels('Week')
    fig_2.set_ylabels('Sales Price (USD)')
    fig_2.tick_params(labelrotation=45)
    st.pyplot(fig_2)



with tab2:
    st.header("Game comparison")
    st.markdown("Select games to compare sales")

    # Game filter 
    Game_selector = st.multiselect(
    'Select Games',
    list(pd.unique(data["game"])),
    [data.game.iloc[0]]
    # ['Apeiron']
    )


    # filter dataset based on selector 
    filterd_weekly_data = weekly_data[weekly_data["game"].isin(Game_selector)]
    filterd_weekly_data['monday_of_week'] = filterd_weekly_data['monday_of_week'].dt.date
    filterd_weekly_data = filterd_weekly_data.sort_values(by="monday_of_week")


    col_1, col_2, col_3 = st.columns(3)

    with col_1:

        st.markdown("### Number of NFTs sold")
        fig_1 = px.line(filterd_weekly_data, x="monday_of_week", y="NFTs_Sold",color="game")
        fig_1.update_layout(autosize=False
                            ,width=500,height=500,margin=dict(l=50,r=50,b=25,t=25,pad=4), xaxis_title="Week")
        st.write(fig_1)

    with col_2:

        st.markdown("### Weekly Sales Volume")
        fig_2 = px.line(filterd_weekly_data, x="monday_of_week", y="Sales_volume",color="game")
        fig_2.update_layout(autosize=False
                            ,width=500,height=500,margin=dict(l=50,r=50,b=25,t=25,pad=4), xaxis_title="Week")
        st.write(fig_2)
 
    with col_3:

        st.markdown("### Weekly unique buyer count")
        fig_3 = px.line(filterd_weekly_data, x="monday_of_week", y="Unique_buyers",color="game")
        fig_3.update_layout(autosize=False
                            ,width=500,height=500,margin=dict(l=50,r=50,b=25,t=25,pad=4), xaxis_title="Week")
        st.write(fig_3)



with tab3:

    st.header("Collection sales")
    st.markdown("Select a game and collection to view sales numbers. Enable toggle to drill down into collections and individual tokens.")

    col_4, col_5, col_6 = st.columns(3)

    with col_4:

        # Game_selector_2 = st.multiselect(
        # 'Select Game Name',
        # list(pd.unique(data["game"])),
        # [data.game.iloc[0]])

        Game_selector_2 = st.selectbox(
                'Chose Game (One game)',
                list(pd.unique(data["game"])))

        
    with col_5:
        collection_data_for_game = data[data["game"]==Game_selector_2]

        multi_collection = st.toggle('Multi collections')

        if multi_collection:
            Collection_selector_2 = st.multiselect(
            'Chose collections',
            list(pd.unique(collection_data_for_game["collection_name"])),
            [collection_data_for_game.collection_name.iloc[0]])
            token_data_for_collection = collection_data_for_game[collection_data_for_game["collection_name"].isin(Collection_selector_2)]

        else: 
            Collection_selector_2 = st.selectbox(
            'Chose Collection',
            list(pd.unique(collection_data_for_game["collection_name"])))
            token_data_for_collection = collection_data_for_game[collection_data_for_game["collection_name"]==  Collection_selector_2]
 
    with col_6:
        
        token_selections = st.toggle('Pick Tokens')
        if token_selections:
            
            token_selector_2 = st.multiselect(
            'Select tokens',
            list(pd.unique(token_data_for_collection["nft_token_id"])),
            [token_data_for_collection.nft_token_id.iloc[0]])
            token_data_for_collection = token_data_for_collection[token_data_for_collection["nft_token_id"].isin(token_selector_2)]

    st.markdown("---")
    st.markdown("### Sales summary")

    col1, col2, col3, col_4, col_5, col_6 = st.columns(6)
    col1.metric(label="NFTs Sold", value=token_data_for_collection.nft_token_id.count())
    col1.metric(label="Unique NFTs Sold", value=token_data_for_collection.nft_token_id.nunique())



    col3.metric(label="Mean Price", value=token_data_for_collection.value_per_nft_USD.mean().round(2))
    col3.metric(label="Floor Price", value=token_data_for_collection.value_per_nft_USD.min().round(2))
    col3.metric(label="Price StDev", value=token_data_for_collection.value_per_nft_USD.std().round(2))
    # st.metric(label="NFTs Sold", value=token_data_for_collection.nft_token_id.count())


with tab4:

    st.header("Game interactions - GFC")
    st.markdown("On-chain interactions for game play. GFC only at the moment")

    combine_interactions = st.toggle('combine interactions', value=True)
    if combine_interactions:
        fig_gi_game = px.line(weekly_gi_game, x="week_start", y="Unique_users")
        fig_gi_game.update_layout(autosize=False
                             ,width=1000,height=500,margin=dict(l=50,r=50,b=25,t=25,pad=4), xaxis_title="Week", yaxis_title="unique users"
        , yaxis=dict(range=[0,weekly_gi_game.Unique_users.max()]))
        st.write(fig_gi_game)
    else: 

        fig_gi_event = px.line(weekly_gi_events, x="week_start", y="Unique_users", color='event')
        fig_gi_event.update_layout(autosize=False
                             ,width=1000,height=500,margin=dict(l=50,r=50,b=25,t=25,pad=4), xaxis_title="Week", yaxis_title="unique users"
        , yaxis=dict(range=[0,weekly_gi_events.Unique_users.max()]))
        st.write(fig_gi_event)

    


   
