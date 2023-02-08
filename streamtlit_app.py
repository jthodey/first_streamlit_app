import streamlit ## contects to the streamlit app
import pandas ## enables data changes and visualized for table
import requests ## enables calls to apis 
import snowflake.connector ## establish the connection to snowflake. Note that the requirements doc is used to say we use python
from urllib.error import URLError

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

## create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

##new section to call and display fruitvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice =streamlit.text_input("What fruite would you like information about?")
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error

#dont run anything past this line while we troubleshoot
streamlit.stop

## query data from snowflake in our streamlit app
streamlit.header("The fruit load list contains:")
#snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from fruit_load_list")
      return my_cur.fetchall()
 
## add button to load the fruit 
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

#create input box for user to add in a new fruit
add_my_fruit =streamlit.text_input("What fruit would you liketo add?")
streamlit.write('thank you for adding', add_my_fruit)

# SQL query to add new data 
my_cur.execute("insert into fruit_load_list values ('from streamlit')");
