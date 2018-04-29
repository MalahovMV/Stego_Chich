import PyPDF2
import sys
from reportlab.pdfgen import canvas
import io


letter_dict = {'A':'А', 'a':'а', 'E':'Е', 'e':'е', 'T':'Т', 'O':'О', 'o':'о', 'P':'Р',
               'p':'р', 'H':'Н', 'K':'К', 'X':'Х', 'x':'х', 'C':'С', 'c':'с', 'B':'В', 'M':'М'}


def extraction_inf(symbol):
    if ord(symbol) > 256:
        return 1

    elif symbol in letter_dict.keys():
        return 0

    else:
        return 2

def main():
    in_pdf = PyPDF2.PdfFileReader(open('Test.pdf', 'rb'))
    page = in_pdf.getPage(in_pdf.getNumPages() - 1).extractText()
    string = ''
    for el in page:
        flag = extraction_inf(el)
        print(ord(el))
        if flag < 2:
            string += str(flag)

    print(string)


if __name__ == '__main__':
    main()