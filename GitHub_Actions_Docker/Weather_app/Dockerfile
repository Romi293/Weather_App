# start by pulling the python image
FROM python:3.10.12-alpine as builder

# copy the requirements file into the image
COPY ./requirements.txt /weather_app/requirements.txt

# copy every content from the local file to the image
COPY . /weather_app

# switch working directory
WORKDIR /weather_app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt



###############################################################


FROM python:3.10.12-alpine

WORKDIR /weather_app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/ /usr/local/lib/python3.10/

COPY . /weather_app

COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

EXPOSE 8000

CMD ["gunicorn","-b","0.0.0.0:8000", "wsgi:app"]

################################################################


