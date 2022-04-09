import os
import re
import sys


# to determine which is the previous one of node x
def find_previous(pre_list, this_list, x):
    _result = 0
    candidates = []
    for j in range(0, len(this_list)):
        if x == this_list[j]:
            candidates.append(pre_list[j])
    if 0 == len(candidates):
        _result = -1
    elif 1 == len(candidates):
        _result = candidates[0]
    else:
        _result = min(candidates)
    return _result


def traverse_layers(adjacent_list, debug_print="false"):
    travel_res = []
    pre = []
    child = []
    layers_for_each_node = []

    for i in range(0, len(adjacent_list)):
        pre.append(adjacent_list[i][0])
        child.append(adjacent_list[i][1])

    number = max(max(pre), max(child))
    # total number is 27 (from 0 to 26). that is (0, max(child) + 1)
    for i in range(0, number + 1):
        if 0 == i:
            layers_for_each_node.append(0)
        else:
            layers_for_each_node.append(-1)

    # note that <label0> is always in layer0
    for i in range(0, number + 1):
        if i in child:
            # print("Counting previous nodes for <label" + str(i) + ">:")
            number_of_pres = 0
            buffer = 0
            x = i
            while buffer != -1:
                buffer = find_previous(pre, child, x)
                previous_node = -1
                if buffer != -1:
                    previous_node = buffer
                    # print(previous_node, end="\t")
                    number_of_pres += 1
                    x = previous_node
                else:
                    # print("到头啦", end="\t")
                    # print("depth == " + str(number_of_pres), end="\n")
                    layers_for_each_node[i] = number_of_pres
    depth = max(layers_for_each_node) + 1
    for i in range(0, depth):
        travel_res.append(0)
    for i in range(0, len(layers_for_each_node)):
        if layers_for_each_node[i] != -1:
            travel_res[layers_for_each_node[i]] += 1
    if debug_print == "true":
        print("Layers debug info. You can compare it with LLVM command \" opt -dom-cfg filename.ll\" ")
    return travel_res


def HD(seq1, seq2):
    length1 = max(len(seq1), len(seq2))
    length2 = min(len(seq1), len(seq2))
    num1 = length1 - length2
    num2 = 0
    for i in range(0, length2):
        if seq1[i] != seq2[i]:
            num2 += 1
    num3 = num2 + num1
    return num3


def matching_blocks(filename, name="main", debug_mode="false"):
    res = []
#    with open("1.1.ll", "r") as fd:
# TODO 通过匹配define ret关键词划分基本块所属的函数
# TODO 和define同一行的@后面，()的前面 是 函数名: @xxx()
# 做到了这里 I catched a function	It is['@base64_parser(']
    with open(filename, "r") as fd:
        bb_matrix = []
        bb_in_funs = []
        function_name_list = []
        for line in fd.readlines():
            # print(line)
            preds = re.findall(r"<label>.*?\n", line)  # find basic blocks by matching "<label x>" in IR file.
            funs = re.findall(r"define.*?\n", line)

            if funs:
                # print("I catched a function", end="\t")
                function_name = re.findall(r"@.*?\(", line)

                name_buffer = str(function_name).strip('[]\'\\@(')
                # print("It is" + str(function_name))
                function_name_list.append(name_buffer)
                if len(bb_in_funs) > 0:
                    # print(sorted(bb_in_funs))
                    bb_matrix.append(sorted(bb_in_funs))
                else:
                    bb_matrix.append([])
                bb_in_funs = []
            if preds:
                node = re.findall(r"\d+", preds[0])  # 匹配结果, 根据preds行, 第一个是有向终点, 后面是起点
                # print(node)
                for i in range(len(node) - 1):
                    # res.append((int(node[i + 1]), int(node[0])))
                    bb_in_funs.append((int(node[i + 1]), int(node[0])))
        # print(sorted(bb_in_funs))
        bb_matrix.append(sorted(bb_in_funs))
    for i in range(0, len(function_name_list)):
        if function_name_list[i] == name:
            res = bb_matrix[i+1]
            if debug_mode == "true":
                print(function_name_list[i], end="\t")
                print(bb_matrix[i + 1])
    return sorted(res)


# Target: evaluates the Layer-SIMilarity(LSIM) between two intermediate representation
# It takes two .ll file as its parameter, computes their HD(layer_traversal_ir_1, layer_traversal_ir_2) as the output
# params: IR_1(.ll file) IR_2(.ll file)
def LSIM(filename1, filename2, fun_name1="main", fun_name2="main"):
    E2 = 0
    if fun_name1 != fun_name2:
        print("Warning, comparing structure between two different functions is not recommend")
        print("If you insist, we continue")
    IR1 = matching_blocks(filename1, name=fun_name1)
    IR2 = matching_blocks(filename2, name=fun_name2)
    layer1 = traverse_layers(IR1)
    layer2 = traverse_layers(IR2)
    E2 = HD(layer1, layer2)

    return E2


if __name__ == '__main__':
    # cfg1 = [(0, 2), (2, 4), (4, 10), (4, 13), (10, 12), (12, 26), (13, 16), (16, 18), (18, 19), (18, 22), (19, 21),
    #        (21, 25), (22, 24), (24, 25), (25, 26)]
    # cfg2 = []
    # matching_blocks("2.1.ll")
    dissimilarity = LSIM("2.1.ll", "2.1.ll")

    print("Their dissimilarity is " + str(dissimilarity))