from PyQt5.QtWidgets import QApplication

app = QApplication([])


def run():
    # app.exec()

    # It's a test
    from sf_app.logic import compress_huffman, decompress
    with open("test.txt", "rb") as if_stream, open("test.bin", "wb") as of_stream:
        compress_huffman(if_stream, of_stream, "test.txt")
    with open("test.bin", "rb") as if_stream, open("test2.txt", "wb") as of_stream:
        print(decompress(if_stream, of_stream))
