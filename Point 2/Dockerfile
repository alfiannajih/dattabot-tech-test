FROM eclipse-temurin:21-jre

WORKDIR /usr/src/metabase

# Default to 'latest' if not passed via --build-arg
ARG METABASE_VERSION=latest
RUN apt-get update && apt-get install -y curl && \
    curl -L https://downloads.metabase.com/${METABASE_VERSION}/metabase.jar -o metabase.jar && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV MB_PLUGINS_DIR=/home/plugins/
ADD https://github.com/MotherDuck-Open-Source/metabase_duckdb_driver/releases/download/0.2.12/duckdb.metabase-driver.jar /home/plugins/

RUN chmod 744 /home/plugins/duckdb.metabase-driver.jar

CMD ["java", "--add-opens", "java.base/java.nio=ALL-UNNAMED", "-jar", "metabase.jar"]