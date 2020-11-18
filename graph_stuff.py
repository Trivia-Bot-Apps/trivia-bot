import plotly.graph_objects as go
import numpy as np
import redis

redisurl = input("Please enter the REDIS URL:")

triviadb = redis.from_url(redisurl)

Running = True

byte_list = triviadb.lrange("serverdata", 0, 10000000)

results = []

for count in byte_list:
    results.append(int(count.decode('utf-8')))

results.reverse()
y = results
x = np.arange(len(y))

fig = go.Figure(data=go.Scatter(x=x, y=y))

fig.update_layout(
    title="Trivia Bot Server Count",
    xaxis_title="Time",
    yaxis_title="Number of Servers",
    font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
)

fig.show()
