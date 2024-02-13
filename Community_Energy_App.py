import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import folium
from streamlit_folium import folium_static
import requests
import warnings

warnings.filterwarnings('ignore')

fp = r'Community_Buildings_Data.csv'
df = pd.read_csv(fp)




# set titles/icon/layout ----------------------------------
st.set_page_config(page_title="Community Energy App")

#set title -----------------------------------------------------------------------------------
st.title('Community Energy App')
#move title a little higher. uses div function to change padding (not working atm?)
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
#--------------------------------------------------------------------------------------------


# Introduction --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.header("Introduction")
st.write("This web app is designed as a support tool for the article released by SIB titled ______. It displays publically available data on the energy performance of non-domestic community buildings in England. Please see the article for further analysis on this data.")
st.write("It is critical to understand energy eficiency as we work towards meeting the law set in 2019 to reach Net Zero by 2050. To deliver on Net Zero there are likely to be incremental rule changes for Energy Performance Certificate (EPC) ratings. A ‘C’ rating is commonly suggested as the minimum required for sale or let in proposed legislation of domestic properties by 2035, whilst a minimum of ‘B’ has been suggested for renting non-domestic properties by 2030.")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# gloassary --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.header("Glossarry:")
st.write("- EPC (Energy Performance Certificate) - A certificate issued to a building by an accredited assessor, rating the buildings’ energy efficiency  from A+ (most efficient) to G (least efficient).")
st.write("- EPC Score - A score given from 0 - 150 to determine the EPC letter band of a building. For example; 0-25 = A. A score 0 or below (aka. A+) is given to any building that is net zero. Please note, it is possible to be given a score outide the 0-150 range if your building is an outlier in some way, but this does apply to the majority of buildings.")
st.write("- IMD (Index of Multiple Deprivation) - a measure of relative deprivation (published by the Ministry of Housing, Communities & Local Government) ranked from 1 (most deprived) to 10 (least deprived).")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Sidebar with search functionality --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Checkbox for filtering or displaying the entire dataset
st.sidebar.header('Search your Local Authority')

# Checkbox for filtering or displaying the entire dataset
filter_option = st.sidebar.checkbox('Filter Data')

if filter_option:
    # Selectbox for Local Authority
    selected_local_authority = st.sidebar.selectbox('Type or select Local Authority', df['Local Authority'].unique())

    # Filter DataFrame based on selected Local Authority
    filtered_df = df[df['Local Authority'] == selected_local_authority]
    
    if filtered_df.empty:
        st.sidebar.error(f"Whoops: '{selected_local_authority}' doesn't exist in the dataset.")
else:
    # If not filtering, display the entire dataset
    filtered_df = df
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




# Main content
st.title('Grouping and Searching DataFrame')

# Display the selected or searched Local Authority --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if filter_option:
    if selected_local_authority:
        st.write(f'### Filtered DataFrame for "{selected_local_authority}":')
else:
    st.write(f'### Entire DataFrame:')
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# breakdown for LA --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
col1, col2 = st.columns((2))
st.header('EPC Breakdown')
with col1:
    mode_EPC = filtered_df["ASSET_RATING_BAND"].mode().iloc[0]
    count_EPC = filtered_df['BUILDING_REFERENCE_NUMBER'].count()
    st.write('Number of EPCs:', count_EPC)
    st.write('Most Common EPC:', mode_EPC)
with col2:
    imd_epc = filtered_df["IMD"].mean().round(0)
    st.write('Mean IMD:', imd_epc)
    floor_epc = filtered_df['FLOOR_AREA'].mean().round(1)
    st.write('Mean floor area (m2)', floor_epc)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Calculate percentage with one decimal place and create a bar chart for ASSET_RATING_BAND breakdown --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
epc_df = filtered_df.groupby(by=["ASSET_RATING_BAND"], as_index=False)["BUILDING_REFERENCE_NUMBER"].count()
epc_df['Percentage'] = (epc_df['BUILDING_REFERENCE_NUMBER'] / epc_df['BUILDING_REFERENCE_NUMBER'].sum() * 100).round(1)

fig = px.bar(epc_df, x="ASSET_RATING_BAND", y="Percentage", text="Percentage",
             labels={"Percentage": "Percentage of Total"},
             title="Percentage of EPCs by Rating Band")
fig.update_traces(texttemplate='%{text}%', textposition='outside')
st.plotly_chart(fig, use_container_width=True, height=200)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# Create a new DataFrame for the selected region --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
selected_region_df = df[df['Region'].isin(filtered_df['Region'].unique())]
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# show region data for selection # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.header("What does your region look like?")
your_region = filtered_df['Region'].unique()
st.text('Selected region: ' + str(your_region))
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# breakdown stats for region --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
col1, col2 = st.columns((2))
with col1:
    region_mode_EPC = selected_region_df["ASSET_RATING_BAND"].mode().iloc[0]
    region_count_EPC = selected_region_df['BUILDING_REFERENCE_NUMBER'].count()
    st.write('Number of EPCs:', region_count_EPC)
    st.write('Most Common EPC:', region_mode_EPC)
with col2:
    region_imd_epc = selected_region_df["IMD"].mean().round(0)
    st.write('Mean IMD:', region_imd_epc)
    region_floor_epc = selected_region_df['FLOOR_AREA'].mean().round(1)
    st.write('Mean floor area (m2)', region_floor_epc)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------






# visuals for region --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
region_df = selected_region_df.groupby(by=["ASSET_RATING_BAND"], as_index=False)["BUILDING_REFERENCE_NUMBER"].count()
region_df['Percentage'] = (region_df['BUILDING_REFERENCE_NUMBER'] / region_df['BUILDING_REFERENCE_NUMBER'].sum() * 100).round(1)

fig2 = px.bar(region_df, x="ASSET_RATING_BAND", y="Percentage", text="Percentage",
             labels={"Percentage": "Percentage of Total"},
             title="Percentage of EPCs by Rating Band in Selected Region")
fig2.update_traces(texttemplate='%{text}%', textposition='outside')
st.plotly_chart(fig2, use_container_width=True, height=200)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# make a table for LA breakdown ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
cross_table = pd.crosstab(filtered_df['Local Authority'], filtered_df['ASSET_RATING_BAND'])
# Display the table
st.header('Table: Region by Asset rating Band (EPC)')
st.write(cross_table)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# make a table for LA breakdown ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
cross_table2 = pd.crosstab(filtered_df['Local Authority'], filtered_df['IMD'])
# Display the table
st.header('Table: IMD by Asset rating Band (EPC)')
st.write(cross_table2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------









# Display the filtered DataFrame based on search ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with st.expander('View Data'):
    st.write(filtered_df)


# download filtered data 
with st.expander("Download Data"):
    # groups data by region. It is different to col1 because we defined category_df earlier on 
    #st.write(filtered_df.style.background_gradient(cmap="Oranges"))
    csv = filtered_df.to_csv(index = False).encode('utf-8')
    st.download_button("Click Here", data = csv, file_name = "Data.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    

with st.expander("See relevant links (including to public datasets)"):
    st.write("IMD Data: " + " https://www.gov.uk/government/collections/english-indices-of-deprivation")
    st.write("EPC Data: " + " https://epc.opendatacommunities.org/")
    st.write("EPC related energy bill in parliament: " + " https://bills.parliament.uk/bills/3036 ")
