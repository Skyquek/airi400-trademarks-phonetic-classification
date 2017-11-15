import pandas as pd
from data.text_to_img import save_pair_image, text_to_image, textpair_to_image
from converter.romanize import romanize
import re

data = pd.read_csv('sample_trademark_data.csv')

num_data = len(data)
print(num_data)
MAX_LENGTH = 20

for i in range(num_data):
    title1_roman = romanize(data['title1'][i]).lower()
    title2_roman = romanize(data['title2'][i]).lower()
    title1_roman_wo_space = re.sub(r" ", r"_-", re.sub(r"[`;<>~\[\]|:+-/.,!?@#$%^*()\'\"]", r"",
                                                       re.sub(r"&", r" and ", title1_roman)))
    title2_roman_wo_space = re.sub(r" ", r"_-", re.sub(r"[`;<>~\[\]|:+-/.,!?@#$%^*()\'\"]", r"",
                                                       re.sub(r"&", r" and ", title2_roman)))

    if len(title1_roman_wo_space) < MAX_LENGTH and len(title2_roman_wo_space) < MAX_LENGTH:
        if bool(re.search(r'\d', data['title1'][i])) == False and bool(re.search(r'\d', data['title2'][i])) == False:
            try:
                save_pair_image(data['title1'][i], data['title2'][i], data['similarity'][i])
            except:
                pass
        else:
            pass
    elif len(title1_roman_wo_space) == 0 or len(title2_roman_wo_space) == 0:
        pass
    else:
        pass

    if i % 10 == 0:
        print("step : " + str(i) + "/" + str(num_data))

print('done')