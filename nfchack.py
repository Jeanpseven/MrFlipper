import nfc
import pickle
import os
import sys
import ctypes

FREQUENCIA_ARQUIVO = 'frequencias.pkl'

# Verifica se a biblioteca nfcpy está instalada
try:
    import nfc
except ImportError:
    print("A biblioteca 'nfcpy' não está instalada. Instalando...")
    os.system(f"{sys.executable} -m pip install nfcpy")
    print("Biblioteca 'nfcpy' instalada com sucesso!")

# Função para definir a cor de fundo
def set_terminal_background_color(color):
    if sys.platform.startswith("linux"):
        os.system(f"tput setab {color}")
    elif sys.platform.startswith("win"):
        ctypes.windll.kernel32.SetConsoleScreenBufferAttribute(ctypes.windll.kernel32.GetStdHandle(-11), color)

# Define a cor de fundo
set_terminal_background_color(202)  # R:255, G:130, B:0


def flipper_art():
   print("""                                                                     
         =+++++++++++++++++                                        
   -+++**#*==============+#%%%#*++=                                   
=+##%%%########%#%#+*+*%%#%=++-=++####==--                         
%+          -=****#*#%@%=     -*#%%+-*@@#=--                       
            =*#*#*#*#%%+ -  ##@#=-=*#*  **@+                       
            =#*#**#@@*- =#@**---+*=--=#*- *@*        +******+      
            =#*#*##@*- +%*---**= -+*+ ---+%%%* =+*@**=-----=#**@*-    
 -*@##########%#@@%+-  +%%+   -**= ---++@%+-*%###==         -++*@@+   
+%#==**********==%%+-   -+%%    ===+%#%====*+=           -=+%@@@@%+   
%+=#+----------*#-+%%+    -@#####%#++ --#++-         --*#%@@@@@@*-    
=#+--*@@@@@@@@*- *#=%%+           --=***-        ---*@@@@@@@@@*-     
** -@@@@@@@@@@@@  **=#*          =***           -*@@@@@@@@@@*         
# =@@@@+-#@@@@@@@- %+#*      ++**+-          =#@@@@@@@@@@%*-          
# =@@@@@%@@@@@@@@  %+#*-+*%##+=-           =#@@@@@@@@@@@*-            
# =@@@@@@@@@@@@@@==%+*%##=+              =#@@@@@@@@@@@*-              
**-*@@@@@@@@@@+++++%+                 --#@@@@@@@@@@@+-                
=**  @@@@%*+                         -#@@@@@@@@@@@*                   
#-=@*#----                       -=*#@@@@@@@@@@@@***************#*@@%=
*#@#--                          =#@@@@@#=------+####@#*=-------*+#=-#*
**=               ==-        ==#@@@@#==             =#%%%#=*%##==- =*+
=                 =##+===+%%%@@@@@@@#===============%##%*+++=     -#+ 
                   - =+++++++++++++++++++++++++++++++-  -       -**=  
                                                               *#-    
                                                      ++++*****--     
                                              =+++++##=----           
                                        ===****=====                  
                                     ---@@@+                          
                                --+###@@@@*-                          
                               +@@@@@@@@@-                            """)



def ler_tag():
    with nfc.ContactlessFrontend('usb') as clf:
        print('Aproxime a tag NFC...')
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        print('Tag NFC detectada!')
        return tag

def ler_id(tag):
    return tag.identifier

def ler_tipo(tag):
    return tag.type

def ler_tecnologia(tag):
    return tag.technologies

def ler_protocolo(tag):
    return tag.protocol

def ler_frequencia(tag):
    return tag.frequency

def ler_dados(tag):
    records = tag.ndef.records
    dados = []
    for record in records:
        if 'Text' in record.type:
            dados.append(record.text)
        elif 'URI' in record.type:
            dados.append(record.uri)
    return dados

def escrever_dados(dados):
    with nfc.ContactlessFrontend('usb') as clf:
        print('Aproxime a tag NFC...')
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        print('Tag NFC detectada!')
        ndef_records = []
        for dado in dados:
            if dado.startswith('http://') or dado.startswith('https://'):
                ndef_records.append(nfc.ndef.UriRecord(dado))
            else:
                ndef_records.append(nfc.ndef.TextRecord(dado))
        tag.ndef.records = ndef_records
        print('Dados escritos na tag com sucesso!')

def apagar_dados():
    with nfc.ContactlessFrontend('usb') as clf:
        print('Aproxime a tag NFC...')
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        print('Tag NFC detectada!')
        tag.ndef.records = []
        print('Dados da tag apagados com sucesso!')

def calcular_uid(tag):
    uid = tag.identifier.hex()
    return uid

def exibir_informacoes(tag):
    print('--- Informações da Tag ---')
    print('Identificador:', ler_id(tag))
    print('Tipo:', ler_tipo(tag))
    print('Tecnologia:', ler_tecnologia(tag))
    print('Protocolo:', ler_protocolo(tag))
    print('Frequência:', ler_frequencia(tag))
    dados = ler_dados(tag)
    if dados:
        print('Dados da tag:')
        for dado in dados:
            print('- ' + dado)
    else:
        print('A tag não contém dados.')

def salvar_frequencia(frequencia):
    frequencias = carregar_frequencias()
    frequencias.append(frequencia)
    with open(FREQUENCIA_ARQUIVO, 'wb') as arquivo:
        pickle.dump(frequencias, arquivo)

def carregar_frequencias():
    try:
        with open(FREQUENCIA_ARQUIVO, 'rb') as arquivo:
            frequencias = pickle.load(arquivo)
    except FileNotFoundError:
        frequencias = []
    return frequencias

def repetir_frequencia(frequencia):
    with nfc.ContactlessFrontend('usb') as clf:
        print('Aproxime o dispositivo NFC para repetir a frequência...')
        clf.connect(rdwr={'on-startup': lambda target: False, 'beep-on-connect': True}, terminate=lambda target: False, rdwr_timeout=10.0, target=[nfc.clf.RemoteTarget('212F', 'DEP'), nfc.clf.RemoteTarget('424F', 'DEP')])
        print('Frequência NFC repetida com sucesso!')

# Menu de escolhas
while True:
    flipper_art()
    print('--- Menu ---')
    print('1. Ler Tag')
    print('2. Exibir informações da Tag')
    print('3. Escrever dados na Tag')
    print('4. Apagar dados da Tag')
    print('5. Salvar frequência')
    print('6. Repetir frequência')
    print('7. Calcular UID')
    print('0. Sair')
    escolha = input('Digite a opção desejada: ')

    if escolha == '1':
        tag = ler_tag()
        print('Tag lida com sucesso!')
    elif escolha == '2':
        if 'tag' in locals():
            exibir_informacoes(tag)
        else:
            print('Nenhuma tag lida. Por favor, leia uma tag antes de exibir as informações.')
    elif escolha == '3':
        if 'tag' in locals():
            qtd_dados = int(input('Quantos dados deseja escrever na tag? '))
            dados = []
            for i in range(qtd_dados):
                dado = input('Digite o dado {}: '.format(i+1))
                dados.append(dado)
            escrever_dados(dados)
            print('Dados escritos na tag com sucesso!')
        else:
            print('Nenhuma tag lida. Por favor, leia uma tag antes de escrever dados.')
    elif escolha == '4':
        if 'tag' in locals():
            apagar_dados()
            print('Dados da tag apagados com sucesso!')
        else:
            print('Nenhuma tag lida. Por favor, leia uma tag antes de apagar os dados.')
    elif escolha == '5':
        if 'tag' in locals():
            frequencia = ler_frequencia(tag)
            nome_onda = input('Digite um nome para a onda capturada: ')
            salvar_frequencia((nome_onda, frequencia))
            print('Frequência salva com sucesso!')
        else:
            print('Nenhuma tag lida. Por favor, leia uma tag antes de salvar a frequência.')
    elif escolha == '6':
        frequencias = carregar_frequencias()
        if frequencias:
            print('--- Frequências Salvas ---')
            for i, (nome_onda, frequencia) in enumerate(frequencias):
                print('{}. {} - {}'.format(i+1, nome_onda, frequencia))
            indice = int(input('Digite o número da frequência que deseja repetir: '))
            if indice >= 1 and indice <= len(frequencias):
                nome_onda, frequencia = frequencias[indice-1]
                print('Repetindo a frequência: {} - {}'.format(nome_onda, frequencia))
                repetir_frequencia(frequencia)
            else:
                print('Índice inválido! Tente novamente.')
        else:
            print('Nenhuma frequência salva. Por favor, salve uma frequência antes de repetir.')
    elif escolha == '7':
        if 'tag' in locals():
            uid = calcular_uid(tag)
            print('UID da tag:', uid)
        else:
            print('Nenhuma tag lida. Por favor, leia uma tag antes de salvar a frequência.')
    elif escolha == '0':
        print('Encerrando o programa...')
        break
    else:
        print('Opção inválida! Tente novamente.')
