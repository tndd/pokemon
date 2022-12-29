import json
from itertools import combinations
from collections import defaultdict
from concurrent import futures

import pandas as pd


def party_combinations(title='md80', top=30, unit=6):
    df = pd.read_csv(f'out/pokemon_score/{title}.csv')[:top]
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
    executer = futures.ProcessPoolExecutor(max_workers=4)
    fts = [executer.submit(party_score, battle_results, party) for party in parties]
    for future in fts:
        party_name = '|'.join(future.result()[0])
        scores[party_name] = future.result()[1]
    df = pd.DataFrame.from_dict(data=scores, orient="index")
    df.index.name = 'Party'
    df.to_csv('out/party/score.csv')
    return scores


def main() -> None:
    p = party_combinations(top=100, unit=3)
    with open('out/battle_results/md80.json', 'r') as f:
        br = json.load(f)
    party_scores(br, p)


if __name__ == '__main__':
    main()
