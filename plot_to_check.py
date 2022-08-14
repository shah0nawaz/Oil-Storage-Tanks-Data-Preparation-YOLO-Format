import cv2
import glob
import argparse


def main(opt):

	for fil in sorted(glob.glob(opt.saved_crops + '*.jpg')):
		img = cv2.imread(fil)
		txt_name = fil.split('/')[-1].split('.')[0]
		f = open(opt.save_annotations + txt_name + '.txt', 'r')
		print(f'image name {txt_name}')
		for f1 in f.readlines():
			f2 =f1.split(' ')
			top_left_x = (float(f2[1]) * opt.crop_size[0]) - ((float(f2[3]) * opt.crop_size[0])/2)
			top_left_y = (float(f2[2]) * opt.crop_size[1]) - ((float(f2[4]) * opt.crop_size[1])/2)

			right_botom_x = (float(f2[1]) * opt.crop_size[0]) + ((float(f2[3]) * opt.crop_size[0])/2)
			right_botom_y= (float(f2[2]) *opt.crop_size[1]) + ((float(f2[4]) * opt.crop_size[0])/2)

			cv2.rectangle(img, (int(top_left_x),int(top_left_y)), (int(right_botom_x), int(right_botom_y)),(0,127,255),7 )

			cv2.imshow('img', img)
			cv2.waitKey(1100)


if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--saved_crops', type=str, default='crops/', help='path to crops directory')
	parser.add_argument('--crop_size', type=tuple, default=(640, 640), help='cropped image dimenssions')
	parser.add_argument('--stride', type=int, default=500, help='crop overlap')
	parser.add_argument('--save_annotations', type=str, default='annotations/', help='crops annotations path')
	opt = parser.parse_args()
	main(opt)

