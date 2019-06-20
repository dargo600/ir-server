FROM python:3


COPY . /app
WORKDIR /app

RUN pip install  --no-cache-dir -r requirements.txt

CMD ["./start_rest_server.sh" ]
