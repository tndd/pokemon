import json
from itertools import combinations
from collections import defaultdict
from concurrent import futures

import pandas as pd
import numpy as np


def party_combinations(top=10, unit=6):
    df = pd.read_csv(f'out/battle_results/avg.csv')[:top]
    return list(combinations(df['Self'], unit))


def party_score(battle_results, party):
    print(' | '.join(party))
    party_score = defaultdict(float)
    for pokemon_pty in party:
        r = battle_results.loc[pokemon_pty]
        for pokemon, score in r.items():
            party_score[pokemon] += score
    return (party, party_score)


def party_scores(battle_results, parties):
    scores = {}
    for party in parties:
        r = party_score(battle_results, party)
        party_name = '|'.join(r[0])
        scores[party_name] = r[1]
    df = pd.DataFrame.from_dict(data=scores, orient="index")
    df.index.name = 'Party'
    return df


def party_scores_multi_process(battle_results, parties, max_workers=4):
    parties_splited = list(np.array_split(parties, 4))
    executer = futures.ProcessPoolExecutor(max_workers=max_workers)
    fts = [executer.submit(party_scores, battle_results, parties) for parties in parties_splited]
    dfs = [f.result() for f in fts]
    df_score = pd.concat(dfs)
    df_score.insert(0, 'score', df_score.sum(axis=1))
    df_score = df_score.sort_values('score', ascending=False)
    df_score.to_csv('out/party/score.csv', chunksize=1000)


def main() -> None:
    p = party_combinations(top=50, unit=3)
    br = pd.read_csv('out/battle_results/avg.csv').set_index('Self').drop('score', axis=1)
    party_scores_multi_process(br, p)


if __name__ == '__main__':
    main()
