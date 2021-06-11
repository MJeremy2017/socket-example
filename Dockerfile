FROM python:3.7-slim

ENV APP_DIR /app

RUN mkdir -p ${APP_DIR}

WORKDIR ${APP_DIR}

ADD ./requirements.txt ${APP_DIR}
ADD ./examples ${APP_DIR}/examples

RUN pip install -r requirements.txt

CMD ["python", "./examples/chatroom/server.py"]