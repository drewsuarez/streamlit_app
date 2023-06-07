import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions", "Correlation Analysis"))

if web_apps == "Exploratory Data Analysis":

  uploaded_file = st.sidebar.file_uploader("Choose a file")

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="disabled")

    num_rows = df.shape[0]
    num_cols = df.shape[1]

    # Count of categorical, numerical, and boolean variables
    data_types = df.dtypes.astype(str).value_counts()
    num_categorical = data_types.get('object', 0)
    num_numerical = data_types.get('float64', 0) + data_types.get('int64', 0)
    num_bool = data_types.get('bool', 0)

    # Display the statistics
    st.write("Number of rows: {}".format(num_rows))
    st.write("Number of columns: {}".format(num_cols))
    st.write("Number of categorical variables: {}".format(num_categorical))
    st.write("Number of numerical variables: {}".format(num_numerical))
    st.write("Number of boolean variables: {}".format(num_bool))
    
    if show_df:
      st.write(df)

    column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical"))

    if column_type == "Numerical":
      numerical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)
      
      # five numer summary table
      summary = df[numerical_column].describe()

      summary_table = pd.DataFrame(summary).transpose()
      st.write(summary_table)

      # histogram
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05, value=1.0)

      hist_bins = st.slider('Number of bins', min_value=5,
                            max_value=150, value=30)
      hist_title = st.text_input('Set Title', 'Histogram')
      hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

      fig, ax = plt.subplots()
      ax.hist(df[numerical_column], bins=hist_bins,
              edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(hist_title)
      ax.set_xlabel(hist_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="plot.png",
            mime="image/png"
        )
    if column_type == "Categorical":
      categorical_column = st.sidebar.selectbox(
        'Select a Column', df.select_dtypes(include=['object']).columns)
      
      category_proportions = df[categorical_column].value_counts(normalize=True)

      # Create a table of proportions
      category_table = pd.DataFrame({'Category': category_proportions.index, 'Proportion': category_proportions.values})
      st.write(category_table)

      # bar plot
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
        'Color Opacity', min_value=0.0, max_value=1.0, step=0.05, value=1.0)

      bar_title = st.text_input('Set Title', 'Bar Plot')
      bar_xtitle = st.text_input('Set x-axis Title', categorical_column)

      fig, ax = plt.subplots()
      ax.bar(category_table['Category'], df[categorical_column].value_counts(), edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(bar_title)
      ax.set_xlabel(bar_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
          label="Download image",
          data=file,
          file_name="plot.png",
          mime="image/png"
        )
