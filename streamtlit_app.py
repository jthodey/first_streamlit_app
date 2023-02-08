import streamlit ## contects to the streamlit app
import pandas ## enables data changes and visualized for table
import requests ## enables calls to apis 

#Set up the text on the webapp
streamlit.title("My Mom's New Healthy Diner") 
streamlit.header('Breakfast Favorites') 
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal') 
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie') 
streamlit.text('🐔 Hard-Boiled Free-Range Egg') 
streamlit.text('🥑🍞 Avocado Toast') 
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import dataframe from the server as, pull from a csv
##import the data
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

##let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick Some Fruits:", list(my_fruit_list.index),["Avocado", "Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

##display the table on the page
streamlit.dataframe(fruits_to_show)

##new section to call and display fruitvice api response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice =streamlit.text_input("What fruite would you like information about?", "Kiwi")
streamlit.write('The user entered', fruit_choice)

##call the data from the api link
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

#take thejson file and normalize it to make it human readable
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

## establish the connection to snowflake. Note that the requirements doc is used to say we use python
import snowflake.connector

## query data from snowflake in our streamlit app
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)


