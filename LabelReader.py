from PIL import Image
from RGBReader import visualizeData

palette_index = {(255, 0, 209): 0, #Road
                 (255, 204, 0): 1, #Building
                 (6, 255, 0): 2, # Tree
                 (0, 0, 255): 3, # Car
                 (219, 24, 22): 4, # Traffic
                 (43, 37, 67): 5, # Other
                 (0, 0, 0): 5}


def anlayzeLabel(path):
    image = Image.open(path)
    image = image.convert("RGB")
    rgb_values = image.getdata()
    rgb_counts = {}
    for rgb in rgb_values:
        if rgb in rgb_counts:
            rgb_counts[rgb] += 1
        else:
            rgb_counts[rgb] = 1

    return transformDic(rgb_counts)

def transformDic(dic):
    new_dic = {}
    for rgb, count in dic.items():
        new_dic[palette_index[rgb]] = count

    if 0 not in new_dic.keys():
        new_dic[0] = 0
    if 1 not in new_dic.keys():
        new_dic[1] = 0
    if 2 not in new_dic.keys():
        new_dic[2] = 0
    if 3 not in new_dic.keys():
        new_dic[3] = 0
    if 4 not in new_dic.keys():
        new_dic[4] = 0
    if 5 not in new_dic.keys():
        new_dic[5] = 0

    return new_dic

def getTotalCounts(dic):
    sum = 0

    for im_class, count in dic.items():
        # if im_class != 3:
        sum = sum + count
    
    return sum

def calculatePercents(dic):
    total_sum = getTotalCounts(dic)
    class_1 = dic[0] / total_sum
    class_2 = dic[1] / total_sum
    class_3 = dic[2] / total_sum
    class_4 = dic[3] / total_sum
    class_5 = dic[4] / total_sum
    class_6 = dic[5] / total_sum

    return class_1, class_2, class_3, class_4, class_5, class_6
    
def main():
    rgb_counts = anlayzeLabel("Labels/aachen_000000_000019_leftImg8bit.png")
    # rgb_counts = transformDic(rgb_counts)

    # Checking Class Counts
    for rgb, count in rgb_counts.items():
        print("Class: %s, Count: %d" % (rgb, count))

    # Visualize Data
    # visualizeData(rgb_counts)

    # Calculate Image Percentage
    # total_counts = getTotalCounts(rgb_counts)
    class_1, class_2, class_3, class_4, class_5, class_6 =calculatePercents(rgb_counts)

    print('Class 1: {:.2%}'.format(class_1))
    print('Class 2: {:.2%}'.format(class_2))
    print('Class 3: {:.2%}'.format(class_3))
    print('Class 4: {:.2%}'.format(class_4))
    print('Class 5: {:.2%}'.format(class_5))
    print('Class 6: {:.2%}'.format(class_6))
    
if __name__ == '__main__':
    main()