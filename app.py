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
# display_1 = weekly_data.loc[weekly_data['game'].isin(options)][['game', 'NFTs_Sold', 'Sales_volume', 'Unique_buyers']]

# st.markdown("### Weekly Data View")
# st.dataframe(display_1)







### ------- filtered data plots 

# filterd_data = data[data["game"].isin(Game_selector)]
# filterd_weekly_data = weekly_data[weekly_data["game"].isin(Game_selector)]
# filterd_weekly_data['monday_of_week'] = filterd_weekly_data['monday_of_week'].dt.date
# filterd_weekly_data = filterd_weekly_data.sort_values(by="monday_of_week")


tab1, tab2, tab3 = st.tabs(["Summary", "Game comparison", "Collection comparison"])

with tab1:
    st.header("Sales data")

    st.markdown("### Last week Sales")
#    weekly_data_display, plot_game_sales = st.columns(2)
   
#    with weekly_data_display:

    st.dataframe(weekly_data_table)

    # plot game sales data 
    st.markdown("---")
    st.markdown("### Weekly sales trend")

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
    ['Apeiron'])


    # filter dataset based on selector 
    filterd_weekly_data = weekly_data[weekly_data["game"].isin(Game_selector)]
    filterd_weekly_data['monday_of_week'] = filterd_weekly_data['monday_of_week'].dt.date
    filterd_weekly_data = filterd_weekly_data.sort_values(by="monday_of_week")


    col_1, col_2, col_3 = st.columns(3)

    with col_1:

        st.markdown("### Number of NFTs sold")
        fig_1 = px.line(filterd_weekly_data, x="monday_of_week", y="NFTs_Sold",color="game")
        st.write(fig_1)

    with col_2:

        st.markdown("### Weekly Sales Volume")
        fig_2 = px.line(filterd_weekly_data, x="monday_of_week", y="Sales_volume",color="game")
        st.write(fig_2)
 
    with col_3:

        st.markdown("### Weekly unique buyer count")
        fig_3 = px.line(filterd_weekly_data, x="monday_of_week", y="Unique_buyers",color="game")
        st.write(fig_3)



with tab3:
   st.header("Collection comparison")





# with weekly_data_display:
#     st.dataframe(filterd_weekly_data)


# with plot_game_sales:
    # st.line_chart(data = filterd_weekly_data, x="monday_of_week", y="NFTs_Sold", color = 'game')

    # fig = plt.figure(figsize=(10, 4))
    # sns.lineplot(data=filterd_weekly_data, x="monday_of_week", y="NFTs_Sold", hue = 'game')

    # fig = px.line(filterd_weekly_data, x="monday_of_week", y="NFTs_Sold",color="game")
    
    # ax.set(ylim=(0, weekly_data.NFTs_Sold.max()))
    # ax.set_xlabel('Week')
    # ax.set_ylabel('Tokens sold')
    # ax.tick_params(labelrotation=45)
    # st.write(fig)
    # st.pyplot(fig)

    # fig = sns.relplot(x="monday_of_week", y="value_per_nft_USD",
    #         hue="game",
    #         data=filterd_data,  
    #         col="game",  
    #         kind="line", 
    #         errorbar = 'sd',
    #         col_wrap=2, 
    #         legend=False)

    # fig.set(ylim=(0, 1400))
    # fig.set_xlabels('Week')
    # fig.set_ylabels('Sales Price (USD)')
    # fig.tick_params(labelrotation=45)
    # st.pyplot(fig)

# with plot_weekly_sales_volume:
#     # fig_2 = sns.relplot(x="monday_of_week", y="value_per_nft_USD",
#     #         hue="game",
#     #         data=filterd_data,  
#     #         col="game",  
#     #         kind="line", 
#     #         errorbar = 'sd',
#     #         col_wrap=2, 
#     #         legend=False)
#     fig_2 = sns.lineplot(data=filterd_weekly_data, x="monday_of_week", y="Sales_volume", color = 'Green')
#     # fig_2.set(ylim=(0, 1400))
#     # fig_2.set_xlabels('Week')
#     # fig_2.set_ylabels('Sales Price (USD)')
#     # fig_2.tick_params(labelrotation=45)
#     st.pyplot(fig_2)


    # fig_2 = sns.lineplot(data=weekly_data, x="monday_of_week", y="Sales_volume", color = 'Green')

    # fig_2.set(ylim=(0, weekly_data.Sales_volume.max()))
    # fig_2.set_xlabel('Week')
    # fig_2.set_ylabel('Sales volume (USD)')
    # fig_2.tick_params(labelrotation=45)
    # st.pyplot(fig_2)






# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)

# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows


# progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
# st.button("Re-run")