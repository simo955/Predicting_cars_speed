import sys
import os
sys.path.append(os.getcwd())

from src.features.avg_speed_street import AvgSpeedStreet
from src.features.avg_speed_sensor import AvgSpeedSensor
from src import data

"""
    merge objects of class feature_base to the base dataset

    features array: array of features class name ([F1, F2, ..]) -> to all of them will be
                        applied the default one hot
                    array of tuples of class names and boolean ([(F1, True), (F2, False), ..]) ->
                        will be applied the onehot only if specified by the boolean attribute
"""
def merge_single_mode(base_dataset, features_array, default_one_hot=False):
    print(f'df_shape: {base_dataset.shape}')
    for f in features_array:
        if type(f) == tuple:
            feature = f[0]().read_feature(one_hot=f[1])
        else:
            feature = f().read_feature(one_hot=default_one_hot)
        print(f'len of feature:{len(feature)}')
        base_dataset = base_dataset.merge(feature)
        print(f'df_shape: {base_dataset.shape}')
    return base_dataset

def merge(features_array, default_one_hot=False):
    save_path = 'resources/dataset/preprocessed/'
    train_base = data.base_dataset('train')
    test_base = data.base_dataset('test')
    merged_train = merge_single_mode(train_base, features_array, default_one_hot)
    print('train completed \n')
    merged_test = merge_single_mode(test_base, features_array, default_one_hot)
    merged_train.to_csv(save_path + 'merged_dataframe_train.csv.gz', compression='gzip', index=False)
    merged_test.to_csv(save_path + 'merged_dataframe_test.csv.gz', compression='gzip', index=False)

if __name__ == '__main__':
    features_array = [AvgSpeedStreet, AvgSpeedSensor]
    merge(features_array)