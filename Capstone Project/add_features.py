#load all necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import seaborn as sns

from IPython.display import display

data = pd.read_csv('Data/bids.csv')
data.drop(['ip', 'url'], axis = 1, inplace = True)

bidder_train = pd.read_csv('Data/train.csv')
bidder_train.drop(['payment_account', 'address'], axis=1, inplace = True)

bidder_test = pd.read_csv('Data/test.csv')
bidder_test.drop(['payment_account', 'address'], axis=1, inplace = True)

#Feature: Number of auctions
df = data[['bidder_id', 'auction', 'merchandise']].groupby(['bidder_id', 'auction']).count()
#min, max, mean
min_num_bids = df.merchandise.min(level=0)
max_num_bids = df.merchandise.max(level=0)
avg_num_bids = df.merchandise.mean(level=0)
std_num_bids = df.merchandise.std(level=0).fillna(0)

#Feature: Speed of making bids
start_time = data[['bidder_id','time','auction']].groupby(['bidder_id','auction']).time.min()
end_time = data[['bidder_id', 'time', 'auction']].groupby(['bidder_id','auction']).time.max()
time_interval = pd.DataFrame((end_time - start_time)*10e-10).rename(columns={0: 'time'})
#nbids = num_bids.reset_index().sort('bidder_id').bid_id
time = time_interval.reset_index().time
nbids = data[['bidder_id', 'bid_id', 'auction']].groupby(['bidder_id', 'auction']).bid_id.count()
nbids = nbids.reset_index().rename(columns={0:'num_bids'})
nbids_s = nbids.bid_id
nbids['speed'] = (nbids_s/time)
nbids.replace(np.inf, 0, inplace = True)

min_speed = nbids.groupby('bidder_id').speed.min()
max_speed = nbids.groupby('bidder_id').speed.max()
avg_speed = nbids.groupby('bidder_id').speed.mean()
std_speed = nbids.groupby('bidder_id').speed.std().fillna(0)

#Feature: Countries
#data[['country', 'device']] = data[['country', 'device']].astype('category').apply(lambda x:x.cat.codes)
countries_auc = data[['bidder_id', 'country', 'auction']].groupby(['bidder_id', 'auction']).country.count()

min_num_cou = countries_auc.min(level=0)
max_num_cou = countries_auc.max(level=0)
mean_num_cou = countries_auc.mean(level=0)
std_num_cou = countries_auc.std(level=0).fillna(0)

#Feature: device
devices_auc = data[['bidder_id', 'device', 'auction']].groupby(['bidder_id', 'auction']).device.count()

min_dev = devices_auc.min(level=0)
max_dev = devices_auc.max(level=0)
mean_dev = devices_auc.mean(level=0)
std_dev = devices_auc.std(level=0).fillna(0)

d = {'min_num_bids':min_num_bids, 'max_num_bids': max_num_bids, 'avg_num_bids':avg_num_bids,
     'min_speed':min_speed, 'max_speed':max_speed, 'avg_speed':avg_speed,
     'min_num_cou':min_num_cou, 'max_num_cou':max_num_cou, 'avg_num_cou': mean_num_cou,
     'min_dev':min_dev, 'max_dev':max_dev, 'avg_dev': mean_dev}
     #'std_num_bids': std_num_bids, 'std_num_cou':std_num_cou, 'std_speed':std_speed, 'std_dev':std_dev}

features = pd.DataFrame(d).reset_index()

merged_train = pd.merge(bidder_train, features, left_on='bidder_id', right_on='bidder_id')
ddd = data[['bidder_id', 'merchandise','bid_id']].groupby(['bidder_id', 'merchandise']).count()
ddd = ddd.reset_index('merchandise')
ddd.drop('bid_id', axis = 1, inplace = True)
dddd = pd.merge(merged_train, ddd, left_on='bidder_id', right_index = True, how = 'left')
dddd.merchandise = dddd.merchandise.astype('category')
dddd.merchandise = dddd[['merchandise']].apply(lambda x:x.cat.codes)
cccc = data[['country', 'bidder_id']].groupby('bidder_id')['country'].nunique()
cccc = cccc.reset_index()
ccccc = pd.merge(dddd, cccc, left_on = 'bidder_id', right_on = 'bidder_id', how='left')
devices = data[['device', 'bidder_id']].groupby('bidder_id')['device'].nunique()
devices = devices.reset_index()
abcde = pd.merge(ccccc, devices, left_on='bidder_id', right_on='bidder_id', how='left')
labels = abcde['outcome']
train_data = abcde.drop('outcome', axis=1)
#train = train_data.set_index('bidder_id')

merged_test = pd.merge(bidder_test, features, left_on = 'bidder_id', right_on = 'bidder_id', how = 'left').fillna(0)
ddd_t = data[['bidder_id', 'merchandise','bid_id']].groupby(['bidder_id', 'merchandise']).count()
ddd_t = ddd_t.reset_index('merchandise')
ddd_t.drop('bid_id', axis = 1, inplace = True)
dddd_t = pd.merge(merged_test, ddd, left_on='bidder_id', right_index = True, how = 'left')
dddd_t.merchandise = dddd_t.merchandise.astype('category')
dddd_t.merchandise = dddd_t[['merchandise']].apply(lambda x:x.cat.codes)
cccc_t = data[['country', 'bidder_id']].groupby('bidder_id')['country'].nunique()
cccc_t = cccc_t.reset_index()
ccccc_t = pd.merge(dddd_t, cccc_t, left_on = 'bidder_id', right_on = 'bidder_id', how='left')
devices_t = data[['device', 'bidder_id']].groupby('bidder_id')['device'].nunique()
devices_t = devices_t.reset_index()
abcde_t = pd.merge(ccccc_t, devices_t, left_on='bidder_id', right_on='bidder_id', how='left')
#test_data = abcde_t.set_index('bidder_id')

url = pd.read_csv('results/url.csv')
country = pd.read_csv('results/country.csv')
device = pd.read_csv('results/device.csv')
ip = pd.read_csv('results/ip.csv')

merged_1 = pd.merge(train_data, url, on='bidder_id', how = 'left')
merged_2 = pd.merge(merged_1, country, on='bidder_id', how='left')
merged_3 = pd.merge(merged_2, device, on='bidder_id', how='left')
train = pd.merge(merged_3, ip, on='bidder_id', how='left').set_index('bidder_id')

merged_11 = pd.merge(abcde_t, url, on='bidder_id', how = 'left')
merged_22 = pd.merge(merged_11, country, on='bidder_id', how='left')
merged_33 = pd.merge(merged_22, device, on='bidder_id', how='left')
test = pd.merge(merged_33, ip, on='bidder_id', how='left').set_index('bidder_id')


print('Train data')
display(train.head())
print('Test data')
display(test.head())
