# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your smoothie
  """
)

# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Bananas", "Strawberries", "Peaches"),
# )

# st.write("You selected:", option)
name_on_order = st.text_input("Name on Smothie")
st.write("The name on your smothie will be", name_on_order)

#session = get_active_session()
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width=True)

pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()


Ingredents_list=st.multiselect('Choose upto 5 ingredents:',my_dataframe,max_selections=5 )
if Ingredents_list:
  ingredients_string=''
  for fruit_choosen in Ingredents_list:
    ingredients_string+=fruit_choosen+' '
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', fruit_choosen,' is ', search_on, '.')
    st.subheader(fruit_choosen+' Nutrition Information ')
    #smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
    #st_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

  my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) values ('""" + ingredients_string + """','""" + name_on_order + """')"""

#st.write(my_insert_stmt)
time_to_insert=st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")


