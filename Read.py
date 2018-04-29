import PyPDF2
import hmac
import hashlib

letter_dict = {'A':'А', 'a':'а', 'E':'Е', 'e':'е', 'T':'Т', 'O':'О', 'o':'о', 'P':'Р',
               'p':'р', 'H':'Н', 'K':'К', 'X':'Х', 'x':'х', 'C':'С', 'c':'с', 'B':'В', 'M':'М'}


def extraction_inf(symbol):
    if ord(symbol) > 256:
        return 1

    elif symbol in letter_dict.keys():
        return 0

    else:
        return 2


def calc_check_inf(login, password):
    check_line = ''
    for el in hmac.new(b'1234567890', msg=(login + password).encode('utf-8'), digestmod=hashlib.md5).digest():
        s = str(bin(el))[2:]
        while len(s) < 8:
            s = '0' + s

        check_line += s

    return check_line


def main(login, password):
    check_line = calc_check_inf(login, password)
    in_pdf = PyPDF2.PdfFileReader(open('Test.pdf', 'rb'))
    in_pdf.decrypt('Cypher_key')
    page = in_pdf.getPage(in_pdf.getNumPages() - 1).extractText()
    string = ''
    for el in page:
        flag = extraction_inf(el)
        if flag < 2:
            string += str(flag)

    if string[:128] == check_line:
        output = PyPDF2.PdfFileWriter()
        for i in range(in_pdf.getNumPages()):
            output.addPage(in_pdf.getPage(i))

        file = open('Ready_PDF.pdf', 'wb')
        output.write(file)
        file.close()

    else:
        print('Неудача')


if __name__ == '__main__':
    login = 'Mikle'
    password = 'Qwer123'
    main(login, password)