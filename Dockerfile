FROM python:3.9
RUN python -m pip install --upgrade pip
RUN pip install pandas pyarrow fastparquet psycopg2 sqlalchemy

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]
