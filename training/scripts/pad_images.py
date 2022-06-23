import os
import sys
import getopt
import glob
import cv2 as cv


def pad_images(img_dir):
    os.chdir(img_dir)

    files = glob.glob('*.jpg') + glob.glob('*.png') + glob.glob('*.jpeg')
    count = 0
    total = len(files)

    for file in files:
        img = cv.imread(file)

        rows = img.shape[0]
        cols = img.shape[1]

        if cols > rows:
            diff = cols - rows
            img = cv.copyMakeBorder(img, 0, diff, 0, 0, cv.BORDER_CONSTANT, (0, 0, 0))
        elif rows > cols:
            diff = rows - cols
            img = cv.copyMakeBorder(img, 0, 0, 0, diff, cv.BORDER_CONSTANT, (0, 0, 0))

        count += 1
        cv.imwrite(file, img)
        print(f'{count} of {total} images padded')


def main(argv):
    # TODO - Arguments
    try:
        opts, args = getopt.getopt(argv, '', ['img_dir='])
    except getopt.GetoptError:
        print('generate_project.py --img_dir=<project_name>')

    for opt, arg in opts:
        if opt == '--img_dir':
            pad_images(arg)

    print('generate_project.py --img_dir=<project_name>')


if __name__ == '__main__':
    main(sys.argv[1:])
