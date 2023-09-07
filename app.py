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

# sample data
data = pd.read_csv('gamesync_sales_data_transformed.csv').iloc[:,1:]
data['monday_of_week']=pd.to_datetime(data['monday_of_week'])

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


tab1, tab2, tab3 = st.tabs(["Summary", "Game comparison", "Collection Sales"])

with tab1:
    st.header("Sales data")

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
                            ,width=500,height=500,margin=dict(l=50,r=50,b=25,t=25,pad=4))
        st.write(fig_1)

    with col_2:

        st.markdown("### Weekly Sales Volume")
        fig_2 = px.line(filterd_weekly_data, x="monday_of_week", y="Sales_volume",color="game")
        fig_2.update_layout(autosize=False
                            ,width=500,height=500,margin=dict(l=50,r=50,b=25,t=25,pad=4))
        st.write(fig_2)
 
    with col_3:

        st.markdown("### Weekly unique buyer count")
        fig_3 = px.line(filterd_weekly_data, x="monday_of_week", y="Unique_buyers",color="game")
        fig_3.update_layout(autosize=False
                            ,width=500,height=500,margin=dict(l=50,r=50,b=25,t=25,pad=4))
        st.write(fig_3)



with tab3:

    st.header("Collection sales")


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
