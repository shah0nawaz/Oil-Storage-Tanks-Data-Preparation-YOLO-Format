import os
import pandas as pd
import numpy as np
import cv2
import glob
import argparse
import warnings
import shutil
warnings.simplefilter(action='ignore', category=FutureWarning)


def filter_anno(x,y, img_data, crop_size = (640,640)):
	x1 = x
	y1 = y
	x2 = x + crop_size[0]
	y2 = y + crop_size[1]

	df1 = img_data[img_data['x1']<=x2]
	df2 = df1[df1['x2'] >= x1]
	df3 = df2[df2['y1'] <= y2]
	df4 = df3[df3['y2'] >= y1]

	return df4


def trim_localize_normalize_bbox(df,x_img,y_img, img_name, opt):
	txt_name = img_name.split('.')[0]
	with open(opt.save_annotations + txt_name + '.txt', 'w') as f:
		for idx in range(len(df)):
			bbox = df.iloc[idx,:]
			x1 = bbox.x1
			x2 = bbox.x2

			y1 = bbox.y1
			y2 = bbox.y2

			if x1 < x_img:
				x1 = x_img
			if x2 > (x_img+opt.crop_size[0]):
				x2 = x_img+opt.crop_size[0]
			if y1<y_img:
				y1 = y_img
			if y2 >= (y_img + opt.crop_size[1]):
				y2 = y_img + opt.crop_size[1]

			w = x2-x1
			h = y2-y1
			x_center = ((x1 + w//2) - x_img)/opt.crop_size[0]
			y_center = ((y1 + h//2) - y_img)/opt.crop_size[0]
			w = w/opt.crop_size[0]
			h = h/opt.crop_size[0]
			bbox = [x_center, y_center, w, h]
			bbox = [str(x) for x in bbox]
			bbox = ' '.join(bbox)
			label = str(0) + ' ' + bbox + '\n'
			f.write(label)


def croping(img,df_img,name, opt):
	count = 0
	for y in range(0,img.shape[0]-opt.stride, opt.stride):
		for x in range(0, img.shape[1]-opt.stride, opt.stride):
			print(y,x)
			count +=1
			img_name = ''
			image_data = df_img
			if x + opt.crop_size[0] > img.shape[1]:
				diff = img.shape[1]-x
				add_value = opt.crop_size[0] - diff
				x = x - add_value
				crop_img = img[y:y + opt.crop_size[1], x:x + opt.crop_size[1]]
				df = filter_anno(x,y,image_data)

			elif y + opt.crop_size[1] > img.shape[0]:
				diff = img.shape[0]-y
				add_value = opt.crop_size[0] - diff
				y = y - add_value
				crop_img = img[y:y + opt.crop_size[1], x:x + opt.crop_size[1]]
				df = filter_anno(x, y, image_data)

			elif (x + opt.crop_size[1] > img.shape[1]) and (y + opt.crop_size[1] > img.shape[0]) :

				diff = img.shape[1] - x
				add_value = opt.crop_size[0] - diff
				x = x - add_value

				diff = img.shape[0]-y
				add_value = opt.crop_size[0] - diff
				y = y - add_value
				crop_img = img[y:y + opt.crop_size[1], x:x + opt.crop_size[1]]
				df = filter_anno(x, y, image_data)
			else:
				crop_img = img[y:y + opt.crop_size[1], x:x + opt.crop_size[1]]
				df = filter_anno(x, y, image_data)
			img_name = name + '_'+str(y) +'_'+ str(x) + '.jpg'
			print(f'crop image data {len(df)}, {img_name}, {df}')
			if len(df) ==0:
				copy_name = img_name
				txt_name = copy_name.split('.')[0]
				with open(opt.save_annotations + img_name.split('.')[0] + '.txt', 'w') as f:
					f.write('')
				cv2.imwrite(opt.saved_crops+ img_name, crop_img)
			else:
				trim_localize_normalize_bbox(df,x,y,img_name, opt)
				cv2.imwrite(opt.saved_crops +  img_name , crop_img)


def read_df(annotations):
	df = pd.read_csv(annotations)
	g = df.groupby('image_id')
	return g


def main(opt):

	if os.path.exists(opt.saved_crops):
		shutil.rmtree(opt.saved_crops)
		os.mkdir(opt.saved_crops)
	else:
		os.mkdir(opt.saved_crops)

	if os.path.exists(opt.save_annotations):
		shutil.rmtree(opt.save_annotations)
		os.mkdir(opt.save_annotations)
	else:
		os.mkdir(opt.save_annotations)

	g = read_df(opt.annotations)
	for g1,g2 in g:
		name = g1
		img = cv2.imread(opt.input_images+ g1 + '.jpg')
		df_bbox = pd.DataFrame(columns = ['x1','y1','x2','y2'])
		for idx, row in g2.iterrows():
			row = row.bounds
			row = row[1:-1]
			row = [int(x) for x in row.split(', ')]
			df_bbox = df_bbox.append(pd.Series(row, index = ['x1','y1','x2','y2']), ignore_index = True)
		croping(img, df_bbox, name, opt)


if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--input_images', type=str, default='images/', help='path to the large input images')
	parser.add_argument('--saved_crops', type=str, default='crops/', help='path to crops directory')
	parser.add_argument('--annotations', type=str, default='annotations.csv', help='path to annotations file')
	parser.add_argument('--crop_size', type=tuple, default=(640,640), help='cropped image dimenssions')
	parser.add_argument('--stride', type=int, default=500, help='crop overlap')
	parser.add_argument('--save_annotations', type=str, default='annotations/', help='crops annotations path')
	opt = parser.parse_args()
	main(opt)

