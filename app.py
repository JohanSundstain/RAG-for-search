import os

import numpy as np

from config import config
from db import texts_interface
from embedder import embeder_model

def upload():
	pass


def main():
	# чтение данных из таблицы

	texts = texts_interface.get_all_texts()	

	for i in texts:
		print(i.pk_id)

if __name__ == "__main__":
    main()
