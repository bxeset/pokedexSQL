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
        altura REAL
    )
""")
conexao.commit()
conexao.close()


# classe base pra organizar os dados dos pokemons
class Pokemon:

  def __init__(self, nome, peso, altura):
    self.nome = nome
    self.peso = peso
    self.altura = altura

  def __str__(self):
    return f"Pokémon: {self.nome} | Peso: {self.peso}kg | Altura: {self.altura}m"


# salvar as infos organizadas do pokemon no banco de dados
def salvar_pokemon_no_banco(pokemon):
  conexao = sqlite3.connect(caminho_do_banco)
  cursor = conexao.cursor()
  cursor.execute(
      """
        INSERT INTO pokemons (nome, peso, altura)
        VALUES (?, ?, ?)
    """,
      (pokemon.nome, pokemon.peso, pokemon.altura),
  )
  conexao.commit()
  conexao.close()


# aqui ele conecta de novo no banco de dados e usa o comando SELECT pra selecionar nome peso e altura da tabela pokemons
# onde nome tem que bater com o que foi digitado pelo usuário pra previnir problemas, depois, pega o primeiro resultado (fetchone)
# e salva na variavel resultado, fechando a conexao com o banco de dados em seugida

def consultar_pokemon_no_banco(nome_pokemon):
  conexao = sqlite3.connect(caminho_do_banco)
  cursor = conexao.cursor()
  cursor.execute(
      "SELECT nome, peso, altura FROM pokemons WHERE nome = ?", (nome_pokemon,)
  )
  resultado = cursor.fetchone()
  conexao.close()

# depois, cria uma condição em que se houver resultado pra busca, ou seja, se aquele pokemon for gravado corretamente no banco de dados
# ele exibe todas as informações corretamente. Do contrário, informa que não foi encontrado no banco de dados

  if resultado:
    print(
        f"\n dados vindos DIRETO DO BANCO DE DADOS: \nPokémon:"
        f" {resultado[0]} | Peso: {resultado[1]}kg | Altura: {resultado[2]}m"
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


# buscar o pokémon esclhido na API, url possui uma f-string pra se tornar universal, mudando de acordo com a entrada do usuário
# requests.get pega as 3 informações do pokémon (nome, peso, altura). em seguida, rola um teste rápido pra ver se a consulta deu certo 
# (status code == 200), se sim, ele da sequencia com o processo de pegar as 3 informações do pokémon e salvar em variáveis ↓↓↓

def buscar_e_salvar_pokemon(pokemon_escolhido):
  url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_escolhido}"
  resposta = requests.get(url)

  if resposta.status_code == 200:
    dados_pokemon = resposta.json()
    nome = dados_pokemon["name"].capitalize()
    peso = dados_pokemon["weight"] / 10
    altura = dados_pokemon["height"] / 10

    # cria o objeto meu_pokemon, usando a classe criada lá em cima pra salvar os 3 atributos do pokemon de forma organizada
    # em seguioda, chama a função, também criada lá em cima, salvar_pokemon_no_banco pra justamente fazer o que ela diz que vai fazer
    # com o objeto meu_pokemon, que contem os 3 atributos. em seguida, exibe uma mensagem pra mostrar que deu certo. Do contrário,
    # informa que o pokemon não foi encontrado na pokedex ↓↓↓

    meu_pokemon = Pokemon(nome, peso, altura)
    salvar_pokemon_no_banco(meu_pokemon)
    print(f"Sucesso! {nome} foi baixado da API e salvo no banco.")
  else:
    print("Pokémon não encontrado na PokeAPI.")


# fluxo principal do programa, aqui ele salva a variável do nome do pokemon que voce quer buscar as infos na pokedex em nome_digitado

# aqui é o segundo passo, onde ele busca as informações desse pokemon, lê o json que a API retorna, seleciona as 3 informações 
# que você quer, cria um objeto com essas informações pra organizar bonitinho e por fim salva no banco de dados



# aqui ele chama a outra função criada pra consultar o banco de dados, essa função inicia uma conexao com banco,
# usa o comando SELECT pra selecionar nome peso e altura da tabela pokemons, onde nome tem que bater com o que foi digitado
# pelo usuário pra previnir problemas, depois, pega o primeiro resultado (fetchone) e salva na variavel resultado,
# fechando a conexao com o banco de dados em seguida. a partir disso, ele cria uma condicional que se houver resultado pra busca,
# ele retorna com esse resultado escrito bonitinho, mostrando as informações do pokémon que você escreveu lá na variável nome_digitado
# do contrário, ele retorna que esse pokémon não foi encontrado no banco.


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
    break  # Encerra o loop e fecha o programa

  else:
    print("\nOpção inválida! Escolha um número entre 1 e 4.")
