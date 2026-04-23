# Python Individual Project - To-Do App

This is a complete CLI-based To-Do List application built in Python for the individual project.

## Implemented Features

- User registration and login
- Category management
- Add task
- View tasks with filters
- Edit task
- Delete task
- Mark task as completed
- JSON file storage
- Input validation

## Project Structure

- `main.py` - Main application code (CLI)
- `storage.json` - Persistent data for users and tasks
- `docs/SRS.md` - Software requirements specification
- `docs/FEATURES.md` - Feature list and implementation details
- `docs/PROJECT_TIMELINE.md` - Day-by-day completion mapping
- `docs/PROBLEMS_AND_SOLUTIONS.md` - Challenges and fixes
- `docs/SCREENSHOTS.md` - Screenshot section for submission

## How to Run

1. Open terminal in this project folder.
2. Run:

```bash
python3 main.py
```

## Demo Flow

1. Register a new user.
2. Login.
3. Add categories if needed.
4. Add tasks.
5. View tasks with status.
6. Edit/Delete/Complete tasks.
7. Logout.

## Notes

- Password is stored as SHA-256 hash in JSON.
- Data is separated by user.
- Date format is `YYYY-MM-DD`.
