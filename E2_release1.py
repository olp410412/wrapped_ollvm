import os
import sys
import itertools
import time

import numpy as np
import csv

import LSIM_release1


def optimal_subset_method_backwise_selection():

    return 0


# TODO complete this function
def gen_statistics(sim_matrix, statistic="median", log_level=0):
    cur_size = sim_matrix.shape()
    _row = np.sum(sim_matrix, axis=1)
    # Besides the average, target can also be the top 25% or xx.
    _target = np.median(_row)
    print("Cur batch dissimilarity is (a row): " + str(_target))
    print("Cur Avg Dis (before) is (instance each other): " + str(_target / list(cur_size)[0]))
    return 0


def evaluate_and_gen_sim_matrix(ir_batch, working_dic):
    """
    :param ir_batch: a list of IR files
    :param working_dic:
    :return:
    """
    mini_batch_size = len(ir_batch)
    sim_matrix = np.zeros((mini_batch_size, mini_batch_size))

    # compare each other
    enumerated_list = list(itertools.combinations(ir_batch, 2))

    cur_diss_list = []
    for _i in range(0, len(enumerated_list)):
        # DBG info: print(enumerated_list)
        # DBG info: print(str(enumerated_list[i][0]) + " " + str(enumerated_list[i][1]))

        ir_1_name = str(working_dic + "/" + str(enumerated_list[_i][0]))
        ir_2_name = str(working_dic + "/" + str(enumerated_list[_i][1]))

        # Remastered
        cur_diss_list.append(LSIM_release1.LSIM_Controller(ir_1_name, ir_2_name, "String_matching"))

    _cnt = 0
    for _i in range(0, len(ir_batch)):
        for _j in range(1 + _i, len(ir_batch)):
            sim_matrix[_i][_j] = cur_diss_list[_cnt]
            _cnt += 1
    sim_matrix = sim_matrix + sim_matrix.transpose()

    return sim_matrix


def top_k_method(cur_batch_size, matrix, row, target):
    # 输入参数后面的不需要，在函数内部进行计算，并通过参数选择采用的统计量类型
    result_seq = []

    for _i in range(0, cur_batch_size):
        # the word ``already'' means that, this is total the same to a previous node
        # if they are totally the same, their dissimilarity points to other nodes are also the same
        # Note that, even if SIMAtrix(i,j) is 1, we cannot specify where the dissimilarity point is
        # 虽然有一个不一样，但是无法确定哪里不一样，所以不能用前面那个替代。只有完全相同时，结构特征才有传递性，因为只记录了数量，没有记录位置
        _sim_already = 0

        for _j in range(0, _i):
            if 0 == matrix[_i][_j]:
                _sim_already += 1

        if row[_i] >= target and 0 == _sim_already:
            result_seq.append(1)
            # i.e., satisfy[i] = 1
        else:
            result_seq.append(0)

    return result_seq


def e2_controller(working_dir_name, cur_batch_size):

    return 0


"""
Args: 
[1] Working dir name
[2] batch size
[3] where to store the log.txt
"""

if __name__ == "__main__":
    # e2 = os.system("python3 LSIM1.py 2.ll 2.without.r1.ll")

    # os.system("rm E2.tmp0")
    t0 = time.time()
    dir_path = sys.argv[1]
    batch_size = int(sys.argv[2])
    log_file = sys.argv[3]

    for root, dirs, files in os.walk(dir_path):
        # print(files)
        nop = 0
    file_names = list(files)
    # rename bb using .cpp ?
    batch_num = int(len(file_names) / batch_size)
    batch_tail = len(file_names) % batch_size
    eor1 = os.system("touch " + log_file)

    for cur_batch in range(0, batch_num + 1):
        batch = []
        """
        # Version 1
        e0 = os.system("touch E2.tmp0")
        if 0 != e0:
            print("In E2.py main, error while touching E2.tmp0")
        """

        flag_final_batch = 0

        if 0 == batch_tail:
            if batch_num - 1 == cur_batch:
                t1 = time.time()
                print("Evaluation completed, cur_batch: " + str(cur_batch) + " time: " + str(t1 - t0))
                exit(0)
            else:
                for cnt in range(0, batch_size):
                    batch.append(file_names[cur_batch * batch_size + cnt])

        else:
            if cur_batch < batch_num:
                for cnt in range(0, batch_size):
                    batch.append(file_names[cur_batch * batch_size + cnt])
            else:
                for cnt in range(0, batch_tail):
                    batch.append(file_names[cur_batch * batch_size + cnt])

        # -------------------------------------------------------------------------------------------------------------
        # begin the loop handling
        # compare each other

        file_name_list = list(batch)
        # retain this, because the following code require the ``file_name_list''
        print(file_name_list)

        """
        file_list = list(itertools.combinations(batch, 2))
        length = len(file_list)
        diss_list = []

        for i in range(0, length):
            # DBG info: print(str(file_list[i][0]) + " " + str(file_list[i][1]))
            # command_line = "python3 ./LSIM_release1.py " + dir_path + "/" + str(file_list[i][0]) + " " + \
            # dir_path + "/" + str(file_list[i][1]) + " mode_str >> E2.tmp0"
            IR1_name = str(dir_path + "/" + str(file_list[i][0]))
            IR2_name = str(dir_path + "/" + str(file_list[i][1]))

            
            # Version 1{
            command_line = "python3 ./LSIM_release1.py " + str(IR1_name) + " " + str(IR2_name) + " mode_str >> E2.tmp0"
            eor = os.system(command_line)
            if 0 != eor:
                print("Error in E2.py main")
                exit(0)
            }Version 1

            # Remastered
            diss_list.append(LSIM_release1.LSIM_Controller(IR1_name, IR2_name, "String_matching"))
        """

        # handling data
        """
        SIMAtrix = np.zeros((len(batch), len(batch)))
        # Note that, in the last batch, its size may not equal to the parameter: batch_size
        # but, we can use ``cur_batch_size'' instead of using the ``len(batch)''. 

        # Version 1
        buf_list1 = []
        with open("E2.tmp0") as f:
            lines = csv.reader(f, delimiter='\n')
            for x in lines:
                res = str(x).split(',')[3]
                # print(res)
                res1 = res.strip(']')
                res2 = res1.strip('\'')
                # print(res2)
                buf_list1.append(res2)
                # Note that, the dissimilarity in buf_list1 is string typed. type in "diss_list" is integer

        print(buf_list1)
        print(50 * '*')
        print(diss_list)
        

        cnt = 0
        for i in range(0, len(batch)):
            for j in range(1 + i, len(batch)):
                # SIMAtrix[i][j] = buf_list1[cnt]
                SIMAtrix[i][j] = diss_list[cnt]
                cnt += 1
        SIMAtrix = SIMAtrix + SIMAtrix.transpose()
        buf_matrix = evaluate_and_gen_sim_matrix(batch, dir_path)
        buf_matrix_diss = buf_matrix - SIMAtrix

        print(SIMAtrix)
        print(buf_matrix_diss)
        """

        SIMAtrix = evaluate_and_gen_sim_matrix(batch, dir_path)
        print(SIMAtrix)

        SIM_row = np.sum(SIMAtrix, axis=1)
        # Besides the average, target can also be the top 25% or xx.
        SIM_target = np.median(SIM_row)
        print("Cur batch dissimilarity is (a row): " + str(SIM_target))
        print("Cur Avg Dis (before) is (instance each other): " + str(SIM_target / batch_size))

        # -------------------------------------------------------------------------------------------------------------
        """
        # REQUIRE: batch, SIMAtrix, SIM_row, SIM_target
        # ENSURE: satisfy
        # bu'zhu'shi'diao, er'shi'jia'ru'xin'de, bi'jiao'ta'men'de'jie'guo, shi'fou'yi'zhi
        satisfy = []

        for i in range(0, len(batch)):
            # the word ``already'' means that, this is total the same to a previous node
            # if they are totally the same, their dissimilarity points to other nodes are also the same
            # Note that, even if SIMAtrix(i,j) is 1, we cannot specify where the dissimilarity point is
            # 虽然有一个不一样，但是无法确定哪里不一样，所以不能用前面那个替代。只有完全相同时，结构特征才有传递性，因为只记录了数量，没有记录位置
            sim_already = 0

            for j in range(0, i):
                if 0 == SIMAtrix[i][j]:
                    sim_already += 1

            if SIM_row[i] >= SIM_target and 0 == sim_already:
                satisfy.append(1)
                # i.e., satisfy[i] = 1
            else:
                satisfy.append(0)
        """

        # the variable ``satisfy'' is for deciding which IR to be retained
        satisfy = top_k_method(len(batch), SIMAtrix, SIM_row, SIM_target)

        # debug info: file_name_list = list(batch)
        # debug info: print(file_name_list)
        # debug info: test_buffer_for_SEQ_satisfy = top_k_method(len(batch), SIMAtrix, SIM_row, SIM_target)
        # debug info: print(50 * '*')
        # debug info: print(test_buffer_for_SEQ_satisfy)
        # debug info: print(satisfy)
        # debug info: print(50 * '+')

        # listing those nodes to be retained
        final_list = []
        for i in range(0, len(batch)):
            if 1 == satisfy[i]:
                final_list.append(file_name_list[i])

        mat_buf = evaluate_and_gen_sim_matrix(final_list, dir_path)
        SIM_row2 = np.sum(mat_buf, axis=1)
        # Besides the average, target can also be the top 25% or xx.
        SIM_target2 = np.median(SIM_row2)
        print("Cur batch dissimilarity (after) is (a row, note that the row length is shortened): " + str(SIM_target2))
        print("Cur Avg Dis (after) is (instance each other): " + str(SIM_target2 / len(final_list)))

        with open(log_file, "a+") as f_out:
            for i in range(0, len(final_list)):
                if 0 == i and cur_batch == 0:
                    # final_list, aka the whitelist.
                    # IR, only those in the final list, can take part in the next transformations
                    f_out.write(final_list[i])
                else:
                    f_out.write("\t" + final_list[i])

        print(final_list)
        print("------------------------------------------------")

        """
        # Version 1
        e3 = os.system("rm E2.tmp0")
        if 0 != e3:
            print("In E2_release1.py, main. Error while deleting E2.tmp0")
        """

    t2 = time.time()
    print("Evaluation completed, time: " + str(t2 - t0))



