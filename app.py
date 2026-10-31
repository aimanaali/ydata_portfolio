import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_ydata_profiling import st_profile_report
import seaborn as sns
import pandas as pd
# dataset
c = {0: 'anagrams', 1: 'anscombe', 2: 'attention', 3: 'brain_networks',
      4: 'car_crashes', 5: 'diamonds', 6: 'dots', 7: 'dowjones', 8: 'exercise', 
      9: 'flights', 10: 'fmri', 11: 'geyser', 12: 'glue', 13: 'healthexp', 14: 'iris',
        15: 'mpg', 16: 'penguins', 17: 'planets', 18: 'seaice', 19: 'taxis',
         20: 'tips', 21: 'titanic'}
st.header("Data AIMSAT set profile report")
# selectbox
selected_values=st.sidebar.selectbox('Select a dataset',list(c.values()))
uploaded_file=st.sidebar.file_uploader("Upload a CSV,XLsx file", type=["csv","xlsx "])
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        dataset = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        dataset = pd.read_excel(uploaded_file)

# st.siderbar.text_input("Enter a dataset name","Enter a dataset name")
# Display the selected value
st.write(f'You selected: {selected_values},{uploaded_file.name if uploaded_file is not None else "No file uploaded"}')


dataset=(sns.load_dataset(selected_values))


pr = ProfileReport(dataset, title="Report")
st_profile_report(pr)



