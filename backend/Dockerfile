FROM python:3.8
COPY ./ /backend
RUN pip install -r /backend/requirements.txt
WORKDIR /backend
RUN ["chmod", "+x", "./docker-entrypoint.sh"]
ENTRYPOINT "./docker-entrypoint.sh"