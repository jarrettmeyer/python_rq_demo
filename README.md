# Python RQ Demo

## System Requirements

* There are four [Docker](https://www.docker.com/) containers for this application. You will need to have the [appropriate Docker desktop](https://www.docker.com/products/docker-desktop) for your system. The Docker binaries will need to be in your `PATH`, including the `docker-compose` function.
* This program was written using [Visual Studio Code](https://code.visualstudio.com/). While not required that you use this editor, it will make development easier.
* You will need a version of [Python >= 3.6](https://www.python.org/) on your host system. Both `python` and `pip` will need to be in your `PATH`.

## Running the Application

### Clone the Repository

```
git clone git@github.com:jarrettmeyer/python_rq_demo.git
cd python_rq_demo
```

### Install and Activate VirtualEnv

```
pip install virtualenv
virturalenv venv
```

The activation script will vary on your system. On Windows, the following command will activate the virtual environment.

```
.\venv\Scripts\activate
```

Your mileage may vary.

### Start the Application Containers

```
docker-compose build
docker-compose up -d
```

The `-d` flag will run the containers in the background. To the following command will show the logs for a given container.

```
docker-compose logs <service-name>
```

or

```
docker-compose logs --follow <service-name>
```

### Set a FLASK_APP Environment Variable

On Windows...

```ps1
$env:FLASK_APP = 'web.py'
```

### Set Up the Database

Run the database migrations. This will update the database schema, adding tables, sequences, indexes, etc. for the application. Migrations are managed with [Flask-Migrate](https://pypi.org/project/Flask-Migrate/).

```
flask db upgrade
```

### Open Your Browser

Finally, open your browser to [http://localhost](http://localhost/). You should now see the application up and running successfully.

### To Stop the Application

The `down` command will bring down all running containers.

```
docker-compose down
```

## Questions, Comment, etc.

Send questions to [jarrettmeyer at gmail dot com](mailto:jarrettmeyer@gmail.com).

Send bugs to [Github issuess](https://github.com/jarrettmeyer/python_rq_demo/issues).
