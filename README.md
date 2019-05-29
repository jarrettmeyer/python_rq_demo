# Python RQ Demo

## System Requirements

* There are four [Docker](https://www.docker.com/) containers for this application. You will need to have the [appropriate Docker desktop](https://www.docker.com/products/docker-desktop) for your system.
* This program was written using [Visual Studio Code](https://code.visualstudio.com/). While not required that you use this editor, it will make development easier.
* You will need a version of [Python >= 3.6](https://www.python.org/) on your host system.

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

### Set a FLASK_APP Environment Variable

On Windows...

```
$env:FLASK_APP = 'web.py'
```

### Set Up the Database

```
flask db upgrade
```

### Open Your Browser

Finally, open your browser to [http://localhost:5000](http://localhost:5000).

## Questions, Comment, etc.

Send questions to [jarrettmeyer at gmail dot com](mailto:jarrettmeyer@gmail.com).

Send bugs to [Github issuess](https://github.com/jarrettmeyer/python_rq_demo/issues).
