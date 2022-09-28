# Oil-Storage-Tanks-Data-Preparation-YOLO-Format

# Introduction
Object detection algorithms can not input large dimenssions satellite images during training and testing. In order to prepare the satellite imagery for object detection algorithms, it is needed to crop the images into small patches according the requirments of the algorithm. This repository will help you to crop the images as well annotations according to the algorithm requirments.


# About Dataset
Aboveground Petroleum, Oil and Lubricant (POL) storage areas are common in the manufacturing industry and government facilities. It is also a critical infrastructure for transportation (vehicles, ships and aircrafts) and industry (refineries, power stations, manufacturing). Deep Learning can be used to detect automatically the number, size and type of POL storage present on a site. This can help monitoring the state of aboveground fuel storage tanks including the prevention of spills, overfills, and corrosion.


# Imagery for training
The images folder contains 98 extract of SPOT imagery at roughly 1.2 meters resolution. Each each image is stored as a JPEG file of size 2560 x 2560 pixels (i.e. 3 kilometers on ground). The locations are selected worldwide.

# Annotations
All aircrafts have been annotated with bounding boxes on the provided imagery. The annotations are provided in the form of closed GeoJSON polygons. A CSV file named annotations.csv provides all anotations - one annotation per line with the corresponding filename of the image as image_id and the class of the annotation, mainly oil-storage-tank.


# Extra imagery
A folder named extras contains 5 extra images which are not annotated but could be used to visually test a model on new - unseen before - images.

# Dataset Directory
  ```
    -- oil storage tanks dataset 
      - images
      - extras
        annotations.csv
  ```
  
  ```
  python image&annotations_cropping_Tool.py 
  ```
  
  In order to check the correctness of the procedure, you can plot the cropped annotations on cropped images.
```
python plot_to_check.py
```


# Original Image
![alt text](https://github.com/shah0nawaz/Oil-Storage-Tanks-Data-Preparation-YOLO-Format/blob/main/plots/1cdf51ee-e753-437f-b22f-7fcd7e9e2bfe.jpg)
# Original Image with labels
![alt text](https://github.com/shah0nawaz/Oil-Storage-Tanks-Data-Preparation-YOLO-Format/blob/main/plots/1cdf51ee-e753-437f-b22f-7fcd7e9e2bfe_result.jpg)

## Overlapping crops of the image
![alt text](https://github.com/shah0nawaz/Oil-Storage-Tanks-Data-Preparation-YOLO-Format/blob/main/plots/Drawing1.png)
## Overlapping crops with labels
![alt text](https://github.com/shah0nawaz/Oil-Storage-Tanks-Data-Preparation-YOLO-Format/blob/main/plots/Drawing2.png)

