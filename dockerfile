FROM python:3.10.13

WORKDIR /RespiSense

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8888  

CMD ["waitress-serve", "--port=8888", "app:app"] 

