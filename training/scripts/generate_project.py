import sys
import getopt
import os


def main(argv):

    try:
        opts, args = getopt.getopt(argv, '', ['name='])
    except getopt.GetoptError:
        print('generate_project.py --name=<project_name>')

    for opt, arg in opts:
        if opt == '--name':
            print(f'Creating new project, {arg}')
            os.mkdir(f'./workspace/{arg}')
            os.chdir(f'./workspace/{arg}')
            os.mkdir('./annotations')
            os.mkdir('./models')
            os.mkdir('./exported_models')
            os.mkdir('./images')
            sys.exit()

    print('generate_project.py --name=<project_name>')


if __name__ == '__main__':
    main(sys.argv[1:])
