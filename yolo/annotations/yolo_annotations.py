#YOLO format of annotations
'''
It's .txt-file with the same name as image-file, but with .txt-extension.
Structure: <object_class> <x_center> <y_center> <width> <height>
- <object_class> - integer object number from 0 to (classes - 1)
- <x_center> = <absolute_x> / <image_width>
- <y_center> = <absolute_y> / <image_height>
- <width> = <absolute_width> / <image_width>
- <height> = <absolute_height> / <image_height>
- <x_center> <y_center> - are center of rectangle
'''

#Class of annotation yolo format
class bbox_yolo():
    def __init__(self, object_class, x_center, y_center, width, height):
        self.object_class = object_class
        self.x_center = x_center
        self.y_center = y_center
        self.width = width
        self.height = height

#Function for getting yolo format annotations as a two-dimensional array from a text file
def get_yolo_annotations(txt_file):
    boxes = []
    with open(txt_file, 'r') as yolo_txt:
        for line in yolo_txt.readlines():
            line = line.strip('\n').split(' ')
            boxes.append(bbox_yolo(int(line[0]),
                                   float(line[1]),
                                   float(line[2]),
                                   float(line[3]),
                                   float(line[4])))
    return boxes

#Function for getting a dictionary of class names (index - name)
def get_dict_class_names(txt_file):
    names = {}
    with open(txt_file, 'r') as class_names_txt:
        for id_class, class_name in enumerate(class_names_txt.readlines()):
            names[id_class] = class_name.strip('\n')

    return names

