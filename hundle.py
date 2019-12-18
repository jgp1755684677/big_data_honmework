import os
import pandas as pd
from matplotlib import pyplot as plt

# csv files path
csv_path = './data/'

# image path
months_image = './image/'

# get csv files list 
csv_list = os.listdir(csv_path)

# draw months change image
for csv_file in csv_list:
	print("start to draw months change image")
	print("start to handle" + csv_file)
	
	# get csv path
	csv_file = csv_path + csv_file
	
	# define save image path
	months_image = months_image + csv_file.split('.')[1].split('/')[-1] + '.png'
	
	# get data
	df = pd.read_csv(csv_file, names=['data_time','quality','AQI','ranking','PM2.5','Pm10','So2','No2','Co','O3'])
	df["timeStamp"] = pd.to_datetime(df["data_time"])
	df.set_index('timeStamp',inplace=True)
	
	# Calculate months mean
	df=df.resample('M').mean()
	
	# draw image
	plt.figure(figsize=(20, 8), dpi=80)
	data=df['PM2.5']
	_x=data.index
	_y=data.values
	_x = [i.strftime("%Y%m%d") for i in _x]
	plt.plot(range(len(_x)), _y)
	plt.xticks(range(len(_x)), _x, rotation=45)
	
	# save image
	plt.savefig(months_image)
	plt.close()
	print(months_image + 'save successfully!')
	# redefine image path
	months_image = './image/'
	
# save year mean data
for csv_file in csv_list:
	print("start to save year mean data")
	print("start to handle" + csv_file)
	
	# get csv path
	csv_file = csv_path + csv_file
	
	# get data
	df = pd.read_csv(csv_file, names=['data_time','quality','AQI','ranking','PM2.5','Pm10','So2','No2','Co','O3'])
	df["timeStamp"] = pd.to_datetime(df["data_time"])
	df.set_index('timeStamp',inplace=True)
	
	# Calculate months mean
	df=df.resample('Y').mean()
	print(df)
	df["region"] = csv_file.split('.')[1].split('/')[-1]
	df.to_csv("temp.csv", mode='a', header=False)

# save year mean to csv order by datetime
df = pd.read_csv("temp.csv", names=['data_time','AQI','ranking','PM2.5','Pm10','So2','No2','Co','O3','region'])
df.sort_values('data_time',inplace=True)
df[['data_time','PM2.5','region']].to_csv("all_yaer_mean.csv", mode='a', header=False)
os.remove("temp.csv")
print(df)
