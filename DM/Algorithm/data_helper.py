import numpy as np


def loadSamples():
    data_x = dict()
    data_y = dict()
    fp = open('../DataSet/character/train_x.csv')
    line = fp.readline()
    line = fp.readline()
    while line:
        parts = line.replace('"', '').strip().split(',')
        if len(parts) != 1139:
            print(line)
            continue
        sample = list()
        for i in parts[1:]:
            sample.append(float(i))
        data_x[parts[0]] = sample
        line = fp.readline()
    fp = open('../DataSet/character/train_y.csv')
    line = fp.readline()
    line = fp.readline()
    while line:
        parts = line.replace('"', '').strip().split(',')
        if len(parts) != 2:
            print(line)
            continue
        data_y[parts[0]] = float(parts[1])
        line = fp.readline()
    samples_x = list()
    samples_y = list()
    user_ids = list()
    for k, v in data_x.items():
        samples_x.append(v)
        samples_y.append([data_y[k]])
        user_ids.append(k)
    samples_x = np.array(samples_x)
    samples_y = np.array(samples_y)
    sample_size = len(samples_x)
    train_sample_size = int(sample_size * 0.9)
    return (samples_x[:train_sample_size], samples_y[:train_sample_size], user_ids[:train_sample_size],
            samples_x[train_sample_size:], samples_y[train_sample_size:], user_ids[train_sample_size:])
