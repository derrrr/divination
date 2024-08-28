from random import randint

def mod(a, b):
    """計算 a 除以 b 的餘數，如果餘數為 0，返回 b"""
    return a % b or b

def ying_4(pile):
    """四營而成易"""
    # 分而為二以象兩
    pile_right = randint(1, pile - 1)
    pile_left = pile - pile_right

    # 掛一以象三
    if randint(0, 1) == 0:
        pile_left -= 1
    else:
        pile_right -= 1

    # 揲之以四以象四時，歸奇於扐以象閏
    hand = 1 + mod(pile_right, 4) + mod(pile_left, 4)
    return pile - hand

def var_3():
    """三變而成爻"""
    pile = 49  # 大衍之數五十，其用四十有九
    for _ in range(3):
        pile = ying_4(pile)
    return pile // 4

def calculate_probabilities():
    """計算爻的機率"""
    prob_6 = (7 / 15) * (9 / 19) * (11 / 47)
    prob_7 = ((8 / 17) * (10 / 21) * (36 / 47) + (10 / 19) * (11 / 47)) + (8 / 15) * (9 / 19) * (11 / 47)
    prob_8 = (9 / 19) * (11 / 21) * (36 / 47) + ((9 / 17) * (10 / 21) * (36 / 47) + (10 / 19) * (11 / 47))
    prob_9 = (10 / 19) * (11 / 21) * (36 / 47)
    return prob_6, prob_7, prob_8, prob_9

# 計算機率
prob_6, prob_7, prob_8, prob_9 = calculate_probabilities()
yao_prob = [prob_6, prob_7, prob_8, prob_9]

# 十有八變而成卦
yao_list = [var_3() for _ in range(6)]

# 組合成卦象
yao_quo = [6, 7, 8, 9]
yao_origin = ["--", "－", "--", "－"]
yao_var = ["－", "－", "--", "--"]
yao_dict = dict(zip(yao_quo, zip(yao_origin, yao_var, yao_prob)))


user_question = input("冥想問題或輸入後Enter: ")

def print_results(yao_list, yao_dict):
    """顯示本卦、變卦及機率"""
    print(f"\n得到的卦是：\n{yao_list}\n")
    print("本卦\t\t變卦")
    total_prob = 1.0
    for yao in reversed(yao_list):
        origin, var, prob_yao = yao_dict.get(yao, ("--", "--", 0))
        print(f"{origin}\t\t{var}\n")
        total_prob *= prob_yao

    print(f"probability: {total_prob:.4%}\n")

print_results(yao_list, yao_dict)