# Problems Faced and Solutions

## 1. Problem: Data loss after closing the program

Solution: Implemented JSON read/write functions to persist users and tasks in `storage.json`.

## 2. Problem: Password security

Solution: Used SHA-256 hashing before storing passwords.

## 3. Problem: Invalid date formats

Solution: Added strict date validation using Python `datetime.strptime` with `YYYY-MM-DD` format.

## 4. Problem: Invalid task IDs

Solution: Added numeric input validation for task ID fields.

## 5. Problem: Category duplication

Solution: Prevented duplicate categories and reused existing categories when possible.

## 6. Problem: Keeping menu flow simple

Solution: Built a clear numbered CLI menu and separated each feature into dedicated methods.
