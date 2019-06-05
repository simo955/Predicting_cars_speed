import sys
import os
sys.path.append(os.getcwd())

from src.features.feature_base import FeatureBase
from src import data
import pandas as pd

class SpeedsSensorDaysBefore(FeatureBase):
    """
    say for each street the avg speed
    | KEY | KM | DATETIME_UTC_y_0 | speed_avg_sensor_day_i_before | speed_sd_sensor_day_i_before | speed_min_sensor_day_i_before | speed_max_sensor_day_i_before | n_vehicles_sensor_day_i_before
    """

    def __init__(self, n_days_before=1):
        name = 'SpeedsSensorDaysBefore'
        self.n_days_before = n_days_before
        super(SpeedsSensorDaysBefore, self).__init__(
            name=name)

    def extract_feature(self):
        tr = data.speeds_original('train').drop(['KEY_2'], axis=1)
        te = data.speed_test_masked().drop(['KEY_2'], axis=1)
        s = pd.concat([tr, te])
        del te
        del tr
        f = s[['KEY', 'DATETIME_UTC', 'KM']].copy()
        s = s.rename(columns={'DATETIME_UTC': 'DATETIME_UTC_drop'})
        for i in range(self.n_days_before):
            colname = 'DATETIME_UTC_{}_D'.format(i)
            f[colname] = f.DATETIME_UTC - pd.Timedelta(days=i)
            f = pd.merge(f, s, how='left', left_on=['KEY', 'KM', colname], \
                        right_on=['KEY', 'KM', 'DATETIME_UTC_drop']) \
                        .drop([colname, 'DATETIME_UTC_drop'], axis=1)
            f = f.rename(columns={'SPEED_AVG': 'SPEED_AVG_{}_DAY_BEFORE'.format(i),
                            'SPEED_SD': 'SPEED_SD_{}_DAY_BEFORE'.format(i),
                            'SPEED_MIN': 'SPEED_MIN_{}_DAY_BEFORE'.format(i),
                            'SPEED_MAX': 'SPEED_MAX_{}_DAY_BEFORE'.format(i),
                            'N_VEHICLES': 'N_VEHICLES_{}_DAY_BEFORE'.format(i)})
        return f.rename(columns={'DATETIME_UTC': 'DATETIME_UTC_y_0'})

if __name__ == '__main__':
    print('how many days before do you want?')
    days = int(input())
    c = SpeedsSensorDaysBefore(days)

    print('Creating {}'.format(c.name))
    c.save_feature()

    print(c.read_feature(one_hot=True))
