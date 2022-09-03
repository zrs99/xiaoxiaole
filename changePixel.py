from PIL import Image


def produceImage(file_in, width, height, file_out):
    image = Image.open(file_in)
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    resized_image.save(file_out)


if __name__ == '__main__':
    width = 900
    height = 670
    for i in range(1, 13):
        file_in = './images/背景1.jpg'
        file_out = './images/背景1.png'
        produceImage(file_in, width, height, file_out)
