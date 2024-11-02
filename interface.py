import tkinter as tk
from tkinter import filedialog
from registro_imagens import get_conexao, fechar_conexao, inserir_imagem
from ordenacao_imagens import Ordenacao

class InterfaceOrdenacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Ordenação de Imagens")
        self.root.attributes('-fullscreen', True)  # Tela cheia

        self.root.configure(bg="#87CEEB")  # Azul claro

        self.ordenacao = Ordenacao()
        self.imagens = []  # Armazenar as imagens para exibição

        # Criação dos widgets
        self.create_widgets()

    def create_widgets(self):
        # Frame esquerdo para seleção e registro de imagem
        left_frame = tk.Frame(self.root, bg="#87CEEB")
        left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Campo para arrastar a imagem
        self.canvas = tk.Canvas(left_frame, width=400, height=200, bg="#FFFFFF")  # 200x200
        self.canvas.create_text(200, 100, text="Insira sua imagem", font=("Helvetica", 18), tags="mensagem")
        self.canvas.pack(pady=20)

        # Botão para selecionar a imagem
        self.button_selecionar = tk.Button(left_frame, text="Selecionar Imagem", command=self.selecionar_imagem, bg="#4682B4", fg="#FFFFFF", height=2)
        self.button_selecionar.pack(pady=10, fill=tk.X)

        # Campo para inserir o número de vezes que quer registrar no estilo blob
        self.label_numero_registros = tk.Label(left_frame, text="Número de registros:", bg="#87CEEB", fg="#000000")
        self.label_numero_registros.pack(pady=10)

        self.entry_numero_registros = tk.Entry(left_frame, width=10)  # Diminuindo o tamanho
        self.entry_numero_registros.pack(pady=5)

        # Botão para registrar no banco de dados
        self.button_registrar = tk.Button(left_frame, text="Registrar Imagem", command=self.registrar_imagem, bg="#4682B4", fg="#FFFFFF", height=2)
        self.button_registrar.pack(pady=5, fill=tk.X)

        # Frame direito para exibição da lista e ordenação
        right_frame = tk.Frame(self.root, bg="#87CEEB")
        right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Cabeçalho da lista
        self.label_cabecalho = tk.Label(right_frame, text="Lista de Imagens Registradas", bg="#87CEEB", fg="#000000", font=("Helvetica", 14, "bold"))
        self.label_cabecalho.pack(pady=10)

        # Lista para exibir as imagens
        self.lista_imagens = tk.Listbox(right_frame, width=40, height=15)  # Diminuindo a largura da lista e ajustando a altura
        self.lista_imagens.pack(pady=20, fill=tk.BOTH, expand=True)

        # Texto explicativo para os botões de ordenação
        self.label_ordenacao = tk.Label(right_frame, text="Selecione o tipo de método de ordenação:", bg="#87CEEB", fg="#000000")
        self.label_ordenacao.pack()

        # Botões de ordenação
        frame_botoes = tk.Frame(right_frame, bg="#87CEEB")
        frame_botoes.pack(pady=20)

        insertion_button = tk.Button(frame_botoes, text="Insertion Sort", command=self.insertion_sort, bg="#4682B4", fg="#FFFFFF")
        insertion_button.grid(row=0, column=0, padx=10)

        merge_button = tk.Button(frame_botoes, text="Merge Sort", command=self.merge_sort, bg="#4682B4", fg="#FFFFFF")
        merge_button.grid(row=0, column=1, padx=10)

        quick_button = tk.Button(frame_botoes, text="Quick Sort", command=self.quick_sort, bg="#4682B4", fg="#FFFFFF")
        quick_button.grid(row=0, column=2, padx=10)

        # Label para resultado e mensagem
        self.label_resultado = tk.Label(right_frame, text="", font=("Helvetica", 12), bg="#87CEEB", fg="#000000")
        self.label_resultado.pack(pady=20)

        self.label_mensagem = tk.Label(right_frame, text="", font=("Helvetica", 12, "bold"), bg="#87CEEB", fg="#008000")  # Mensagem em verde
        self.label_mensagem.pack(pady=10)

        # Botões para fechar e minimizar a janela
        frame_botoes_finais = tk.Frame(self.root, bg="#87CEEB")
        frame_botoes_finais.pack(side=tk.TOP, fill=tk.X)

        button_fechar = tk.Button(frame_botoes_finais, text="Fechar", command=self.root.quit, bg="#C00000", fg="#FFFFFF")
        button_fechar.pack(side=tk.RIGHT, padx=5, pady=5)

        button_minimizar = tk.Button(frame_botoes_finais, text="Minimizar", command=self.minimizar_janela, bg="#FFA500", fg="#FFFFFF")
        button_minimizar.pack(side=tk.RIGHT, padx=5, pady=5)

        # Atualiza a lista de imagens ao iniciar
        self.atualizar_lista_imagens()

    def minimizar_janela(self):
        self.root.iconify()  # Minimiza a janela

    def selecionar_imagem(self):
        self.caminho_imagem = filedialog.askopenfilename(title="Selecionar Imagem", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp")])
        if self.caminho_imagem:
            self.canvas.delete("mensagem")
            self.canvas.create_text(200, 100, text="Imagem selecionada com sucesso", font=("Helvetica", 16), fill="#008000")

    def registrar_imagem(self):
        conexao = get_conexao()
        if conexao:
            cursor = conexao.cursor()
            numero_registros = int(self.entry_numero_registros.get())

            try:
                with open(self.caminho_imagem, 'rb') as file:
                    blob_data = file.read()

                for _ in range(numero_registros):
                    inserir_imagem(cursor, conexao, blob_data)

                self.label_resultado.config(text="Imagem inserida com sucesso!")
                self.atualizar_lista_imagens()  # Atualiza a lista após inserção
                self.label_mensagem.config(text="Lista atualizada com sucesso!")  # Mensagem de sucesso
            except Exception as e:
                self.label_resultado.config(text=f"Erro ao registrar imagem: {e}")
                self.label_mensagem.config(text="")  # Limpa a mensagem em caso de erro
            finally:
                cursor.close()
                fechar_conexao(conexao)

    def atualizar_lista_imagens(self):
        """Atualiza a lista de imagens na interface."""
        self.lista_imagens.delete(0, tk.END)  # Limpa a lista
        conexao = get_conexao()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, data_registro FROM imagens")
            self.imagens = cursor.fetchall()  # Armazena as imagens
            for img in self.imagens:
                self.lista_imagens.insert(tk.END, f"ID: {img[0]}, Data: {img[1]}")
            cursor.close()
            fechar_conexao(conexao)

    def insertion_sort(self):
        tempo, imagens = self.ordenacao.insertion_sort()
        self.label_resultado.config(text=f"Insertion Sort: {tempo:.2f} segundos\nImagens processadas: {imagens}")
        self.label_mensagem.config(text="Lista atualizada com sucesso!")  # Mensagem de sucesso
        self.atualizar_lista_imagens()  # Atualiza a lista após a ordenação

    def merge_sort(self):
        tempo, imagens = self.ordenacao.merge_sort()
        self.label_resultado.config(text=f"Merge Sort: {tempo:.2f} segundos\nImagens processadas: {imagens}")
        self.label_mensagem.config(text="Lista atualizada com sucesso!")  # Mensagem de sucesso
        self.atualizar_lista_imagens()  # Atualiza a lista após a ordenação

    def quick_sort(self):
        tempo, imagens = self.ordenacao.quick_sort()
        self.label_resultado.config(text=f"Quick Sort: {tempo:.2f} segundos\nImagens processadas: {imagens}")
        self.label_mensagem.config(text="Lista atualizada com sucesso!")  # Mensagem de sucesso
        self.atualizar_lista_imagens()  # Atualiza a lista após a ordenação

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceOrdenacao(root)
    root.mainloop()
