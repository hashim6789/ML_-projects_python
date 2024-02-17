import streamlit as st
import pandas as pd
import pickle

# Define the list of teams and their numerical values
team_mapping = {
    'Select Any Team': 0,
    'Gujarat Titans': 12, 'Rajasthan Royals': 1, 'Lucknow Super Giants': 2,
    'Punjab Kings': 3, 'Mumbai Indians': 4, 'Royal Challengers Bangalore': 5,
    'Kolkata Knight Riders': 6, 'Sunrisers Hyderabad': 7, 'Delhi Capitals': 8,
    'Chennai Super Kings': 9, 'Pune Warriors': 10, 'Kochi Tuskers Kerala': 11
}

# Load the trained Random Forest model
with open('random_forest_model.sav', 'rb') as file:
    model = pickle.load(file)

# Function to predict match outcome
def predict_match_outcome(data):
    prediction = model.predict(data)
    return prediction

# Function to generate user report
def user_report(team_mapping):
    batting_team = st.sidebar.selectbox('Batting Team', list(team_mapping.keys()), index=0)
    bowling_team = st.sidebar.selectbox('Bowling Team', list(team_mapping.keys()), index=0)
    runs_left = st.sidebar.slider('Runs Left', 0, 200, 0)
    balls_left = st.sidebar.slider('Balls Left', 0, 300, 0)
    wickets_remaining = st.sidebar.slider('Wickets Remaining', 0, 10, 0)
    total_run_x = st.sidebar.slider('Total Run X', 0, 300, 0)

    batting_team_value = team_mapping.get(batting_team)
    bowling_team_value = team_mapping.get(bowling_team)

    user_report_data = {
        'Batting Team': [batting_team_value],
        'Bowling Team': [bowling_team_value],
        'Runs Left': [runs_left],
        'Balls Left': [balls_left],
        'Wickets Remaining': [wickets_remaining],
        'Total Run X': [total_run_x]
    }
    return user_report_data

# Streamlit App
def main():
    st.title("Cricket Match Outcome Predictor")

    # Generate user report
    user_data = user_report(team_mapping)

    # Validation check: Ensure batting and bowling teams are not the same
    if user_data['Batting Team'][0] == 0 or user_data['Bowling Team'][0] == 0 or user_data['Batting Team'][0] == user_data['Bowling Team'][0]:
        st.error("Batting and bowling teams cannot be the same. Please select different teams.")
    else:
        # Display input features table
        st.subheader("Input Features")
        input_df = pd.DataFrame(user_data)
        st.table(input_df)

        # Prediction button
        if st.button("Predict"):
            # Prepare input data
            input_data = [[user_data['Batting Team'][0], user_data['Bowling Team'][0], user_data['Runs Left'][0],
                           user_data['Balls Left'][0], user_data['Wickets Remaining'][0], user_data['Total Run X'][0]]]

            # Make prediction
            prediction = predict_match_outcome(input_data)

            # Display prediction
            if prediction == 1:
                st.success("The batting team is predicted to win!")
            else:
                st.error("The batting team is not predicted to win.")

if __name__ == "__main__":
    main()
