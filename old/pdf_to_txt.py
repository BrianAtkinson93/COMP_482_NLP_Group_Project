import os
import PyPDF2
import sys
import pdfplumber


def convert(file):
    base, ext = os.path.splitext(file)
    out_name = base + '.txt'

    print(f'Opening: {file}...')
    with pdfplumber.open(file) as pdf:
        text = ''

        for i, page in enumerate(pdf.pages):
            print(f'page: {i}...')
            text += page.extract_text() + "\n"

        with open(out_name, 'w', encoding='utf-8') as of:
            of.write(text)


def main():
    for file in os.listdir('../GroupProject/docs'):
        convert(f"../GroupProject/docs/{file}" )


if __name__ == "__main__":
    main()
