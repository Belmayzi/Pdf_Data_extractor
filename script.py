from operator import index
from pdf2image import convert_from_path
from pytesseract import image_to_string
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import pytesseract
import os
from os import listdir, walk
import shutil
from natsort import natsorted

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def convert_pdf_to_img(pdf_file):
    return convert_from_path(pdf_file, poppler_path=r'C:\Users\Yasser\Desktop\coding\python\Pdfextractor\poppler-0.68.0\bin')


def convert_image_to_text(file):

    text = image_to_string(file)

    return text


def get_text_from_any_pdf(pdf_file):

    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    for pg, img in enumerate(images):

        final_text += convert_image_to_text(img)

    return final_text


os.chdir('C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/Original_docs')

original_docs = os.listdir()


def find_first_page(Current_document):
    os.chdir(
        'C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/temporary_separated_docs/%s' % Current_document)
    global index_of_first_page, separated_docs

    separated_docs = natsorted(os.listdir())

    for i in separated_docs:
        path_to_pdf = "%s" % i
        pdftotxt = get_text_from_any_pdf(path_to_pdf)
        x = pdftotxt.find("Page 1")

        if x != -1:
            index_of_first_page = separated_docs.index(i)
            break


def find_number_of_pages(current_document):
    os.chdir(
        'C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/temporary_separated_docs/%s' % current_document)

    global number_of_pages, number_of_pages_index
    pdftotxt = get_text_from_any_pdf(separated_docs[index_of_first_page])
    find = 'Page 1 sur '
    x = pdftotxt.find(find)
    if x == -1:
        find = 'Page 1 sur'
    number_of_pages = int(pdftotxt[x+len(find)] + pdftotxt[x+len(find)+1])
    if index_of_first_page != 0:
        number_of_pages_index = index_of_first_page+number_of_pages
    else:
        number_of_pages_index = number_of_pages


def get_annexes(current_document):
    os.chdir(
        'C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/temporary_separated_docs/%s' % current_document)
    annexes_list = separated_docs[index_of_first_page+number_of_pages:]
    i = 0
    filtred_annexes = []
    while i < len(annexes_list):
        # find page string
        find = 'Page 1 sur '
        find2 = 'Page '
        pdftotxt = get_text_from_any_pdf(annexes_list[i])

        x = pdftotxt.find(find)

        if x == -1:
            find = 'Page 1 sur'
            x = pdftotxt.find(find)

        number_of_pages_annexe = int(
            pdftotxt[x+len(find)] + pdftotxt[x+len(find)+1])

        if number_of_pages_annexe > 1:
            index_of_first_page_annexe = annexes_list.index(annexes_list[i])

            # correct number of pages annexe
            skip = False
            correct = number_of_pages_index+index_of_first_page_annexe + \
                number_of_pages_annexe-number_of_pages_pdf
            if correct > 0:
                skip = True
                number_of_pages_annexe = number_of_pages_annexe-correct

            list_of_files_to_merge = annexes_list[index_of_first_page_annexe:
                                                  number_of_pages_annexe+index_of_first_page_annexe]

            # check if all pages of annexe are in the annex
            index_of_last_page = len(list_of_files_to_merge)-1
            last_page_of_annexe = get_text_from_any_pdf(
                list_of_files_to_merge[index_of_last_page])
            y = last_page_of_annexe.find(find2)

            actual_number_last_page_annexe = int(
                last_page_of_annexe[y+len(find2)] + last_page_of_annexe[y+len(find2)+1])

            if actual_number_last_page_annexe != number_of_pages_annexe:
                check = index_of_last_page
                while True:
                    check = check-actual_number_last_page_annexe
                    check_backwards = get_text_from_any_pdf(
                        list_of_files_to_merge[check])
                    check_backwards_page_number = int(
                        check_backwards[x+len(find)] + check_backwards[x+len(find)+1])
                    if check_backwards_page_number != number_of_pages_annexe:
                        actual_number_last_page_annexe = check_backwards_page_number
                    else:
                        i += check+1
                        break
            else:
                filtred_annexes.append(list_of_files_to_merge)
                i += number_of_pages_annexe

        else:
            filtred_annexes.append(annexes_list[i])
            i += 1
    os.chdir(
        'C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/Filtred_docs')
    file_name = "{}" .format(current_document)
    os.mkdir(current_document)

    i = 0
    while i < len(filtred_annexes):
        count = i+1
        annexe_name = "Annexe {} {}.pdf" .format(count, current_document)

        if isinstance(filtred_annexes[i], list):
            os.chdir(
                'C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/temporary_separated_docs/{}'.format(current_document))
            merger = PdfFileMerger()
            for pdf in filtred_annexes[i]:
                merger.append(pdf)
            with open("%s" % annexe_name, "wb") as outputStream:
                merger.write(outputStream)

            shutil.move("C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/temporary_separated_docs/{}/{}" .format(current_document, annexe_name),
                        "C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/Filtred_docs/{}/{}" .format(current_document, annexe_name))
        else:
            shutil.move("C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/temporary_separated_docs/{}/{}" .format(current_document,
                        filtred_annexes[i]), "C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/Filtred_docs/{}/{}" .format(current_document, annexe_name))
        i += 1


def separate_docs():
    global number_of_pages_pdf, document_name
    for doc in original_docs:
        inputpdf = PdfFileReader(open(doc, "rb"))
        os.chdir(
            'C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/temporary_separated_docs')

        document_name = '%s' % doc
        document_name = document_name.replace(".pdf", '')
        os.mkdir(document_name)

        number_of_pages_pdf = inputpdf.numPages
        for i in range(inputpdf.numPages):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))

            os.chdir(
                'C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/temporary_separated_docs/%s' % document_name)
            with open("doc%s.pdf" % i, "wb") as outputStream:
                output.write(outputStream)

        find_first_page(document_name)
        find_number_of_pages(document_name)
        get_annexes(document_name)
        os.chdir('C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/Original_docs')


separate_docs()
