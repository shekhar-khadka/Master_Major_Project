from datetime import datetime
import subprocess
from multiprocessing import Pool
import os
from producer_app import ProducerThread
from producer_config import config as producer_config




video_list = []


for dirpath, dirs, files in os.walk('/home/shekhar/mp_pr/multi_processing_prod/videos/'):
   for filename in files:
       fname = os.path.join(dirpath, filename)
       video_list.append((fname,filename.split('.')[0]))


print(video_list)


def worker(video_metadta):
   # subprocess.call(f"./mp_column_spliter.sh {x[0]}  {x[1]}", shell=True)
   producer_thread = ProducerThread(producer_config)
   producer_thread.publishFrame(video_metadta[0],video_metadta[1])




def main():
   start_time=datetime.now()
   with Pool(processes=2) as pool:
       print(pool.map(worker, video_list))


   diff_time=datetime.now()-start_time
   print('total time take :',diff_time.total_seconds()/60 )