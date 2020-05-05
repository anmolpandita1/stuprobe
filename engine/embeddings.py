import os
import sys
from os import path

from PIL import Image

from numpy import load
from numpy import asarray
from numpy import expand_dims
from numpy import savez_compressed
from mtcnn.mtcnn import MTCNN

from keras.models import load_model

#folder names
emm_save_folder_name = sys.argv[1]
get_folder_name = sys.argv[1]
recog_script_path = "C:/project/be/engine/recog.py"
registered_npz = "C:/project/be/data/registered/registered.npz"

#for file name increment
count = 0 


#for face array, to be saved in npz 
burst_detected_faces = list()



def detect(filename):
	frame = Image.open(filename)
	frame = frame.convert('RGB')
	frame = asarray(frame)
	# create the detector, using default weights
	detector = MTCNN()
	# detect faces in the image
	faces = detector.detect_faces(frame)
	extraction(frame, faces)


# extract the faces detected
def extraction(frame, faces, required_size=(160, 160)):
	print('\t\tExtracting Face... :)')
	for face in faces:
		global count
		# get coordinates
		x1, y1, width, height = face['box']
		x1, y1 = abs(x1), abs(y1) #bug fix
		x2, y2 = x1 + width, y1 + height

		# extract the face
		face = frame[y1:y2, x1:x2]

		#Resize pixels to the model size
		
		#_____create image from numpy array
		image = Image.fromarray(face)						
		#_____resize the created image
		image = image.resize(required_size)	
		
		#Get numpy array again to save in the face list
		face_array = asarray(image)	
		#_____append to face list()
		burst_detected_faces.append(face_array)		
		count+=1


# get the face embedding for one face
def get_embedding(model, face_pixels):
	# scale pixel values
	face_pixels = face_pixels.astype('float32')
	# standardize pixel values across channels (global)
	mean, std = face_pixels.mean(), face_pixels.std()
	face_pixels = (face_pixels - mean) / std
	# transform face into one sample
	samples = expand_dims(face_pixels, axis=0)
	print("___________________________________")
	print(samples.shape)
	print("___________________________________")
	# make prediction to get embedding
	yhat = model.predict(samples)
	return yhat[0]



# create folder if not found
if not path.exists(emm_save_folder_name):
	os.mkdir(emm_save_folder_name)


#scan through the folder for file names
with os.scandir(get_folder_name) as entries:
    for entry in entries:
        print('____________________________________')
        print('Working on File: ' + entry.name)
        print('____________________________________')
        detect(get_folder_name + entry.name)
        


# load the face dataset
trainX = burst_detected_faces

# load the facenet model
model = load_model('C:/project/be/engine/facenet_keras.h5', compile=False)
print('Loaded Model')

# convert each face in the train set to an embedding
newTrainX = list()
for face_pixels in trainX:
	embedding = get_embedding(model, face_pixels)
	newTrainX.append(embedding)
newTrainX = asarray(newTrainX)
print('Faces found: ' + str(newTrainX.shape[0]))

# save arrays to one file in compressed format
#Course_CS_1/
#["Course_CS_1",""]

npz_dir = emm_save_folder_name + emm_save_folder_name.split("/")[-2]
npz_name = emm_save_folder_name.split("/")[-2]
savez_compressed(npz_dir, newTrainX)
print('\nSaved!\n\n')

os.system("python "+ recog_script_path + " " + npz_name + " " + registered_npz)

