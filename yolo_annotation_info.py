from yolo.annotations.annotation_info import annotation_yolo_info
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_imgs", type=str, help="Path to annotatoins and images.")
    parser.add_argument('-cn', '--class_names', type=str, default=None, help="Path to txt file with class names.")
    args = parser.parse_args()

    if(os.path.isdir(args.path_to_imgs)):
        if(args.class_names is None):
            annotation_yolo_info(args.path_to_imgs)
        else:
            if(os.path.isfile(args.class_names)):
                annotation_yolo_info(args.path_to_imgs, args.class_names)
            else:
                print("The path does not exists or is not file: {}".format(args.class_names))
    else:
        print("The path does not exist or is not directory: {}".format(args.path_to_imgs))


if __name__ == "__main__":
    main()