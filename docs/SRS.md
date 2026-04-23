# Software Requirements Specification (SRS)

## 1. Project Title

Python CLI To-Do List Application

## 2. Objective

Develop a Python-based To-Do List system where users can manage daily tasks with authentication, categories, and task status tracking.

## 3. Functional Requirements

1. The system shall allow user registration.
2. The system shall allow user login.
3. The system shall allow users to add categories.
4. The system shall allow users to add tasks.
5. The system shall display tasks with status (`pending` / `completed`).
6. The system shall allow users to edit tasks.
7. The system shall allow users to delete tasks.
8. The system shall allow users to mark tasks as completed.
9. The system shall store and retrieve data from JSON storage.

## 4. Non-Functional Requirements

1. The app shall run in a terminal (CLI).
2. The app shall be easy to use through menu navigation.
3. Input validation shall prevent invalid task IDs and dates.
4. Data shall persist between program runs.

## 5. Data Design

### User Object

- username
- password_hash
- created_at
- categories

### Task Object

- id
- title
- description
- category
- due_date
- status
- created_at
- updated_at

## 6. Constraints

- Python standard library only.
- Single local JSON file (`storage.json`) for persistence.
