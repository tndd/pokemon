import pandas as pd

from frequency import get_frequency


def get_poke_weight():
    freq = get_frequency()
    values_sum = sum(freq['freq'].values())
    poke_weight = {}
    for poke, freq_num in freq['freq'].items():
        poke_weight[poke] = (freq_num / values_sum) * 100
    return poke_weight


def main() -> None:
    get_poke_weight()


if __name__ == '__main__':
    main()
