### This is a basic Data Analysis project 
In this project i used olympics dataset to show case my skills 
##### Technologies

- python
- pandas
- plotly
- Streamlit


#### 1.Sidebar and User Input :
The script creates a sidebar which acts as the main control panel for the user.

Selection Boxes: Four selectbox widgets are placed in the sidebar, allowing the user to filter the data by:

- Year: A specific Olympic year or an overall view ("1896 - 2024").

- Country: A specific participating country.

- Sport: A specific Olympic sport.

- Athlete: A specific athlete's name.

- Mutual Exclusivity Logic: A clever function clear_other_selections is implemented.

- Purpose: This ensures that you can only analyze one category at a time.

- How it works: When you select an option from any selectbox (e.g., you pick the year '2012'), this function is triggered. It immediately clears the selections in the other three boxes (Country, Sport, and Athlete). This prevents confusion and ensures the dashboard shows a clear, focused analysis. This state management is handled by st.session_state.

#### 2.Core Logic: Dynamic Page Rendering 
The main part of the app is controlled by a simple but powerful if/elif/else block at the end of the script. This block checks which selectbox in the sidebar has a value and calls the corresponding function to build the main page content.

Is a Year selected?

If "1896 - 2024" is chosen, call load_overall().

If a specific year is chosen, call load_yearwise().

If not, is a Country selected?

If yes, call load_country().

If not, is a Sport selected?

If yes, call load_sport().

If not, is an Athlete selected?

If yes, call load_athlete().

If nothing is selected (default state):

Call load_overall() to show the main dashboard.

#### 3.Content Display Functions 
Each load_...() function is a self-contained module responsible for fetching the right data and displaying it.

##### a.load_overall()

- Displays: A high-level summary of all Summer Olympics.

- Key Metrics: Total editions, nations, sports, events, and athletes.

- Visuals: Line charts showing athlete and gender participation over time.

- Tables: Expandable tables for the overall medal tally by country and top athletes of all time.

- load_yearwise(option)

- Displays: A detailed analysis of a single Olympic year.

- Key Metrics: Statistics for that specific year (e.g., number of nations, athletes, events).

- Tables: A detailed medal tally for the selected year and a list of its top-performing athletes.

##### b.load_country(country)

- Displays: A deep dive into a single country's Olympic history.

- Key Metrics: Total athletes, editions participated, and medal breakdown

- Visuals: Line chart of the country's medal count over time, a pie chart of its top sports, and gender-wise analysis.

- Special Feature: A "Country vs. Country Rivalry" section to compare performance against another selected nation.

- load_sport(sport)

- Displays: An analysis of a specific sport.

- Key Metrics: Total events, participating nations, and number of male/female athletes.

- Visuals: Line charts showing the growth of events and participation over time.

- Tables: Shows the most dominant countries and top athletes in that sport.

##### c.load_athlete(name)

- Displays: A profile page for a single athlete.

- Key Metrics: Their country, sport, gender, total medals, and events participated in.

- Table: A list of all Olympic events the athlete participated in, along with the results.