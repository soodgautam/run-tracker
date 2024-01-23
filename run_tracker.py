import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

# Title of the application
st.title('Half Marathon Training Tracker')

# Sidebar for user selection
user = st.sidebar.selectbox('Select Your Name', ['Gautam', 'Spiro'])  # Add more user names as needed

# Input form
with st.form(key='run_form'):
    date = st.date_input('Date of run')
    distance = st.number_input('Distance ran (in km)', min_value=0.0, format='%.2f')
    time_taken = st.text_input('Time taken HH:MM:SS')
    run_type = st.selectbox('Run Type', ['Easy', 'Tempo'])
    submit_button = st.form_submit_button(label='Submit')

# Placeholder for the dataframe display
data_placeholder = st.empty()

# Placeholder for any messages (like confirmation of data addition)
message_placeholder = st.empty()

# Function to load data
def load_data():
    try:
        return pd.read_csv('run_data.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['User', 'Date', 'Distance', 'Time', 'Type'])

# Function to save data
def save_data(df):
    df.to_csv('run_data.csv', index=False)

# Handling form submission
if submit_button:
    data = load_data()
    new_run = {'User': user, 'Date': date, 'Distance': distance, 'Time': time_taken, 'Type': run_type}
    data = data.append(new_run, ignore_index=True)
    save_data(data)
    message_placeholder.success('Run added successfully!')

# Display the data and the line chart
data = load_data()
user_data = data[data['User'] == user]
data_placeholder.write(user_data)

# Filter data
easy_runs = data[data['Type'] == 'Easy']
tempo_runs = data[data['Type'] == 'Tempo']

# Bar Chart for Easy Runs
easy_bar_chart = alt.Chart(easy_runs).mark_bar().encode(
    x='Distance:Q',
    y='Time:Q',
    tooltip=['Date', 'Distance', 'Time']
).properties(
    title='Easy Runs - Time vs. Distance'
)

# Bar Chart for Tempo Runs
tempo_bar_chart = alt.Chart(tempo_runs).mark_bar().encode(
    x='Distance:Q',
    y='Time:Q',
    tooltip=['Date', 'Distance', 'Time']
).properties(
    title='Tempo Runs - Time vs. Distance'
)

easy_runs['Run ID'] = range(1, len(easy_runs) + 1)
tempo_runs['Run ID'] = range(1, len(tempo_runs) + 1)


# Bar Chart for Easy Runs
easy_bar_chart = alt.Chart(easy_runs).mark_bar().encode(
    x=alt.X('Run ID:O', axis=alt.Axis(title='Run Identifier')),  # O indicates ordinal
    y='Time:Q',
    color='Distance:N',  # Optional: Color encode by Distance
    tooltip=['Date', 'Distance', 'Time']
).properties(
    title='Easy Runs - Time for Each Run'
)

# Bar Chart for Tempo Runs
tempo_bar_chart = alt.Chart(tempo_runs).mark_bar().encode(
    x=alt.X('Run ID:O', axis=alt.Axis(title='Run Identifier')),
    y='Time:Q',
    color='Distance:N',  # Optional: Color encode by Distance
    tooltip=['Date', 'Distance', 'Time']
).properties(
    title='Tempo Runs - Time for Each Run'
)

# Display the bar charts in Streamlit
st.altair_chart(easy_bar_chart, use_container_width=True)
st.altair_chart(tempo_bar_chart, use_container_width=True)
