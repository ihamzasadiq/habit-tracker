# ✅ Habit Tracker

A simple and beginner-friendly **Python + Streamlit** app for building better habits, logging completions, and tracking progress over time.

## 🚀 Overview

Habit Tracker helps users stay consistent with positive habits by making it easy to:

- Add habits
- Log completions
- View streaks
- Check progress
- Get simple reminders
- See habit statistics

The app stores data locally using CSV files, making it easy to understand and explain as a beginner Python project.

## 🎯 Problem Statement

People often start good habits but forget to track them. This app solves that by giving users a simple way to record habits, log progress, and stay motivated through streaks and rewards.

## ✨ Features

- ➕ Add new habits
- ✅ Log habit completions
- 📋 View all habits
- 🔥 Track current and best streaks
- 📊 View completion rates and statistics
- 🏆 Earn reward badges
- 📅 See a calendar-style completion view
- ⏰ Get mock habit reminders
- 🕒 Analyze best completion times
- 🔗 Get habit stacking suggestions
- 🗂️ Store data in CSV files

## 🧠 How It Works

The project has two main parts:

app.py = what the user sees
habit_tracker.py = how the app works

app.py creates the Streamlit interface with menus, forms, buttons, tables, and progress bars.

habit_tracker.py contains the HabitTracker class, which handles adding habits, logging completions, saving data, calculating streaks, and generating statistics.

## 🗂️ Data Storage

The app uses two CSV files:

habits.csv

Stores habit details such as:

Habit ID
Habit name
Frequency
Target goal
Category
Start date
Reminder time
Active status
logs.csv

Stores completion records such as:

Log ID
Habit ID
Completion timestamp
Amount completed
Note

The habit_id connects each completion log to the correct habit.

## ▶️ How to Run

Install the required packages:

pip install streamlit pandas

Run the app:

streamlit run app.py

Then open the local Streamlit link in your browser.

## This project demonstrates:

- Classes and objects
- Functions and methods
- Lists and dictionaries
- Loops and conditionals
- CSV reading and writing
- Date and time handling
- Basic statistics
- Streamlit app development
## 🌱 Future Improvements
- Add charts for progress
- Add real notifications
- Prevent duplicate habit names
- Add user login
- Store data in a database
- Add a requirements.txt file


## ✅ Conclusion

Habit Tracker is a simple but useful Python project that helps users stay consistent with positive habits. It combines a clean Streamlit interface with CSV storage and beginner-friendly Python logic.
