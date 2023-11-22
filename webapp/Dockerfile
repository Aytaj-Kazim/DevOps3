FROM python:3.8-slim
#RUN apt-get update && apt-get install -y libmariadb-dev-compat && rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
    apt-get install -y gcc libmariadb-dev pkg-config default-mysql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip config set global.index-url https://pypi.org/simple
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install --default-timeout=100 Flask flask-mysqldb



EXPOSE 80

ENV NAME World

CMD ["python", "app.py"]

