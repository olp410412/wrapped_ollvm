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


def sort_bb(bb_sequence, adjacent_list):
    new_adjacent_list = []

    return new_adjacent_list


def rename_bb(adjacent_list, ir_names, debug_mode=False):
    rename_adjacent_list = []
    # check: adjacent_list is a 2-elements tuple
    for i in range(0, len(adjacent_list)):
        if 2 != len(adjacent_list[i]):
            if debug_mode:
                print("The shape of adjacent_list is unexpected")
                exit(0)
            else:
                return [(0, 1)]

    """
    pre = []
    child = []
    # change name
    pre_names = []
    child_names = []
    """

    # TODO check the elements in ir_names to make sure they are identical
    """
    for i in range(0, len(adjacent_list)):
        pre.append(adjacent_list[i][0])
        child.append(adjacent_list[i][1])
    """

    # begin: renaming
    for i in range(0, len(adjacent_list)):
        buffer_pre = -1
        buffer_child = -1

        for j in range(0, len(ir_names)):
            if 0 == i:
                buffer_pre = 0
            if adjacent_list[i][0] == ir_names[j]:
                buffer_pre = j + 1
            if adjacent_list[i][1] == ir_names[j]:
                buffer_child = j + 1

        # begin: removing loops.
        # Note that: With the pre-condition that, the child node already has a pre node
        # TODO While removing, make sure the child node actually has a pre node

        if buffer_pre < buffer_child:
            rename_adjacent_list.append((buffer_pre, buffer_child))
        else:
            print("Here is a loop in i==" + str(i))
            nop = 0

    """
        for i in range(0, len(pre)):
        pre_names.append(pre[i])
    for i in range(0, len(child)):
        child_names.append(child[i])

    for i in range(0, len(pre)):
        for j in range(0, len(ir_names)):
            if pre[i] == ir_names[j]:
                pre_names[i] = j + 1
    for i in range(0, len(child)):
        for j in range(0, len(ir_names)):
            if child[i] == ir_names[j]:
                child_names[i] = j + 1

    pre_names[0] = 0
    # dbg_info: checking renaming is matched or not
    # for i in range(0, len(pre)):
    #     print(str(pre[i]) + "        " + str(ir_names[pre_names[i] - 1]) + "        " + str(pre_names[i]))

    """
    # check: Does every block renamed ?
    for i in range(0, len(rename_adjacent_list)):
        if (-1 == rename_adjacent_list[i][0]) or (-1 == rename_adjacent_list[i][1]):
            if debug_mode:
                print("The block " + str(i) + " was not renamed")
                exit(0)
            else:
                return [(0, 1)]

    return sorted(rename_adjacent_list)


def traverse_layers(adjacent_list, ir_names, debug_print="false"):
    # TODO clairify that, loop should be excluded
    # TODO identifying loop and turn a loop into a single node label
    travel_res = []
    pre = []
    child = []
    layers_for_each_node = []

    renamed_adjacent_list = rename_bb(adjacent_list, ir_names)
    if len(renamed_adjacent_list) != len(adjacent_list):
        # TODO: Solve the renaming error
        # print("renaming length error")
        return [0]
    for i in range(0, len(adjacent_list)):
        pre.append(renamed_adjacent_list[i][0])
        child.append(renamed_adjacent_list[i][1])

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
            cnt = 0
            while buffer != -1:
                # TODO: does it may become an infinite loop

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
                cnt += 1
                if cnt >= 10000000:
                    if debug_print:
                        print("Loop may be infinite in traverse--LSIM_release1.py, please check!")
                        exit(0)
                    else:
                        return []

    depth = max(layers_for_each_node) + 1
    for i in range(0, depth):
        travel_res.append(0)
    for i in range(0, len(layers_for_each_node)):
        if layers_for_each_node[i] != -1:
            travel_res[layers_for_each_node[i]] += 1
    if debug_print == "true":
        print("Layers debug info. You can compare it with LLVM command \" opt -dom-cfg filename.ll\" ")

    """
    # dbg info: Do: Print cfg
    depth_cnt = 0
    cur_layer = 0
    for i in range(0, len(renamed_adjacent_list)):
        cur_layer = renamed_adjacent_list[i][0]
        if cur_layer == depth_cnt:
            print(renamed_adjacent_list[i], end=" ")
        if depth_cnt < cur_layer:
            print(renamed_adjacent_list[i], end=" ")
            print("  ")
            depth_cnt = cur_layer
        if depth_cnt > cur_layer:
            if debug_print == "true":
                print("Error in printing layers")
                exit(0)
            else:
                return [0]

    # Do: Print travel result
    for i in range(0, len(travel_res)):
        print(" x " * travel_res[i])
    """
    return travel_res


def HD(seq1, seq2):
    length1 = max(len(seq1), len(seq2))
    length2 = min(len(seq1), len(seq2))
    num1 = length1 - length2
    num2 = 0
    for i in range(0, length2):
        if seq1[i] != seq2[i]:
            num2 += 1
    hamming_distance = num2 + num1
    return hamming_distance


# Find and sequence each basic block in IR, by matching function name and block name
# -> Find a function name
# -> In this function, every named block has a label. by matching the ``<label>'',
# -> therefore, it forms a : FUNCTION1 bb1,bb2,bb3 | FUNCTION2 bb1,bb2,bb3,bb4 | , ... ,
def matching_blocks(filename, name="main", debug_mode="false"):
    res = []
    names = []
    with open(filename, "r") as fd:
        bb_matrix = []
        bb_in_funs = []
        bb_name_in_funs = []
        bb_name_matrix = []
        function_name_list = []
        buf_cnt = 0
        for line in fd.readlines():
            # print(line)
            buf_cnt += 1
            preds = re.findall(r"<label>:.*?\n|[^%]split.*:", line)  # find basic blocks by matching "<label x>" in IR file.
            # TODO preds need, discuss their situations ?
            # preds = re.findall(r"<label>:.*?\n", line)
            funs = re.findall(r"define.*?\n", line)

            if funs:
                # print("I catched a function", end="\t")
                function_name = re.findall(r"@.*?\(", line)

                name_buffer = str(function_name).strip('[]\'\\@(')
                # print("It is" + str(function_name))
                function_name_list.append(name_buffer)
                if len(bb_in_funs) > 0:
                    # print(sorted(bb_in_funs))
                    # bb_matrix.append(sorted(bb_in_funs))
                    bb_matrix.append(bb_in_funs)
                    bb_name_matrix.append(bb_name_in_funs)
                else:
                    bb_matrix.append([])
                    bb_name_matrix.append([])
                bb_in_funs = []
                bb_name_in_funs = []
            if preds:
                # TODO split this string and handle
                # Here to discuss
                buf_find_label = []
                buf_find_split = []
                buf_find_label = re.findall(r"<label>:.*:", line) # do not extract the numbers in splitxx
                node = [] # current basic block
                buf_str = line.strip(';').split(';')
                if len(buf_str) > 2 or 0 == len(buf_str):
                    print("Error while processing line " + str(buf_cnt) + " in file " + str(filename)
                          + "In matching_blocks, LSIM_release.py. We extracted an unexpected candidate string number")
                    exit(0)

                if 1 == len(buf_find_label):
                    label = re.findall(r"\d+", buf_find_label[0])
                    node.append(label[0])
                elif 0 == len(buf_find_label):
                    node.append(re.findall(r".split.*?:", buf_str[0])[0].strip(':'))
                elif len(buf_find_label) > 1:
                    print("In matching_blocks, LSIM_release.py, we extracted more than one <label> in file: " + str(filename))
                    exit(0)
                else:
                    print("Unexpected error in matching_blocks, LSIM_release.py")
                    exit(0)

                if 2 == len(buf_str):
                    node1 = re.findall(r"%.*", buf_str[1])  # 匹配结果, 根据preds行, 第一个是有向终点, 后面是起点

                node_2 = re.split(', ', node1[0])

                # node.append(node1[0])
                for i in range(len(node_2)):
                    str_buf = str(node_2[i])
                    node.append(str_buf.strip('%'))
                # print(node)
                bb_name_in_funs.append(node[0])
                for i in range(len(node) - 1):
                    # res.append((int(node[i + 1]), int(node[0])))
                    bb_in_funs.append((node[i + 1], node[0]))
                    # dbg info: if name == name_buffer:
                    # dbg info:    print((node[i + 1], node[0]))
        # print(sorted(bb_in_funs))
        # bb_matrix.append(sorted(bb_in_funs))
        bb_matrix.append(bb_in_funs)
        bb_name_matrix.append(bb_name_in_funs)

    for i in range(0, len(function_name_list)):
        if function_name_list[i] == name:
            res = bb_matrix[i+1]
            names = bb_name_matrix[i + 1]
            if debug_mode == "true":
                print(function_name_list[i], end="\t")
                print(bb_matrix[i + 1])
    return res, names


def LSIM(filename1, filename2, fun_name1="main", fun_name2="main"):
    """
    LSIM evaluates the Layer-SIMilarity(LSIM) between two intermediate representation
    It takes two .ll file as its parameter, computes their HD(layer_traversal_ir_1, layer_traversal_ir_2) as the output
    @:param filename1: TYPE STRING:
    @:param fun_name1: TYPE STRING:
    """

    E2 = 0
    if fun_name1 != fun_name2:
        print("Warning, comparing structure between two different functions is not recommend")
        print("If you insist, we continue")

    IR1, ir_names1 = matching_blocks(filename1, name=fun_name1)
    # print("-" * 60)
    IR2, ir_names2 = matching_blocks(filename2, name=fun_name2)
    layer1 = traverse_layers(IR1, ir_names1)
    layer2 = traverse_layers(IR2, ir_names2)
    E2 = HD(layer1, layer2)

    return E2


def LSIM_SCC(filename1, filename2, fun_name1="main", fun_name2="main"):
    res = -1

    return res


def LSIM_Controller(IR1, IR2, matching_mode):
    """
    @:param src_file: TYPE=STRING:
    @:param dst_file: TYPE=STRING:
    @:param matching_mode: TYPE=STRING:

    """
    result = 0
    if "String_matching" == matching_mode:
        result = LSIM(IR1, IR2)
    elif "SCC_matching" == matching_mode:
        result = LSIM_SCC(IR1, IR2)
    else:
        print("Please specify the matching mode in finding the basic blocks in the IR files")
        return -1

    return result


if __name__ == '__main__':
    # cf g1 = [(0, 2), (2, 4), (4, 10), (4, 13), (10, 12), (12, 26), (13, 16), (16, 18), (18, 19), (18, 22), (19, 21),
    #        (21, 25), (22, 24), (24, 25), (25, 26)]
    # cfg2 = []
    # matching_blocks("2.1.ll")
    # print((sys.argv))

    file_src = sys.argv[1]
    file_dst = sys.argv[2]
    mode = sys.argv[3]

    if "" == file_src or "" == file_dst:
        print("void param! In LSIM_release1.py")
        exit(0)

    if "mode_str" == mode:
        dissimilarity = LSIM(file_src, file_dst)
    else:
        dissimilarity = LSIM_SCC(file_src, file_dst)

    print("Dissimilarity," + str(sys.argv[1]) + "," + str(sys.argv[2]) + "," + str(dissimilarity))
    # print("Their dissimilarity is " + str(dissimilarity))
    # exit(dissimilarity)
