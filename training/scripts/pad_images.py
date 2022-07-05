import os
import glob
import cv2 as cv


if __name__ == '__main__':
    os.chdir('./images/imgs')

    # NOTE - Only JPG files work
    files = glob.glob('*.jpg')
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
