from .yolo_annotations import bbox_yolo, get_yolo_annotations, get_dict_class_names
import os
IMAGES_EXT = ['.png', '.jpg']
import sys
import pandas as pd
from PIL import Image

def annotation_yolo_info(direcotry_path_annotation_and_imgs, path_class_names_txt = None):

    #Images
    amount_imgs = 0
    amount_with_bboxes = 0
    amount_without_bboxes = 0

    #Image resolution info
    min_width_imgs = 10000
    max_width_imgs = -10000
    mean_width_imgs = 0

    min_height_imgs = 10000
    max_height_imgs = -10000
    mean_height_imgs = 0

    #Bounding boxes
    total_amount_boxes = 0
    amount_classes = {}

    #Bounding boxes resolution info
    min_width_bbox = 10000
    max_width_bbox = -10000
    mean_width_bbox = 0

    min_height_bbox = 10000
    max_height_bbox = -10000
    mean_height_bbox = 0

    imgs_without_annotation = []

    couples = set()

    for subdirectory in os.walk(direcotry_path_annotation_and_imgs):
        #Gathering a list of images
        for file in os.listdir(subdirectory[0]):
            filename, file_ext = os.path.splitext(file)
            if(file_ext in IMAGES_EXT):
                if(os.path.exists(subdirectory[0] + os.sep + filename + ".txt")):
                    couples.add((subdirectory[0] + os.sep + filename, file_ext))
                    with open(subdirectory[0] + os.sep + filename + '.txt') as file_txt:
                        tmp_amount_line = 0
                        for _ in file_txt.readlines():
                            tmp_amount_line += 1
                        if(tmp_amount_line == 0):
                            amount_without_bboxes += 1
                        else:
                            amount_with_bboxes += 1
                else:
                    imgs_without_annotation.append(subdirectory[0] + os.sep + filename + file_ext)

    amount_imgs = len(couples)
    tmp_counter = 0
    #Image resolution info
    for img, img_ext in couples:
        tmp_counter += 1
        sys.stdout.write("\rComputing information about images: {0}%".format(str(round((tmp_counter / amount_imgs) * 100, 2))))
        img = Image.open(img + img_ext)
        width, height = img.size
        if(width < min_width_imgs):
            min_width_imgs = width
        if(height < min_height_imgs):
            min_height_imgs = height
        if(width > max_width_imgs):
            max_width_imgs = width
        if(height > max_height_imgs):
            max_height_imgs = height
        mean_height_imgs += height
        mean_width_imgs += width
    sys.stdout.write('\n')
    mean_height_imgs = mean_height_imgs / amount_imgs
    mean_width_imgs = mean_width_imgs / amount_imgs

    max_height_imgs = int(max_height_imgs)
    min_height_imgs = int(min_height_imgs)
    max_width_imgs = int(max_width_imgs)
    min_width_imgs = int(min_width_imgs)
    mean_width_imgs = int(mean_width_imgs)
    mean_height_imgs = int(mean_height_imgs)

    #Bounding boxes info
    class_names = {}
    if(path_class_names_txt is not None):
        class_names = get_dict_class_names(path_class_names_txt)
        for id_class in class_names:
            amount_classes[id_class] = 0
    tmp_counter = 0
    for img, img_ext in couples:
        tmp_counter += 1
        sys.stdout.write("\rComputing information about bonding-boxes: {0}%".format(str(round((tmp_counter / amount_imgs) * 100, 2))))
        width, height = Image.open(img + img_ext).size

        tmp_bboxes = get_yolo_annotations(img + ".txt")
        for box in tmp_bboxes:
            total_amount_boxes += 1
            if(path_class_names_txt is not None):
                amount_classes[box.object_class] += 1
            else:
                if(box.object_class in amount_classes):
                    amount_classes[box.object_class] += 1
                else:
                    amount_classes[box.object_class] = 0
                    amount_classes[box.object_class] += 1

            if (box.width * width < min_width_bbox):
                min_width_bbox = box.width * width
            if (box.height * height < min_height_bbox):
                min_height_bbox = box.height * height
            if (box.width * width > max_width_bbox):
                max_width_bbox = box.width * width
            if (box.height * height > max_height_bbox):
                max_height_bbox = box.height * height
            mean_height_bbox += box.height * height
            mean_width_bbox += box.width * height
    mean_height_bbox = mean_height_bbox / total_amount_boxes
    mean_width_bbox = mean_width_bbox / total_amount_boxes
    print("\n")
    max_height_bbox = int(max_height_bbox)
    min_height_bbox = int(min_height_bbox)
    max_width_bbox = int(max_width_bbox)
    min_width_bbox = int(min_width_bbox)
    mean_width_bbox = int(mean_width_bbox)
    mean_height_bbox = int(mean_height_bbox)
    amount_classes_copy = amount_classes.copy()
    amount_classes = ""
    for id_class in amount_classes_copy:
        if(path_class_names_txt is None):
            amount_classes += "-" + str(id_class) + ": " + str(amount_classes_copy[id_class]) + "\n"
        else:
            amount_classes += "-" + str(class_names[id_class]) + ": " + str(amount_classes_copy[id_class]) + "\n"

    sys.stdout.write("Total number of images: {0} (With bboxes {1}, without bboxes {2})\n".format(amount_imgs, amount_with_bboxes, amount_without_bboxes))
    sys.stdout.write("Total number of bbox: {0}\n".format(total_amount_boxes))
    sys.stdout.write("\nResolution information:\n")
    df = pd.DataFrame([[min_width_imgs, min_height_imgs, min_width_bbox, min_height_bbox],
                       [max_width_imgs, max_height_imgs, max_width_bbox, max_height_bbox],
                       [mean_width_imgs, mean_height_imgs, mean_width_bbox, mean_height_bbox]],
                        index = ['min', 'max', 'mean'],
                        columns = ["width(img)", 'height(img)', 'width(bbox)', 'height(bbox)'])
    sys.stdout.write(df.to_string())
    sys.stdout.write("\n\nNumber of classes:\n{0}".format(amount_classes))