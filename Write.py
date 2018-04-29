# -*- coding: utf-8 -*-
import PyPDF2
from reportlab.pdfgen import canvas
import io
from reportlab.pdfbase import pdfmetrics, ttfonts
import hmac
import hashlib
import base64

'''
Словарь схожих по написанию букв в английском и русском языке
{Английская: Русская}
'''
letter_dict = {'A':'А', 'a':'а', 'E':'Е', 'e':'е', 'T':'Т', 'O':'О', 'o':'о', 'P':'Р',
               'p':'р', 'H':'Н', 'K':'К', 'X':'Х', 'x':'х', 'C':'С', 'c':'с', 'B':'В', 'M':'М'}


def creat_key(login, password):
    bynary_line = []
    for el in hmac.new(b'1234567890', msg=(login + password).encode('utf-8'), digestmod=hashlib.md5).digest():
        s = str(bin(el))[2:]
        while len(s) < 8:
            s = '0' + s

        for elem in s:
            if elem == '1':
                bynary_line.append(1)

            else:
                bynary_line.append(0)

    return bynary_line


def replacement_letter(line, pointer_bynary, bynary_line):
    out_line = ''
    for el in line:
        if (el in letter_dict.keys()) and (pointer_bynary < len(bynary_line)):
            if bynary_line[pointer_bynary]:
                out_line += letter_dict[el]

            else:
                out_line += el

            pointer_bynary += 1

        else:
            out_line += el

    return out_line, pointer_bynary


def new_information(login, password):
    bynary_line = creat_key(login, password)
    pdfmetrics.registerFont(ttfonts.TTFont('Arial', 'arial.ttf'))
    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    can.setFont('Arial', 10)
    file = open('Text with stego.txt')
    next_line = 0
    pointer_bynary_line = 0
    for line in file:
        out_line, pointer_bynary_line = replacement_letter(line[:-1], pointer_bynary_line, bynary_line)
        can.drawString(10, 800 - next_line, out_line)
        next_line += 12

    print(pointer_bynary_line)
    file.close()
    can.showPage()
    can.save()
    packet.seek(0)
    new_pdf = PyPDF2.PdfFileReader(packet)
    return new_pdf


def main(in_file, login, password):
    new_pdf = new_information(login, password)
    in_pdf = PyPDF2.PdfFileReader(open(in_file, 'rb'))
    output = PyPDF2.PdfFileWriter()
    for i in range(in_pdf.getNumPages()):
        output.addPage(in_pdf.getPage(i))

    output.addPage(new_pdf.getPage(0))
    output.encrypt('Cypher_key')
    file = open('Test.pdf', 'wb')
    output.write(file)
    file.close()


if __name__ == '__main__':
    in_file = 'Base_PDF/idiot.pdf'
    login = 'Mikle'
    password = 'Qwer123'
    main(in_file, login, password)

