import sys
import numpy as np

from os import listdir
from os.path import isdir
from os import path
from PIL import Image

from numpy import load
from numpy import asarray
from numpy import expand_dims
from numpy import savez_compressed
from keras.models import load_model
from mtcnn.mtcnn import MTCNN


created_folder_path = sys.argv[1]
created_folder_name = created_folder_path.split("/")[-2]


emm_save_folder_name = 'C:/project/be/data/registered/'



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
	embedding = model.predict(samples)
	return embedding[0]



# extract a single face from a given image
def extract_face(filename, required_size=(160, 160)):
	# load image from file
	image = Image.open(filename)
	# convert to RGB, if needed
	image = image.convert('RGB')
	# convert to array
	pixels = asarray(image)
	# create the detector, using default weights
	detector = MTCNN()
	# detect faces in the image
	results = detector.detect_faces(pixels)
	# extract the bounding box from the first face
	x1, y1, width, height = results[0]['box']
	# was outputting negatives
	x1, y1 = abs(x1), abs(y1)
	x2, y2 = x1 + width, y1 + height
	# extract the face
	face = pixels[y1:y2, x1:x2]
	# resize pixels to the model size
	image = Image.fromarray(face)
	image = image.resize(required_size)
	face_array = asarray(image)
	return face_array




# load images and extract faces for all images in a directory
def load_faces(directory):
	faces = list()
	# enumerate files
	for filename in listdir(directory):
		# path
		path = directory + filename
		print(path)
		# get face
		face = extract_face(path)
		# store
		faces.append(face)
	return faces



def load_dataset(created_folder_path):
	x, y = list(), list()
	# path
	faces = load_faces(created_folder_path)
	# create labels
	labels = [created_folder_name for _ in range(len(faces))]
	# summarize progress
	print('>loaded %d images for student id: %s' % (len(faces), created_folder_name))
	# store
	x.extend(faces)
	y.extend(labels)
	return asarray(x), asarray(y)




# load  dataset
loaded_faces, loaded_labels = load_dataset(created_folder_path)
print('Faces and lables loaded........')


# load the  model
model = load_model('C:/project/be/engine/facenet_keras.h5', compile=False)
print('Loaded Model...................')




# convert each face in the train set to an embedding
face_embeddings = list()
for face_pixels in loaded_faces:
	embedding = get_embedding(model, face_pixels)
	face_embeddings.append(embedding)
face_embeddings = asarray(face_embeddings)
print(face_embeddings.shape)


fresh_faces = face_embeddings




if not path.exists('C:/project/be/data/registered/registered_students.npz'):
	savez_compressed(emm_save_folder_name + 'registered_students', fresh_faces, loaded_labels)
	print("Student saved!")
else:
	# load older npz
	data = load('C:/project/be/data/registered/registered_students.npz')
	npz_faces, npz_labels = data['arr_0'], data['arr_1']
	# add new faces to the older npz
	faces_list = npz_faces.tolist()
	faces_list.extend(fresh_faces)
	final_face_array = asarray(faces_list)
	# add new labels
	final_face_labels = np.append(npz_labels, loaded_labels)
	# save to a compressed file
	savez_compressed(emm_save_folder_name + 'registered_students', final_face_array, final_face_labels)
	print("Student saved!")





