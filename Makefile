up:
	docker compose -f ./spark/docker-compose.yaml up -d
	docker compose -f ./trino/docker-compose.yaml up -d
	docker compose -f ./data-source/docker-compose.yaml up -d
	docker compose -f ./data-lake/docker-compose.yaml up -d
	docker compose -f ./metastore/docker-compose.yaml up -d

down:
	docker compose -f ./metastore/docker-compose.yaml down
	docker compose -f ./data-lake/docker-compose.yaml down
	docker compose -f ./data-source/docker-compose.yaml down
	docker compose -f ./trino/docker-compose.yaml down
	docker compose -f ./spark/docker-compose.yaml down

.PHONY: up down