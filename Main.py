import PyPDF2
import sys
from reportlab.pdfgen import canvas
import io

standart_mask = '''This\xa0file was automate created.\xa0
This\xa0book is protected.\xa0Project made students IU8.
'''


def new_information():
    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    can.drawString(10, 800, standart_mask)
    can.save()
    packet.seek(0)
    new_pdf = PyPDF2.PdfFileReader(packet)
    return new_pdf


def main(in_file):
    new_pdf = new_information()
    text_page = new_pdf.getPage(0).extractText()
    in_pdf = PyPDF2.PdfFileReader(open(in_file, 'rb'))
    output = PyPDF2.PdfFileWriter()
    for i in range(in_pdf.getNumPages()):
        output.addPage(in_pdf.getPage(i))

    output.addPage(new_pdf.getPage(0))
    file = open('Test.pdf', 'wb')
    #output.encrypt('qwerty')
    output.write(file)
    file.close()
    string = ''
    for el in text_page:
        string += hex(ord(el)) + ' '

    print(string)


if __name__ == '__main__':
    in_file = sys.argv[1]
    main(in_file)
    #file = open('Test.pdf', 'a')
    #s = 'sdfgsdhsdghgh'
    #file.write(s)
    #file.close()