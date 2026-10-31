# import streamlit as st
# from ydata_profiling import ProfileReport
# from streamlit_ydata_profiling import st_profile_report
# import seaborn as sns
# import pandas as pd
# # dataset
# c = {0: 'anagrams', 1: 'anscombe', 2: 'attention', 3: 'brain_networks',
#       4: 'car_crashes', 5: 'diamonds', 6: 'dots', 7: 'dowjones', 8: 'exercise', 
#       9: 'flights', 10: 'fmri', 11: 'geyser', 12: 'glue', 13: 'healthexp', 14: 'iris',
#         15: 'mpg', 16: 'penguins', 17: 'planets', 18: 'seaice', 19: 'taxis',
#          20: 'tips', 21: 'titanic'}
# st.header("Data AIMSAT talagang set profile report")
# # selectbox
# selected_values = st.sidebar.selectbox("Select a dataset", list(c.values()))
# uploaded_file = st.sidebar.file_uploader(
#     "Upload a CSV or XLSX file", type=["csv", "xlsx"]
# )

# if uploaded_file is not None:
#     if uploaded_file.name.lower().endswith(".csv"):
#         dataset = pd.read_csv(uploaded_file)
#     else:
#         dataset = pd.read_excel(uploaded_file)
# else:
#     dataset = sns.load_dataset(selected_values)

# st.subheader("Data preview")
# st.dataframe(dataset.head())

# pr = ProfileReport(dataset, title="Report")
# st_profile_report(pr)

import pandas as pd
import seaborn as sns
import streamlit as st
from streamlit_ydata_profiling import st_profile_report
from ydata_profiling import ProfileReport

# 1. App Title
st.header("Data AIMSAT Talagang Set Profile Report")

# 2. Sidebar: File Uploader
uploaded_file = st.sidebar.file_uploader(
    "Upload your own CSV or XLSX file", type=["csv", "xlsx"]
)

# 3. Sidebar: Dataset Selection (Only active if no file is uploaded)
c = {
    0: "anagrams",
    1: "anscombe",
    2: "attention",
    3: "brain_networks",
    4: "car_crashes",
    5: "diamonds",
    6: "dots",
    7: "dowjones",
    8: "exercise",
    9: "flights",
    10: "fmri",
    11: "geyser",
    12: "glue",
    13: "healthexp",
    14: "iris",
    15: "mpg",
    16: "penguins",
    17: "planets",
    18: "seaice",
    19: "taxis",
    20: "tips",
    21: "titanic",
}

# If a file is uploaded, we disable the selectbox to avoid confusion
is_file_uploaded = uploaded_file is not None
selected_values = st.sidebar.selectbox(
    "Or select a built-in dataset",
    list(c.values()),
    disabled=is_file_uploaded,
    help="Disabled while an uploaded file is active.",
)

# # 4. Load the Dataset based on user input
# if is_file_uploaded:
#     if uploaded_file.name.lower().endswith(".csv"):
#         dataset = pd.read_csv(uploaded_file)
#     else:
#         dataset = pd.read_excel(uploaded_file)
#     st.sidebar.success(f"Loaded uploaded file: {uploaded_file.name}")
# else:
#     dataset = sns.load_dataset(selected_values)
#     st.sidebar.info(f"Analyzing built-in dataset: {selected_values}")

# 4. Load the Dataset based on user input
if is_file_uploaded:
    try:
        # Check by file extension first
        if uploaded_file.name.lower().endswith(".csv"):
            dataset = pd.read_csv(uploaded_file)
        else:
            # Explicitly specifying engine can give clearer errors if openpyxl is missing
            dataset = pd.read_excel(uploaded_file, engine="openpyxl")
        st.sidebar.success(f"Loaded uploaded file: {uploaded_file.name}")
        
    except ImportError as e:
        st.error("⚠️ **Missing library:** This app requires `openpyxl` to read Excel files. Please add `openpyxl` to your requirements.txt file.")
        st.stop()
        
    except Exception as e:
        # Fallback layer: If Excel reader failed, try CSV fallback just in case the format was mislabeled
        st.sidebar.warning("Excel parsing failed. Attempting CSV fallback reading format...")
        try:
            uploaded_file.seek(0) # Reset file pointer back to start
            dataset = pd.read_csv(uploaded_file)
            st.sidebar.success(f"Loaded file as CSV text: {uploaded_file.name}")
        except Exception as fallback_error:
            st.error(f"Could not parse file structure. Original Error: {e}")
            st.stop()
else:
    dataset = sns.load_dataset(selected_values)
    st.sidebar.info(f"Analyzing built-in dataset: {selected_values}")


# 5. Display Data Preview & Profile Report
st.subheader("Data Preview")
st.dataframe(dataset.head())

st.subheader("Automated Data Analysis Report")
with st.spinner("Generating Profile Report... This may take a minute."):
    pr = ProfileReport(dataset, title="Data Profile Report", explorative=True)
    st_profile_report(pr)

