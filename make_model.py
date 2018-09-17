import os 
import cv2 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib 
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


def show(img,name) : 
	cv2.namedWindow(name, cv2.WINDOW_NORMAL)
	cv2.imshow(name,img)
	cv2.waitKey(0)
	cv2.destroyWindow(name)

###----------LOAD THE DATA ------------------###
list_folder = os.listdir("./Data")					# list of folders/files in a given directory 
dataset = []
labels_dataset = []
i = 0
for folder in list_folder:
	flist = os.listdir(os.path.join("./Data", folder)) # list files in a subdirectory 
	for f in flist:
		im = cv2.imread(os.path.join("./Data", folder, f))	#read the images 
		im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY )	
		im = cv2.blur(im,(3,3))
		im = cv2.resize(im, (36,36))		
		dataset.append(im)			
		labels_dataset.append(int(folder))							# make the dataset 
		
dataset = np.reshape(dataset,(len(dataset),-1))

###---------TRAIN THE MODEL-----------------###

clf = KNeighborsClassifier()
clf.fit(dataset,labels_dataset)
###--------SAVE THE MODEL -------------------###
joblib.dump(clf,"model.sav")				
