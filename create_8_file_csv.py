import pandas as pd 
import os 
from tqdm import tqdm
import ast 

df = pd.read_csv('data/additional_infor:train_emotion_polarity.csv')
d = {'image_id': df['image_id'], 'emotion_polarity': df['emotion_polarity']}

my_df = pd.DataFrame(d)
list_emotion = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral', 'others']

list_image_name = []
list_new_emotion = []

with tqdm(total=my_df.shape[0]) as pbar:
  for index, row in my_df.iterrows():
      image_name = row['image_id'] + '.jpg'
      emotion = row['emotion_polarity']
      emotion = ast.literal_eval(emotion)
      for key_emotion in list_emotion:
        if key_emotion not in emotion:
          emotion[key_emotion] = 0

      list_image_name.append(image_name)
      list_new_emotion.append(emotion)

      pbar.update(1)

final_df = {'image_id': list_image_name, 'emotion_polarity': list_new_emotion}
final_df = pd.DataFrame(final_df)

def create_new_csv(df, emotion_name):
    list_image_name = []
    list_prob = []
    with tqdm(total=df.shape[0]) as pbar:
        for index, row in df.iterrows():
            image_name = row['image_id'] 
            prob = row['emotion_polarity'][emotion_name]
            if prob != 0:
                list_image_name.append(image_name)
                list_prob.append(prob)

            pbar.update(1)
        
    d = {'image_id': list_image_name, 'prob': list_prob}
    new_df = pd.DataFrame(d)

    new_df.to_csv('data/'+emotion_name+'.csv', index=False)

create_new_csv(final_df, 'angry')
create_new_csv(final_df, 'disgust')
create_new_csv(final_df, 'fear')
create_new_csv(final_df, 'happy')
create_new_csv(final_df, 'sad')
create_new_csv(final_df, 'surprise')
create_new_csv(final_df, 'neutral')
create_new_csv(final_df, 'others')