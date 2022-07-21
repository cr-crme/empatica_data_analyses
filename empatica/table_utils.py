import os
import sys

from .empatica_reader import EmpaticaReader


class TableUtils:
    @staticmethod
    def print_document_header(path_folder: str):
        elements = TableUtils.prepare_to_print(path_folder)
        EmpaticaReader.print_document_header()
        return elements

    @staticmethod
    def print_document_tail(elements):
        EmpaticaReader.print_document_tail()
        TableUtils.finish_to_print(*elements)

    @staticmethod
    def prepare_to_print(path_folder):
        orig_stdout = sys.stdout

        if not os.path.isdir(path_folder):
            os.mkdir(path_folder)

        f = open(f"{path_folder}/tables.tex", 'w')
        sys.stdout = f
        return f, orig_stdout

    @staticmethod
    def finish_to_print(f, orig_stdout):
        sys.stdout = orig_stdout
        f.close()
