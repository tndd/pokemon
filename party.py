from itertools import combinations
from collections import defaultdict
from concurrent import futures

import pandas as pd
import numpy as np


def party_combinations(top, unit):
    df = pd.read_csv(f'out/battle_results/avg.csv')[:top]
    return list(combinations(df['Self'], unit))


def get_party_score(battle_results, party):
    print(' | '.join(party))
    party_score = defaultdict(float)
    for pokemon_pty in party:
        r = battle_results.loc[pokemon_pty]
        for pokemon, score in r.items():
            party_score[pokemon] += score
    return (party, party_score)


def get_df_party_scores(battle_results, parties):
    scores = {}
    for party in parties:
        r = get_party_score(battle_results, party)
        party_name = '|'.join(r[0])
        scores[party_name] = r[1]
    df = pd.DataFrame.from_dict(data=scores, orient="index")
    df.index.name = 'Party'
    return df


def get_df_party_scores_multi_process(battle_results, parties, max_workers):
    parties_splited = list(np.array_split(parties, max_workers))
    with futures.ProcessPoolExecutor(max_workers=max_workers) as executer:
        fts = [executer.submit(get_df_party_scores, battle_results, parties) for parties in parties_splited]
    dfs = [f.result() for f in fts]
    df_score = pd.concat(dfs)
    df_score.insert(0, 'score', df_score.sum(axis=1))
    df_score = df_score.sort_values('score', ascending=False)
    return df_score


def party_score(top, unit, max_workers=4):
    p = party_combinations(top, unit)
    br = pd.read_csv('out/battle_results/avg.csv').set_index('Self').drop('score', axis=1)
    df_score = get_df_party_scores_multi_process(br, p, max_workers)
    df_score.to_csv(f'out/party/score_top{top}_unit{unit}.csv', chunksize=1000)


def main() -> None:
    party_score(top=30, unit=6, max_workers=2)


if __name__ == '__main__':
    main()
