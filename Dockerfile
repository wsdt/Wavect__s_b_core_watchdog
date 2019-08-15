FROM python:3
MAINTAINER Kevin A. Riedl <kevin.riedl@wavect.io>

ADD ./requirements.txt /requirements.txt 
RUN pip install -r /requirements.txt
ADD ./main.py /main.py
CMD ["python", "./main.py"]