import connection as cn
import random

q_table_path = "resultado.txt" 

# --- CLASSES:
# Classe que representa e manipula a tabela Q.
class Qtable:
    def __init__(self):
        self._start_value = 0.000000
        self._table_size = 96
        self._table = {"giro_esq": [], "giro_dir": [], "pulo": []}

    # Cria uma tabela com o tamanho definido e um valor padrão pata todos os elementos.
    def resetQTable(self):
        self._table = {"giro_esq": ([self._start_value] * self._table_size), "giro_dir": ([self._start_value] * self._table_size), "pulo": ([self._start_value] * self._table_size)}
    
    # Gera a tabela Q com valores aleatorios.
    def randomizeQTable(self):
        self._table = {"giro_esq": [], "giro_dir": [], "pulo": []} # Limpa a tabela.
        for i in range(self._table_size):
            # Gera os valores aleatorios e os adiciona a tabela.
            value = Qtable._generateRandomValue()
            self._table["giro_esq"].append(value)
            value = Qtable._generateRandomValue()
            self._table["giro_dir"].append(value)
            value = Qtable._generateRandomValue()
            self._table["pulo"].append(value)

    # Gera um float aleatorio entre 0 e 10, com precisão de 6 casas decimais.
    def _generateRandomValue():
        return round(random.uniform(0.0, 10.0), 6)

    # Salva o conteudo da tabelaQ da classe para o arquivo.
    def save(self, path):
        with open(path, "w") as file:
            for i in range(self._table_size):
                line = f"{self._table["giro_esq"][i]:.6f} {self._table["giro_dir"][i]:.6f} {self._table["pulo"][i]:.6f}"
                file.write(line + "\n")
            file.close()
    
    # Carrega a tabela Q do arquivo para a classe.
    def load(self, path):
        with open(path, "r") as file: # Abre o arquivo para ler o conteudo dele:
            file_lines = file.readlines() # Coloca as linhas do arquivo em uma lista.
            for line in file_lines:
                values = line.rstrip("\n").split(" ") # rstrip remove o \n no fim da linha; split separa os valores da linha.
                # Salva os valores em suas respectivas colunas:
                self._table["giro_esq"].append(float(values[0]))
                self._table["giro_dir"].append(float(values[1]))
                self._table["pulo"].append(float(values[2]))
            file.close()


# --- EXECUÇÃO:
# Reseta a tabela Q:
def reset():
    q_table = Qtable()
    q_table.resetQTable()
    q_table.save(q_table_path)

# Inicia o processo de aprendizado:
def learn():
    q_table = Qtable()
    q_table.load(q_table_path)
    s = cn.connect(2037)
    print(cn.get_state_reward(s, "right"))
    q_table.save(q_table_path)

# Recria a tabela Q com valores aleatorios:
def randomize():
    q_table = Qtable()
    q_table.randomizeQTable()
    q_table.save(q_table_path)

if __name__ == "__main__":
    print("COMANDOS:\n   t = Treinar\n   a - Deixa a tabela Q aleatoria\n   r - Reseta a tabela\n")
    command = input(">> ").lower()
    if command == "t":
        learn()
    elif command == "a":
        randomize()
    elif command == "r": 
        reset()
    else:
        print("COMANDO INVALIDO!")