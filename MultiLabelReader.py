from LabelReader import anlayzeLabel, calculatePercents
import os
from tqdm import tqdm

'''
palette_index = {(255, 0, 209): 0, #Road
                 (255, 204, 0): 1, #Building
                 (6, 255, 0): 2, # Tree
                 (0, 0, 255): 3, # Car
                 (219, 24, 22): 4, # Traffic
                 (43, 37, 67): 5, # Other
                 (0, 0, 0): 5}
'''


def Average(lst):
    return sum(lst) / len(lst)

def getAverages(path):
    class_1_percents = []
    class_2_percents = []
    class_3_percents = []
    class_4_percents = []
    class_5_percents = []
    class_6_percents = []

    for image in tqdm(os.listdir(path)):
        im_path = os.path.join(path, image)
        class_counts = anlayzeLabel(im_path)

        # print(class_counts.keys())

        # for rgb, count in class_counts.items():
        #     print("Class: %s, Count: %d" % (rgb, count))
        # break
        class_1, class_2, class_3, class_4, class_5, class_6 = calculatePercents(class_counts)

        class_1_percents.append(class_1)
        class_2_percents.append(class_2)
        class_3_percents.append(class_3)
        class_4_percents.append(class_4)
        class_5_percents.append(class_5)
        class_6_percents.append(class_6)

    # class_1_percents, class_2_percents, class_3_percents, class_4_percents, class_5_percents
    average1 = Average(class_1_percents)
    average2 = Average(class_2_percents)
    average3 = Average(class_3_percents) 
    average4 = Average(class_4_percents) 
    average5 = Average(class_5_percents)
    average6 = Average(class_6_percents)

    return [average1, average2, average3, average4, average5, average6]
    # return [average1, average2, average3, average5, average6]


def main():
    # class_1_percents, class_2_percents, class_3_percents, class_4_percents, class_5_percents = readFiles("Labels")
    # average1, average2, average3, average4, average5 = getAverages(class_1_percents, class_2_percents, class_3_percents, class_4_percents, class_5_percents)
    avgs = getAverages("datasets/FCG_Increased_Cars/labels")
    print('Class 1: {:.2%}'.format(avgs[0]))
    print('Class 2: {:.2%}'.format(avgs[1]))
    print('Class 3: {:.2%}'.format(avgs[2]))
    print('Class 4: {:.2%}'.format(avgs[3]))
    print('Class 5: {:.2%}'.format(avgs[4]))
    print('Class 6: {:.2%}'.format(avgs[5]))
    sum = avgs[0] + avgs[1] + avgs[2] + avgs[3] + avgs[4] + avgs[5]
    print(sum)

if __name__ == '__main__':
    main()