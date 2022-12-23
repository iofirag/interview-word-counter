FROM python:slim

WORKDIR /service

# copy files
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY main.py ./
COPY .env ./

# run main
CMD [ "python", "main.py" ]