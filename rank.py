import json
import re
from glob import glob

import pandas as pd


def poke_score():
    file_paths = glob('out/battle_results/*.json')
    dfs = []
    for path in file_paths:
        with open(path, 'r') as f:
            d = json.load(f)
        poke_score = []
        for poke_name_me, battle_results in d.items():
            score_win = sum(battle_results['win'].values())
            score_lose = sum(battle_results['lose'].values())
            poke_score.append([poke_name_me, score_win - score_lose])
        condition = re.findall(r'.+/(.+)\.json', path)[0]
        df = pd.DataFrame(poke_score, columns=('name', f'score_{condition}')).set_index('name')
        dfs.append(df)
    df_score = pd.concat(dfs, axis=1)
    df_score.insert(0, 'score_mean', df_score.mean(axis=1))
    _std = df_score['score_mean'].std(ddof=0)
    _mean = df_score['score_mean'].mean()
    df_score.insert(0, 'deviation_score_mean', df_score[f'score_mean'].map(lambda x: (10 * (x - _mean) / _std) + 50).astype(float))
    df_score = df_score.sort_values('deviation_score_mean', ascending=False)
    df_score.to_csv(f'out/pokemon_rank.csv')


def main() -> None:
    poke_score()


if __name__ == '__main__':
    main()
