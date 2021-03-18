# Luizalabs

API Rest de Produtos (Marketing)

### Arquitetura da Aplicação

1. Toda a aplicação foi desenvolvida em Python utilizando o microframework Flask.
2. Foi criada uma estrutura redundante (2 APIs - Considerando um cenário de alta disponibilidade) utilizando o NGINX como Load Balancer (Na regra padrão de balanceamento utilizando o algoritmo Round Robin).
3. Deploy da API utilizando o Gunicorn.
4. Banco de Dados: PostgreSQL 12.
5. Toda arquitetura foi desenvolvida utilizando Docker.
6. A API possui cache utilizando o Redis.
7. Toda a aplicação está coberta por Testes Unitários.
8. No diretório doc-postman, há uma collection do Postman para testes.

### Como executar a aplicação?

#### Build 
```
docker-compose build
```

#### Subir as aplicações
```
docker-compose up -d
```


### Sugestões de Melhorias
