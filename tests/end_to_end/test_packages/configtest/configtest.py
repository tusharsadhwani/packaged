import os.path

from PIL import Image


def main():
    with Image.open(os.path.join(os.path.dirname(__file__), "testimage.jpg")) as img:
        print(img.getbands())
        cmyk_img = img.convert("CMYK")
        print(cmyk_img.getbands())


if __name__ == "__main__":
    main()
