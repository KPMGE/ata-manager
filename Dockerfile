FROM python:3.10

WORKDIR /ata-manager

COPY . .

RUN pip install -r documentation/requirements.txt

CMD ["python", "./src/main.py"] 
