from itertools import izip
from collections import defaultdict
from math import sqrt


class User(object):
	def __init__(self,idd,age,sex,prof,zipcode):
		self.id = idd
		self.age = age
		self.sex = sex
		self.prof = prof
		self.zipcode = zipcode
		self.watched = defaultdict(int)
		self.genre_value = {i:[0,0] for i in range(19)}
		self.sum = 0
		


class Movie(object):
	def __init__(self,idd,title,year=1900,genres=" ",link=" "):
		self.id = idd
		self.title = title
		self.year = year
		self.link = link
		self.genres = genres
		self.movie_sex = [[0,0],[0,0]]
		self.movie_age = {i:[0,0] for i in range(10)}
		self.sum = 0
		self.seenBy = []


''' Declaring all the global Variables used by the program '''

user_object = {}
movie_object = {}
FOLD = 5
INCREMENT = 1
Total_count = 0
Mad_count = 0
Avg_count = 0


def readUser(filename):
	file = open(filename,'r')
	lines = file.readlines()
	for line in lines:
		words = line.split('|')
		obj = User(words[0],int(words[1]),words[2],words[3],words[4])
		user_object[words[0]] = obj
	file.close()


def readMovie(filename):
	file = open(filename,'r')
	lines = file.readlines()
	for line in lines:
		words = line.split('|')
		titles = words[1].split('(')
		genre_list = [int(words[ind]) for ind in range(5,24)]
		obj = Movie(words[0],titles[0],words[2],genre_list)
		movie_object[words[0]] = obj
	file.close()

def readTrain(filename):
	file = open(filename,'r')
	lines = file.readlines()
	# print len(lines)
	for line in lines:
		tokens = line.split()
		user = tokens[0]
		movie = tokens[1]
		rating = int(tokens[2])

		user_object[user].watched[movie] = int(tokens[2])
		user_object[user].sum += rating
		movie_object[movie].seenBy.append(user)
		movie_object[movie].sum += rating
		for ind in range(19):
			if movie_object[movie].genres[ind]:
					user_object[user].genre_value[ind][0] += rating
					user_object[user].genre_value[ind][1] += 1
		sex = 1 if user_object[user].sex == 'M' else 0
		movie_object[movie].movie_sex[sex][0] += rating
		movie_object[movie].movie_sex[sex][1] += 1
		age = user_object[user].age
		age /= 9
		movie_object[movie].movie_age[age][0] += rating
		movie_object[movie].movie_age[age][0] += 1
	file.close()

def readTest(filename):
	test_data = defaultdict()
	with open(filename,'r') as file:
		for line in file:
			tokens = line.split()
			test_data[(tokens[0],tokens[1])] = int(tokens[2])
	file.close()
	return test_data


train_files = ["u1.base"]#,"u2.base","u3.base","u4.base","u5.base"]
test_files = ["u1.test"]#,"u2.test","u3.test","u4.test","u5.test"]



def compute_common(user1,user2,algo,guess_movie):
	uobj1 = user_object[user1];
	uobj2 = user_object[user2];

	movie_obj = movie_object[guess_movie]
	try:
		female_avg = float(movie_obj.movie_sex[0][0])/movie_object.movie_sex[0][1]
		female_avg *= 0.1
	except:
		female_avg = .25
	try:
		male_avg = float(movie_obj.movie_sex[1][0])/movie_object.movie_sex[1][1]
		male_avg *= 0.1
	except:
		male_avg = .25

	try:
		male_avg = float(male_avg)/(male_avg+female_avg)
	except:
		male_avg = 0.5

	female_avg = 1-male_avg
	genre1, genre2 = 0,0
	for ind in range(19):
		if movie_obj.genres[ind] == 1:
			try:
				genre1 += float(uobj1.genre_value[ind][0])/uobj1.genre_value[ind][1]
			except:
				genre1 += 2.5
			try:
				genre2 += float(uobj2.genre_value[ind][0])/uobj2.genre_value[ind][1]
			except:
				genre2 += 2.5

	try:
		genre1 = genre1 / (genre1+genre2)
	except:
		genre1 = 0.5

	genre2 = 1 - genre1

	age1 = uobj1.age / 9
	age2 = uobj2.age / 9

	try:
		age_rating1 = float(movie_obj.age[age1][0])/movie_obj.age[age1][1]
	except:
		age_rating1 = 2.5
	try:
		age_rating2 = float(movie_obj.age[age2][0])/movie_obj.age[age2][1]
	except:
		age_rating2 = 2.5
	try:
		age_rating1 =  float(age_rating1)/(age_rating1+age_rating2)
	except:
		age_rating1 = 0.5

	intersection = 0
	dist = 0
	high = 0
	for movie in uobj1.watched.keys():
		if movie in uobj2.watched.keys():
			intersection += 1
			if algo == euclidian or algo == manhattan:
				dist += algo(uobj1,uobj2,genre1,genre2,male_avg,age_rating1,movie)
			newhigh = abs(uobj1.watched[movie] - uobj2.watched[movie])
			if newhigh > high:
				high = newhigh
			
	if algo == euclidian:
		dist = sqrt(dist)
	elif algo == L_max:
		dist = high

	
	return (dist,intersection)

def euclidian(user1,user2,genre1,genre2,male_avg,age_rating,movie):
	if user1.sex != user2.sex:
		if user1.sex == 'M':
			dist = (user1.watched[movie]*age_rating) - (user2.watched[movie]*(1-age_rating))
		else:
			dist = (user1.watched[movie]*age_rating) - (user2.watched[movie]*(1-age_rating))
	else:
		dist = (user1.watched[movie]*age_rating) - (user2.watched[movie]*(1-age_rating))
	dist = dist**2
	return dist

def manhattan(user1,user2,movie):
	dist = user1.watched[movie]-user2.watched[movie]
	return abs(dist)





def similar_weight(result,movie,user, k=300):
	bin1,bin2,bin3,bin4 = [],[],[],[]
	length = len(result)
	len_watched = len(user_object[user].watched)
	sum1,sum2,sum3,sum4 = 0,0,0,0
	if(length > 10):
		high = result[0][0]
		low = result[-1][0]
		diff = high-low
		diff = float(diff)/4
		bin1_cut = high - diff
		bin2_cut = high - (2*diff)
		bin3_cut = high - (3*diff)

		if len(result) > k:
			similar_k = result[:k+1]
		else:
			similar_k = result[:]

		for output in similar_k:
			if output[0] >= bin1_cut:
				bin1.append(output)
				sum1 += user_object[output[1]].watched[movie]
			elif output[0] >= bin2_cut:
				bin2.append(output)
				sum2 += user_object[output[1]].watched[movie]
			elif output[0] >= bin3_cut:
				sum3 += user_object[output[1]].watched[movie]
				bin3.append(output)
			else:
				sum4 += user_object[output[1]].watched[movie]
				bin4.append(output)
		
		flag1, flag2, flag3, flag4 = False,False,False,False


		try:
			avg1 = float(sum1)/len(bin1)
		except:
			avg1 = 0
			flag1 = True

		try:
			avg2 = float(sum2)/len(bin2)
		except:
			avg2 = 0
			flag2 = True
		try:
			avg3 = float(sum3)/len(bin3)
		except:
			avg3 = 0
			flag3 = True
		try:
			avg4 = float(sum4)/len(bin4)
		except:
			avg4 = 0
			flag4 = True

		flag_list = [flag1,flag2,flag3, flag4]
		bin_list = [avg1,avg2,avg3,avg4]

		count_flag = 0
		
		for value in flag_list:
			if value == True:
				count_flag += 1

		list3 = [0.6,0.3,0.1]
		list2 = [0.6,0.4]


		if count_flag == 0:
			rating = avg1 * 0.5 + avg2 * 0.3 + avg3 * 0.15 + avg4 * 0.05
		elif count_flag == 1:
			rating = 0
			itr = 0
			index = 0
			for i in flag_list:
				if i == False:
					rating += (list3[index] * bin_list[itr])
					index += 1
				itr += 1
		elif count_flag == 2:
			rating = 0
			itr = 0
			index = 0
			for i in flag_list:
				if i == False:
					rating += (list2[index]*bin_list[i])
					index += 1
				itr += 1
		elif count_flag == 3:
			rating = 0
			itr = 0
			for i in flag_list:
				if i == False:
					rating += (1*bin_list[itr])
				itr += 1
		else:
			rating = 3.0
			

	else:
		avg_sum = 0
		count = 0
		try:
			user_average = user_object[user].sum / float(len_watched)
		except:
			user_average = 3.0

		if length > 0:
			for output in result:
				avg_sum += user_object[output[1]].watched[movie]
				count += 1
			rating = 0.3 * user_average  + 0.7 * avg_sum/float(count)
		else:
			rating = user_average
	return round(rating)

def predict_rating(user,movie):
	result = []
	all_users = movie_object[movie].seenBy
	size_watched = len(user_object[user].watched)
	for curr_user in all_users:
		(corr,intersection) = compute_common(user,curr_user,euclidian,movie)
		try:
			corr = 1/float(corr)
		except:
			if intersection == 0:
				corr = 0.01
			else:
				corr = 1

		ratio = float(intersection)/size_watched
		cost = corr*ratio
		cost *= INCREMENT
		result.append((cost,curr_user))
	
	result.sort(key=lambda tup: tup[0],reverse= True)
	rating = similar_weight(result,movie,user)
	return rating



def MAD_score(actual,guess,movie):
	global Total_count,Mad_count,Avg_count
	Total_count += 1
	Mad_count += abs(actual-guess)
	try:
		avg_score = round(movie_object[movie].sum / float(len(movie_object[movie].seenBy)))
	except:
		avg_score = 0.0
	Avg_count += abs(avg_score - actual)


def clear_data():
# clear all the user watched movie data and movie seen by data	
	for user in user_object.values():
		user.watched = {}
		user.sum = 0
		user.genre_value = {}
	
	for movie in  movie_object.values():
		movie.seenBy = []
		movie.sum = 0
		movie.movie_sex = []
		movie.movie_age = {}
		


def cross_validation(train_files,test_files):
	''' print "total user: ", len(user_object)
	print "total movie: ", len(movie_object
	Read each train file and test file for 5-fold times '''

 	for train_file,test_file in izip(train_files,test_files):
		readTrain(train_file)
		test_data = readTest(test_file)
		for key in test_data:
			(user,movie) = key
			rating = test_data[key]
			if type(rating) == int and rating >= 1 and rating <= 5:
				# print "movie:  "+ movie + "  user:  " + user
				guess_rating = predict_rating(user,movie)
				# print "rating: ",rating
				# print "guess_rating: ", guess_rating
				# raw_input("check")
				MAD_score(rating,guess_rating,movie)

		clear_data()


if __name__ == '__main__':
# Read user file and create User object
# Read Movie file and create Movie object
	
	readUser("u.user")
	readMovie("u.item")

	cross_validation(train_files,test_files)

	mad_score = float(Mad_count)/Total_count
	avg_score = float(Avg_count)/Total_count

	print "Algorithm mad_score:  ", mad_score
	print "Naive mad_score:  ", avg_score
    