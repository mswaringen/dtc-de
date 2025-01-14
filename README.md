# dtc-de
Data engineering course projects

Run locally
- requires docker and uv for dependencies
- more details on running Jupyter notebooks in VSCode with uv: https://docs.astral.sh/uv/guides/integration/jupyter/#using-jupyter-from-vs-code

..

## Docker commands

#### Build a new container in the current dir
docker build -t [repository:][tag] .
docker build -t myapp:v1 .

#### Create and start a new container
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13

docker run -it \
--network=pg-network \
-e DB_HOST=pg-database \
yellow-taxi-pipeline:v4

docker run -it \
  --network=pg-network \
  yellow-taxi-pipeline:v1

#### Start an existing container
docker start pg-database


## Download and unzipdata

wget -O data/yellow_tripdata_2021-01.csv.gz https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz

gzip -d data/yellow_tripdata_2021-01.csv.gz


### Docker Compose
docker compose up
##### runs the pipeline script in the container
docker compose run --rm data-loader python scripts/pipeline.py /app/data/yellow_tripdata_2021-01.csv