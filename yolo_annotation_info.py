from yolo.annotations.annotation_info import annotation_yolo_info
import sys

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        if(len(sys.argv) == 2):
            annotation_yolo_info(sys.argv[1])
        elif(len(sys.argv) == 3):
            annotation_yolo_info(sys.argv[1], sys.argv[2])