
# import streamlit as st


# if 'my_lst' not in st.session_state:
#     st.session_state['my_lst'] = []

# def manager():
#     with st.expander("Example"):
#         #user_input = st.text_input("Enter a key")
#         user_input = st.selectbox(label="podaj izotop", options = ["pierwszy", "drugi", "trzeci"])
#         add_button = st.button("Add", key='add_button')
#         if add_button:
#             if len(user_input) > 0:
#                 st.session_state['my_lst'] += [user_input]
#                 st.write( st.session_state['my_lst'] )
#             else:
#                 st.warning("Enter text")


#manager()


import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import math
from pathlib import Path

class Isotopes_in_Waste:
    def __init__(self, isotope, activity):
        self.isotope_name = isotope
        self.activity = activity

st.markdown("###### :blue[author: ]Andrzej Grzegrzłka" )
st.markdown("###### :blue[contact: ]andrzej.grzegrzolka@zuop.gov.pl")

# title of the app
st.subheader('Isotope activity calculator')

path = Path(__file__).parent / "Isotope.csv"
# dataframe loading
df = pd.read_csv(path , sep = ";", index_col = 0, 
        names = ["Name", "ExemptionConcentr", "ExemptionActivity", "HalfLife"])
df.loc[df['HalfLife'] == "#N/D!", 'HalfLife'] = '0'
df['HalfLife'] = df['HalfLife'].str.replace(',', '.').astype(float)

# visualize dataframe
st.write(df)

# input dates
start_date = st.date_input("Enter beginng date:", min_value="1900-01-01", max_value="2300-01-01")
end_date = st.date_input("Enter end date:", min_value="1900-01-01", max_value="2300-01-01")
elapsed_years = round((end_date - start_date).days/365,2)
elapsed_months = int(elapsed_years*12)

st.divider()

isotopes_in_waste = {}

isotopes_names = df.index.to_list()
if 'isotopes' not in st.session_state:
    st.session_state['isotopes'] = []

def manager():
    isotope_name = st.selectbox(label="Enter isotope:", options = isotopes_names)
    activity = st.number_input("Enter activity:")
    add_button = st.button("Add isotope", key='add_button', type="primary")
    clear_button = st.button("Clear", key='clear', type="primary")
    selected_isotope_names = [isotope.isotope_name for isotope in st.session_state['isotopes']]
    if add_button:
        if activity > 0 and isotope_name not in selected_isotope_names:
            new_isotope = Isotopes_in_Waste(isotope_name, activity)
            isotopes_in_waste[isotope_name] = new_isotope
            st.session_state['isotopes'] += [new_isotope]
            selected_isotope_names.append(isotope_name)
        else:
            st.warning("Juz wybrales ten izotop")
        
    if clear_button:
        st.session_state['isotopes'] = []
        selected_isotope_names = [isotope.isotope_name for isotope in st.session_state['isotopes']]
        plt.clf()

st.markdown("###### :green[Start date:] {}".format(start_date))
st.markdown("###### :green[End date:] {}".format(end_date))
st.markdown("###### :blue[Elapsed years:] {}".format(elapsed_years))
st.markdown("###### :blue[Elapsed months:] {}".format(elapsed_months))

st.divider()

manager()

data = []

x = range(elapsed_months)
for isotope in st.session_state['isotopes']:
    #calculate activity
    halflife = float(df.loc[isotope.isotope_name]["HalfLife"])
    calc_activity = round(isotope.activity * pow(math.e, -(math.log(2) * (elapsed_years / halflife))),2)
    calc_3_year_activity = round(isotope.activity * pow(math.e, -(math.log(2) * (3 / halflife))),2)
    data.append([isotope.isotope_name, halflife, isotope.activity, calc_activity, calc_3_year_activity])
    
    #create plot
    activities_by_month = []
    for month in range(elapsed_months):
        time = month / 12 
        activities_by_month.append(round(isotope.activity * pow(math.e, - (math.log(2) * (time / halflife) )),2))
    
    plt.plot(x, activities_by_month, label = isotope.isotope_name)

# 
plt.ticklabel_format(style='plain')
plt.xlabel("Time (months)")
plt.ylabel("Activity")
plt.title("Activity of isotope in time")
plt.legend()  #add a legend
#plt.savefig('chart.png') #/Users/andy/Desktop/Programming/Python/JacekIsot/chart.png
st.pyplot(plt)

#print dataframe
#st.write("Data początkowa", start_date )
#st.write("Data końcowa", end_date )
#st.write("Elapsed years: ", round(elapsed_years,2))
#st.write("Elapsed months: ", elapsed_months)

st.divider()  

selected_isotopes_df = pd.DataFrame(data, columns=['Isotope', 'Halflife', 'Begining Act', 'Calculated Act', 'Act after 3 Years'])
st.write(selected_isotopes_df )

