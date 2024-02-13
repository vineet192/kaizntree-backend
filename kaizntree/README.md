# Steps to run
- clone the repository
- install the dependencies with `pip install -r requirements.txt`
- run `python3 manage.py makemigrations kaizntree` and `python3 manage.py migrate`
- run the server with `python3 manage.py runserver`
- The server should be running and listengin on http://localhost:8000

# Steps to run (Docker)
- clone the repository
- run `docker build -t kaizntree_vineet .` to build the docker image
- run `docker run -t kaizntree_vineet -p 8000:8000` to run the docker image
- The server should be running and listengin on http://localhost:8000

# API Reference
The API documentation can be found [here](https://app.swaggerhub.com/apis/VKALGHATGI192_1/calander-ai/1.0.0)