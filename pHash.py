import imagehash
from PIL import Image
import json
import os


def hamming_dist(str1, str2):
    return sum([ch1 != ch2 for ch1, ch2 in zip(str1, str2)])

def image_phash(filepath):
    img = Image.open(filepath)
    hash_value = imagehash.phash(img)
    return str(hash_value)

def search_similar_images(src_img_path, dir_path):
    result = []
    src_phash_value = image_phash(src_img_path)
    file_path_list = os.listdir(dir_path)
    if 'phash_data.json' in file_path_list:
        with open(dir_path + '/phash_data.json', 'r') as f:
            hash_data = json.load(f)
    else:
        hash_data = {}
    for img in os.listdir(dir_path):
        filetype = img.split('.')[-1]
        if filetype not in ['jpg', 'jpeg', 'png', 'gif']:
            continue
        img_path = dir_path + '/' + img
        if img_path in hash_data:
            dest_phash_value = hash_data[img_path]
        else:
            dest_phash_value = image_phash(img_path)
            hash_data[img_path] = dest_phash_value
        img_dist = hamming_dist(src_phash_value, dest_phash_value)
        if img_dist <= 5:
            result.append([img_path, img_dist])
    with open(dir_path + '/phash_data.json', 'w') as f:
        json.dump(hash_data, f)
    result = sorted(result, key=lambda x: x[1])
    return result

def generate_images_html(src_img_path,similar_images):
    template='''
    <html>
        <title>图片搜索结果</title>
        <body>
            <div>
                <h2>原图片</h2>
                {}
            </div>
            <div>
                <h2>搜索结果</h2>
                {}
            </div>
        </body>
    </html>
    '''
    src_img='<img src="{}" alt=""> '.format(src_img_path)
    search_result=''
    for item in similar_images:
        search_result+='<img src="{}" alt="">\n'.format(item[0])
    html=template.format(src_img,search_result)
    with open('result.html','w',encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    result = search_similar_images(
        'images/3e5252c290ae2429d7ab9941649727e8.png', 'images')
    generate_images_html('images/3e5252c290ae2429d7ab9941649727e8.png',result)