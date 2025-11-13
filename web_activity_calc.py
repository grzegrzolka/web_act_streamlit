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

# title of the app
st.subheader(':blue[Isotope activity calculator]')
st.markdown('###### :green[This application displays some data about choosen isotopes, calculate their activity and displays the activity decrease within a given time period.]')

path = Path(__file__).parent / "IA1_A2_TS_D_ActConcente.csv"
# dataframe loading
df = pd.read_csv('A1_A2_TS_D_ActConcent.csv', sep = ";", index_col = 0, names = ["Activity concentration for exempt material (kBq/kg)", 
                                                                                 "Activity limit for an exempt consignment (Bq)", "A1 [TBq]", "A2 [TBq]", 
                                                                                 "Transport Security Threshold [TBq]", "D-Value [TBq]", "Desintegration [Years]"])
df['A1 [TBq]'] = df['A1 [TBq]'].str.replace(',', '.')
df['A2 [TBq]'] = df['A2 [TBq]'].str.replace(',', '.')
df['Transport Security Threshold [TBq]'] = df['Transport Security Threshold [TBq]'].str.replace(',', '.')
df['D-Value [TBq]'] = df['D-Value [TBq]'].str.replace(',', '.')
df['Desintegration [Years]'] = df['Desintegration [Years]'].str.replace(',', '.')

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
    act_conc_limit = float(df.loc[isotope.isotope_name]["Activity concentration for exempt material (kBq/kg)"])
    exemption_act = float(df.loc[isotope.isotope_name]["Activity limit for an exempt consignment (Bq)"])
    #calculate activity
    halfLife = float(df.loc[isotope.isotope_name]["Desintegration [Years]"])
    calc_activity = round(isotope.activity * pow(math.e, -(math.log(2) * (elapsed_years / halfLife))),2)
    calc_3_year_activity = round(isotope.activity * pow(math.e, -(math.log(2) * (3 / halfLife))),2)
    data.append([isotope.isotope_name, act_conc_limit, exemption_act / 1000, halfLife, isotope.activity, calc_activity])
    
    #create plot
    activities_by_month = []
    for month in range(elapsed_months):
        time = month / 12 
        activities_by_month.append(round(isotope.activity * pow(math.e, - (math.log(2) * (time / halfLife) )),2))
    
    plt.plot(x, activities_by_month, label = isotope.isotope_name)

plt.ticklabel_format(style='plain')
plt.xlabel("Time (months)")
plt.ylabel("Activity")
plt.title("Activity of isotope in time")
plt.legend()  #add a legend
#plt.savefig('chart.png') #/Users/andy/Desktop/Programming/Python/JacekIsot/chart.png
st.pyplot(plt)

st.divider()  
selected_isotopes_df = pd.DataFrame(data, columns=['Isotope', 'Act concent for exempt material [kBq/kg]', 'Act limit for exempt mat [kBq]', 'Desintegration [Years]', 'Begining Activity', 'Calculated Activity'])
st.dataframe(selected_isotopes_df.T,  column_config= {"_index": st.column_config.Column("", width = "medium")})  #display dataframe with selected isotopes

st.divider() 
st.text("Made by: Andrzej Grzegrzółka")
st.markdown("contact: :blue[andrzej.grzegrzolka@zuop.gov.pl]" )