import os
video_list = []
# Using os.walk()
for dirpath, dirs, files in os.walk('/home/shekhar/mp_pr/multi_processing_prod/videos/'):
    for filename in files:
        fname = os.path.join(dirpath, filename)
        video_list.append((fname,filename.split('.')[0]))
print(video_list)

