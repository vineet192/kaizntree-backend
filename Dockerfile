FROM python:3-alpine3.19

WORKDIR /app

COPY . .

RUN pip3 install -r /app/requirements.txt

RUN python3 /app/manage.py makemigrations kaizntree
RUN python3 /app/manage.py migrate
RUN python3 /app/manage.py syncdb

EXPOSE 8000

CMD ["python3", "/app/manage.py", "runserver", "0.0.0.0:8000"]