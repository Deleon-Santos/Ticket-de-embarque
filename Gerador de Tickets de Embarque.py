#Estou desenvolvendo um gerenciador de Ticket de passagens aereas ou embarques por vias terrestres
#O objetivo é gerar um QRcode e imprimir num PDF com as informações do passageiro 
import PySimpleGUI as sg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
sg.SetOptions(background_color='#363636', text_element_background_color='#363636', element_background_color='#363636', scrollbar_color=None, input_elements_background_color='#F7F3EC', button_color=('white', '#4F4F4F'))

col1=[[sg.Listbox(["São Paulo","Rio de Janeiro","Maceio","Curitiba","Paraiba","Porto Seguro","Manaus","Belém","São Luiz"],
                    size=(50,5),font=('Any',11),select_mode="single",key="-DESTINO-")],]
#col2=[[sg.Image(filename="Jotchua.jpeg",size=(400,100))],]

layout=[
        [sg.Text("Nome Completo:",size=(10,1),font=('Any',10))],
        [sg.Input("João Ferreira de Souza",key="-NOME-",do_not_clear=True,size=(32,1),font=('Any',18))],
        [sg.Text("N° Passaporte",size=(30,1)),sg.T('Sexo')],
        [sg.Input("123456789-9",key="-PASSAPORTE-",do_not_clear=True,size=(18,1),font=('Any',18)),
         sg.Radio("Masculino","RADIO",key="-masculino-",default=True),sg.Radio("Feminino","RADIO",key="-feminino-")],
        [sg.T("Embarque",size=(26,1)),sg.T("Retorno")],
        [sg.CalendarButton("Data",size=(5,1),font=('Any',9),close_when_date_chosen=True,target="-partida-",location=(0,0),no_titlebar=False),
         sg.Input("2024-04-16 19:13:13",key="-partida-",size=(18,1),font=('Any',11)),sg.Push(),
        sg.CalendarButton("Data",size=(5,1),font=('Any',9),close_when_date_chosen=True,target="-retorno-",location=(0,0),no_titlebar=False),
         sg.Input("2024-04-16 19:13:13",key="-retorno-",size=(18,1),font=('Any',11))],
        [sg.Text("Lista de Destinos")],
        [sg.Col(col1)],
        
        [sg.Button("RESERVAR"),sg.Button("SAIR")],]

window=sg.Window("PASSAGEIRO",layout)

#A função "informação" revebe os valores e formata em uma unica strig
def informacao(valores):
    informacao = f" TICKET DE EMBARQUE\n\n"
    informacao += f" Name Completo:{valores['-NOME-']}\n"
    informacao += f" Numero do Passaporte:{valores['-PASSAPORTE-']}\n"
    informacao += f" Genero:{'Feminino' if valores['-feminino-'] else 'Masculino'}\n"
    
    informacao += f" Data de Partida: {valores['-partida-']}\n"
    informacao += f" Data de Retorno: {valores['-retorno-']}\n"
    informacao += f" Destino : {valores['-DESTINO-'] [0]} \n"
    informacao += f"""

Aqui estão alguns exemplos de termos de uso comuns em passagens aéreas relacionados a políticas
de cancelamento e alterações de voo:

Políticas de Cancelamento:

Os cancelamentos de voos  estão sujeitos  a  taxas, que  variam de  acordo com o tipo de tarifa 
adquirida e o momento do cancelamento.
As taxas de cancelamento podem ser aplicadas se o passageiro decidir cancelar a reserva após um 
determinado prazo da compra ou próxima à data do voo.
Em alguns casos, as tarifas não são reembolsáveis ​e podem resultar na perda total do valor pago 
em caso de cancelamento.

Alterações de Voo:

As alterações na data, horário ou rota do voo podem estar sujeitas a taxas e restrições.
As tarifas com mais flexibilidade geralmente permitem alterações com menos restrições, enquanto 
tarifas mais econômicas podem ter políticas mais rígidas quanto a alterações.
Alterações estão sujeitas à disponibilidade e podem ser permitidas apenas dentro de um  período 
específico antes da partida do voo.

Reembolsos:

Os reembolsos  totais ou  parciais podem ser  oferecidos em  determinadas  circunstâncias, como 
cancelamento  do  voo pela  companhia  aérea  ou  de acordo com os termos específicos da tarifa 
adquirida.
Em alguns casos, o valor do  reembolso  pode  ser  reduzido  devido  a  taxas  de  cancelamento 
aplicáveis.

Restrições de Tarifas:

Diferentes tipos de tarifas têm diferentes políticas de cancelamento e alteração.
Tarifas mais flexíveis geralmente permitem alterações com menos restrições,  enquanto  tarifas 
mais econômicas podem ter políticas mais restritivas.
"""
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
    c.setFont("Helvetica-Bold", 18)
    title_text = "TICKET DE EMBARQUE"
    title_width = c.stringWidth(title_text, "Helvetica-Bold", 18)
    c.drawString((letter[0] - title_width) / 2, 750, title_text)

    c.setFont("Helvetica", 12)
    text_object = c.beginText(50, 650)
    text_object.textLines(content)
    c.drawText(text_object)

    c.drawInlineImage(qr_filename, 430, 530, width=150, height=150)

    c.save()
    return pdf_filename

while True:
    try:
        eventos, valores = window.read()
        if eventos in (sg.WIN_CLOSED, "SAIR"):
            break
        
        elif eventos == "RESERVAR":
            
            ticket_info = informacao(valores)
            qr_code_file = gerar_qrcode(ticket_info)
            pdf_file = criar_pdf(ticket_info, qr_code_file)
            sg.popup(f"PDF gerado: {pdf_file}")
            
    except Exception as e:
        sg.popup(f'Erro{e}')
window.close()