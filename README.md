# Django microservice for a personalised dashboard 


## For HLD refer architechure folder

## Cloning the repository 
To clone the repository using SSH, follow these steps:

1. Copy the SSH clone URL of your repository. You can find this on the repository's page on GitHub, and it looks like:

    ```bash
    git@github.com:your-username/PersonlisedParentDashboard.git
    ```

2. Open a terminal window.

3. Change to the directory where you want to clone the repository:

    ```bash
    cd /path/to/your/desired/directory
    ```

4. Run the following command to clone the repository:

    ```bash
    git clone git@github.com:your-username/PersonlisedParentDashboard.git
    ```

   Replace `your-username` with your GitHub username.

## Running the Server

To run the Django development server, follow these steps:

1. Ensure you have Python installed. 
2. Create and activate a virtual environment. It's recommended to use a virtual environment to isolate the project dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install project dependencies by running the following command in the project directory:

    ```bash
    pip install -r requirements.txt
    ```

4. Start the development server:

    ```bash
    python manage.py runserver
    ```

The development server should now be running at `http://127.0.0.1:8000/`.


# Technologies Used
 - Django
 - SQL

# Project requirements
Configurations can be provided in the env file of the project, ideally we need the following values:
SECRET_KEY=
DEBUG=
X_API_KEY=
MASTER_DB_ENGINE=
MASTER_DB_NAME=
MASTER_DB_USER=
MASTER_DB_PASSWORD=
MASTER_DB_HOST=
MASTER_DB_PORT=
SLAVE_DB_ENGINE=
SLAVE_DB_NAME=
SLAVE_DB_USER=
SLAVE_DB_PASSWORD=
SLAVE_DB_HOST=
SLAVE_DB_PORT=
