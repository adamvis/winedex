# Use the official PostgreSQL image as a base image
FROM kartoza/postgis:9.6-2.4

# Install PostGIS extension
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgis\
        postgresql-postgis 

# Set environment variables
ENV POSTGRES_USER=winedex_user
ENV POSTGRES_PASSWORD=winedex_password
ENV POSTGRES_DB=winedex_db

COPY setup/* /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port
EXPOSE 5432
