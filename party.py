import json
from itertools import combinations
from collections import defaultdict
from concurrent import futures

import pandas as pd
import numpy as np


def party_combinations(title='md80', top=30, unit=6):
    df = pd.read_csv(f'out/pokemon_rank.csv')[:top]
    return list(combinations(df['name'], unit))


def party_score(battle_results, party):
    print(party)
    party_score = defaultdict(float)
    for pty_pokemon in party:
        r = battle_results[pty_pokemon]
        for poke, score in r['win'].items():
            party_score[poke] += score
        for poke, score in r['lose'].items():
            party_score[poke] -= score
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
    df_score.to_csv('out/party/score.csv', chunksize=1000)


def main() -> None:
    p = party_combinations(top=50, unit=3)
    with open('out/battle_results/md80.json', 'r') as f:
        br = json.load(f)
    party_scores_multi_process(br, p)


if __name__ == '__main__':
    main()
