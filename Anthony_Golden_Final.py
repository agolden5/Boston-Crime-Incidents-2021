'''
Anthony Golden
12/18/2022
This is my interactive website of Boston Crime Incidents for 2021
This is all my own work
'''

# Importing needed packages
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt
import pandas as pd
import csv
import random as rd

#data file
data = "BostonCrime2021_7000.csv"

#file to read in data into list of dictionaries
def read_file(filename):
    content=[]
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)

        for row in csv_reader:
            row_data = {key: value for key, value in zip(headers,row)}
            content.append(row_data)
    return content

#setting up app
st.title("Boston Crime Incident Reports 2021")
st.sidebar.header("UI Controls")
st.sidebar.success("Map filters: ")
#reading data into dataframe and removing data with no information on locaiton
df_bos = pd.read_csv(data)
df_bos = df_bos.loc[df_bos["Lat"] != 0]
df_bos.rename(columns={"Lat":"lat","Long":"lon"}, inplace = True)

#getting the distinct districts from dataframe
district_list = []
for d in df_bos.DISTRICT:
    if d not in district_list:
        district_list.append(d)

#making a sub-dataframe from distinct districts
sub_df_list =[]
for d in district_list:
    sub_df_bos = df_bos[df_bos["DISTRICT"] == d]
    sub_df_bos = sub_df_bos.dropna()
    sub_df_list.append(sub_df_bos)

#layer to scatter map
layer_list = []
for sub_df_bos in sub_df_list:
    layer = pdk.Layer(type = 'ScatterplotLayer',
                      data = sub_df_bos,
                      get_position = '[lon, lat]',
                      get_radius = 40,
                      get_color = [rd.randint(0,255), rd.randint(0,255),rd.randint(0,255)],
                      pickable = True
                      )
    layer_list.append(layer)

#tool styling
tool_tip = {"html" : "Incident: <br/> <b>{OFFENSE_DESCRIPTION}</b>",
            "style": {"backgroundColor": "blue",
                      "color": "white"}
            }
#default view of map
view_state = pdk.ViewState(
    latitude=df_bos["lat"].mean(),
    longitude= df_bos["lon"].mean(),
    zoom= 11,
    pitch=0
)
#organizing the district list
district_list.insert(0,"")
district_list.insert(-1,"All")
district_list.remove('External')
district_list.pop(-1)
selected_district = st.sidebar.selectbox("Please select a district", district_list)

#selection of districts
for i in range(len(district_list)):
    if selected_district == district_list[i]:
        # if user selects all, theres a specific layer with all points
        if i == len(district_list)-1:
            map = pdk.Deck(
                map_style='mapbox://styles/mapbox/outdoors-v11',
                initial_view_state=view_state,
                layers=layer_list,
                tooltip= tool_tip
                )
        #rest of district selections
        else:
            map = pdk.Deck(
                map_style='mapbox://styles/mapbox/outdoors-v11',
                initial_view_state=view_state,
                layers=[layer_list[i-1]],
                tooltip= tool_tip
                )
        #displaying map
        st.pydeck_chart(map)
st.text("Map of Boston")

#Creating sub dataframe counting district incident reports
df_count = df_bos['DISTRICT'].value_counts()
df_count=df_count.drop('External')
#bar chart for crime per district
st.bar_chart(df_count)
st.text("Bar Chart for Crime Incident Reports Per District")

# iterating through list of dictionaries from read function
shootings=[]
for i in read_file(data):
# if the key shooting has a value of 1 that means there was a shooting
    if i["SHOOTING"] == '1':
        # appending these dictionaries to new list of shootings
        shootings.append(i)
#making Data frame
df_shootings = pd.DataFrame(shootings)
# sort by street in alphabetical order
df_shootings.sort_values(by =['STREET'], inplace = True)
st.write(df_shootings[['OFFENSE_DESCRIPTION', 'DISTRICT', 'STREET','OCCURRED_ON_DATE']])
st.text("Incidents where there was a shooting.")

#user questions to set up charts
st.sidebar.success("These questions will generate charts based on the selection of what data you would like to view.")
selected_data = st.sidebar.selectbox("Select Data you would like to view", ["", "Month of the report", "Day of the week of the report", "Hour of the day of the report"])
selected_chart = st.sidebar.selectbox("How would you like to view your data?", ["", "Bar Chart", "Pie Chart", "Line Chart"])

#function that takes in the data the user wants to see and what type of chart they want to see it in
def chart(data_choice, type_chart):
    #if statement for month and bar chart
    if data_choice == "Month of the report" and type_chart == "Bar Chart":
        incidents_by_month = df_bos.groupby(by = ["MONTH"]).size().reset_index(name='count')
        plt.bar(incidents_by_month["MONTH"], incidents_by_month['count'], width= 0.5, color = "green")
        plt.xlabel('Month')
        plt.ylabel('Number of Incidents')
        plt.title('Number of Crime Incidents by Month in Boston')
        st.pyplot(plt)
        st.text("Chart of Selected Data")
    #if statement for day and bar chart
    elif data_choice == "Day of the week of the report" and type_chart == "Bar Chart":
        incidents_by_day = df_bos.groupby(by = ["DAY_OF_WEEK"]).size().reset_index(name='count')
        plt.bar(incidents_by_day["DAY_OF_WEEK"], incidents_by_day['count'], width= 0.5, color = "green")
        plt.xlabel('Day')
        plt.ylabel('Number of Incidents')
        plt.title('Number of Crime Incidents by Day in Boston')
        st.pyplot(plt)
        st.text("Chart of Selected Data")
    #if statement for hour and bar chart
    elif data_choice == "Hour of the day of the report" and type_chart == "Bar Chart":
        incidents_by_hour = df_bos.groupby(by = ["HOUR"]).size().reset_index(name='count')
        plt.bar(incidents_by_hour["HOUR"], incidents_by_hour['count'], width= 0.5, color = "green")
        plt.xlabel('Hour')
        plt.ylabel('Number of Incidents')
        plt.title('Number of Crime Incidents by Hour in Boston')
        st.pyplot(plt)
        st.text("Chart of Selected Data")
    # if statement for month and line chart
    elif data_choice == "Month of the report" and type_chart == "Line Chart":
        incidents_by_month = df_bos.groupby(by = ['MONTH']).size().reset_index(name='count')
        plt.plot(incidents_by_month['MONTH'], incidents_by_month['count'])
        plt.xlabel('Month')
        plt.ylabel('Number of Incidents')
        plt.title('Trend in Crime Incidents in Boston')
        st.pyplot(plt)
        st.text("Chart of Selected Data")
    # if statement for day and line chart
    elif data_choice == "Day of the week of the report" and type_chart == "Line Chart":
        incidents_by_day = df_bos.groupby(by = ['DAY_OF_WEEK']).size().reset_index(name='count')
        plt.plot(incidents_by_day['DAY_OF_WEEK'], incidents_by_day['count'])
        plt.xlabel('Day')
        plt.ylabel('Number of Incidents')
        plt.title('Trend in Crime Incidents in a week in Boston')
        st.pyplot(plt)
        st.text("Chart of Selected Data")
    # if statement for hour and line chart
    elif data_choice == "Hour of the day of the report" and type_chart == "Line Chart":
        incidents_by_hour = df_bos.groupby(by = ['HOUR']).size().reset_index(name='count')
        plt.plot(incidents_by_hour['HOUR'], incidents_by_hour['count'])
        plt.xlabel('Hour')
        plt.ylabel('Number of Incidents')
        plt.title('Trend in Crime Incidents in a single day in Boston')
        st.pyplot(plt)
        st.text("Chart of Selected Data")
    # if statement for month and pie chart
    elif data_choice == "Month of the report" and type_chart == "Pie Chart":
        incidents_by_month = df_bos.groupby(by = ["MONTH"]).size().reset_index(name='count')
        plt.pie(incidents_by_month['count'], labels=incidents_by_month["MONTH"], autopct = "%.2f%%")
        plt.title('Proportion of Crime Incidents by Month in Boston')
        st.pyplot(plt)
        st.text("Chart of Selected Data")
    # if statement for day and pie chart
    elif data_choice == "Day of the week of the report" and type_chart == "Pie Chart":
        incidents_by_day = df_bos.groupby(by = ["DAY_OF_WEEK"]).size().reset_index(name='count')
        plt.pie(incidents_by_day['count'], labels=incidents_by_day["DAY_OF_WEEK"], autopct = "%.2f%%")
        plt.title('Proportion of Crime Incidents by Day of the week in Boston')
        st.pyplot(plt)
        st.text("Chart of Selected Data")
    #if statement for hour and pie chart
    elif data_choice == "Hour of the day of the report" and type_chart == "Pie Chart":
        incidents_by_hour = df_bos.groupby(by = ["HOUR"]).size().reset_index(name='count')
        plt.pie(incidents_by_hour['count'], labels=incidents_by_hour["HOUR"], autopct = "%.2f%%")
        plt.title('Proportion of Crime Incidents by Hour of the Day in Boston')
        st.pyplot(plt)
        st.text("Chart of Selected Data")


#displaying charts to main
chart(selected_data, selected_chart)

#askingn user if they want to display a pivot table counting number of incident reports per month
st.sidebar.success("The following will create a pivot table based on incident types.")
select_pivot = st.sidebar.selectbox("Would you like to see a pivot table that shows the number of incident reports per month?", ["", "Yes", "No"])
# if statement for yes input, creating pivot table with description and months as column counting incident number
if select_pivot == "Yes":
    incidents_by_type = df_bos.pivot_table(index='OFFENSE_DESCRIPTION', columns='MONTH', values='INCIDENT_NUMBER', aggfunc='count').fillna(0).astype(int)
    st.success("Count of each incident per month")
    st.write(incidents_by_type)



