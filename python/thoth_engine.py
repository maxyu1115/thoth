import argparse

parser = argparse.ArgumentParser(description='Run the thoth pipeline. ')
parser.add_argument('--vid', type=str, help='location of the video')
parser.add_argument('--target', type=str, help='location of output folder')

args = parser.parse_args()

def main():
    # do stuff here

if __name__ == '__main__':
    main()