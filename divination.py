from random import randint

def mod(a, b):
    rem = a % b
    if rem == 0:
        rem = b
    return rem

# 四營而成易
def ying_4(pile):
    # 分而為二以象兩
    pile_right = randint(1, pile - 1)
    pile_left = pile - pile_right

    # print(pile_right, pile_left)

    # 掛一以象三
    if randint(0, 1) == 0:
        pile_left = pile_left - 1
    else:
        pile_right = pile_right - 1

    # print(pile_right, pile_left)

    # 揲之以四以象四時，歸奇於扐以象閏
    mod_right = mod(pile_right, 4)
    mod_left = mod(pile_left, 4)

    # print(mod_right, mod_left)

    hand = 1 + mod_right + mod_left

    pile = pile - hand

    # print(hand)
    # print("{}\n".format(pile))

    return pile

# 三變而成爻
def var_3():
    # 大衍之數五十，其用四十有九
    total = 50
    pile = total -1

    for i in range(3):
        pile = ying_4(pile)
    return pile

yao_list = []
for i in range(6):
    yao_list.append(var_3() // 4)

print("{}\n".format(yao_list))

prob_6 = (7/15)*(9/19)*(11/47)
prob_7 = ((8/17)*(10/21)*(36/47)+(10/19)*(11/47))+(8/15)*(9/19)*(11/47)
prob_8 = (9/19)*(11/21)*(36/47)+((9/17)*(10/21)*(36/47)+(10/19)*(11/47))
prob_9 = (10/19)*(11/21)*(36/47)

yao_quo = [6, 7, 8, 9]
yao_origin = ["--", "－", "--", "－"]
yao_var = ["－", "－", "--", "--"]
yao_prob = [prob_6, prob_7, prob_8, prob_9]
yao_content = [list(a) for a in zip(yao_origin, yao_var, yao_prob)]

yao_dict = dict(zip(yao_quo, yao_content))
# print(yao_dict)

print("本卦\t\t變卦")
prob = 1
for yao in reversed(yao_list):
    print("{}\t\t{}\n".format(yao_dict.get(yao)[0], yao_dict.get(yao)[1]))
    prob = prob * yao_dict[yao][2]

print("probability: {:.4%}\n".format(prob))