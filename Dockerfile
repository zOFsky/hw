FROM python
RUN mkdir /data
WORKDIR /data
ADD requirements.txt /data
RUN pip3 install -r requirements.txt
ADD . /data
