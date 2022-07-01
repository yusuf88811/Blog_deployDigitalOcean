FROM python:3.10.5

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt 

EXPOSE 8000

COPY entrypoint.sh .
ENTRYPOINT ["sh",'./entrypoint.sh']