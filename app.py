import torch
from tkinter import END,Tk,Label,Text,WORD,Scrollbar,RIGHT,Y,Entry,Button,NORMAL,DISABLED
from chat import obter_resposta, nome_bot, RedeNeural

BG_CINZA = "#ABB2B9"
COR_FUNDO = "#17202A"
COR_TEXTO = "#EAECEE"

FONTE = "Helvetica 14"
FONTE_NEGRITO = "Helvetica 13 bold"

class AplicacaoChat:

    def __init__(self):
        self.janela = Tk()
        self._configurar_janela_principal()
        self.texto_widget.insert(END, "Bem-vindo! Diga 'olá' ou 'oi' para iniciar a conversa.")

    def executar(self):
        self.janela.mainloop()

    def _configurar_janela_principal(self):
        self.janela.title("Chat")
        self.janela.configure(bg=COR_FUNDO)
        self.janela.geometry("455x550")
        self.janela.resizable(True, False)

        # rótulo principal
        rotulo_principal = Label(self.janela, bg=COR_FUNDO, fg=COR_TEXTO,
                                text="Bem-vindo", font=FONTE_NEGRITO, pady=10)
        rotulo_principal.place(relwidth=1)

        # divisor pequeno
        linha = Label(self.janela, width=450, bg=BG_CINZA)
        linha.place(relwidth=1, rely=0.07, relheight=0.012)

        # widget de texto
        self.texto_widget = Text(self.janela, wrap=WORD, bg=COR_FUNDO, fg=COR_TEXTO,
                                 font=FONTE, padx=5, pady=5)
        self.texto_widget.place(relheight=0.745, relwidth=1, rely=0.08)

        # barra de rolagem
        barra_rolagem = Scrollbar(self.texto_widget, bg=COR_FUNDO)
        barra_rolagem.pack(side=RIGHT, fill=Y)
        self.texto_widget.config(yscrollcommand=barra_rolagem.set)
        barra_rolagem.config(command=self.texto_widget.yview)

        # rótulo inferior
        rotulo_inferior = Label(self.janela, bg=BG_CINZA, height=80)
        rotulo_inferior.place(relwidth=1, rely=0.825)

        # caixa de entrada de mensagem
        self.entrada_msg = Entry(rotulo_inferior, bg="#2C3E50", fg=COR_TEXTO, font=FONTE)
        self.entrada_msg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entrada_msg.focus()
        self.entrada_msg.bind("<Return>", self._ao_pressionar_enter)

        # botão de envio
        botao_enviar = Button(rotulo_inferior, text="Enviar", font=FONTE_NEGRITO, width=20, bg=BG_CINZA,
                              command=lambda: self._ao_pressionar_enter(None))
        botao_enviar.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        # Configurar a tag vermelha para o nome do chatbot
        self.texto_widget.tag_configure("tag_bot", foreground="red")
        self.texto_widget.tag_configure("tag_voce", foreground="green")

    def _ao_pressionar_enter(self, evento):
        msg = self.entrada_msg.get()
        self._inserir_mensagem(msg, "Você")

    def _inserir_mensagem(self, msg, remetente):
        if not msg:
            return

        self.entrada_msg.delete(0, END)
        # Divide o texto em duas partes: nome do "remetente" e conteúdo da mensagem
        texto_remetente = f"\n{remetente}: "
        texto_mensagem = msg

        self.texto_widget.configure(state=NORMAL)

        # Insere o nome do "remetente" com a formatação da tag "tag_voce" (verde)
        self.texto_widget.insert(END, texto_remetente, "tag_voce")

        # Insere o conteúdo da mensagem sem formatação
        self.texto_widget.insert(END, texto_mensagem)

        self.texto_widget.configure(state=DISABLED)

        resposta_bot = obter_resposta(msg)
        nome_resposta_bot = f"\n{nome_bot}: "
        texto_resposta_bot = resposta_bot

        self.texto_widget.configure(state=NORMAL)
        self.texto_widget.insert(END, nome_resposta_bot, "tag_bot")
        self.texto_widget.insert(END, texto_resposta_bot)
        self.texto_widget.configure(state=DISABLED)

        self.texto_widget.see(END)

if __name__ == "__main__":
    dispositivo = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    ARQUIVO = "dados.pth"
    dados = torch.load(ARQUIVO)

    tamanho_entrada = dados["tamanho_entrada"]
    tamanho_oculto = dados["tamanho_oculto"]
    tamanho_saida = dados["tamanho_saida"]
    todas_palavras = dados['todas_palavras']
    tags = dados['tags']
    estado_modelo = dados["estado_do_modelo"]

    modelo = RedeNeural(tamanho_entrada, tamanho_oculto, tamanho_saida).to(dispositivo)
    modelo.load_state_dict(estado_modelo)
    modelo.eval()

    app = AplicacaoChat()
    app.executar()