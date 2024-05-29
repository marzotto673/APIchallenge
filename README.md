
# API challenge

Usando Python + Flash + Yara + Docker
### Rodar com

```
docker compose up --build
```

A aplicação da API estará disponível em ```http://localhost:8000```

### Rotas disponíveis

#### GET /

Rota padrão do projeto

---

#### GET /rules
Retorna uma lista de rules

---

#### GET /rules/:id
Mostra dados de uma role cadastrada

---

#### POST /rules
Exemplo payload de uma rule que encontra 3 variações de uma sentença (case sensitive):

````rule helloworld_checker { strings: $hello_world = \"Hello World!\" $hello_world_lowercase = \"hello world\" $hello_world_uppercase = \"HELLO WORLD\" condition: any of them }````

---

#### POST /analyze/text
Exemplo payload rule detectada:

````{ "text": "Hello World!", "rules": [{ "rule_id": 1 }] }````

Exemplo payload rule não detectada:

````{ "text": "hello", "rules": [{ "rule_id": 1 }] }````
