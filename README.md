# Student Task & Progress Tracker

## Overview

The StudySmart is a full-stack web application built with Flask, HTML, and CSS.  
It helps students organize their study tasks, track progress, manage deadlines, and stay productive through a simple personal dashboard.

---

## Features

### User System
- User registration (signup)
- Secure login system using sessions
- Individual user accounts

### Task Management
- Create study tasks with:
  - Title
  - Description
  - Priority level (Low / Medium / High)
  - Start date and due date
- Mark tasks as completed
- Delete tasks when no longer needed

### Progress Tracking
- Personal dashboard for each user
- Overview of total tasks vs completed tasks
- Automatic progress calculation
- Daily tracking using current date

---

## Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS
- **Database:** SQLite (via SQLAlchemy ORM)
- **Other:** Flask sessions, Jinja2 templates

---

## Project Structure
app.py
templates/
index.html
login.html
signup.html
progress_log.html
static/
css/
study.db


---

## How It Works

1. Users create an account and log in
2. They add study tasks with deadlines and priorities
3. Tasks are stored and displayed in a personal dashboard
4. Users can mark tasks as completed or delete them
5. Progress is automatically calculated and shown visually

---

## Current Status

The project is currently under active development. Core functionality is complete and working, including authentication, task creation, and progress tracking.

---

## Future Features

- Study goals system (long-term academic targets)
- Study session tracking (time-based learning logs)
- Subject categorization system
- Improved dashboard UI with better analytics
- Notifications and reminders for deadlines
- Deployment to a live hosting platform

---

## Learning Purpose

This project was built to strengthen skills in:
- Flask web development
- Full-stack application structure
- User authentication systems
- CRUD operations (Create, Read, Update, Delete)
- Database integration using SQLAlchemy ORM

---

## Author

Built by a student developer as part of a learning journey in web development.

