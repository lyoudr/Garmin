from cassandra.cluster import Cluster 
from cassandra.auth import PlainTextAuthProvider

from .config import (
    CASSANDRA_CONTACT_POINTS,
    CASSANDRA_KEYSPACE,
    CASSANDRA_PORT
)

# Create the keyspace and table
def run_migration():
    # Authentication provider for Cassandra
    auth_provider = PlainTextAuthProvider(
        username='cassandra',
        password='cassandra'
    )
    cluster = Cluster(
        [CASSANDRA_CONTACT_POINTS], 
        port=CASSANDRA_PORT,
        auth_provider=auth_provider,
    )
    session = cluster.connect()

    # Create keyspace if it doesn't exist
    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {CASSANDRA_KEYSPACE}
        WITH REPLICATION = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
    """)

    # Use the keyspace
    session.set_keyspace(CASSANDRA_KEYSPACE)

    # Create table if it doesn't exist
    session.execute("""
    CREATE TABLE IF NOT EXISTS billing_report (
        company TEXT PRIMARY KEY,
        total_cost DECIMAL,
        discounted_cost DECIMAL,
        tech_fee DECIMAL
    )
    """)

    print("Keyspace and table created successfully.")
    session.shutdown()