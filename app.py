import pandas as pd
import streamlit as st
from datetime import date
from habit_tracker import HabitTracker


tracker = HabitTracker()

st.set_page_config(page_title="Habit Tracker", page_icon="✅", layout="wide")

st.title("✅ Habit Tracker")
st.write("A simple app to build and maintain positive habits.")

menu = st.sidebar.radio(
    "Choose an option",
    [
        "Home",
        "Add New Habit",
        "Log Completion",
        "View All Habits",
        "Streaks and Statistics",
        "Edit or Remove Habit",
    ],
)

if menu == "Home":


    st.subheader("About this app")
    st.write(
        "This app stores habits in `habits.csv` and completion logs in `logs.csv`. "
        "You can add habits, log completions, view streaks, and check your progress."
    )

elif menu == "Add New Habit":
    st.header("Add a New Habit")

    with st.form("add_habit_form"):
        name = st.text_input("Habit name", placeholder="Example: Drink water")
        frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])
        target_goal = st.number_input("Target goal", min_value=1, value=1)
        category = st.selectbox("Category", ["Health", "Productivity", "Learning", "Fitness", "Other"])
        start_date = st.date_input("Start date", value=date.today())
        #reminder_time = st.text_input("Reminder time", value="09:00")

        submitted = st.form_submit_button("Add Habit")

    if submitted:
        if name.strip() == "":
            st.error("Please enter a habit name.")
        else:
            new_habit = tracker.add_habit(name, frequency, target_goal, category, start_date,)
            st.success(f"Habit added: {new_habit['name']}")

elif menu == "Log Completion":
    st.header("Log Completion")

    habits = tracker.get_active_habits_for_today()

    if len(habits) == 0:
        st.warning("No active habits found. Add a habit first.")
    else:
        habit_options = {habit["name"]: habit["habit_id"] for habit in habits}
        selected_name = st.selectbox("Which habit did you complete?", list(habit_options.keys()))
        amount = st.number_input("Amount completed", min_value=1, value=1)
        note = st.text_input("Note", placeholder="Optional")

        if st.button("Log Completion"):
            tracker.log_completion(habit_options[selected_name], amount=amount, note=note)
            st.success(f"Completion logged for: {selected_name}")

elif menu == "View All Habits":
    st.header("All Habits")

    habits = tracker.get_all_habits()
    if len(habits) == 0:
        st.warning("No habits added yet.")
    else:
        st.dataframe(pd.DataFrame(habits), use_container_width=True)
        st.subheader("Calendar View")
        habit_options = {habit["name"]: habit["habit_id"] for habit in habits}
        selected_name = st.selectbox("Choose a habit", list(habit_options.keys()))
        calendar_rows = tracker.get_calendar_view(habit_options[selected_name], days=30)
        st.dataframe(pd.DataFrame(calendar_rows), use_container_width=True)

elif menu == "Streaks and Statistics":
    st.header("Streaks and Statistics")

    stats = tracker.get_statistics()
    if len(stats) == 0:
        st.warning("No statistics yet. Add and complete some habits first.")
    else:
        stats_df = pd.DataFrame(stats)
        st.dataframe(stats_df, use_container_width=True)


elif menu == "Edit or Remove Habit":
    st.header("Edit or Remove Habit")

    habits = tracker.get_all_habits()
    if len(habits) == 0:
        st.warning("No habits to edit or remove.")
    else:
        habit_options = {habit["name"]: habit["habit_id"] for habit in habits}
        selected_name = st.selectbox("Choose a habit", list(habit_options.keys()))
        selected_id = habit_options[selected_name]
        habit = tracker.find_habit(selected_id)

        st.subheader("Edit Habit")
        with st.form("edit_habit_form"):
            new_name = st.text_input("Habit name", value=habit["name"])
            new_frequency = st.selectbox(
                "Frequency",
                ["Daily", "Weekly", "Monthly"],
                index=["Daily", "Weekly", "Monthly"].index(habit["frequency"]),
            )
            new_target_goal = st.number_input("Target goal", min_value=1, value=int(habit["target_goal"]))
            new_category = st.text_input("Category", value=habit["category"])
            new_start_date = st.date_input("Start date", value=pd.to_datetime(habit["start_date"]).date())
           #new_reminder_time = st.text_input("Reminder time", value=habit["reminder_time"])
            update_button = st.form_submit_button("Update Habit")

        if update_button:
            tracker.update_habit(
                selected_id,
                name=new_name,
                frequency=new_frequency,
                target_goal=new_target_goal,
                category=new_category,
                start_date=new_start_date,
                #sreminder_time=new_reminder_time,
            )
            st.success("Habit updated successfully.")

        st.subheader("Remove Habit")
        confirm_delete = st.checkbox("I understand this will remove the habit and its logs.")
        if st.button("Delete Habit"):
            if confirm_delete:
                tracker.remove_habit(selected_id)
                st.success("Habit deleted successfully. Refresh the page to update the list.")
            else:
                st.error("Please tick the confirmation checkbox first.")
