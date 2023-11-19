FROM python:3

WORKDIR /btc-dashboard

COPY . /btc-dashboard
RUN pip3 install -r requirements.txt
EXPOSE 8050
CMD [ "python3", "app.py"]

