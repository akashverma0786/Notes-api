# Notes-api
This Django project implements a simple notes API where users can sign up, log in, create notes, share notes with other users, view note version history, and update notes.

## Features

- User Authentication: Users can sign up and log in to the app.
- Note Management: Authenticated users can create, view, and update their notes.
- Note Sharing: Authenticated users can share their notes with other users.
- Note Version History: Users can view the version history of their notes.
- Automated Testing: The project includes automated tests to ensure the functionality is working as expected.

## Installation

1. Clone the repository to your local machine:

  ```bash
  git clone https://github.com/akashverma0786/Notes-api.git
  cd notes-api
  ```


2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   # on MacOS
   source env/bin/activate
   # On Windows:
   env\Scripts\activate
   ```

   
4. Install dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

    
6. Apply migrations to set up the database:
   ```bash
   python manage.py migrate
   ```

   
8. Run the development server:
   ```bash
   python manage.py runserver
   ```

   
9. Access the application at 'http://localhost:8000'.


API Endpoints
- POST /signup/: Allows new users to sign up by providing their details.
- POST /login/: Authenticates users by their username and password.
- POST /notes/create/: Allows authenticated users to create a new note.
- GET /notes/<id>/: Retrieves a specific note by its ID.
- POST /notes/share/: Allows users to share a note with other users.
- PUT /notes/<id>/update/: Allows users to update a note they own.
- GET /notes/version-history/<id>/: Retrieves the version history of a specific note.

Automated Testing
The project includes automated tests to ensure the functionality works correctly. To run the tests, use the following command:
```bash
python manage.py test
```
## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

