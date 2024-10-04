import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from scipy.stats import spearmanr
sns.set_style("whitegrid")

plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['figure.facecolor'] = 'black'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'white'
plt.rcParams['figure.edgecolor'] = 'white'

# FUNGSI AIR POLUTION
def air_polution_df(df, option):
    df['yr'] = df['year']
    df['mo'] = df['month']
    df['dd'] = df ['day']
    df['hr'] =df['hour']
    df['PM2.5'] = df['PM2.5']
    df['PM10'] = df['PM10']
    df['SO2'] = df['SO2']
    df['NO2'] = df['NO2']
    df['CO'] = df['CO']
    df['O3'] = df['O3']
    air_polution_df = df[['yr', 'mo', 'dd', 'hr', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].copy()
    air_polution_df = air_polution_df.rename(columns ={
        'yr' :'year',
        'mo' :'month',
        'dd' : 'day',
        'hr' :'hour',
        'PM2.5' : 'PM2.5',
        'PM10' : 'PM10',
        'SO2'  : 'SO2',
        'NO2'  : 'NO2',
        'CO'  : 'CO',
        'O3' : 'O3'})
    if (option == "1 Day"):
        air_polution_df = df.groupby(by = ['year', 'month', 'day','hour'] ).agg({
            "PM2.5" : "mean",
            "PM10" : "mean",
            "SO2" : "mean",
            "NO2" : "mean",
            "CO" : "mean",
            "O3" : "mean"}).sort_values(by = ['year', 'month', 'day','hour'], ascending = True)
        air_polution_df = air_polution_df.reset_index()
        air_polution_df['time'] = air_polution_df["hour"].astype(str) + ":00"
    elif (option == "Daily"):
        air_polution_df = df.groupby(by = ['year', 'month', 'day'] ).agg({
            "PM2.5" : "mean",
            "PM10" : "mean",
            "SO2" : "mean",
            "NO2" : "mean",
            "CO" : "mean",
            "O3" : "mean"}).sort_values(by = ['year', 'month', 'day'], ascending = True)
        air_polution_df = air_polution_df.reset_index()
        air_polution_df['time'] = air_polution_df["year"].astype(str) + "-" + air_polution_df["month"].astype(str) + "-" + air_polution_df["day"].astype(str)
    elif (option == "Monthly"):
        air_polution_df = df.groupby(by = ['year', 'month'] ).agg({
            "PM2.5" : "mean",
            "PM10" : "mean",
            "SO2" : "mean",
            "NO2" : "mean",
            "CO" : "mean",
            "O3" : "mean"}).sort_values(by = ['year', 'month'], ascending = True)
        air_polution_df = air_polution_df.reset_index()
        air_polution_df['time'] = air_polution_df["year"].astype(str) + "-" + air_polution_df["month"].astype(str)
    else:
        air_polution_df = df.groupby(by = ['year'] ).agg({
            "PM2.5" : "mean",
            "PM10" : "mean",
            "SO2" : "mean",
            "NO2" : "mean",
            "CO" : "mean",
            "O3" : "mean"}).sort_values(by = ['year'], ascending = True)
        air_polution_df = air_polution_df.reset_index()
        air_polution_df['time'] = air_polution_df["year"].astype(str)
    return air_polution_df

def airpolution_display(df):
    pm25= round(df['PM2.5'].mean(), 2)
    pm10= round(df['PM10'].mean(), 2)
    SO2= round(df['SO2'].mean(), 2)
    NO2= round(df['NO2'].mean(), 2)
    CO= round(df['CO'].mean(), 2)
    O3= round(df['O3'].mean(),2)

    with st.container():
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            if pm25 >= 250.0:
                st.metric("PM25: " + str(pm25), value= "BERBAHAYA" )
            elif pm25 >= 150.4:
                st.metric("PM25: " + str(pm25), value= "SANGAT TIDAK SEHAT")
            elif pm25 >= 55.4:
                st.metric("PM25: " + str(pm25), value= "TIDAK SEHAT" )
            elif pm25 >= 15.6:
                st.metric("PM25: " + str(pm25), value= "SEDANG" )
            else:
                st.metric("PM25: " + str(pm25), value= "BAIK" )
        with col2:
            st.metric("SO2:", value = SO2)
        with col3:
                st.metric("NO2:", value = NO2)

    with st.container():
        col1,col2, col3 = st.columns([2,1,1])
        with col1:
            if pm10 >= 421:
                st.metric("PM10: " + str(pm10), value= "BERBAHAYA" )
            elif pm10 >= 351:
                st.metric("PM10: " + str(pm10), value= "SANGAT TIDAK SEHAT" )
            elif pm10 >= 151:
                st.metric("PM10: " + str(pm10), value= "TIDAK SEHAT" )
            elif pm10 >= 51:
                st.metric("PM10: " + str(pm10), value= "SEDANG" )
            else:
                st.metric("PM10: " + str(pm10), value= "BAIK" )
        with col2:
            st.metric("CO:", value = CO)
        with col3:
            st.metric("O3:", value = O3)
            
def air_polution_graph(df):
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(df['time'], df['PM2.5'], marker='o', linewidth=2)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20, labelrotation = 45)
    ax.set_ylabel("PM2.5", fontsize=25)
    ax.set_title("PM2.5", loc="center", fontsize=35)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(df['time'], df['PM10'], marker='o', linewidth=2)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20, labelrotation = 45)
    ax.set_ylabel("PM10", fontsize=25)
    ax.set_title("PM10", loc="center", fontsize=35)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(df['time'], df['SO2'], marker='o', linewidth=2)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20, labelrotation = 45)
    ax.set_ylabel("SO2", fontsize=25)
    ax.set_title("SO2", loc="center", fontsize=35)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(df['time'], df['NO2'], marker='o', linewidth=2)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20, labelrotation = 45)
    ax.set_ylabel("NO2", fontsize=25)
    ax.set_title("NO2", loc="center", fontsize=35)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(df['time'], df['CO'], marker='o', linewidth=2)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20, labelrotation = 45)
    ax.set_ylabel("CO", fontsize=25)
    ax.set_title("CO", loc="center", fontsize=35)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(df['time'], df['O3'], marker='o', linewidth=2)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20, labelrotation = 45)
    ax.set_ylabel("O3", fontsize=25)
    ax.set_title("O3", loc="center", fontsize=35)
    st.pyplot(fig)

#FUNGSI AIR PARAMETERS
def air_parameters_df(df, option):
    df['yr'] = df['year']
    df['mo'] = df['month']
    df['dd'] = df ['day']
    df['hr'] =df['hour']
    df['suhu'] = df['TEMP']
    df['tekanan'] = df['PRES']
    df['SO2'] = df['SO2']
    df['NO2'] = df['NO2']
    df['CO'] = df['CO']
    df['O3'] = df['O3']
    air_parameters_df = df[['yr', 'mo', 'dd', 'hr', 'suhu', 'tekanan']].copy()
    air_parameters_df = air_parameters_df.rename(columns ={
        'yr' :'year',
        'mo' :'month',
        'dd' : 'day',
        'hr' :'hour',
        'suhu' : 'TEMP',
        'tekanan' : 'PRES'})
    if (option == "1 Day"):
        air_parameters_df = df.groupby(by = ['year', 'month', 'day','hour'] ).agg({
            "TEMP" : "mean",
            "PRES" : "mean"}).sort_values(by = ['year', 'month', 'day','hour'], ascending = True)
        air_parameters_df = air_parameters_df.reset_index()
        air_parameters_df['time'] = air_parameters_df["hour"].astype(str) + ":00"
    elif (option == "Daily"):
        air_parameters_df = df.groupby(by = ['year', 'month', 'day'] ).agg({
            "TEMP" : "mean",
            "PRES" : "mean"}).sort_values(by = ['year', 'month', 'day'], ascending = True)
        air_parameters_df = air_parameters_df.reset_index()
        air_parameters_df['time'] = air_parameters_df["year"].astype(str) + "-" + air_parameters_df["month"].astype(str) + "-" + air_parameters_df["day"].astype(str)
    elif (option == "Monthly"):
        air_parameters_df = df.groupby(by = ['year', 'month'] ).agg({
            "TEMP" : "mean",
            "PRES" : "mean"}).sort_values(by = ['year', 'month'], ascending = True)
        air_parameters_df = air_parameters_df.reset_index()
        air_parameters_df['time'] = air_parameters_df["year"].astype(str) + "-" + air_parameters_df["month"].astype(str)
    else:
        air_parameters_df = df.groupby(by = ['year'] ).agg({
            "TEMP" : "mean",
            "PRES" : "mean"}).sort_values(by = ['year'], ascending = True)
        air_parameters_df = air_parameters_df.reset_index()
        air_parameters_df['time'] = air_parameters_df["year"].astype(str)
    return air_parameters_df

def airparameters_display(df):
    suhu= round(df['TEMP'].mean(), 2)
    tekanan= round(df['PRES'].mean(), 2)

    with st.container():
        col1, col2= st.columns(2)
        with col1:
            st.metric("TEMPERATURE:", value = str(suhu) + " °C")
        with col2:
                st.metric("PRESSURE:", value = str(tekanan) + " hPa")
                
def air_parameters_graph(df):
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(df['time'], df['TEMP'], marker='o', linewidth=2)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20, labelrotation = 45)
    ax.set_ylabel("Temperature (°C)", fontsize=25)
    ax.set_title("Temperature", loc="center", fontsize=35)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(df['time'], df['PRES'], marker='o', linewidth=2)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20, labelrotation = 45)
    ax.set_ylabel("Pressure (hPa)", fontsize=25)
    ax.set_title("Pressure", loc="center", fontsize=35)
    st.pyplot(fig)

#Fungsi Correlation
def correlation_df(df):
    df['PM2.5'] = df['PM2.5']
    df['PM10'] = df['PM10']
    df['SO2'] = df['SO2']
    df['NO2'] = df['NO2']
    df['CO'] = df['CO']
    df['O3'] = df['O3']
    df['suhu'] = df['TEMP']
    df['tekanan'] =df['PRES']
    correlation_dataframe = df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'suhu', 'tekanan']].copy()
    correlation_dataframe = correlation_dataframe.rename(columns ={
        'PM2.5' : 'PM2.5',
        'PM10' : 'PM10',
        'SO2'  : 'SO2',
        'NO2'  : 'NO2',
        'CO'  : 'CO',
        'O3' : 'O3',
        'suhu' : 'TEMP',
        'tekanan' : 'PRES'
    })
    return correlation_dataframe

def temp_correlation(df):
    temp_PM25 = spearmanr(df['PM2.5'], df['TEMP'])
    temp_PM10 = spearmanr(df['PM10'], df['TEMP'])
    temp_SO2 = spearmanr(df['SO2'], df['TEMP'])
    temp_NO2 = spearmanr(df['NO2'], df['TEMP'])
    temp_CO = spearmanr(df['CO'], df['TEMP'])
    temp_O3 = spearmanr(df['O3'], df['TEMP'])  
    temp_correlation = {'parameter': ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"],
                        'values' : [temp_PM25, temp_PM10, temp_SO2, temp_NO2, temp_CO, temp_O3]}
    temp_correlation_df = pd.DataFrame(temp_correlation)
    temp_correlation_df
    
def pres_correlation(df):
    pres_PM25 = spearmanr(df['PM2.5'], df['PRES'])
    pres_PM10 = spearmanr(df['PM10'], df['PRES'])
    pres_SO2 = spearmanr(df['SO2'], df['PRES'])
    pres_NO2 = spearmanr(df['NO2'], df['PRES'])
    pres_CO = spearmanr(df['CO'], df['PRES'])
    pres_O3 = spearmanr(df['O3'], df['PRES'])

    pres_correlation = {'parameter': ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"],
                        'values' : [pres_PM25, pres_PM10, pres_SO2, pres_NO2, pres_CO, pres_O3]}
    pres_correlation_df = pd.DataFrame(pres_correlation)
    pres_correlation_df
    
def heatmap_graph(df):
    correlation = df.corr(method="spearman")
    fig, ax = plt.subplots(figsize=(15,10))
    sns.heatmap(correlation, vmax=1, vmin=-1, center=0, cmap="Blues")
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20)
    ax.set_title("Korelasi Polusi dengan Suhu dan Tekanan", loc='center', fontsize=35)

    plt.show()

# Fungsi Partikel by Time Span
def time_category_particle_df(df):
    df['time_category'] = df.hour.apply(
        lambda x: "Night" if x<6
        else "Morning" if x<12
        else "Afternoon" if x<18
        else "Evening"
    )
    
    time_category_group = df.groupby('time_category').agg({
        'hour' : 'first',
        'PM2.5' : 'mean',
        'PM10' : 'mean'})\
        .sort_values(by=['hour'], ascending=True)
    time_category_group = time_category_group.reset_index()

    return time_category_group

def time_category_bar_graph(df):
    warna = ['#D0EFFF', '#2A9DF4','#187BCD','#1167B1']
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))
    ax[0].bar(x= df['time_category'], height = df['PM2.5'], color = warna)
    ax[0].tick_params(axis='y', labelsize=20)
    ax[0].tick_params(axis='x', labelsize=20)
    ax[0].set_xlabel(None)
    ax[0].set_ylabel("PM2.5", fontsize = 20)

    ax[1].bar(x= df['time_category'], height = df['PM10'], color = warna)
    ax[1].tick_params(axis='y', labelsize=20)
    ax[1].tick_params(axis='x', labelsize=20)
    ax[1].set_xlabel(None)
    ax[1].set_ylabel("PM10", fontsize = 20)

    st.pyplot(fig)

# Get data
all_df = pd.read_csv("dashboard_data.csv")
all_df.sort_values(by="date_time", inplace=True)
all_df.reset_index(inplace=True)
all_df['date_time'] = pd.to_datetime(all_df['date_time'], format='%Y-%m-%d %H:%M:%S')

#extract date_time
min_date = all_df['date_time'].min()
max_date = all_df['date_time'].max()

#MAIN
st.title("Air Quality in TIANTAN")
with st.sidebar:
    option = st.selectbox("Tampilkan data:", ("1 Day", "Daily", "Monthly", "Yearly"))

if (option == "1 Day") :
    # Mengambil exact date dari date_input
    with st.sidebar:
        exact_date = st.date_input(
            label='Tanggal',
            min_value= min_date,
            max_value= max_date,
            value= None,
            format = "YYYY-MM-DD"
        )
        start_time = st.time_input(
            label = "Mulai dari" ,
            value = None,
            step = 3600
        )
        end_time = st.time_input(
            label = "Sampai" ,
            value = None,
            step = 3600
        )

    date_start = str(exact_date) + " " + str(start_time)
    date_end = str(exact_date) + " " + str(end_time)


    main_df = all_df[(all_df['date_time'].astype(str) >= date_start) &
                     (all_df['date_time'].astype(str) <= date_end)]
    air_polution = air_polution_df(main_df, option)
    air_parameters = air_parameters_df(main_df, option)

    # Visualisasi Data Air Polution
    with st.container():
        st.header("Air Polution in TIANTAN")
        airpolution_display(air_polution)
        air_polution_graph(air_polution)

    # Visualisasi Data Air Parameter
    with st.container():
        st.header("Air Parameters in TIANTAN")
        airparameters_display(air_parameters)
        air_parameters_graph(air_parameters)

    #KORELASI
    polusi_parameter = correlation_df(main_df)

    with st.container():
        st.header("Air Polution VS Air Parameters")
        with st.container():
            st.subheader("Correlation Heatmap")
            col1, col2 = st.columns([2,1])
            with col1:
                heatmap_graph(polusi_parameter)
            with col2:
                with st.expander("Air Quality VS Temperature"):
                    temp_correlation(polusi_parameter)
                with st.expander("Air Quality VS Pressure"):
                    pres_correlation(polusi_parameter)

    #Partikel pada rentang waktu
    particle = time_category_particle_df(main_df)
    with st.container():
        st.header("Air Polution Particulate Matter in TIANTAN")
        time_category_bar_graph(particle)

elif (option == "Daily"):
    with st.sidebar:
    # Mengambil exact date dari date_input
        start_date, end_date = st.date_input(
            label='Tanggal',
            min_value= min_date,
            max_value= max_date,
            value= [min_date, max_date]
            )

    date_start = str(start_date) + " 00:00:00"
    date_end = str(end_date) + " 23:00:00"

    main_df = all_df[(all_df['date_time'].astype(str) >= date_start) &
                     (all_df['date_time'].astype(str) <= date_end)]

    air_polution = air_polution_df(main_df, option)
    air_parameters = air_parameters_df(main_df, option)

    # Visualisasi Data Air Polution
    with st.container():
        st.header("Air Polution in TIANTAN")
        airpolution_display(air_polution)
        air_polution_graph(air_polution)

    # Visualisasi Data Air Parameter
    with st.container():
        st.header("Air Parameters in TIANTAN")
        airparameters_display(air_parameters)
        air_parameters_graph(air_parameters)

    #KORELASI
    polusi_parameter = correlation_df(main_df)
    with st.container():
        st.header("Air Polution VS Air Parameters")
        with st.container():
            st.subheader("Correlation Heatmap")
            col1, col2 = st.columns([2,1])
            with col1:
                heatmap_graph(polusi_parameter)
            with col2:
                with st.expander("Air Quality VS Temperature"):
                    temp_correlation(polusi_parameter)
                with st.expander("Air Quality VS Pressure"):
                    pres_correlation(polusi_parameter)

    #Partikel pada rentang waktu
    particle = time_category_particle_df(main_df)
    with st.container():
        st.header("Air Polution Particulate Matter in TIANTAN")
        time_category_bar_graph(particle)

elif (option == "Monthly"):
    with st.sidebar:
        # Mengambil exact date dari date_input
        start_date_bulan, end_date_bulan = st.date_input(
            label='Tanggal',
            min_value= min_date,
            max_value= max_date,
            value= [min_date, max_date]
        )

    date_start = str(start_date_bulan) + " 00:00:00"
    date_end = str(end_date_bulan) + " 23:00:00"

    main_df = all_df[(all_df['date_time'].astype(str) >= date_start) &
                     (all_df['date_time'].astype(str) <= date_end)]

    air_polution = air_polution_df(main_df, option)
    air_parameters = air_parameters_df(main_df, option)

    # Visualisasi Data Air Polution
    with st.container():
        st.header("Air Polution in TIANTAN")
        airpolution_display(air_polution)
        air_polution_graph(air_polution)

    # Visualisasi Data Air Parameter
    with st.container():
        st.header("Air Parameters in TIANTAN")
        airparameters_display(air_parameters)
        air_parameters_graph(air_parameters)

    #KORELASI
    polusi_parameter = correlation_df(main_df)
    with st.container():
        st.header("Air Polution VS Air Parameters")
        with st.container():
            st.subheader("Correlation Heatmap")
            col1, col2 = st.columns([2,1])
            with col1:
                heatmap_graph(polusi_parameter)
            with col2:
                with st.expander("Air Quality VS Temperature"):
                    temp_correlation(polusi_parameter)
                with st.expander("Air Quality VS Pressure"):
                    pres_correlation(polusi_parameter)

    #Partikel pada rentang waktu
    particle = time_category_particle_df(main_df)
    with st.container():
        st.header("Air Polution Particulate Matter in TIANTAN")
        time_category_bar_graph(particle)

else:
    # Mengambil exact date dari date_input
    with st.sidebar:
        start_date_tahun, end_date_tahun = st.date_input(
            label='Tanggal',
            min_value = min_date,
            max_value = max_date,
            value = [min_date, max_date]
        )

    date_start = str(start_date_tahun) + " 00:00:00"
    date_end = str(end_date_tahun) + " 23:00:00"

    main_df = all_df[(all_df['date_time'].astype(str) >= date_start) &
                     (all_df['date_time'].astype(str) <= date_end)]

    air_polution = air_polution_df(main_df, option)
    air_parameters = air_parameters_df(main_df, option)

    # Visualisasi Data Air Polution
    with st.container():
        st.header("Air Polution in TIANTAN")
        airpolution_display(air_polution)
        air_polution_graph(air_polution)

    # Visualisasi Data Air Parameter
    with st.container():
        st.header("Air Parameters in TIANTAN")
        airparameters_display(air_parameters)
        air_parameters_graph(air_parameters)

    #KORELASI
    polusi_parameter = correlation_df(main_df)

    with st.container():
        st.header("Air Polution VS Air Parameters")
        with st.container():
            st.subheader("Correlation Heatmap")
            col1, col2 = st.columns([2,1])
            with col1:
                heatmap_graph(polusi_parameter)
            with col2:
                with st.expander("Air Quality VS Temperature"):
                    temp_correlation(polusi_parameter)
                with st.expander("Air Quality VS Pressure"):
                    pres_correlation(polusi_parameter)

    #Partikel pada rentang waktu
    particle = time_category_particle_df(main_df)
    with st.container():
        st.header("Time Category Air Polution Particulate in TIANTAN")
        time_category_bar_graph(particle)
