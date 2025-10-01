# BMG Backend (Flask) project

## About the Project

This is the Flask backend side of the BMG project. For further information on the whole project see the [main readme](https://github.com/mecsbalint/boci-minesweeper-game/blob/main/README.md)

### Set up manually
#### Prerequisites

* **PostgreSQL** [Download](https://www.postgresql.org/download/)
* **Redis** [Download](https://redis.io/downloads/)


#### Download

You can download the application here: [BMG Backend (Flask) GitHub page](https://github.com/mecsbalint/boci-minesweeper-game-backend-python). Click on the Code button and choose the Download ZIP option. After downloading unzip it.
Or alternatively clone the repository: ```git clone https://github.com/mecsbalint/boci-minesweeper-game-backend-python```


#### Installation

1. **Rename `.env.example` to `.env`**

2. **Set up PostgreSQL Database**
    1. Create a database dedicated to this application ([step-by-step guide](https://www.postgresql.org/docs/current/tutorial-createdb.html))
    2. Replace the `SQLALCHEMY_DATABASE_URI` variable in `.env` with your PostgreSQL database connection string

3. **Set up Redis**
    1. Install redis ([step-by-step guides](https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/))
    2. Optionally replace the `REDIS_URL` in `.env` if you don't want to use the locally run redis server
    3. Optionall replace the `CACHE_DEFAULT_TIMEOUT`in `.env` to set how long it should store the caching data (by default it's 300 seconds)

4. **Install dependencies and set up Flask or python-socketio related variables**
    1. Open the terminal and navigate to the root directory
    2. Run the `pip install -r requirements.txt` command (install dependencies)
    3. Fill up the `JWT_SECRET_KEY` variable in `.env`
    4. Optionally change the `FRONTEND_URI` variable in `.env` (it doesn't necessary if you start this frontend server on the same device: [BMG Frontend (React) GitHub page](https://github.com/mecsbalint/boci-minesweeper-game-frontend-React))


#### Run

1. Run the `python run.py` command (run the backend application)

## Contact

mecsbalint@gmail.com - https://github.com/mecsbalint
