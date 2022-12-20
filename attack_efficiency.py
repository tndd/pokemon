import pandas as pd


def attack_efficiency(data_type, type_atk, type_def_1, type_def_2):
    effect = data_type.loc[type_atk][type_def_1]
    if type_def_2 != '':
        effect *= data_type.loc[type_atk][type_def_2]
    return effect


if __name__ == '__main__':
    d_type = pd.read_csv('type.csv', index_col=0)
    print(
        attack_efficiency(
            data_type=d_type,
            type_atk='Electric',
            type_def_1='Water',
            type_def_2='Flying'
        )
    )
