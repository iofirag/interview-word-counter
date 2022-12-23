FROM python:3.8-alpine

# ports
EXPOSE 5000

WORKDIR /app

# cache
COPY . .
RUN pip install -r requirements.txt

# run main
CMD [ "python", "main.py" ]