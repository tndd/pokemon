import json
import re
from glob import glob
from collections import defaultdict


def poke_score():
    file_paths = glob('out/battle_results/*.json')
    poke_score_avg = defaultdict(float)
    for path in file_paths:
        with open(path, 'r') as f:
            d = json.load(f)
        poke_score = {}
        for poke_name_me, battle_results in d.items():
            score_win = sum(battle_results['win'].values())
            score_lose = sum(battle_results['lose'].values())
            poke_score[poke_name_me] = score_win - score_lose
            poke_score_avg[poke_name_me] += poke_score[poke_name_me]
        poke_score = dict(sorted(poke_score.items(), key=lambda x:x[1], reverse=True))
        out_file_name = re.findall(r'.+/(.+)\.json', path)
        with open(f'out/pokemon_score/{out_file_name[0]}.json', 'w') as f:
            json.dump(poke_score, f, indent=4)
    for poke_name_me in poke_score_avg.keys():
        poke_score_avg[poke_name_me] /= len(file_paths)
    poke_score_avg = dict(sorted(poke_score_avg.items(), key=lambda x:x[1], reverse=True))
    with open('out/pokemon_score/average.json', 'w') as f:
        json.dump(poke_score_avg, f, indent=4)



def main() -> None:
    poke_score()


if __name__ == '__main__':
    main()
