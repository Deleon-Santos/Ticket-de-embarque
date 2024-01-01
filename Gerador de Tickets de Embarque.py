#Estou desenvolvendo um gerenciador de Ticket de passagens aereas ou embarques por vias terrestres
#O objetivo é gerar um QRcode e imprimir num PDF com as informações do passageiro 
import PySimpleGUI as sg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode

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

window=sg.Window("PASSAGEIRO",layout,resizable=True)

#A função "informação" revebe os valores e formata em uma unica strig
def informacao(valores):
    informacao = "TICKET DE EMBARQUE"
    space="\n"
    informacao+=space
    line="\n-------------------------------------------------------------------"
    informacao+=line
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
    destino = '\nDestino: ' + valores['-DESTINO-'][0]
    informacao += destino
    return informacao

#A função criar qrcode gera o grafico e salva as informaçãos 
def gerar_qrcode(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.png")
    return "qrcode.png"

#A função criar pdf gera um aquiv com as informações e o qrcode gerado
def criar_pdf(content, qr_filename):
    pdf_filename = "ticket_embarque.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 18)
    c.setFillColorRGB(0, 0, 0)
    text_object = c.beginText(110, 710)
    text_object.textLines(content)
    c.drawText(text_object)
    c.drawInlineImage(qr_filename, 230, 320, width=150, height=150)
    c.save()
    return pdf_filename

while True:
    eventos, valores = window.read()
    if eventos in (sg.WIN_CLOSED, "SAIR"):
        break
    elif eventos == "RESERVAR":
        ticket_info = informacao(valores)
        qr_code_file = gerar_qrcode(ticket_info)
        pdf_file = criar_pdf(ticket_info, qr_code_file)
        sg.popup(f"PDF gerado: {pdf_file}")
        sg.popup(informacao(valores))
window.close()