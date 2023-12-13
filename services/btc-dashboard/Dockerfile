FROM python:3

WORKDIR /btc-dashboard

COPY . /btc-dashboard
RUN apt-get update && \
    apt-get upgrade --yes\
    pip3 install -r requirements.txt \
    python -m flake8 /btc-dashboard && \
    python -m isort /btc-dashboard --check && \
    python -m black /btc-dashboard --check --quiet && \
    python -m pylint /btc-dashboard --disable=C0114,C0116,R1705 && \
    python -m bandit -r /btc-dashboard --disable=-B101 --quiet

EXPOSE 8050
CMD [ "python3", "app.py"]

