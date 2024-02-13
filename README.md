# Steps to test api manually
- The backend is hosted on Google cloud run here: https://kaizntree-django-server-zlsyklqmba-ue.a.run.app
- An incomplete frontend that provides the auth token is hosted here: https://kaizntree-frontend.onrender.com/
- Go to the frontend and login with these test credentials: vkalghat@gmail.com, password
- Open the console log and you will find the auth token to copy on logging in
- Grab the token and paste it in the Authorization section in Postman or whichever client you use
- The format of the Auth header will be `Bearer <your-token>`
- Once that is done, you can run the APIs documented [here](https://app.swaggerhub.com/apis/VKALGHATGI192_1/calander-ai/1.0.0) on the backend url specified above

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