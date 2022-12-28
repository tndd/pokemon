import json
import re
from glob import glob

import pandas as pd


def poke_score():
    file_paths = glob('out/battle_results/*.json')
    for path in file_paths:
        with open(path, 'r') as f:
            d = json.load(f)
        poke_score = []
        for poke_name_me, battle_results in d.items():
            score_win = sum(battle_results['win'].values())
            score_lose = sum(battle_results['lose'].values())
            poke_score.append([poke_name_me, score_win - score_lose])
        out_file_name = re.findall(r'.+/(.+)\.json', path)
        df = pd.DataFrame(poke_score, columns=('name', 'score')).set_index('name').sort_values('score', ascending=False)
        _std = df.std(ddof=0)
        _mean = df.mean()
        df['deviation'] = df['score'].map(lambda x: (10 * (x - _mean) / _std) + 50).astype(float)
        df.to_csv(f'out/pokemon_score/{out_file_name[0]}.csv')


def main() -> None:
    poke_score()


if __name__ == '__main__':
    main()
