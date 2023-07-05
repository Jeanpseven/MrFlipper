import os
import pickle
from rfidiot.protocol import ISO14443A

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

# Verifica e instala as bibliotecas necessárias
try:
    import rfidiot
except ImportError:
    print("Biblioteca 'rfidiot' não encontrada. Instalando...")
    os.system('pip install rfidiot')

try:
    import iso14443a
except ImportError:
    print("Biblioteca 'iso14443a' não encontrada. Instalando...")
    os.system('pip install iso14443a')

from rfidiot.protocol import ISO14443A

def clear_screen():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

def read_card():
    clear_screen()
    print("Aproxime o cartão RFID para leitura...")
    
    card_data = ISO14443A().read_card()
    if card_data:
        print("Cartão lido com sucesso:")
        print(card_data)
        
        save_option = input("Deseja salvar esses dados? (S/N): ")
        if save_option.upper() == "S":
            save_wave(card_data)
    else:
        print("Nenhum cartão detectado.")

def write_card():
    clear_screen()
    print("Aproxime o cartão RFID para escrita...")
    
    data = input("Digite os dados que deseja gravar no cartão: ")
    if data:
        ISO14443A().write_card(data)
        print("Dados gravados no cartão com sucesso.")
    else:
        print("Nenhum dado fornecido.")

def save_wave(data):
    wave_name = input("Digite um nome para a onda: ")
    if wave_name:
        try:
            waves = load_waves()
            waves[wave_name] = data
        except FileNotFoundError:
            waves = {wave_name: data}
        
        with open("waves.pickle", "wb") as file:
            pickle.dump(waves, file)
        
        print("Onda salva com sucesso.")
    else:
        print("Nome da onda não fornecido.")

def load_waves():
    try:
        with open("waves.pickle", "rb") as file:
            waves = pickle.load(file)
        return waves
    except FileNotFoundError:
        return {}

def list_waves():
    waves = load_waves()
    if waves:
        clear_screen()
        print("Lista de ondas salvas:")
        for wave_name in waves:
            print(wave_name)
    else:
        print("Nenhuma onda salva.")

def replay_wave():
    waves = load_waves()
    if waves:
        clear_screen()
        print("Lista de ondas salvas:")
        for wave_name in waves:
            print(wave_name)
        
        wave_name = input("Digite o nome da onda que deseja reproduzir: ")
        if wave_name in waves:
            clear_screen()
            print("Reproduzindo a onda:", wave_name)
            print(waves[wave_name])
        else:
            print("Onda não encontrada.")
    else:
        print("Nenhuma onda salva.")

def exit_program():
    clear_screen()
    print("Encerrando o programa...")
    exit()

def main():
    while True:
        clear_screen()
        flipper_art()
        print("Menu:")
        print("1. Ler cartão RFID")
        print("2. Escrever em um cartão RFID")
        print("3. Salvar onda RFID")
        print("4. Listar ondas salvas")
        print("5. Reproduzir onda RFID")
        print("6. Sair")
        
        choice = input("Digite o número da opção desejada: ")
        
        if choice == "1":
            read_card()
        elif choice == "2":
            write_card()
        elif choice == "3":
            save_wave()
        elif choice ==```python
            list_waves()
        elif choice == "5":
            replay_wave()
        elif choice == "6":
            exit_program()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
