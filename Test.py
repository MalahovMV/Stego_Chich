import PyPDF2
import sys
import io
from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter


def main(in_file):
    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    can.drawString(10, 100, "Hello world")
    can.save()

    packet.seek(0)
    new_pdf = PyPDF2.PdfFileReader(packet)
    existing_pdf = PyPDF2.PdfFileReader(open(in_file, 'rb'))
    output = PyPDF2.PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    outputStream = open("dest.pdf", 'wb')
    output.write(outputStream)
    outputStream.close()



if __name__ == '__main__':
    in_file = sys.argv[1]
    main(in_file)
