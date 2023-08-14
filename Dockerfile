FROM python:3.10-alpine

COPY . /code
WORKDIR /code

RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 9001

ENTRYPOINT [ "python" ]

CMD ["app.py"]