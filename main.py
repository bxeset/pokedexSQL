import os
import requests
import sqlite3

# garante que a tabela existe no banco
caminho_do_banco = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "pokedex.db"
)
conexao = sqlite3.connect(caminho_do_banco)
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokemons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        peso REAL,
        altura REAL,
        tipo TEXT,
        evolucoes TEXT
    )
""")
conexao.commit()
conexao.close()


# classe base pra organizar os dados dos pokemons
class Pokemon:

  def __init__(self, nome, peso, altura, tipo, evolucoes):
    self.nome = nome
    self.peso = peso
    self.altura = altura
    self.tipo = tipo
    self.evolucoes = evolucoes

  def __str__(self):
    return (
        f"Pokémon: {self.nome} | Tipo: {self.tipo} | Peso: {self.peso}kg |"
        f" Altura: {self.altura}m | Evoluções: {self.evolucoes}"
    )


# salvar as infos organizadas do pokemon no banco de dados
def salvar_pokemon_no_banco(pokemon):
  conexao = sqlite3.connect(caminho_do_banco)
  cursor = conexao.cursor()
  cursor.execute(
      """
        INSERT INTO pokemons (nome, peso, altura, tipo, evolucoes)
        VALUES (?, ?, ?, ?, ?)
    """,
      (
          pokemon.nome,
          pokemon.peso,
          pokemon.altura,
          pokemon.tipo,
          pokemon.evolucoes,
      ),
  )
  conexao.commit()
  conexao.close()


# aqui ele conecta de novo no banco de dados e usa o comando SELECT pra selecionar nome, peso, altura, tipo e evoluções da tabela pokemons
# onde nome tem que bater com o que foi digitado pelo usuário pra previnir problemas, depois, pega o primeiro resultado (fetchone)
# e salva na variavel resultado, fechando a conexao com o banco de dados em seguida


def consultar_pokemon_no_banco(nome_pokemon):
  conexao = sqlite3.connect(caminho_do_banco)
  cursor = conexao.cursor()
  cursor.execute(
      "SELECT nome, peso, altura, tipo, evolucoes FROM pokemons WHERE nome = ?",
      (nome_pokemon,),
  )
  resultado = cursor.fetchone()
  conexao.close()

  # depois, cria uma condição em que se houver resultado pra busca, ou seja, se aquele pokemon for gravado corretamente no banco de dados
  # ele exibe todas as informações corretamente. Do contrário, informa que não foi encontrado no banco de dados

  if resultado:
    print(
        f"\n dados vindos DIRETO DO BANCO DE DADOS: \nPokémon:"
        f" {resultado[0]} | Tipo(s): {resultado[3]} | Peso: {resultado[1]}kg |"
        f" Altura: {resultado[2]}m | Evoluções: {resultado[4]}"
    )
  else:
    print(f"O Pokémon '{nome_pokemon}' não foi encontrado no banco.")


def deletar_pokemon_do_banco(nome_pokemon):
  conexao = sqlite3.connect(caminho_do_banco)
  cursor = conexao.cursor()
  cursor.execute("DELETE FROM pokemons WHERE nome = ?", (nome_pokemon,))
  conexao.commit()
  conexao.close()
  print(f"\no Pokémon '{nome_pokemon}' foi removido do banco de dados.")


# função auxiliar para buscar a cadeia de evoluções na API através da URL da espécie
def obter_cadeia_evolucao(url_especie):
  try:
    resp_especie = requests.get(url_especie)
    if resp_especie.status_code != 200:
      return "Desconhecido"

    url_evo = resp_especie.json()["evolution_chain"]["url"]
    resp_evo = requests.get(url_evo)
    if resp_evo.status_code != 200:
      return "Desconhecido"

    data_evo = resp_evo.json()
    nomes = []

    def percorrer_cadeia(node):
      if node and "species" in node:
        nomes.append(node["species"]["name"].capitalize())
        for proximo in node.get("evolves_to", []):
          percorrer_cadeia(proximo)

    percorrer_cadeia(data_evo["chain"])
    return " -> ".join(nomes)
  except:
    return "Não disponível"


# buscar o pokémon escolhido na API, url possui uma f-string pra se tornar universal, mudando de acordo com a entrada do usuário
# requests.get pega as informações do pokémon. em seguida, rola um teste rápido pra ver se a consulta deu certo 
# (status code == 200), se sim, ele da sequencia com o processo de pegar as informações do pokémon e salvar em variáveis ↓↓↓


def buscar_e_salvar_pokemon(pokemon_escolhido):
  url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_escolhido}"
  resposta = requests.get(url)

  if resposta.status_code == 200:
    dados_pokemon = resposta.json()
    nome = dados_pokemon["name"].capitalize()
    peso = dados_pokemon["weight"] / 10
    altura = dados_pokemon["height"] / 10

    # extraindo os tipos do pokemon
    tipos = [t["type"]["name"].capitalize() for t in dados_pokemon["types"]]
    tipo_str = ", ".join(tipos)

    # buscando a cadeia de evoluções através da url da espécie
    url_especie = dados_pokemon["species"]["url"]
    evolucoes = obter_cadeia_evolucao(url_especie)

    # cria o objeto meu_pokemon, usando a classe criada lá em cima pra salvar os atributos do pokemon de forma organizada
    # em seguioda, chama a função, também criada lá em cima, salvar_pokemon_no_banco pra justamente fazer o que ela diz que vai fazer
    # com o objeto meu_pokemon. em seguida, exibe uma mensagem pra mostrar que deu certo. Do contrário,
    # informa que o pokemon não foi encontrado na pokedex ↓↓↓

    meu_pokemon = Pokemon(nome, peso, altura, tipo_str, evolucoes)
    salvar_pokemon_no_banco(meu_pokemon)
    print(f"Sucesso! {nome} foi baixado da API e salvo no banco.")
  else:
    print("Pokémon não encontrado na PokeAPI.")


# FLUXO PRINCIPAL DO PROGRAMA: aqui ele vai começar um loop que serve de "menu principal" pra você conseguir escolher o que quer fazer,
# aumentando sua gama de possibilidades de interação com o programa em vários niveis. no lugar de simplesmente buscar um pokemon,
# salvar ele no banco de dados e te passar as informações, voce pode fazer isso, pode conslutar os dados de um outro pokemon que ja 
# esta no banco de dados, pode remover as informações relacionadas um pokemon que já está no banco de dados também, e, por fim,
# pode simplesmente fechar o menu, que quebra o loop totalmente e encerra o programa.

while True:
  print("\n" + "=" * 30)
  print("        POKÉDEX BXESET V1.0        ")
  print("=" * 30)
  print("1. Buscar na API e Salvar Pokémon")
  print("2. Consultar Pokémon no Banco")
  print("3. Deletar Pokémon do Banco")
  print("4. Sair")
  print("=" * 30)

  opcao = input("Escolha uma opção (1 a 4): ").strip()

  if opcao == "1":
    nome_digitado = (
        input("\nDigite o nome do Pokémon para buscar: ").strip().lower()
    )
    buscar_e_salvar_pokemon(nome_digitado)

  elif opcao == "2":
    nome_consulta = (
        input("\nDigite o nome do Pokémon para consultar: ").strip().capitalize()
    )
    consultar_pokemon_no_banco(nome_consulta)

  elif opcao == "3":
    nome_delecao = (
        input("\nDigite o nome do Pokémon para deletar: ").strip().capitalize()
    )
    deletar_pokemon_do_banco(nome_delecao)

  elif opcao == "4":
    print("\nDesligando a Pokédex. Até mais!")
    break  # encerra o loop e fecha o programa

  else:
    print("\nOpção inválida! Escolha um número entre 1 e 4.")