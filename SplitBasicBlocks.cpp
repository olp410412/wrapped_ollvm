//===- SplitBasicBlock.cpp - SplitBasicBlokc Obfuscation pass--------------===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
// This file implements the split basic block pass while extending its granularity in guided code randomization
// 
//
//===----------------------------------------------------------------------===//

#include "llvm/Transforms/Obfuscation/Split.h"
#include "llvm/Transforms/Obfuscation/Utils.h"
#include "llvm/CryptoUtils.h"

#define DEBUG_TYPE "split"

using namespace llvm;
using namespace std;

// Stats
STATISTIC(Split, "Basicblock splitted");

static cl::opt<int> SplitNum("split_num", cl::init(2),
                             cl::desc("Split <split_num> time each BB"));
static cl::opt<int> lyp233("lyp233", cl::init(0),
                           cl::desc("my parameters"));
static cl::opt<string> my_fun_name("function_name", cl::init("main"),
                                   cl::desc("Target function we split"));
// extern std::string mystring;
// static cl::opt<std::string> CtrlSeq("ctrl_seq", cl::init(""), cl::location(mystring),
//                                  cl::desc("Controlling if split or not"));

namespace {
struct SplitBasicBlock : public FunctionPass {
  static char ID; // Pass identification, replacement for typeid
  bool flag;

  SplitBasicBlock() : FunctionPass(ID) {}
  SplitBasicBlock(bool flag) : FunctionPass(ID) {
    
    this->flag = flag;
  }

  bool runOnFunction(Function &F);
  void split(Function *f);

  bool containsPHI(BasicBlock *b);
  void shuffle(std::vector<int> &vec);
};
}

char SplitBasicBlock::ID = 0;
static RegisterPass<SplitBasicBlock> X("splitbbl", "BasicBlock splitting");

Pass *llvm::createSplitBasicBlock(bool flag) {
  return new SplitBasicBlock(flag);
}

bool SplitBasicBlock::runOnFunction(Function &F) {
  // Check if the number of applications is correct
  if (!((SplitNum > 1) && (SplitNum <= 12))) {
    errs()<<"Split application basic block percentage\
            -split_num=x must be 1 < x <= 12";
    return false;
  }
  if (lyp233 == 1){
    // errs() << "yeah" << "\n";
  }
  Function *tmp = &F;

  // Do we obfuscate
  if (toObfuscate(flag, tmp, "split")) {
    split(tmp);
    ++Split;
  }

  return false;
}

// int my0 = 0;
// errs() << "Hello, this is a new function: " << f->getName() << "\n";
// errs() << "Hello this is a basic block, saving..." << "\n";
// errs() << "The length of the blocks is: " << bb_length << "\n";
// errs() << "Split01: Blocks that we may split is:\n" << lyp_split << "\n";
// errs() << "This block is too small or it has Phi node" << "\n";

void SplitBasicBlock::split(Function *f) {
  std::vector<BasicBlock *> origBB;

  int splitN = SplitNum;
  int bb_length = 0;
  int lyp_cnt = 0;
  int lyp_index = 0;
  int function_mask = -1;

  //-------------------- Save all basic blocks ----------------------
  for (Function::iterator I = f->begin(), IE = f->end(); I != IE; ++I) {
    origBB.push_back(&*I);
    bb_length += 1;
  }

  char *lyp_split = (char *)malloc(bb_length + 1);
  char *lyp_sequence = (char *)malloc(bb_length + 1);


  if (NULL == lyp_split || NULL == lyp_sequence)
  {
    errs() << "Malloc error\n\n";
    exit(-1);
  }
  /* In order to give feed back on the terminal, we use ascii code as mask */
  memset(lyp_split, 0x31, bb_length + 1); // [0x31, 0x31, 0x31, 0x31,..., 0x31]
  memset(lyp_split + bb_length, 0, 1); // [0x31, 0x31, 0x31, 0x31,..., 0x00]
  memset(lyp_sequence, 0x30, bb_length + 1); // [0x30, 0x30, 0x30, 0x30,..., 0x30]
  memset(lyp_sequence + bb_length, 0, 1); // [0x30, 0x30, 0x30, 0x30,..., 0x00]



  errs() << my_fun_name << "\t";
  errs() << f->getName() << "\n";
  // errs() << 500 << "\n"; it is supported

  function_mask = my_fun_name.compare(f->getName()); // split activated when function_mask equals to 0
  errs() << function_mask << "\n";
  if (0 == function_mask)
  {
    errs() << "We are splitting on Function: " << f->getName() << "\n";
    int buffer = 1;
    int buffer2 = 0;
    //----------- parse lyp233 (input parameter) into lyp_sequence
    //----------- to determine if it would be split or not.
    //----------- The way is to parse decimal number into binary sequence
    if (0 == lyp233)
    {
      for(int i = 0; i < bb_length; i++)
      {
         *(lyp_sequence + i) = 0x33;
      }
    }
    else {
      for (int i = 0; i < bb_length; i++) {
        buffer2 = lyp233 & buffer; // ke neng yue jie du
        if (buffer2 != 0) {
          *(lyp_sequence + i) = 0x33;
        } else {
          *(lyp_sequence + i) = 0x30;
        }
        buffer = buffer * 2;
      }
    }
  }
  else
  {
    errs() << "My_splitting ignore ''" << f->getName() << "'' because the parameters\n";
    for (int i=0;i<bb_length;i++)
    {
      *(lyp_sequence + i) = 0x30;
    }
  }
  for (std::vector<BasicBlock *>::iterator I = origBB.begin(),
           IE = origBB.end();
       I != IE; ++I, lyp_cnt++) {
    BasicBlock *curr = *I;
    // ++I means it starts from position of 1

    // No need to split a 1 inst bb
    // Or it contains a PHI node
    if (curr->size() < 2 || containsPHI(curr))
    {
      *(lyp_split + lyp_cnt) = 0x30;
      continue;
    }
    //if ( 0 == function_mask )
    //{
    if (0x33 == *(lyp_sequence + lyp_cnt))
      *(lyp_split + lyp_cnt) = 0x31;
    else
      *(lyp_split + lyp_cnt) = 0x32;

    //}
    //if (21 != bb_length) {
    //  *(lyp_split + lyp_cnt) = 0x31;
    //}
  }


  // The core part
  for (std::vector<BasicBlock *>::iterator I = origBB.begin(),
                                           IE = origBB.end();
       I != IE; ++I, lyp_index++) {
    BasicBlock *curr = *I;
    // ++I means it starts from position of 1

    // No need to split a 1 inst bb
    // Or ones containing a PHI node
    if (curr->size() < 2 || containsPHI(curr)) {
      // errs() << "This block is too small or it has Phi node" << lyp_index << "\n";
      // *(lyp_split + lyp_index) = 0x30;
      continue;
    }

    if (*(lyp_split + lyp_index) != 0x31){
      // errs() << "I dont want to split this node, for the diversity, Continue\n";
      continue;
    }
    // Check splitN and current BB size
    if ((size_t)splitN > curr->size()) {
      splitN = curr->size() - 1;
      // errs() << "This block is smaller than N, N was adapted to: " << splitN << "\n";
    }

    // Generate splits point
    std::vector<int> test;
    for (unsigned i = 1; i < curr->size(); ++i) {
      test.push_back(i);
    }
    // errs() << "split point generated\n";
    // Shuffle
    if (test.size() != 1) {
      shuffle(test);
      std::sort(test.begin(), test.begin() + splitN);
    }

    // Split
    BasicBlock::iterator it = curr->begin();
    BasicBlock *toSplit = curr;
    int last = 0;
    // errs() << "Well.. we are splitting..." << "\n";
    for (int i = 0; i < splitN; ++i) {
      for (int j = 0; j < test[i] - last; ++j) {
        ++it;
      }
      last = test[i];
      if(toSplit->size() < 2)
        continue;
      toSplit = toSplit->splitBasicBlock(it, toSplit->getName() + ".split");
    }

    ++Split;
  }
  // if (21 == bb_length)
  errs() << "Split03: Blocks that we actually split is:\n" << lyp_split << "\n";
  // else
  free(lyp_split);
  free(lyp_sequence);
}

bool SplitBasicBlock::containsPHI(BasicBlock *b) {
  for (BasicBlock::iterator I = b->begin(), IE = b->end(); I != IE; ++I) {
    if (isa<PHINode>(I)) {
      return true;
    }
  }
  return false;
}

void SplitBasicBlock::shuffle(std::vector<int> &vec) {
  int n = vec.size();
  for (int i = n - 1; i > 0; --i) {
    std::swap(vec[i], vec[cryptoutils->get_uint32_t() % (i + 1)]);
  }
}

