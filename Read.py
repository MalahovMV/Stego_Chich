import PyPDF2
import sys
from reportlab.pdfgen import canvas
import io


def main():
    in_pdf = PyPDF2.PdfFileReader(open('Test.pdf', 'rb'))
    page = in_pdf.getPage(in_pdf.getNumPages() - 1).extractText()
    string = ''
    for el in page:
        string += hex(ord(el)) + ' '

    print(string)


if __name__ == '__main__':
    main()