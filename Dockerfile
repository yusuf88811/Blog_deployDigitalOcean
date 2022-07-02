FROM python:3.10.5

RUN apt-get update \
    && apt-get install -yyq netcat

ADD . /code
WORKDIR /code
COPY requirements.txt ./code
COPY . .

RUN pip install --upgrade pip    
RUN pip install -r requirements.txt 


EXPOSE 8000


COPY entrypoint.sh /code
ENTRYPOINT [ "sh", "/code/entrypoint.sh" ] 

