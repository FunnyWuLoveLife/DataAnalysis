def loadLabel(path):
    label_P = {}
    label_N = {}
    with open(path) as fp:
        header = fp.readline()
        for line in fp.readlines():
            key = line.strip("\n").split(",")[0]
            data = line.strip("\n").split(",")[1]
            data = int(data)
            if data == 1:
                label_P[key] = data
            elif data == 0:
                label_N[key] = data
    return label_P, label_N


def loadScore(path):
    score = {}
    with open(path) as fp:
        header = fp.readline()
        for line in fp.readlines():
            uid = line.strip("\n").split(",")[0]
            data = line.strip("\n").split(",")[1]
            data = float(data)
            score[uid] = data
    return score


if __name__ == '__main__':
    label_P, label_N = loadLabel("test.csv")
    score = loadScore("0.023.csv")
    sumx = 0

    for key_P, val_P in label_P.items():
        if key_P not in score:
            continue
        for key_N, val_N in label_N.items():
            if key_N in score:
                if score[key_P] > score[key_N]:
                    sumx += 1
                elif score[key_P] == score[key_N]:
                    sumx += 0.5
                elif score[key_P] < score[key_N]:
                    sumx += 0

    print(sumx / (len(label_P) * (len(label_N))))
    pass
