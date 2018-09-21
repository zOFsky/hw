FROM alpine
RUN apk add python3-dev \
            gcc \
		    libc-dev \
		    linux-headers \
                    zlib \
                    zlib-dev \
                    jpeg \
                    jpeg-dev
RUN pip3 install --upgrade pip
RUN mkdir /data
WORKDIR /data
ADD requirements.txt /data
RUN pip3 install -r requirements.txt
ADD /happy_walker /data
CMD uwsgi happy_walker/uwsgi.ini
