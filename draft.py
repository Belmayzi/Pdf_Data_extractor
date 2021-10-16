import os

os.chdir(
    'C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/Original_docs')

original_docs = os.listdir()

for i in original_docs:
    os.chdir(
        'C:/Users/Yasser/Desktop/coding/python/GET_ANNEXES/temporary_separated_docs')
    document_name = '%s' % i
    print(document_name.replace(".pdf", ''))
