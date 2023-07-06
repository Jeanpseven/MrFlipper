import mfrc522
import pickle
import os
import sys
import ctypes

FREQUENCIA_ARQUIVO = 'frequencias.pkl'

# Verifica se a biblioteca nfcpy está instalada
try:
    import mfrc522
except ImportError:
    print("A biblioteca 'mfrc522' não está instalada. Instalando...")
    os.system(f"{sys.executable} -m pip install mfrc522")
    print("Biblioteca 'mfrc522' instalada com sucesso!")

# Função para definir a cor de fundo
def set_terminal_background_color(color):
    if sys.platform.startswith("linux"):
        os.system(f"tput setab {color}")
    elif sys.platform.startswith("win"):
        ctypes.windll.kernel32.SetConsoleScreenBufferAttribute(
            ctypes.windll.kernel32.GetStdHandle(-11), color
        )


# Define a cor de fundo
set_terminal_background_color(202)  # R:255, G:130, B:0


def flipper_art():
    print(
        """                                                                     
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
                              ```python
+@@@@@@@@@-                            """)


import pickle
from mfrc522 import SimpleMFRC522

FREQUENCIA_ARQUIVO = 'frequencias.pkl'

def ler_tag():
    reader = SimpleMFRC522()
    print('Aproxime o cartão RFID para leitura...')
    try:
        id, text = reader.read()
        print('Cartão lido com sucesso:')
        print('ID:', id)
        print('Dados:', text)
        return id, text
    except Exception as e:
        print('Erro ao ler o cartão:', str(e))

def salvar_frequencia(frequencia):
    frequencias = carregar_frequencias()
    frequencias.append(frequencia)
    with open(FREQUENCIA_ARQUIVO, 'wb') as arquivo:
        pickle.dump(frequencias, arquivo)
    print('Frequência salva com sucesso!')

def carregar_frequencias():
    try:
        with open(FREQUENCIA_ARQUIVO, 'rb') as arquivo:
            frequencias = pickle.load(arquivo)
    except FileNotFoundError:
        frequencias = []
    return frequencias

def repetir_frequencia(frequencia):
    reader = SimpleMFRC522()
    print('Aproxime o cartão RFID para repetir a frequência...')
    try:
        reader.write(frequencia)
        print('Frequência RFID repetida com sucesso!')
    except Exception as e:
        print('Erro ao repetir a frequência:', str(e))

# Menu de escolhas
while True:
    print('--- Menu ---')
    print('1. Ler Tag RFID')
    print('2. Salvar Frequência')
    print('3. Repetir Frequência')
    print('0. Sair')
    escolha = input('Digite a opção desejada: ')

    if escolha == '1':
        ler_tag()
    elif escolha == '2':
        id, text = ler_tag()
        if id and text:
            nome_onda = input('Digite um nome para a onda capturada: ')
            frequencia = (nome_onda, {'id': id, 'dados': text})
            salvar_frequencia(frequencia)
    elif escolha == '3':
        frequencias = carregar_frequencias()
        if frequencias:
            print('--- Frequências Salvas ---')
            for i, (nome_onda, frequencia) in enumerate(frequencias):
                print('{}. {} - {}'.format(i+1, nome_onda, frequencia['dados']))
            indice = int(input('Digite o número da frequência que deseja repetir: '))
            if indice >= 1 and indice <= len(frequencias):
                nome_onda, frequencia = frequencias[indice-1]
                repetir_frequencia(frequencia['dados'])
            else:
                print('Índice inválido! Tente novamente.')
        else:
            print('Nenhuma frequência salva. Por favor, salve uma frequência antes de repetir.')
    elif escolha == '0':
        print('Encerrando o programa...')
        break
    else:
        print('Opção inválida! Tente novamente.')

if __name__ == "__main__":
    main()
