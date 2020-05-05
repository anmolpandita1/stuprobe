import sys
import os


from random import choice
from numpy import load
from numpy import expand_dims
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC


import sqlite3
from sqlite3 import Error
 


from datetime import datetime
date = datetime.today().strftime('%Y-%m-%d')




#----------------------------------Database handling
def create_connection(db_file):
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn
 
 







#  names
db_script = 'C:/project/be/engine/py_db.py'
reg_dir = 'C:/project/be/data/registered/registered_students.npz'
class_dir = 'C:/project/be/data/classroom_uploads/'
database = "C:/project/be/db.sqlite3"
course_id = sys.argv[1]

# load reg face embeddings
data = load(reg_dir)
trainX, trainy = data['arr_0'], data['arr_1']

# load classroom face embeddings
data = load(class_dir + sys.argv[1] + "/" + sys.argv[1] + ".npz")
testX = data['arr_0']


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
recur = 20  #no of recursion
total=testX.shape[0]
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
		xx[i]=xx[i]+class_probability



names = []
all_students = []



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
		names.append(predict_names[0])
		
print("known:",known,"\n  unknown :",unknown)




sqlite_select_query = "SELECT * from stuprobe_student"

conn = sqlite3.connect(database)
cur = conn.cursor()
cur.execute(sqlite_select_query)
records = cur.fetchall()

for row in records:
	all_students.append(row[0]) 
cur.close()




names = set(names)
all_students = set(all_students)

absent = all_students.difference(names)

names = list(names)
absent = list(absent)


for name in names:
	query = "INSERT INTO stuprobe_attendance (date,status,course_id,student_id) VALUES ('" + date + "', 1, '" + course_id + "' , '" + name + "' )"
	conn = create_connection(database)
	cur = conn.cursor()
	cur.execute(query)
	conn.commit()
for name in absent:
	query = "INSERT INTO stuprobe_attendance (date,status,course_id,student_id) VALUES ('" + date + "', 0, '" + course_id + "' , '" + name + "' )"
	conn = create_connection(database)
	cur = conn.cursor()
	cur.execute(query)
	conn.commit()


