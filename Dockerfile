FROM python:2.7-slim
RUN touch /requirements.installed && mkdir /app
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENV FLASK_APP=main.py

#ENTRYPOINT [ "python" ]
#CMD [ "main.py" ]