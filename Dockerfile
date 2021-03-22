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
ADD ./core/ /app/core/
ADD ./tip-ui2/ /app/tip-ui2/
ADD ./tip-robgogo.json /app/
ADD ./fixtures/ /app/fixtures/
ADD ./fixtures/department.json /app/fixtures/department.json
ADD ./fixtures/services.json /app/fixtures/services.json
RUN chmod +x /app/scripts/runserver.sh

EXPOSE 8000
CMD ["/app/scripts/runserver.sh"]
