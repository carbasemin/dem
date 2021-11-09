FROM python:3.10-alpine
RUN apk update && apk upgrade \
&& pip install pyYaml docker six
WORKDIR /app
COPY /app/* /app/
CMD python main.py
