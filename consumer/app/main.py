from fastapi import FastAPI
from contextlib import asynccontextmanager
from cassandra.cluster import Cluster
from prometheus_fastapi_instrumentator import Instrumentator

from .migration import run_migration
from .routes import router 
from .config import (
    CASSANDRA_CONTACT_POINTS,
    CASSANDRA_PORT,
    CASSANDRA_KEYSPACE
)

# Initialize Cassandra DB
run_migration()

# Connect to Cassandra DB
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to Cassandra
    app.state.cassandra_cluster = Cluster([CASSANDRA_CONTACT_POINTS], port=CASSANDRA_PORT)
    app.state.cassandra_session = app.state.cassandra_cluster.connect(CASSANDRA_KEYSPACE)

    yield 
    
    # Close the Cassandra connection
    app.state.cassandra_session.shutdown()
    app.state.cassandra_cluster.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

# Initialize the instrumentator
instrumentator = Instrumentator()
# Register the instrumentator to the app
instrumentator.instrument(app).expose(app)