import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def read_txt_as_data(filename):
    returnArray = []
    lines = open(filename).readlines()
    for line in lines:
        line = line.strip().split(',')
        if len(line) > 0:
            returnArray.append(np.array([np.float32(x) for x in line]))
    returnArray = np.array(returnArray)
    return returnArray


def load_data():
    action_sequence = read_txt_as_data('../data/cmu/train/basketball/basketball_1.txt')
    t, d = action_sequence.shape
    even_indices = range(0, t, 2)
    sampled_data_set = action_sequence[even_indices, :]
    return sampled_data_set, action_sequence


def normalization_stats(complete_data):
    data_mean = np.mean(complete_data, axis=0)
    data_std = np.std(complete_data, axis=0)
    dimensions_is_zero = []
    dimensions_is_zero.extend(list(np.where(data_std < 1e-4)[0]))
    dimensions_nonzero = []
    dimensions_nonzero.extend(list(np.where(data_std >= 1e-4)[0]))
    data_std[dimensions_is_zero] = 1.0
    

    dim_to_ignore = [0,  1,  2,  3,  4,  5,  6,   7,   8,   21,  22,  23,  24,  25,  26, 
                     39, 40, 41, 60, 61, 62, 63,  64,  65,  81,  82,  83,
                     87, 88, 89, 90, 91, 92, 108, 109, 110, 114, 115, 116]
    dim_to_use = [9,  10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 27, 28, 29, 30, 31,  32,  33,  34,  35,  36,  37,  38, 
                  42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,  59,  66,  67,  68,  69,  70,  71,  72,  73,  74, 
                  75, 76, 77, 78, 79, 80, 84, 85, 86, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 111, 112, 113]
    return data_mean, data_std, dim_to_ignore, dim_to_use, dimensions_is_zero, dimensions_nonzero


if __name__=='__main__':
    sample_data, complete_data = load_data()
    data_mean, data_std, dim_ignore, dim_use, dim_zero, dim_nonzero = normalization_stats(complete_data)

    self_link = [(i, i) for i in range(26)]
    neighbor_link_ = [(1,2),(2,3),(3,4),(5,6),(6,7),(7,8),(1,9),(5,9),
                      (9,10),(10,11),(11,12),(12,13),(13,14),
                      (11,15),(15,16),(16,17),(17,18),(18,19),(17,20),
                      (12,21),(21,22),(22,23),(23,24),(24,25),(23,26)]

    neighbor_link = [(i-1,j-1) for (i,j) in neighbor_link_]
    edge = self_link + neighbor_link

    index = 4
    """
        for i in range(26):
            print(dim_use[num+0], dim_use[num+1], dim_use[num+2])
            data_x.append(sample_data[index][dim_use[num+0]])
            data_y.append(sample_data[index][dim_use[num+1]])
            data_z.append(sample_data[index][dim_use[num+2]])

        data_ = []
        for j in range(3):
            data_.append(sample_data[index][dim_use[num+j]])
        num+=3
        data.append(data_)
    """

    #for index in range(len(sample_data)):
    for index in range(20):
        data_x, data_y, data_z = [], [], []

        num = 0
        for i in range(26):
            data_x.append(sample_data[index][dim_use[num+0]])
            data_y.append(sample_data[index][dim_use[num+1]])
            data_z.append(sample_data[index][dim_use[num+2]])
            num+=3

        x = np.array(data_x)
        y = np.array(data_y)
        z = np.array(data_z)


        fig = plt.figure()
        ax = Axes3D(fig)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        ax.plot(x[:1],  y[:1],  z[:1], marker="o", linestyle="None", color="r")
        ax.plot(x[1:2], y[1:2], z[1:2], marker="o", linestyle="None", color="g")
        ax.plot(x[2:],  y[2:],  z[2:], marker="o", linestyle="None", color="b")

        for link in neighbor_link_:
            ax.plot([data_x[link[0]-1], data_x[link[1]-1]], [data_y[link[0]-1], data_y[link[1]-1]], [data_z[link[0]-1], data_z[link[1]-1]], "o-") 

        plt.show()