import streamlit
import requests
import pandas
import snowflake.connector
from urllib.error import URLError
streamlit.title("My Mom's new healthy Diner")
streamlit.header('Breakfast favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit') #make fruit names as the index#
# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Cantaloupe','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)
## structuring with if else nested
streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
        streamlit.error("Please select a fruit of your choice")
   else:   
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
      # write your own comment -what does the next line do? 
       fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
       streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()
#streamlit.write('The user entered ', fruit_choice)


#import requests

##streamlit.text(fruityvice_response.json())



# import pandas


## Organising , dont run anyting past this
streamlit.stop()

# import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_row)
streamlit.text("what fruit would you like to add?")
add_my_fruit = streamlit.text_input('What fruit would you like information about?','papaya')
#streamlit.write(fruit_choice)
my_cur.execute("insert into fruit_load_list values ('papaya')")
streamlit.text("Thank you for adding")

my_cur.execute("insert into fruit_load_list values ('from streamlit')");





