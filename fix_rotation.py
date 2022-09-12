from PIL import Image
import sys

def fix_rotation(degree, file):
    image = Image.open(file)

    rotated = image.rotate(angle=int(degree), expand=True)

    rotated.save(file)

def main():
    fix_rotation(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
    