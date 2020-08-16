FROM python:3.8.5
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["employeers-server/webapp/app.py"]
