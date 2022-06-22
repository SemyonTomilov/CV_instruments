# CV_instruments

### yolo_annnotation_info
 
```python .\yolo_annotation_info.py <path_to_imgs> <class_names_txt>```  
```<path_to_imgs>``` - Path to directories containing images and their annotations.   
```<class_names_txt>(optional)``` - Path to a text file with class names. If the parameter is omitted, class indexs will be displayed instead of class names.  

Displays the following information about the dataset (yolo format):
total number of images (with bboxes and without bboxes), total number of bboxes,
resolution information of images ad bboxes(min, max, mean resolution of images and  bboxes),
number of each class.