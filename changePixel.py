from PIL import Image


def produceImage(file_in, width, height, file_out):
    image = Image.open(file_in)
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    resized_image.save(file_out)


if __name__ == '__main__':
    width = 47
    height = 47
    for i in range(1, 13):
        file_in = 'D:\Programs\images\image3\%s.png'%i
        file_out = './images/%s.png'%i
        produceImage(file_in, width, height, file_out)
