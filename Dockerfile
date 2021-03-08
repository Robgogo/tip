FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV ENV local

RUN mkdir -p /app/scripts/
WORKDIR /app
ADD ./requirements.txt /app/requirements.txt

RUN pip install -U setuptools
# RUN pip install distribute==0.7.3
RUN pip install urllib3==1.21.1 --force-reinstall
RUN pip install -r /app/requirements.txt

RUN mkdir -p /app/static/
ADD ./manage.py /app/
ADD ./config/ /app/config/
ADD ./scripts/ /app/scripts/
ADD ./api/ /app/api/
ADD ./test_images /app/test_images
RUN chmod +x /app/scripts/runserver.sh

EXPOSE 8000
CMD ["/app/scripts/runserver.sh"]
