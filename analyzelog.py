
import argparse
import json
import pandas as pd
from MultiLabelReader import getAverages
import matplotlib.pyplot as plt
import numpy as np

def parseargs():
    parser = argparse.ArgumentParser(description='Train a segmentor')
    parser.add_argument('--log_file', help='The Text file containing json objects')
    parser.add_argument('--label_dir', help='Directory of label files')
    # parser.add_argument('--label_path', help='Directory of label image files')
    # parser.add_argument('--checkpoint', help='Checkpoint file of config')

    args = parser.parse_args()
    return args

def weighted_average(values, weights):
    assert len(values) == len(weights)
    weighted_avg = 0
    for i in range(len(values)):
        weighted_avg = weighted_avg + values[i] * weights[i]
    # val = pd.DataFrame(values)
    # wei = pd.DataFrame(weights)

    # weighted_avg = wei * val

    # print(weighted_avg)
    return weighted_avg
    # return weighted_avg[0].values.tolist()

def graph_losses(losses, plot_file):
    # define data values
    x = range(len(losses))  # X-axis points
    y = losses # Y-axis points
    
    plt.plot(x, y)  # Plot the chart
    plt.savefig(plot_file)
    plt.show()  # display

def graph_losses_lossvals(losses, loss_vals, plot_file):
    # define data values
    x = range(len(losses))  # X-axis points
    y = losses # Y-axis points
    z = loss_vals
    
    plt.plot(x, y, label = "Train Loss")  # Plot the chart
    plt.plot(range(len(loss_vals)), z, label = "Val Loss")  # Plot the chart
    plt.legend()
    plt.savefig(plot_file)
    plt.show()  # display

def make_figure_name(log_file):
    temp = log_file.split("/")[-1]
    temp = temp.split(".")[0]
    return "figures/" + temp + ".png"


def main():
    args = parseargs()

    file = args.log_file
    labels = args.label_dir
    # labelpath = args.label_path
    assert isinstance(file, str)
    assert isinstance(labels, str)
    # assert isinstance(labelpath, str)
    iou_values = []
    acc_values = []
    loss_values = []
    loss_val_values = []
    with open(file) as txt_file:
        if "val" not in file:
            for item in txt_file:
                try:
                    json_object = json.loads(item)
                except:
                    print(item)
                if 'mode' in json_object:
                    if json_object['mode'] == 'train':
                        loss_values.append(json_object["loss"])
                        if 'loss_val' in json_object:
                            if json_object['loss_val'] < 100:
                                loss_val_values.append(json_object['loss_val'])
                    if json_object['mode'] == 'val' and json_object['epoch'] == 167:
                        # Get the IoU metrics
                        iou_values.append(json_object['IoU.road'])
                        iou_values.append(json_object['IoU.building'])
                        iou_values.append(json_object['IoU.tree'])
                        iou_values.append(json_object['IoU.car'])
                        iou_values.append(json_object['IoU.traffic'])
                        iou_values.append(json_object['IoU.other'])

                        # Get the Acc metrics
                        acc_values.append(json_object['Acc.road'])
                        acc_values.append(json_object['Acc.building'])
                        acc_values.append(json_object['Acc.tree'])
                        acc_values.append(json_object['Acc.car'])
                        acc_values.append(json_object['Acc.traffic'])
                        acc_values.append(json_object['Acc.other'])
    
            # averages = getAverages(labels)
            # iou_wei = weighted_average(iou_values, averages)
            # acc_wei = weighted_average(acc_values, averages)
            # print('Weighted IoU: {:.2%}'.format(iou_wei))
            # print('Weighted Acc: {:.2%}'.format(acc_wei))
            # graph_losses(loss_values, make_figure_name(file))
            graph_losses_lossvals(loss_values, loss_val_values, make_figure_name(file))
        else:
            for item in txt_file:
                json_object = json.loads(item)
                if 'mode' in json_object:
                    if json_object['mode'] == 'val':
                        # Get the IoU metrics
                        iou_values.append(json_object['IoU.road'])
                        iou_values.append(json_object['IoU.building'])
                        iou_values.append(json_object['IoU.tree'])
                        iou_values.append(json_object['IoU.car'])
                        iou_values.append(json_object['IoU.traffic'])
                        iou_values.append(json_object['IoU.other'])

                        # Get the Acc metrics
                        acc_values.append(json_object['Acc.road'])
                        acc_values.append(json_object['Acc.building'])
                        acc_values.append(json_object['Acc.tree'])
                        acc_values.append(json_object['Acc.car'])
                        acc_values.append(json_object['Acc.traffic'])
                        acc_values.append(json_object['Acc.other'])
            averages = getAverages(labels)
            print(averages)
            iou_wei = weighted_average(iou_values, averages)
            acc_wei = weighted_average(acc_values, averages)
            print('IoU Values: ', iou_values)
            print('Accuracy Values: ', acc_values)
            print('Weighted IoU: {:.2%}'.format(iou_wei))
            print('Weighted Acc: {:.2%}'.format(acc_wei))
            

            
if __name__ == '__main__':
    main()