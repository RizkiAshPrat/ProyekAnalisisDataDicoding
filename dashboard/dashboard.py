import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
sns.set(style='dark')


def create_type_user_df(df):
    type_user_df = df.groupby(by='mnth')[['casual', 'registered']].sum().reset_index()
    type_user_df['mnth'] = pd.Categorical(type_user_df['mnth'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
    type_user_df_sorted = type_user_df.sort_values('mnth')
    return type_user_df_sorted

def create_weekly_df(df):
    weekly_df = df.groupby(by='weekday').cnt.count().reset_index()
    weekly_df_sort = weekly_df.sort_values(by='cnt', ascending=False)
    return weekly_df_sort

def create_monthly_df(df):
    monthly_df = df.groupby(by='mnth')[['casual', 'registered', 'cnt']].sum().reset_index()
    return monthly_df

# """
# Mulai Membuat Dashboard
# """
#Load File
all_df = pd.read_csv('https://raw.githubusercontent.com/RizkiAshPrat/ProyekAnalisisDataDicoding/main/dashboard/main_data.csv')
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

#Meskipun dari awal sudah datetime, tetap perlu di datetime ulang
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

#Sidebar
min_date = all_df['dteday'].min()
max_date = all_df['dteday'].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/RizkiAshPrat/ProyekAnalisisDataDicoding/blob/main/dashboard/logo.png?raw=true")

    #Menambahkan Tanggal
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

#Main df merupakan hasil filter all df dari sidebar
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

st.header('Bike Rentals Dashboard :sparkles:')

#Dataframe Utama
st.subheader('Main DataFrame')
st.dataframe(data=main_df)

type_user_df = create_type_user_df(main_df)
weekly_df = create_weekly_df(main_df)
monthly_df = create_monthly_df(main_df)

st.subheader('Daily rentals')
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals_casual = monthly_df.casual.sum()
    st.metric("Total Rentals Casual", value="{:,.0f}".format(total_rentals_casual).replace(",", "."))
with col2:
    total_rentals_registered = monthly_df.registered.sum()
    st.metric("Total Rentals Registered", value="{:,.0f}".format(total_rentals_registered).replace(",", "."))
with col3:
    total_rentals_cnt = monthly_df.cnt.sum()
    st.metric("Total Rentals All", value="{:,.0f}".format(total_rentals_cnt).replace(",", "."))

st.subheader('Bike Rentals Monthly')
fig,ax=plt.subplots(figsize=(12,6))
sns.barplot(x='mnth', y='amount', hue='Jenis',  data=pd.melt(type_user_df, id_vars='mnth', value_name='amount', var_name='Jenis'), palette='bright')
ax.set(xlabel='Bulan', ylabel='Total Bike Rentals')
plt.title('Type Of User V/S Bike Rentals Classification by Month')
st.pyplot(fig)

st.subheader('Bike Rentals Daily')
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(x='weekday', y='cnt', data=weekly_df, order=weekly_df['weekday'], palette='bright')
ax.set(xlabel='Hari', ylabel='Total Bike Rentals')
for label in ax.containers:
    ax.bar_label(label)
plt.title('Total bike rentals V/S Hari dalam Weekday')
st.pyplot(fig)

st.subheader('Bike Rentals in Weather')
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(x='weathersit', y='cnt', data=main_df, palette='bright')
plt.ylabel("Total Bike Rentals")
st.pyplot(fig)

st.subheader('Bike Rentals in Weather sub Type of User')
df_weather_by_user = main_df[['weathersit', 'casual', 'registered']]
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(x='weathersit', y='amount', hue='Jenis',  data=pd.melt(df_weather_by_user, id_vars='weathersit', value_name='amount', var_name='Jenis'), palette='bright')
plt.title('Relationship between weather conditions V/S bike rentals Group by Type of User')
st.pyplot(fig)

st.subheader('Cluster Bike Rentals Ride by Season and Temperature')
fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(x='temp', y='cnt', data=main_df, hue='season')
plt.xlabel("Temperature (Celcius)")
plt.ylabel("Total Bike Rentals")
plt.title("Clusters of bike rentals rides by season and temperature (2011-2012)")
plt.tight_layout()
st.pyplot(fig)
 
st.caption('Copyright (c) Rizki Ashuri Pratama 2023')
