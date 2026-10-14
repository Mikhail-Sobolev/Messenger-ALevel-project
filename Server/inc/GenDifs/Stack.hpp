
#ifndef __inc_gendifs_hpp
#define __inc_gendifs_hpp
#include <stdint.h>
#include <string>

typedef struct stack {
    uint64_t SP;
    uint64_t Stack[512] // max stack size 512 for now
} stack;

namespace stk {

    void push(stack s, uint64_t i);
    void pop(stack s);
    uint64_t peek(stack s);
    std::string tosql(stack s);
};

#endif