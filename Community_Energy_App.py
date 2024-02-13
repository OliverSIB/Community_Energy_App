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


# Sidebar with search functionality
st.sidebar.header('Search your Local Authority')

# Checkbox for filtering or displaying the entire dataset
filter_option = st.sidebar.checkbox('Filter Data')

if filter_option:
    # Text input for Local Authority search
    search_local_authority = st.sidebar.text_input('Type Local Authority', '')

    # Filter DataFrame based on searched Local Authority
    if search_local_authority:
        filtered_df = df[df['Local Authority'].str.contains(search_local_authority, case=False, na=False) | (df['Local Authority'].isna())]
    else:
        selected_local_authority = st.sidebar.selectbox('Select Local Authority', df['Local Authority'].unique())
        filtered_df = df[df['Local Authority'] == selected_local_authority]
else:
    # If not filtering, display the entire dataset
    filtered_df = df

# Main content
st.title('Grouping and Searching DataFrame')

# Display the selected or searched Local Authority
if filter_option:
    if search_local_authority:
        st.write(f'### Filtered DataFrame for "{search_local_authority}":')
    else:
        st.write(f'### Filtered DataFrame for "{selected_local_authority}":')
else:
    st.write(f'### Entire DataFrame:')


# breakdown
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

# Calculate percentage with one decimal place and create a bar chart for ASSET_RATING_BAND breakdown
epc_df = filtered_df.groupby(by=["ASSET_RATING_BAND"], as_index=False)["BUILDING_REFERENCE_NUMBER"].count()
epc_df['Percentage'] = (epc_df['BUILDING_REFERENCE_NUMBER'] / epc_df['BUILDING_REFERENCE_NUMBER'].sum() * 100).round(1)

fig = px.bar(epc_df, x="ASSET_RATING_BAND", y="Percentage", text="Percentage",
             labels={"Percentage": "Percentage of Total"},
             title="Percentage of EPCs by Rating Band")
fig.update_traces(texttemplate='%{text}%', textposition='outside')
st.plotly_chart(fig, use_container_width=True, height=200)

# Create a new DataFrame for the selected region
selected_region_df = df[df['Region'].isin(filtered_df['Region'].unique())]

# show region data for selection
st.header("What does your region look like?")
your_region = filtered_df['Region'].unique()
st.text('Selected region: ' + str(your_region))


# breakdown
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

# visuals
region_df = selected_region_df.groupby(by=["ASSET_RATING_BAND"], as_index=False)["BUILDING_REFERENCE_NUMBER"].count()
region_df['Percentage'] = (region_df['BUILDING_REFERENCE_NUMBER'] / region_df['BUILDING_REFERENCE_NUMBER'].sum() * 100).round(1)

fig2 = px.bar(region_df, x="ASSET_RATING_BAND", y="Percentage", text="Percentage",
             labels={"Percentage": "Percentage of Total"},
             title="Percentage of EPCs by Rating Band in Selected Region")
fig2.update_traces(texttemplate='%{text}%', textposition='outside')
st.plotly_chart(fig2, use_container_width=True, height=200)









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
    