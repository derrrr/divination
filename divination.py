import io
import os
import sys
import unicodedata

import colorama
from collections import defaultdict
from fractions import Fraction
from random import randint

from hexagrams import ORIGIN_YANG, VAR_YANG, hexagram_name

def mod(a: int, b: int) -> int:
    """計算 a 除以 b 的餘數，如果餘數為 0，返回 b"""
    return a % b or b

def ying_4(pile: int) -> int:
    """四營而成易"""
    # 分而為二以象兩
    pile_right = randint(2, pile - 2)
    pile_left = pile - pile_right

    # 掛一以象三
    pile_right -= 1

    # 揲之以四以象四時，歸奇於扐以象閏
    hand = 1 + mod(pile_right, 4) + mod(pile_left, 4)
    return pile - hand

def var_3() -> int:
    """三變而成爻"""
    pile = 49  # 大衍之數五十，其用四十有九
    for _ in range(3):
        pile = ying_4(pile)
    return pile // 4

def calculate_probabilities() -> tuple[float, ...]:
    """計算爻的機率"""
    dist: dict[int, Fraction] = {49: Fraction(1)}
    for _ in range(3):
        next_dist: defaultdict[int, Fraction] = defaultdict(Fraction)
        for pile, prob in dist.items():
            weight = prob / (pile - 3)
            for pile_right in range(2, pile - 1):
                hand = 1 + mod(pile_right - 1, 4) + mod(pile - pile_right, 4)
                next_dist[pile - hand] += weight
        dist = next_dist

    yao_prob: defaultdict[int, Fraction] = defaultdict(Fraction)
    for pile, prob in dist.items():
        yao_prob[pile // 4] += prob
    return tuple(float(yao_prob[yao]) for yao in (6, 7, 8, 9))

def pad(text: str, width: int = 16) -> str:
    display_width = sum(2 if unicodedata.east_asian_width(c) in "FW" else 1 for c in text)
    return text + " " * (width - display_width)

def print_results(yao_list: list[int], yao_dict: dict[int, tuple[str, str, float]], use_color: bool) -> None:
    """顯示本卦、變卦及機率"""
    print(f"\n得到的卦是：\n{yao_list}\n")
    origin_name = hexagram_name([ORIGIN_YANG[yao] for yao in yao_list])
    var_name = hexagram_name([VAR_YANG[yao] for yao in yao_list])
    print(f"{pad('本卦')}變卦")
    print(f"{pad(origin_name)}{var_name}\n")
    total_prob = 1.0
    for yao in reversed(yao_list):
        origin, var, prob_yao = yao_dict[yao]
        line = f"{pad(origin)}{var}"
        if use_color and yao in (6, 9):
            line = f"\033[38;5;167m{line}\033[0m"
        print(f"{line}\n")
        total_prob *= prob_yao

    print(f"probability: {total_prob:.4%}\n")

def main() -> None:
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")

    # 計算機率
    yao_prob = calculate_probabilities()

    # 十有八變而成卦
    yao_list = [var_3() for _ in range(6)]

    # 組合成卦象
    yao_quo = [6, 7, 8, 9]
    yao_origin = ["--", "－", "--", "－"]
    yao_var = ["－", "－", "--", "--"]
    yao_dict = dict(zip(yao_quo, zip(yao_origin, yao_var, yao_prob)))

    input("冥想問題或輸入後Enter: ")

    use_color = sys.stdout.isatty() and "NO_COLOR" not in os.environ
    if use_color:
        colorama.just_fix_windows_console()
    print_results(yao_list, yao_dict, use_color)

if __name__ == "__main__":
    main()
