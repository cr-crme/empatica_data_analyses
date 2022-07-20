import os

from matplotlib import  pyplot as plt

from .enums import DataType


class PlotUtils:
    @staticmethod
    def savefig(path_folder: str, fig: plt.figure, data_type: DataType, postfix: str):
        if fig is None:
            return

        fig.legend()
        fig.set_size_inches(16, 9)
        if not os.path.isdir(path_folder):
            os.mkdir(path_folder)
        fig.savefig(f"{path_folder}/{data_type.value}_{postfix}.png", dpi=300)

    @staticmethod
    def add_legend(fig: plt.figure):
        if fig is None:
            return
        fig.legend()

    @staticmethod
    def show():
        plt.show()
