# Pokédex em Python

Um programa em Python desenvolvido para interagir com a PokeAPI, processar os dados utilizando Programação Orientada a Objetos e persistir as informações de forma segura em um banco de dados local com SQLite.

## Funcionalidades

- **Buscar e Salvar**: Consulta qualquer Pokémon na PokeAPI em tempo real, converte as unidades métricas corretamente e grava os dados no banco.
- **Consultar**: Lê o banco de dados SQLite para resgatar as informações de um Pokémon já registrado.
- **Deletar**: Remove registros específicos de um Pokémon do banco de dados de forma segura.
- **Menu Interativo**: Sistema rodando via terminal com interface de navegação contínua.

## Tecnologias Utilizadas

- **Python 3**
- **Biblioteca `requests`** (para consumo da API)
- **Biblioteca `sqlite3`** (para o banco de dados relacional local)
- **POO** (Programação Orientada a Objetos)