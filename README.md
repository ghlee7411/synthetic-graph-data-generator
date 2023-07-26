# synthetic-graph-data-generator
synthetic-graph-data-generator는 말 그대로 합성 그래프 데이터를 생성하는 프로그램입니다.
LLM을 이용하여 합성 그래프 데이터를 생성하고, 생성된 데이터를 Neo4j DB에 저장합니다. LLM은 학습 단계에서 수 많은 데이터들을 관측하였고
각 데이터 사이의 관계성을 학습하였기 때문에, 학습된 LLM을 이용하여 합성 그래프 데이터를 생성하면 양질의 합성 그래프 데이터를 얻을 수 있습니다.

## Neo4j
LLM으로 생성된 데이터를 저장할 Neo4j DB를 구축합니다.
### Install Neo4j via Docker
- [Neo4j docker hub](https://hub.docker.com/_/neo4j/)
```bash
docker pull neo4j
```
```bash
docker run \
--publish=7474:7474 --publish=7687:7687 \
--volume=$HOME/neo4j/data:/data \
neo4j
```