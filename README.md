# wrapped_ollvm

## LSIM
LSIM is a way to evaluate the structrual dissimilarity between software control-flow(in granular of function-level)
it takes two LLVM IR(.ll) file and function name as its input(default name is "main"). 


## split
substitute file with the same name(in ../obfuscator/lib/Transforms/Obfuscation)

append -mllvm -mysplit to activate its functionality

append -mllvm func_name to specify which needs to split

append -mllvm -lyp233 255() to specify those blocks (255 would be interpreted into a binary sequence as the mask for the corresponding order of block sequence)

### for example
../obfuscator/bin/clang test.c  -S -o test.s -mllvm split -mllvm mysplit -mllvm splitnum=2 -mllvm your-function-name -mllvm -lyp233 255
