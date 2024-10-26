#include <stdio.h>

int stackPop(int stack[], int index) {
    if (index >= 0) {
        int value = stack[index];
        return value;
    } else {
        return 1;
    }
    return 0;
}

int stackPush(int stack[], int index, int value) {
    stack[index] = value;
    return 0;
}

int stackPeek(int stack[], int index) {
    return stack[index];
}

int main() {
    int Stack[64];
    int index = 0;
    
    stackPush(Stack, index, 9);
    index = index + 1;
    printf("%d\n", index);
    stackPush(Stack, index, 15);
    index = index + 1;
    printf("%d\n", index);

    int val = stackPop(Stack, index);
    index = index - 1;
    printf("%d\n", val);

    printf("%d\n", stackPeek(Stack, index));

    return 0;
}

