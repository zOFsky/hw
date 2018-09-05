FROM alpine
RUN apk add python3
RUN pip3 install --upgrade pip
RUN mkdir /data
WORKDIR /data
ADD requirements.txt /data
RUN pip3 install -r requirements.txt
ADD . /data
CMD python3 happy_walker/manage.py runserver 0.0.0.0:$PORT
