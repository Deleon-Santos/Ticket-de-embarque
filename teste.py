
import PySimpleGUI as sg

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

layout=[[sg.Text("Nome Completo:",size=(15,1)),sg.Input(key="-NOME-",do_not_clear=True,size=(25,1))],
        [sg.Text("N° Passaporte:",size=(28,1)),sg.Input(key="-PASSAPORTE-",do_not_clear=True,size=(10,1))],
        [sg.Radio("Masculino","RADIO",key="-masculino-",default=True),sg.Radio("Feminino","RADIO",key="-feminino-")],
        [sg.CalendarButton("Data de Partida",size=(20,1),close_when_date_chosen=True,target="-partida-",location=(0,0),no_titlebar=False),
         sg.Input(key="-partida-",size=(18,1))],
        [sg.CalendarButton("Data de Retorno",size=(20,1),close_when_date_chosen=True,target="-retorno-",location=(0,0),no_titlebar=False),
         sg.Input(key="-retorno-",size=(18,1))],
        [sg.Text("Lista de Destinos")],
        [sg.Listbox(["São Paulo","Rio de Janeiro","Maceio","Curitiba","Paraiba","Porto Seguro","Manaus","Belém","São Luiz"],
                    size=(42,5),select_mode="single",key="-DESTINO-")],
        [sg.Button("RESERVAR"),sg.Button("SAIR")],]

window=sg.Window("PASSAGEIRO",layout)

def informacao(valores):
    informacao = "TICKET DE EMBARQUE"
    "\n"
    name = '\nName Completo: ' + valores['-NOME-']
    informacao += name
    Passaporte = '\nNumero do Passaporte: ' + valores['-PASSAPORTE-']
    informacao += Passaporte
    genero = '\nGenero: ' 
    if valores['-feminino-']: 
        genero += 'Feminino'

    else: 
        genero += 'Masculino'
    informacao += genero
    data_Partida = '\nData de Partida: ' + valores['-partida-']
    informacao += data_Partida
    data_Retorno = '\nData de Retorno: ' + valores['-retorno-']
    informacao += data_Retorno
    # Listbox will return an array of 1 element because it's marked as 'single', otherwise it would return a larger array
    destino = '\nDestino: ' + valores['-DESTINO-'][0]
    informacao += destino
    
    return informacao

def create_pdf(content):
    pdf_filename = "ticket_embarque.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Configurações de formatação
    c.setFont("Helvetica", 20)  # Define a fonte e o tamanho da fonte
    c.setFillColorRGB(0, 0, 0)  # Define a cor do texto (RGB)
    text_object = c.beginText(150, 750)  # Posição inicial do texto

    # Adiciona o conteúdo formatado ao PDF
    text_object.textLines(content)
    c.drawText(text_object)
    
    c.save()
    return pdf_filename

while True:
    eventos,valores=window.read()
    if eventos in (sg.WIN_CLOSED,"SAIR"):
        break

    elif eventos=="RESERVAR":
        ticket_info = informacao(valores)
        pdf_file = create_pdf(ticket_info)
        sg.popup(f"PDF gerado: {pdf_file}")
        sg.popup(informacao(valores))
        