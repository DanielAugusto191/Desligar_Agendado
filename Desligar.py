#!/usr/bin/python3
#-*- coding:utf-8 -*-

# Inteface
from tkinter import *
from tkinter.ttk import Combobox
import tkinter.messagebox as mb
# Controle de tempo
import time
from datetime import datetime
# Sistema
import os
import psutil
from threading import Thread
# Configs
from math import ceil

def main():
    # Essa função será executada após o usuario inserir os dados e apertar no botao para agendar.
    def shutdown():
        # Após o tempo matar os processos
        def sleepTimer(ltime , x=0):
            time.sleep(ltime)
            for myprocess in programas:
                for process in psutil.process_iter():
                    if process.name() == myprocess:
                        os.system(f"killall {process.name()}")
                        break
            
            print("F")
        
        ###### Controler #########
        # Convertendo para int
        try:
            horas = int(En_Horas.get())
            minutos = int(En_Minutos.get())
        except ValueError as e:
            # Caso nao preenchido
            if horas == "" or minutos == "":
                mb.showinfo("Opa", "Preencha o campo de horas e minutos!")
                return
            else: # Caso preenchido com letras ou simbolos
                mb.showwarning("Erro", "Horas, minutos e segundos devem ser números!")
                return
        if horas < 0 or horas > 23:
            mb.showinfo("Opa", "Hora Invalida!")
            return
        if minutos < 0 or minutos > 60:
            mb.showinfo("Opa", "Minutos Invalidos!")
            return


        # Pegando quais programas fechar
        if fecharProgramas.get():
            # onOff recebe o estado de cada botao, se estiver on, entao pega o texto que representa aquele programa
            programas = [Apps[x] for x in range(len(onOff)) if onOff[x].get()]

            # Outros programas
            outroapp = En_outroApp.get() 
            if outroapp.split(":")[0] == "Exemplo": # Retira o exemplo inicial
                pass
            elif outroapp == "":
                pass
            else: # Separa multiplos programas adicionados, e adiciona em programas
                outroapp = outroapp.split(",")
                for x in outroapp:
                    if x not in programas: # Caso já esteja adicionado
                        programas.append(x)
        # Caso haja programas marcado mas a opções de fecha-los esteja desmarcada, exibe uma mensagem de erro!
        else:
            for x in onOff:
                if x.get():
                    resp = mb.askyesno("Desligar Programas", "Você selecionou alguns programsa, mas nao marcou se deseja encerra-los. Tem certeza que deseja Desligar sem encerra-los?")
                    if not resp:
                        return
                    break

        # Se vai desligar ou reiniciar
        power = Cb_poweroff.get()
        command = f"shutdown -h {horas}:{minutos}"
        command = command if power == "Desligar" else command+" -r"

        try:
            # Desligar
            os.system(command)
            mb.showinfo("Pronto!" , f"Agendado com sucesso! O pc irá {power} às {horas} horas {minutos} minutos!")

            # Esperar o tempo para matar os processos!
            agora = datetime.now()
            h = agora.strftime("%H:%M").split(":")
            # Convertendo hora atual pra minutos
            y = (24*60)-((int(h[0])*60+int(h[1])) - (horas*60+minutos))
            if y > 24*60:
                y -= 24*60
            # Thread para esperar o tempo e matar os processos.
            timer = Thread(target=sleepTimer, args=(y*60, 0))
            timer.start()
        except Exception as e:
            mb.showerror("Error", "Erro ao desligar/reiniciar, contate o desenvolvedor!")
            print(e)

    root = Tk()
    root.title("Desligar por tempo")

    Lb_Title = Label(root, text="AGENDAR DESLIGAMENTO", fg="black", font=("Courier New", 14))
    Lb_Title.grid(row=0, column=0, columnspan=3, pady=10)

    # Tempo
    Lf_Time = LabelFrame(root, borderwidth=2)
    Lf_Time.grid(row=1, column=0, columnspan=2, pady=10, ipadx=2, ipady=2)
    #|- Horas
    Lb_Horas = Label(Lf_Time, text="Horas")
    Lb_Horas.grid(row=1, column=0)
    En_Horas = Entry(Lf_Time, width=3)
    En_Horas.insert(0, 0)
    En_Horas.grid(row=1, column=1)
    #|- Minutos
    Lb_Minutos = Label(Lf_Time, text="Minutos")
    Lb_Minutos.grid(row=1, column=2)
    En_Minutos = Entry(Lf_Time, width=3)
    En_Minutos.insert(0,0)
    En_Minutos.grid(row=1, column=3)

    # Fechar Programas
    Lf_fecharProgramas = LabelFrame(root, borderwidth=1)
    Lf_fecharProgramas.grid(row=2, column=0, columnspan=2, padx=10)

    #| Marcar se deve fechar ou nao
    fecharProgramas = BooleanVar()
    Cb_fecharProgramas = Checkbutton(Lf_fecharProgramas, text="Fechar Programas?", variable=fecharProgramas)
    Cb_fecharProgramas.grid(row=0, column=0, columnspan=3, stick="ew")

    #| Lista de Aplicativos
    '''### ADICIONE AQUI PROCESSOS DO OUTROS APP - Deve possuir listas de até 3 elementos! ######'''
    Apps = ["chrome", "firefox", "opera", "parole", "smplayer", "vlc"]
    '''######################################'''
    onOff = [] # Ver o estado dos checkbuttons
    Cb_Apps = [] # Vai armazenar os checkbuttons
    for x in range(len(Apps)):
        onOff.append(BooleanVar())
        Cb_Apps.append(Checkbutton(Lf_fecharProgramas, text=Apps[x], onvalue=1, offvalue=0, variable=onOff[x]))
    linha = 1
    coluna = 0
    for x in Cb_Apps:
        if coluna >= 3:
            coluna = 0
            linha += 1
        x.grid(row=linha, column=coluna)
        coluna += 1


    #| Caso haja algum outro processo
    Lb_outroApp = Label(Lf_fecharProgramas, text="Digite a tarefa de outro app")
    Lb_outroApp.grid(row=5, column=0, columnspan=2)
    En_outroApp = Entry(Lf_fecharProgramas, fg="#444444")
    En_outroApp.insert(0, "Exemplo: mpw, lmao")
    En_outroApp.grid(row=5, column=2, stick="e")

    #| Desligar

    Cb_poweroff = Combobox(root, values=("Desligar", "Reiniciar"), width=8)
    Cb_poweroff.set("Desligar")
    Cb_poweroff.grid(row=4, column=1)
    Btn_desligar = Button(root, text="Agendar", command=lambda: shutdown())
    Btn_desligar.grid(row=4, column=0, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()