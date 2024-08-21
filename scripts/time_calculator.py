import pandas as pd
import argparse

def getTimes(file):
    file = pd.read_csv(file)
    labels = file['Label']
    timestamps = file['Timestamp']

    d = dict()
    start = float(timestamps[0])
    end = 0
    startlabel = labels[0]
    for ind, each in enumerate(labels):
        if each != startlabel:
            startlabel = each
            end = float(timestamps[ind-1])
            d[each] = d.get(each,0) + (end - start)
            start = float(timestamps[ind])
    print(d)

    sum = 0
    print("each class in minutes")
    for k,v in d.items():
        print(f"for class {k} it is {v/60} minutes")
        sum += v/60

    print(f"total minutes:{sum}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Time Calculator', 
                                    description='Calculate each class duration for a specific participant', 
                                    epilog='Text at the bottom of help')
    parser.add_argument('filepath') # "C:/...../participant 05.csv"

    args = parser.parse_args()

    getTimes(args.filepath)
