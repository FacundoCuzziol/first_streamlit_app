import streamlit
import pandas as pd
import requests
import snowflake.connector

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')



streamlit.title('My Moms New Healthy Dinner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#Picklist to choose the fruit to include
fruits_selected = streamlit.multiselect('Pick some fruits:',list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#Display the table on the page
streamlit.dataframe(fruits_to_show)
streamlit.header('Fruityvice Fruit Advice')
fruit_choice = streamlit.text_input('What fruit would you like information about?','kiwi')
streamlit.write(f'The user entered: {fruit_choice}')

fruityvice_response = requests.get(f'https://fruityvice.com/api/fruit/{fruit_choice}')
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#Output as a table
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list constains:")
streamlit.text(my_data_row)
