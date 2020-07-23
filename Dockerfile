FROM python:3.7.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && \
    apt-get install -y redis-server && \
    apt-get clean
   
ENV redisurl=redis://localhost/

EXPOSE 6379

CMD ["redis-server", "--protected-mode no"]

CMD [ "python", "./bot.py" ]
