# FleetTrack

FleetTrack is an application focused on collection, storage and analytics of realtime data received from a fleet of vehicles. 
This application is intended to be used in car, truck and van rental companies. 
In real-world, there will be an embedded device in vehicles which will be connected to the internet and able to make REST API calls to the server.

There are four main components of this project:
1. Producer - A web server built in FastAPI which receives data and pushes them into Kafka topics.
2. Consumer - An infinitely running Python script which listens to messages in the Kafka topic. Each message is cleaned, formatted and validated. After all checks are passed, data is inserted into PostgreSQL database.
3. Metabase - An open-source data visualization tool used to create dashboard on our data. Widget are created as Questions, Questions are put together in dashboard tabs. 
4. Simulation script - A Python script to simulate pings received from vehicles. Leverages Python multiprocessing

## Dashboard

### Tab 1
![](./assets/dashboard_tab_1.png)

### Tab 2
![](./assets/dashboard_tab_2.png)

## Architecture

 <div style="text-align:center">
<img src="./assets/FleetTrack.png"  alt="Architecture"/>
</div>

## Tools used

- FastAPI (Python)
- PostgreSQL w/ SQLAlchemy and Alembic
- Kafka
- Metabase

## Setup

- Start Kafka, Zookeeper, PostgreSQL and Metabase on Docker
  - `cd src`
  - `docker-compose up -d --build`
- Setup Python environment for the project and install dependencies from requirements.txt
- Create .env in root of project, use .env.example as a reference
- Initialize alembic to handle db migrations
  - `alembic init alembic`
  - `alembic revision -m "<message>"`
  - `alembic migrate head`

## Run the project

- Run scripts in the following order:
  - producer.py
  - consumer.py
  - run.py
- Open metabase on [http://localhost:3000](http://localhost:3000), create your widgets and dashboards!