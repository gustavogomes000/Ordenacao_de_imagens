
import mysql.connector
import time

class Ordenacao:
    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.conectar_banco()

    def conectar_banco(self):
        """Conecta ao banco de dados MySQL."""
        self.cnx = mysql.connector.connect(
            host='localhost',
            user='gustavo',
            password='Carmelita.1963',
            database='imagens'
        )
        self.cursor = self.cnx.cursor()

    def fetch_imagens(self):
        """Busca as imagens do banco de dados."""
        self.cursor.execute("SELECT * FROM imagens")
        return self.cursor.fetchall()

    def insertion_sort(self):
        """Ordena as imagens usando o algoritmo Insertion Sort otimizado com busca binária."""
        imagens = self.fetch_imagens()
        inicio = time.time()

        for i in range(1, len(imagens)):
            chave = imagens[i]
            # Busca binária para encontrar a posição correta
            pos = self.binary_search(imagens, chave, 0, i - 1)
            # Move os elementos para a direita
            imagens = imagens[:pos] + [chave] + imagens[pos:i] + imagens[i + 1:]

        fim = time.time()
        return fim - inicio, len(imagens)

    def binary_search(self, arr, chave, low, high):
        """Realiza a busca binária para encontrar a posição de inserção da chave."""
        while low <= high:
            mid = (low + high) // 2
            if chave[1] < arr[mid][1]:  # Ordena pela coluna desejada
                high = mid - 1
            else:
                low = mid + 1
        return low

    def merge_sort(self):
        """Ordena as imagens usando o algoritmo Merge Sort."""
        imagens = self.fetch_imagens()
        inicio = time.time()

        def merge(left, right):
            result = []
            while left and right:
                if left[0][1] < right[0][1]:  # Ordena pela coluna desejada
                    result.append(left.pop(0))
                else:
                    result.append(right.pop(0))
            result.extend(left or right)
            return result

        def merge_sort_helper(arr):
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = merge_sort_helper(arr[:mid])
            right = merge_sort_helper(arr[mid:])
            return merge(left, right)

        sorted_imagens = merge_sort_helper(imagens)

        fim = time.time()
        return fim - inicio, len(sorted_imagens)

    def quick_sort(self):
        """Ordena as imagens usando o algoritmo Quick Sort."""
        imagens = self.fetch_imagens()
        inicio = time.time()

        def quick_sort_helper(arr):
            if len(arr) <= 1:
                return arr
            pivo = arr[len(arr) // 2]
            esquerda = [x for x in arr if x[1] < pivo[1]]
            meio = [x for x in arr if x[1] == pivo[1]]
            direita = [x for x in arr if x[1] > pivo[1]]
            return quick_sort_helper(esquerda) + meio + quick_sort_helper(direita)

        sorted_imagens = quick_sort_helper(imagens)

        fim = time.time()
        return fim - inicio, len(sorted_imagens)

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        self.cursor.close()
        self.cnx.close()
