FROM alpine
RUN apk add python3
RUN pip install --upgrade pip
RUN mkdir /data
WORKDIR /data
ADD requirements.txt /data
RUN pip3 install -r requirements.txt
ADD . /data
