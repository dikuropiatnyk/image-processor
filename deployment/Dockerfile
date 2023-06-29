FROM python:3.9

LABEL maintainer="Danylo Kuropiatnyk <dikuropiatnyk@spscommerce.com>"

ARG APP_PATH=/app

# Install dependencies for OpenCV
RUN apt-get update && apt-get -y install libgl1

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Create APP folder:
RUN mkdir -p ${APP_PATH}

WORKDIR ${APP_PATH}

# Copy source code.
COPY ./api ${APP_PATH}/api
COPY ./config ${APP_PATH}/config
COPY ./core ${APP_PATH}/core
COPY ./models ${APP_PATH}/models
COPY ./providers ${APP_PATH}/providers
COPY ./utils ${APP_PATH}/utils
COPY ./main.py ${APP_PATH}/main.py

CMD ["/bin/bash", "-c", "uvicorn main:app --log-config config/log_conf.yml --host 0.0.0.0 --port 8000"]
