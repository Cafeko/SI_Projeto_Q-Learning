# Feito por: Caio Ferreira Gomes da Silva

import connection as cn
import random

q_table_path = "resultado.txt" 

# --- CLASSES:
# Classe que representa e manipula a tabela Q.
class Qtable:
    def __init__(self):
        self._start_value = 0.000000
        self._table_size = 96
        self._table = {"left": [], "right": [], "jump": []}

    # Cria uma tabela com o tamanho definido e um valor padrão pata todos os elementos.
    def resetQTable(self):
        self._table = {"left": ([self._start_value] * self._table_size), "right": ([self._start_value] * self._table_size), "jump": ([self._start_value] * self._table_size)}
    
    # Gera a tabela Q com valores aleatorios.
    def randomizeQTable(self):
        self._table = {"left": [], "right": [], "jump": []} # Limpa a tabela.
        for i in range(self._table_size):
            # Gera os valores aleatorios e os adiciona a tabela.
            value = Qtable._generateRandomValue()
            self._table["left"].append(value)
            value = Qtable._generateRandomValue()
            self._table["right"].append(value)
            value = Qtable._generateRandomValue()
            self._table["jump"].append(value)

    # Gera um float aleatorio entre -10 e 10, com precisão de 6 casas decimais.
    def _generateRandomValue():
        return round(random.uniform(-10.0, 10.0), 6)

    # Salva o conteudo da tabelaQ da classe para o arquivo.
    def save(self, path):
        with open(path, "w") as file:
            for i in range(self._table_size):
                line = f"{self._table["left"][i]:.6f} {self._table["right"][i]:.6f} {self._table["jump"][i]:.6f}"
                file.write(line + "\n")
            file.close()
    
    # Carrega a tabela Q do arquivo para a classe.
    def load(self, path):
        with open(path, "r") as file: # Abre o arquivo para ler o conteudo dele:
            file_lines = file.readlines() # Coloca as linhas do arquivo em uma lista.
            for line in file_lines:
                values = line.rstrip("\n").split(" ") # rstrip remove o \n no fim da linha; split separa os valores da linha.
                # Salva os valores em suas respectivas colunas:
                self._table["left"].append(float(values[0]))
                self._table["right"].append(float(values[1]))
                self._table["jump"].append(float(values[2]))
            file.close()
    
    # Muda um valor na tabela Q para um estado e ação especifico.
    def setValue(self, state: int, action: str, value: float):
        if Qtable._isValidAction(action):
            if state < self._table_size:
                self._table[action][state] = value
            else:
                print("ERRO: ESTADO INVALIDO")
        else:
            print("ERRO: AÇÃO INVALIDA")
    
    # Verifica se a ação recebida é uma ação valida.
    def _isValidAction(action: str):
        return action == "left" or action == "right" or action == "jump"
    
    # Retorna o valor da tabela Q, que está no estado e ação especificados.
    def getValue(self, state: int, action: str):
        if Qtable._isValidAction(action):
            if state < self._table_size:
                return self._table[action][state]
            else:
                print("ERRO: ESTADO INVALIDO")
        else:
            print("ERRO: AÇÃO INVALIDA")
    
    # Retorna o maior valor de um estado especificado da tabela Q.
    def getMaxValue(self, state: int):
        if state < self._table_size:
            action_left = self._table["left"][state]
            action_right = self._table["right"][state]
            action_jump = self._table["jump"][state]
            return max(action_left, action_right, action_jump)
        else:
            print("ERRO: ESTADO INVALIDO")


# --- CONVERTER:
# Trnasforma uma string de binario para um numero inteiro.
def binaryInt(binary: str):
    return int(binary, 2)

# Transforma um numero inteiro em uma string de binario.
def intBinary(integer: int):
    return bin(integer)


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
    """s = cn.connect(2037)
    state, value = cn.get_state_reward(s, "jump")"""
    q_table.setValue(0, "jump", 10)
    print(q_table.getValue(2, "right"))
    print(q_table.getMaxValue(5))
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