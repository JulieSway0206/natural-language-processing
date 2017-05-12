import csv
from sklearn.cross_validation import train_test_split
import pandas as pd

def split_data():
    list = []
    for row in pd.read_csv('data/amazonreview.csv', chunksize=2000):
        df = pd.DataFrame(data=row)
        list += df.values.tolist()
    list_train, list_test = train_test_split(list, test_size=0.2)


    with open('data/train_data.csv', 'w') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerow(['Id', 'Score', 'Text'])
        wr.writerows(list_train)
    with open('data/test_data.csv', 'w') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerow(['Id', 'Score', 'Text'])
        wr.writerows(list_test)

    # with open('data/ex_data.csv', 'w') as file:
    #     wr = csv.writer(file, dialect='excel')
    #     wr.writerow(['Id', 'Score', 'Text'])







if __name__ == "__main__":
    split_data()

