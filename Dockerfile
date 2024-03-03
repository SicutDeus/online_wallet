FROM python:3.10

RUN apt-get update

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code
WORKDIR /code
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]