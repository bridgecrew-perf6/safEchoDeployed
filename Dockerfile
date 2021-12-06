FROM python:3.7.5-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install nltk
RUN pip install python-dotenv
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD ["manage.py", "runserver"]
