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

    # Gera um float aleatorio entre 1 e 10, com precisão de 6 casas decimais.
    def _generateRandomValue():
        return round(random.uniform(1, 10.0), 6)

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

    def getNextAction(self, state: int):
        if state < self._table_size:
            action_left = self._table["left"][state]
            action_right = self._table["right"][state]
            action_jump = self._table["jump"][state]
            if action_left > action_right and action_left > action_jump:
                return "left"
            elif action_right > action_jump:
                return "right"
            else:
                return "jump"
        else:
            print("ERRO: ESTADO INVALIDO") 


# --- CONVERTER:
# Trnasforma uma string de binario para um numero inteiro.
def binaryInt(binary: str):
    return int(binary, 2)

# Transforma um numero inteiro em uma string de binario.
def intBinary(integer: int):
    return bin(integer)



# --- Q Learning:
def qLearning(q_table: Qtable, start_state: int, random_action: float, action_number=1000, gamma=0.7, alpha=0.5):
    """
    q_table: objeto da classe QTable que contem a tabela que será usada para o aprendizado.
    start_state: estado que está no inicio do treinamento.
    action_number: numero de ações que irá fazer, treinamento acaba ao atingir dado umero de ações.
    gamma: valor de desconto, determina o quanto que a recompenssa futura e valorizada em relação a recompensa atual.
    alpha: taxa de aprendizado.
    """
    # Preparação:
    s = cn.connect(2037)
    current_state = start_state
    act = ""
    for a in range(action_number):
        print(a+1)
        # escolhe ação:
        if random.random() < random_action:
            act = random.choice(["left", "right", "jump"])
        else:
            act = q_table.getNextAction(current_state)
        # executa ação:
        state_binary, reward = cn.get_state_reward(s, act)
        new_state = binaryInt(state_binary)
        # atualiza valor da ação na tabela:
        current_state_action_value = q_table.getValue(current_state, act) # Pega o valor da ação feita, no estado atual.
        q_estimate = bellmanEquation(q_table, new_state, reward, gamma)   # Usa a equação de Bellman para obter a estimativa de Q(s,a).
        error = q_estimate - current_state_action_value                   # Obtem o erro fazendo a estmativa de Q(s,a) menos o valor relacionado a ação e o estado atual.
        update_value = current_state_action_value + (alpha * error)       # Obtem o novo valor da ação, fazendo a soma do valor atual mais o error vezes a taxa de aprendizado.
        q_table.setValue(current_state, act, update_value)                # Atualiza a tabela com o valor obtido.
        # atualiza estado:
        current_state = new_state

def bellmanEquation(q_table: Qtable, new_state: int, reward, gamma: float):
    """
    q_table: objeto da classe QTable que contem a tabela que será usada para o aprendizado.
    new_state: Estado em que foi parar após a ter feito a ação.
    reward: recompensa do novo estado.
    gamma: valor de desconto, determina o quanto que a recompenssa futura e valorizada em relação a recompensa atual.
    """
    return reward + (gamma * q_table.getMaxValue(new_state))



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
    start_state = 0
    random_act = 0.4
    n_actions = 1000
    gamma = 0.9
    alpha = 0.3
    qLearning(q_table, start_state, random_act, n_actions, gamma, alpha)
    q_table.save(q_table_path)

# Recria a tabela Q com valores aleatorios:
def randomize():
    q_table = Qtable()
    q_table.randomizeQTable()
    q_table.save(q_table_path)

def run():
    q_table = Qtable()
    q_table.load(q_table_path)
    s = cn.connect(2037)
    current_state = 0
    while True:
        act = q_table.getNextAction(current_state)
        state_binary, reward = cn.get_state_reward(s, act)
        current_state = binaryInt(state_binary)

if __name__ == "__main__":
    print("COMANDOS:\n   t = Treinar\n   a - Deixa a tabela Q aleatoria\n   r - Reseta a tabela\n   s - Start\n ")
    command = input(">> ").lower()
    if command == "t":
        learn()
    elif command == "a":
        randomize()
    elif command == "r": 
        reset()
    elif command == "s":
        run()
    else:
        print("COMANDO INVALIDO!")