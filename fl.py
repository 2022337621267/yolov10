import os, shutil, random
from tqdm import tqdm

def split_img(img_path, label_path, split_list):
    try:
        Data = 'dataset'
        os.mkdir(Data)

        train_img_dir = Data + '/train/images'
        val_img_dir = Data + '/valid/images'
        test_img_dir = Data + '/test/images'

        train_label_dir = Data + '/train/labels'
        val_label_dir = Data + '/valid/labels'
        test_label_dir = Data + '/test/labels'

        # 创建文件夹
        os.makedirs(train_img_dir, exist_ok=True)
        os.makedirs(train_label_dir, exist_ok=True)
        os.makedirs(val_img_dir, exist_ok=True)
        os.makedirs(val_label_dir, exist_ok=True)
        os.makedirs(test_img_dir, exist_ok=True)
        os.makedirs(test_label_dir, exist_ok=True)

    except:
        print('文件目录已存在')

    train, val, test = split_list
    all_img = os.listdir(img_path)
    all_img_path = [os.path.join(img_path, img) for img in all_img]
    train_img = random.sample(all_img_path, int(train * len(all_img_path)))
    train_label = [toLabelPath(img, label_path) for img in train_img]

    # 将没有标签的图片文件排除
    valid_train_img = [img for img, label in zip(train_img, train_label) if os.path.exists(label)]
    valid_train_label = [label for label in train_label if os.path.exists(label)]

    for i in tqdm(range(len(valid_train_img)), desc='train ', ncols=80, unit='img'):
        _copy(valid_train_img[i], train_img_dir)
        _copy(valid_train_label[i], train_label_dir)
        all_img_path.remove(valid_train_img[i])

    # val 和 test 同样操作
    val_img = random.sample(all_img_path, int(val / (val + test) * len(all_img_path)))
    val_label = [toLabelPath(img, label_path) for img in val_img]
    valid_val_img = [img for img, label in zip(val_img, val_label) if os.path.exists(label)]
    valid_val_label = [label for label in val_label if os.path.exists(label)]

    for i in tqdm(range(len(valid_val_img)), desc='val ', ncols=80, unit='img'):
        _copy(valid_val_img[i], val_img_dir)
        _copy(valid_val_label[i], val_label_dir)
        all_img_path.remove(valid_val_img[i])

    test_img = all_img_path
    test_label = [toLabelPath(img, label_path) for img in test_img]
    valid_test_img = [img for img, label in zip(test_img, test_label) if os.path.exists(label)]
    valid_test_label = [label for label in test_label if os.path.exists(label)]

    for i in tqdm(range(len(valid_test_img)), desc='test ', ncols=80, unit='img'):
        _copy(valid_test_img[i], test_img_dir)
        _copy(valid_test_label[i], test_label_dir)

def _copy(from_path, to_path):
    shutil.copy(from_path, to_path)

def toLabelPath(img_path, label_path):
    img = os.path.basename(img_path)  # 取出图片的文件名
    label = img.split('.jpg')[0] + '.txt'  # 替换扩展名为 .xml
    return os.path.join(label_path, label)

 
def main():
    # 需要修改的地方：装图片的文件夹以及装标签的文件夹
    img_path = '/root/voc_data/voc_images/'
    label_path = '/root/voc_data/labels/'
    split_list = [0.8, 0.1, 0.1]  # 数据集划分比例[train:val:test]
    split_img(img_path, label_path, split_list)
 
 
if __name__ == '__main__':
    main()
    