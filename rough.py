import streamlit as st
import pandas as pd
import pickle

# Define the list of teams and their numerical values with relative file paths
team_mapping = {
    'Select Any Team': {'value': 0, 'logo': None},
    'Gujarat Titans': {'value': 12, 'logo': 'logos/gujarat.png'},
    'Rajasthan Royals': {'value': 1, 'logo': 'logos/rajasthan.png'},
    'Lucknow Super Giants': {'value': 2, 'logo': 'logos/lucknow.png'},
    'Punjab Kings': {'value': 3, 'logo': 'logos/punjab.png'},
    'Mumbai Indians': {'value': 4, 'logo': 'logos/mumbai.png'},
    'Royal Challengers Bangalore': {'value': 5, 'logo': 'logos/bangalore.png'},
    'Kolkata Knight Riders': {'value': 6, 'logo': 'logos/kolkata.png'},
    'Sunrisers Hyderabad': {'value': 7, 'logo': 'logos/hyderabad.png'},
    'Delhi Capitals': {'value': 8, 'logo': 'logos/delhi.png'},
    'Chennai Super Kings': {'value': 9, 'logo': 'logos/chennai.png'},
    'Pune Warriors': {'value': 10, 'logo': 'logos/pune.png'},
    'Kochi Tuskers Kerala': {'value': 11, 'logo': 'logos/kochi.png'}
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
    
    # Check if both batting and bowling teams are selected
    if batting_team != 'Select Any Team' and bowling_team != 'Select Any Team':
        # Check if batting and bowling teams are the same
        if batting_team == bowling_team:
            st.error("Batting and bowling teams cannot be the same. Please select different teams.")
            return None, None, None, None  # Return None to indicate an error
        
        batting_team_value = team_mapping[batting_team]['value']
        bowling_team_value = team_mapping[bowling_team]['value']

        batting_team_logo = team_mapping[batting_team]['logo']
        bowling_team_logo = team_mapping[bowling_team]['logo']

        return batting_team_value, bowling_team_value, batting_team_logo, bowling_team_logo
    else:
        return None, None, None, None

# Streamlit App
def main():
    st.title("Cricket Match Winning Prediction")

    st.image('logos/ipl.png', width=300) 

    # Generate user report
    batting_team_value, bowling_team_value, batting_team_logo, bowling_team_logo = user_report(team_mapping)

    # Validation check: Ensure both batting and bowling teams are selected
    if batting_team_value is not None and bowling_team_value is not None:
        col1,col2,col3 = st.columns(3)
        with col1:
            st.write("""<h3 style="text-align:center;">Batting Team</h3>""",unsafe_allow_html=True)
            st.image(batting_team_logo, width=100)

        with col3:
            st.write("""<h3 style="text-align:center;">Bowling Team</h3>""",unsafe_allow_html=True)
            st.image(bowling_team_logo, width=100)

        # Display input features table with logos
        st.subheader("Input Features")
        runs_left = st.sidebar.slider('Runs Left', 0, 200, 0)
        balls_left = st.sidebar.slider('Balls Left', 0, 120, 0)
        wickets_left = st.sidebar.slider('Wickets Left', 0, 10, 0)
        target = st.sidebar.slider('Target', 0, 300, 0)
        
        input_df = pd.DataFrame({
            'Runs Left': [runs_left],
            'Balls Left': [balls_left],
            'wickets_left': [wickets_left],
            'Target': [target]
        })
        st.table(input_df)

        # Prepare input data
        input_data = [[batting_team_value, bowling_team_value, runs_left, balls_left, wickets_left, target]]

        # Prediction button
        if st.button("Predict"):
            # Make prediction
            prediction = predict_match_outcome(input_data)

            col1,col2,col3 = st.columns(3)
            # Display prediction
            if prediction == 1:
                with col2:
                    st.write("""<h3 style="text-align:center;">Winning Team</h3>""",unsafe_allow_html=True)
                    st.image(batting_team_logo, width=100)           
            else:
                with col2:
                    st.write("""<h3 style="text-align:center;">Winner</h3>""",unsafe_allow_html=True)
                    st.image(bowling_team_logo, width=100)

if __name__ == "__main__":
    main()
