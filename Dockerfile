FROM python:3.11-slim-bullseye

RUN pip install pandas sqlalchemy psycopg2-binary

WORKDIR /app

# Copy the pipeline script
COPY WEEK-1/scripts/pipeline.py scripts/pipeline.py
COPY WEEK-1/scripts/pipeline-green.py scripts/pipeline-green.py

# Copy the CSV file, dont need to do this if mounting as a volume
# COPY data/yellow_tripdata_2021-01.csv data/yellow_tripdata_2021-01.csv


# remove entrypoint and use command instead so that it can be overriden by docker-compose.yml
# ENTRYPOINT [ "python", "scripts/pipeline.py", "yellow_tripdata_2021-01.csv" ]

# Use CMD instead to provide a default command that can be overridden
CMD ["/bin/bash"]