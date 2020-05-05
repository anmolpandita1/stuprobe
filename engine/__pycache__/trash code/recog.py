import os
import sys 
from random import choice
from numpy import load
from numpy import expand_dims
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
from matplotlib import pyplot
# load faces




def load_npz(path):
	all_files = os.listdir(path)
	npz_files = filter(lambda x: x[-4:] == '.npz', all_files)
	file_content = load(npz_files[0])

	return file_content['arr_0'] 

def load_all_npz(directory):
	X, y = list(), list()
	# enumerate folders, on per class
	for subdir in listdir(directory):
		# path
		path = directory + subdir + '/'
		# skip any files that might be in the dir
		if not isdir(path):
			continue
		# load all faces in the subdirectory
		faces = load_npz(path)
		# create labels
		labels = [subdir for _ in range(len(faces))]
		# summarize progress
		print('>loaded %d examples for class: %s' % (len(faces), subdir))
		# store
		X.extend(faces)
		y.extend(labels)
	return asarray(X), asarray(y)


# load test face embeddings
data = load(sys.argv[1])
testX = data['arr_0']

# load train face embeddings
trainX, trainy = load_all_npz(sys.argv[2])




# normalize input vectors
in_encoder = Normalizer(norm='l2')
trainX = in_encoder.transform(trainX)
testX = in_encoder.transform(testX)


# label encode targets
out_encoder = LabelEncoder()
out_encoder.fit(trainy)
trainy = out_encoder.transform(trainy)
#testy = out_encoder.transform(testy)


xx=[]
recur=1  #no of recurtion
total=testX.shape[0];
for i in range(total):
	xx.append(0)

for x in range(0,recur):
	# fit model
	model = SVC(kernel='linear', probability=True)
	model.fit(trainX, trainy)
	# save attendance


	for i in range(testX.shape[0]):
		random_face_emb = testX[i]

		# prediction for the face
		samples = expand_dims(random_face_emb, axis=0)
		yhat_class = model.predict(samples)
		yhat_prob = model.predict_proba(samples)

		# get name
		class_index = yhat_class[0]
		class_probability = yhat_prob[0,class_index] * 100
		predict_names = out_encoder.inverse_transform(yhat_class)
		#print('_________________________')

		#print( str(i) +'. Predicted: %s (%.3f)' % (predict_names[0], class_probability))
		xx[i]=xx[i]+class_probability
print("#############")
known=0
unknown=0
for i in range(testX.shape[0]):
	random_face_emb = testX[i]

	# prediction for the face
	samples = expand_dims(random_face_emb, axis=0)
	yhat_class = model.predict(samples)
	yhat_prob = model.predict_proba(samples)

	# get name
	class_index = yhat_class[0]
	class_probability = yhat_prob[0,class_index] * 100
	predict_names = out_encoder.inverse_transform(yhat_class)
	xy=xx[i]/recur
	if(xy<50):
		unknown+=1
		print(i,' Predicted: unknown as ',predict_names[0],' : ',xy)
	else:	
		known+=1
		print( str(i) +'. Predicted: %s (%.3f)' % (predict_names[0], xy))
print("known:",known,"\n  unknown :",unknown)
		
