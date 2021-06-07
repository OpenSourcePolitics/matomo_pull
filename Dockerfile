FROM python:3.7-slim-stretch
ENV PYTHONUNBUFFERED 1
WORKDIR /workdir
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8080
ENV PORT 8080
CMD python app.py
