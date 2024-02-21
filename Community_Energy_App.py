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
st.set_page_config(page_title="Community Energy App", page_icon=':globe_with_meridians:', layout = 'wide')

#set title -----------------------------------------------------------------------------------
st.title('Analyse the energy performance of community buildings in the UK!s')
#move title a little higher. uses div function to change padding (not working atm?)
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
#--------------------------------------------------------------------------------------------

st.header("What can you use this for?")
st.write("What is this used for? This web application allows you to search for your local authority and see the energy performance (as indicated by the EPC rating) of the community buildings in that area, as well as some other data such as the relative deprivation of the area (indicated by IMD). For a glossary of terms please see the glossary in the sidebar.")

# Introduction --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.header("Have you read our article on community EPCs?")
st.write("This web app is designed to interactively display the analysis from the article released by Social Investment Business titled ______. It displays publically available data on the energy performance of non-domestic community buildings in England. If you want to see more detailed analysis on this topic please find our article at _____________.")
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# about the cause --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.header("Why is this important?")
st.write("We believe it is critical to understand energy eficiency as we work towards meeting the law set in 2019 to reach Net Zero by 2050. To deliver on Net Zero there are likely to be incremental rule changes for Energy Performance Certificate (EPC) ratings. A ‘C’ rating is commonly suggested as the minimum required for sale or let in proposed legislation of domestic properties by 2035, whilst a minimum of ‘B’ has been suggested for renting non-domestic properties by 2030.")

st.header("Why Community Buildings?")
st.write("Community buildings are at the centre of local communities and improving their energy efficiency ensures the future viability of these hubs. With many of them lacking the financila backing enjoyed by other enterprises it is crucial that we do not allow these organisations to be left behind. This data not only shows that help is sorely needed, but where to direct our attention, in order to reach the most struggling.")

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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


# glossary --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.sidebar.header("Glossary:")
st.sidebar.write("- EPC (Energy Performance Certificate) - A certificate issued to a building by an accredited assessor, rating the buildings’ energy efficiency  from A+ (most efficient) to G (least efficient).")
st.sidebar.write("- EPC Score - A score given from 0 - 150 to determine the EPC letter band of a building. For example; 0-25 = A. A score 0 or below (aka. A+) is given to any building that is net zero. Please note, it is possible to be given a score outide the 0-150 range if your building is an outlier in some way, but this does apply to the majority of buildings.")
st.sidebar.write("- IMD (Index of Multiple Deprivation) - a measure of relative deprivation (published by the Ministry of Housing, Communities & Local Government) ranked from 1 (most deprived) to 10 (least deprived).")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




# add image -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
col1, col2 = st.columns((2))
with col1:
    st.image('image.jpg', caption='Community')
with col2:
    st.image('image2.jpg', caption='Community')
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





st.write()
# Main content
st.title("Let's explore the data:")
st.write("**First, remember to select a local authority in the sidebar to the left. Or, if you want to view the whole dataset, leave it blank!**")
st.write("If you want to download the filtered data please use the 'Download Data' button at the bottom of the page. To download the whole dataset use the same buttom, but ensure all filters are turned off. If you wish to download any of the tables, you can do with the icon found in the top right of each table.")

# data for your Local Authority
st.header("Data on your Local Authority:")
st.write("You will find below a breakdown of the energy perfomance of your selected local authority, including general information such as the number of community buildings with EPCs, the average IMD of these buildings, as well as breakdowns of the EPCs in this area.")
# Display the selected or searched Local Authority --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if filter_option:
    if selected_local_authority:
        st.write(f'### Filtered Data for "{selected_local_authority}":')
else:
    st.write(f'### Entire DataFrame:')
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# breakdown for LA --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

col1, col2 = st.columns((2))
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
             title="Percentage of Total by Asset Rating Band (EPC)")
fig.update_traces(texttemplate='%{text}%', textposition='outside')
st.plotly_chart(fig, use_container_width=True, height=200)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# make a table for LA breakdown ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with col1:
    cross_table = pd.crosstab(filtered_df['Local Authority'], filtered_df['ASSET_RATING_BAND'])
    # Display the table
    st.write('**Table: EPC Breakdown**')
    st.write(cross_table)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# make a table for LA breakdown ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with col2:
    cross_table2 = pd.crosstab(filtered_df['Local Authority'], filtered_df['IMD'])
    # Display the table
    st.write('**Table: IMD Breakdown**')
    st.write(cross_table2)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------








# ======================================================================================================================================================================================













# Create a new DataFrame for the selected region --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
selected_region_df = df[df['Region'].isin(filtered_df['Region'].unique())]
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# show region data for selection # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.header("How do you compare to your region?")
st.write("You will find below the same data fields, but for the region of the Local Authority you selected. This can help you compare how one LA performs compared to the rest in its part of the country.")
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




# make a table for region breakdown ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with col1:
    cross_table = pd.crosstab(selected_region_df['Local Authority'], selected_region_df['ASSET_RATING_BAND'])
    # Display the table
    st.header('Table: EPC Breakdown')
    st.write(cross_table)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# make a table for region breakdown ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with col2:
    cross_table2 = pd.crosstab(selected_region_df['Local Authority'], selected_region_df['IMD'])
    # Display the table
    st.header('Table: IMD Breakdown')
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
    
with st.expander("See full methodology"):
    st.write("Utilising public access to national data, we took the 1.29 million non-domestic EPCs available to us in December of 2023, with an EPC registered before the 1st July 2023 (our dataset ranges from 24/12/2007 to 30/06/2023), we applied filtering to the listed ‘Property Type’ so that it included only those that are community related. Please note this data does not include every community building in England. Buildings are not obligated to get an EPC assessment if they are not planning to market that building, meaning a community organisation that has owned a building since before 2008 would not appear on the EPC register. We filtered our data to include only the most EPCs for each building, this is so we have as current a view of the state of the sector as we can. To increase our confidence that we were focussing on the social sector, we completed a manual check of a random sample of 301 organisations to check whether they are community-led or private. The sample shows a low proportion of private businesses and is sufficiently large a sample to conclude that there is a low prevalence throughout the dataset, whilst all other businesses have a clear social purpose. We then merged this data with the publicly accessible IMD data on postcode. Our resulting dataset has 13,187 community and day centre buildings, offering a comprehensive look at energy efficiency trends. Then to ensure this data is representative of the not-for-profit sector, we conducted a word search inspection in python which showed common buildings including Churches, community centres, nurseries, day centres, etc.")

with st.expander("See relevant links (including to public datasets)"):
    st.write("IMD Data: " + " https://www.gov.uk/government/collections/english-indices-of-deprivation")
    st.write("EPC Data: " + " https://epc.opendatacommunities.org/")
    st.write("EPC related energy bill in parliament: " + " https://bills.parliament.uk/bills/3036 ")

