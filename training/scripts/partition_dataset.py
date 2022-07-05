import os
import glob
import random
import shutil


if __name__ == '__main__':
    os.chdir('./images/')
    os.mkdir('test', 0o777)
    os.mkdir('train', 0o777)

    os.chdir('./imgs/')
    files = glob.glob('*.jpg') + glob.glob('*.png') + glob.glob('*.jpeg')
    os.chdir('..')
    total = len(files)
    train_index = int(total * 0.9)  # TODO - Make this a parameter we pass

    random.shuffle(files)

    train_imgs = files[:train_index]
    test_images = files[train_index:]

    count = train_index
    done = 0
    print('Copying training images')
    for img in train_imgs:
        file_name = img.split('.')[:-1]
        file_name.append('xml')
        xml = '.'.join(file_name)

        shutil.copyfile(f'imgs/{img}', f'train/{img}')
        shutil.copyfile(f'imgs/{xml}', f'train/{xml}')

        done += 1
        print(f'Copied {done} of {count}')

    count = total - train_index
    done = 0
    print('Copying test images')
    for img in test_images:
        file_name = img.split('.')[:-1]
        file_name.append('xml')
        xml = '.'.join(file_name)

        shutil.copyfile(f'imgs/{img}', f'test/{img}')
        shutil.copyfile(f'imgs/{xml}', f'test/{xml}')

        done += 1
        print(f'Copied {done} of {count}')