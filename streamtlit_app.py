import streamlit
import pandas

#Set up the text on the webapp
streamlit.title("My Mom's New Healthy Diner") 
streamlit.header('Breakfast Favorites') 
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal') 
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie') 
streamlit.text('🐔 Hard-Boiled Free-Range Egg') 
streamlit.text('🥑🍞 Avocado Toast') 
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import dataframe from se server
##import the data
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

##let's put a pick list here so they can pick the fruit they want to include
streamlit.multiselect("Pick Some Fruits:", list(my_fruit_list.index),["Avocado", "Strawberries"])

##display the table on the page
streamlit.dataframe(my_fruit_list)