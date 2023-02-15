import os
import time
import re
import random


def error_code_checker(code_list):
    """
    Counting the number of error elements.
    @:param flag: TYPE INT: the error quantity
    The deployment of ``flag'' is for debugging which element in the code list got error.
    Using the conditional break point to catch the changing of ``flag''
    """

    flag = 0
    for i in range(0, len(code_list)):
        if code_list[i] != 0:
            flag = flag + 1
            return 1
    return flag


def command_gen_compile(compiler="", infile="", outfile="", method="-split", method_param=[], dbg_level=1,
                        time_start=0.0):
    split_num = random.randint(2, 8)
    t = time.time()
    # delta_t = time_start - t
    seed = int(time.time())
    delta_t = int((t - seed) * pow(10, 8))
    if 0 == len(method_param) and ("-split" == method):
        method_param = [str(" -mllvm -split_num=" + str(split_num) + " "),
                        " -mllvm -function_name=main ",
                        str("-mllvm -ran_seed=" + str(delta_t))]
    param_list = [compiler, infile, " -o ", outfile, " -mllvm ", method]
    cmd_compile = ""

    for i in range(0, len(param_list)):
        cmd_compile = cmd_compile + " " + str(param_list[i])
    for i in range(0, len(method_param)):
        cmd_compile = cmd_compile + " " + str(method_param[i])

    if dbg_level > 0:
        print(cmd_compile)

    return cmd_compile


def my_merge(layer, name_list1, name_list2, dbg_flag=False):
    script_name = "/home/yuanpei/yuanpei1/my1Workspace/E2_release1.py"
    merge_dir_name = "/home/yuanpei/yuanpei1/my1Workspace/layerview_with_merge/L" + str(layer)
    batch_size = 10
    log_file_name = str(layer) + ".log"
    merge_eor = os.system("python3 " + script_name + " " + merge_dir_name + " " + str(batch_size) + " " + log_file_name)
    if merge_eor != 0:
        print("Merging error, in guidiv.py")
        exit(0)
    # zai ying'she hui'lai
    # get list to branch
    # generate branch list (The white list)
    # delete those files in the (The black list)

    white_list = []
    black_list = []
    white_list_file = str(layer) + ".log"

    with open(white_list_file, "r") as wtf:
        white_list = list(wtf.read().split('\t'))
    for i in range(0, len(white_list)):
        name_buf = merge_dir_name + "/" + str(white_list[i])
        white_list[i] = name_buf

    for i in range(0, len(name_list1)):
        name_buf = name_list1[i]
        if name_buf not in white_list:
            # dbg_info:
            print("rm " + str(name_list2[i]))
            # dbg_info:
            print("rm " + str(name_list1[i]))
            # require: absolute file name.
            eor_rm1 = os.system(str("rm " + name_list1[i]))
            eor_rm2 = os.system(str("rm " + name_list2[i]))
            if (0 != eor_rm1) or (0 != eor_rm2):
                if dbg_flag:
                    print("Error while removing files. In the merge stage, func: merge--GuidediveEngine.py")
                    exit(0)

    return 0


def div_engine_v3():
    # environment
    t0 = time.time()

    # basic parameters
    branch_num = 9
    total_tree_depth = 4
    return 0


def div_engine_v2(merge=False):
    # now, it is only for splitting 
    # external_param_list = []
    t0 = time.time()

    branch_num = 7
    total_depth = 4
    cur_layers = 0

    dir_layers = []
    dir_path = '/home/yuanpei/yuanpei1/my1Workspace/branch_with_merge'
    cur_layer_name = "/"
    file_names_tree = []
    file_names_layer = []

    flag = 0
    shadow_dir_ctr = []
    # get .ll using cur_layers
    i = 0
    cnt = 0
    ir_cnt = 0
    t1 = time.time()

    while 0 == flag:
        cur_branch = []

        if 0 == cnt:
            cur_dir = dir_path
            dir_layers.append(dir_path)
            shadow_dir_ctr.append(i)
        elif "nop" != dir_layers[cur_layers]:
            cur_dir = dir_layers[cur_layers]
            # print(cur_dir)

        # Layer      1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2
        # IR name
        # To merge  0 1 0 0 1 0 0 1 1 0 0 0 0 1 1 0 0 1

        if i < total_depth:
            counting_depth_buf = cur_dir
            depth = counting_depth_buf.count('dir')

            if i < depth:
                i = depth
                # It means changing layers
                ir_cnt = 0

                # -prepare for merging
                # The merge happens only after layer changed.
                if merge and i > 0:
                    my_merge(i, file_names_layer, file_names_tree)
                    nop = 0

            # -----
            for root, dirs, files in os.walk(cur_dir):
                # print(files)
                nop = 0

            # file names must end with .ll
            if 0 == len(list(files)):
                tmp_file_name = "removed"
            else:
                tmp_file_name = list(files)[0]

            if 1 < len(files):
                print("eor01: more than one files in this dir before we branch: " + dir_path + cur_layer_name)
                exit(0)

            #
            # -prepare for branching
            #
            layerview = "/home/yuanpei/yuanpei1/my1Workspace/layerview_with_merge/L" + str(i + 1) + "/"

            for j in range(1, branch_num + 1):
                # i.e.: /home/yuanpei/yuanpei1/build/bin/clang 2.c -S -o 2.without.r1.ll -S -emit-llvm
                # -mllvm -split -mllvm -function_name=main -mllvm -lyp233=65535

                my_compile_command = "/home/yuanpei/yuanpei1/build/bin/clang -S -emit-llvm " + tmp_file_name + " -o " \
                                     + str((i + 1) * 10 + j) + ".ll -mllvm -split"
                if "removed" == tmp_file_name:
                    buf = "  "
                    # cur_layers = cur_layers + 1
                    break

                else:
                    buf = command_gen_compile("/home/yuanpei/yuanpei1/build/bin/clang -S -emit-llvm", tmp_file_name,
                                              str(str((i + 1) * 10 + j) + ".ll"), time_start=time.time())

                print(cur_dir)
                eor2 = os.system(str("cd " + cur_dir + " && " + buf))

                if 0 != eor2:
                    print("eor02: compile command error in function div_engine_v2")
                    exit(0)
                tmp_dir_name = str(str((i + 1) * 10 + j) + ".ll.dir")

                # as the next seed
                dir_layers.append(str(cur_dir + "/" + tmp_dir_name))
                shadow_dir_ctr.append(i + 1)
                eor3 = os.system("cd " + cur_dir + " && " + "mkdir " + str(tmp_dir_name))
                eor4 = os.system("cd " + cur_dir + " && " + "cp " + str((i + 1) * 10 + j) + ".ll" + " " + tmp_dir_name)
                eor5 = os.system("cd " + cur_dir + " && " + "cp " + str((i + 1) * 10 + j) + ".ll" + " " + layerview
                                 + str(ir_cnt) + ".ll")

                if 0 == eor3 and 0 == eor4 and 0 == eor5:
                    # Tree <--> Layer
                    file_names_tree.append(str(cur_dir + "/" + tmp_dir_name + "/" + str(i * 10 + 10 + j) + ".ll"))
                    file_names_layer.append(str(layerview + str(ir_cnt) + ".ll"))
                    print(file_names_tree[cnt] + "        " + file_names_layer[cnt])

                cnt = cnt + 1
                ir_cnt += 1

            # dir_layers.append(cur_branch)
            # print(dir_layers)
            t2 = time.time()
            print("L" + str(depth) + "n" + str(cur_layers) + ", total " + str(cnt) + " " + str(
                cnt / (t2 - t1)) + " iter/s")
            cur_layers = cur_layers + 1

        if 5 == i or i > total_depth:
            t3 = time.time()
            print("Div exits normally, " + str(t3 - t0))
            exit(0)

    return 0


if __name__ == "__main__":
    print("Hello yuanpei")
    div_engine_v2(merge=True)
