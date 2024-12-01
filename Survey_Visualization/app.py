import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# Connect to MySQL database and fetch data
@st.cache_data
def fetch_data():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="@Kevin2003",
        database="Survey"
    )
    query = "SELECT * FROM survey_data;"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

# Streamlit App
st.title("Survey Data Visualization")

# Fetch data
data = fetch_data()

# Slider for Year Range
years = st.slider("Select Year Range:", 
                  int(data['Year'].min()), 
                  int(data['Year'].max()), 
                  (int(data['Year'].min()), int(data['Year'].max())))
filtered_data = data[(data['Year'] >= years[0]) & (data['Year'] <= years[1])]

# Display filtered data table
st.subheader("Filtered Data")
st.dataframe(filtered_data)

# Dropdown to select column for analysis
columns = ["Overall"] + list(data.columns)  # Include "Overall" for combined column option
column = st.selectbox("Select Column for Analysis", columns)

# Chart rendering for "Overall Distribution"
if column == "Overall":
    st.subheader("Overall Distribution")
    
    # Dropdown to select chart type for overall distribution
    overall_chart_type = st.selectbox("Select Overall Chart Type", ["Pie", "Bar", "Column", "Line"])
    
    if overall_chart_type == "Pie":
        # Pie chart: Distribution of Tech Trends by Rating
        fig = px.pie(filtered_data, names="Tech_Trend", values="Rating", 
                     title="Overall Rating Distribution by Tech Trend")
    
    elif overall_chart_type == "Bar":
        # Bar chart: Aggregated Rating by Tech Trend
        aggregated_data = filtered_data.groupby("Tech_Trend")["Rating"].sum().reset_index()
        fig = px.bar(aggregated_data, x="Tech_Trend", y="Rating", 
                     title="Overall Rating by Tech Trend", labels={"Rating": "Total Rating"})
    
    elif overall_chart_type == "Column":
        # Column chart: Distribution of Ratings by Year
        fig = px.histogram(filtered_data, x="Year", y="Rating", 
                           title="Overall Rating Distribution by Year", 
                           labels={"Rating": "Total Rating"})
    
    elif overall_chart_type == "Line":
        # Line chart: Ratings over Years
        aggregated_data = filtered_data.groupby("Year")["Rating"].mean().reset_index()
        fig = px.line(aggregated_data, x="Year", y="Rating", 
                      title="Average Rating Over Years", labels={"Rating": "Average Rating"})

else:
    # Chart rendering for specific column
    chart_type = st.selectbox("Select Chart Type", ["Pie", "Bar", "Column", "Line"])
    
    if chart_type == "Pie":
        fig = px.pie(filtered_data, names=column, title=f"Pie Chart of {column}")
    elif chart_type == "Bar":
        fig = px.bar(filtered_data, x=column, y="Rating", title=f"Bar Chart of {column}")
    elif chart_type == "Column":
        fig = px.histogram(filtered_data, x=column, y="Rating", title=f"Column Chart of {column}")
    elif chart_type == "Line":
        fig = px.line(filtered_data, x="Year", y="Rating", title="Line Chart of Ratings Over Years")

# Display the chart
st.plotly_chart(fig)
