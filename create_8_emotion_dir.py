import pandas as pd
import cv2
import os
from tqdm import tqdm

def create_folder(csv_path, my_emotion):
    df = pd.read_csv(csv_path)

    dest_dir = os.path.join('data', my_emotion)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
        
    with tqdm(total=df.shape[0]) as pbar:
        for index, row in df.iterrows():
            image_name = row['image_id']
            image_dest_path = os.path.join(dest_dir, image_name)
            image_path = os.path.join('data/train', image_name)
            image = cv2.imread(image_path)
            cv2.imwrite(image_dest_path, image)

            pbar.update(1)

if __name__ == '__main__':
    create_folder('data/angry.csv', 'angry')
    create_folder('data/disgust.csv', 'disgust')
    create_folder('data/fear.csv', 'fear')
    create_folder('data/happy.csv', 'happy')
    create_folder('data/sad.csv', 'sad')
    create_folder('data/surprise.csv', 'surprise')
    create_folder('data/neutral.csv', 'neutral')
    create_folder('data/others.csv', 'anothersgry')