FROM python:3.2
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install nltk
RUN pip install python-dotenv
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD ["manage.py", "runserver"]
