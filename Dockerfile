FROM python:3.9

WORKDIR /app
COPY ingest_data.py ingest_data.py
COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN source venv\bin\activate
RUN python -m pip install --upgrade pip
RUN pip install pandas pyarrow fastparquet psycopg2 sqlalchemy

ENTRYPOINT [ "python", "ingest_data.py" ]
