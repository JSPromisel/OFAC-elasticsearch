Usage:

1). From the root directory (where the docker-compose.yml file is located) run "docker-compose up -d --build"

2). Visit http://localhost:8080 to view and use the search interface*

3). Visit http://localhost:5601 to interact with a Kibana instance** setup for the Elasticsearch index

Notes:

* The search interface is based off of the work of Patrick Triest and his full text search app described here:
https://blog.patricktriest.com/text-search-docker-elasticsearch/

** To use the Kibana interface, you will have to specify the sdnentries index as the default index on your first visit