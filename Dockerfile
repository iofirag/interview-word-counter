FROM python:3.8-alpine

WORKDIR /app

# cache
COPY requirements.txt ./
RUN pip install -r requirements.txt
# copy files
COPY . ./

# ports
EXPOSE 3000

# run main
CMD [ "python", "main.py" ]