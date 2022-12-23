FROM python:3.10-alpine

# ports
EXPOSE 5000

WORKDIR /app

# cache
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# run main
CMD [ "python", "main.py" ]