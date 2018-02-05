FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /source
WORKDIR /source
RUN pip install Django==1.11
ADD . /source/
EXPOSE 8000
CMD python3 manage.py runserver 0.0.0.0:8000