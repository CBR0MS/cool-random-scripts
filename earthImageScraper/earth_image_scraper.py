from PIL import Image
import requests
from io import BytesIO
import datetime

now = datetime.datetime.now()

url = 'http://rammb-slider.cira.colostate.edu/data/imagery/'
url2 = '/goes-16---full_disk/geocolor/' #geocolor natural_color
day = str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2)

discard = datetime.timedelta(minutes=now.minute % 15,seconds=now.second,microseconds=now.microsecond)
now -= discard

if discard >= datetime.timedelta(minutes=7, seconds=30):
    now += datetime.timedelta(minutes=15)

img_tile_size = 678
tiles_wide = 15
tiles_high = 6
imgs = []
img_data = []

def get_image_data(seconds, og_url1, og_url2, og_day):

    date_time = og_day + str((now.hour + 4)) + str(now.minute).zfill(2) + seconds #20181120174534
    #print(date_time)

    zoom_level = '/04/'
    url = og_url1 + day + og_url2 + date_time + zoom_level

    for i in range(0,tiles_high):
        for j in range (0, tiles_wide):
            url_comp = url + str(i).zfill(3) + '_' + str(j).zfill(3) + '.png'
            response = requests.get(url_comp)
            img = Image.open(BytesIO(response.content))
            imgs.append(img)
            img_data.append({'row': i, 'col': j})
            print("got row {} column {}".format(i, j))

print("fetching images...")

for i in range(60):
    try:
        get_image_data(str(i).zfill(2), url, url2, day)
        break
    except OSError as e:
        # print("failed to get image for second {}".format(i))
        if (i == 59):
            print("failed to collect images! Terminating script")
            exit()


w = img_tile_size * tiles_wide
h = img_tile_size * tiles_high

result = Image.new("RGB", (w, h))

print("creating new image...")

for ind in range(len(imgs)):

    img = imgs[ind]
    row = img_data[ind]['row']
    col = img_data[ind]['col']
    result.paste(img, ((col * img_tile_size), (row * img_tile_size)))

result.save("earth.jpg")
print("new image saved!")