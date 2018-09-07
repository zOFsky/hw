FROM alpine
RUN apk add python3-dev \
            gcc \
		    libc-dev \
		    linux-headers
RUN pip3 install --upgrade pip
RUN mkdir /data
WORKDIR /data
ADD requirements.txt /data
RUN pip3 install -r requirements.txt
ADD . /data
CMD uwsgi tesi.ini