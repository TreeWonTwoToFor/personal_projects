#include <stdio.h>

int main()
{
    int num1 = 1;
    int num2 = 2;
    int sum = num1 + num2;
    printf("%d\n", num1);
    printf("%d\n", num2);
    printf("%d\n", sum);

    int* pvar;
    int var;
    var = 5;
    pvar = &var;

    printf("%d, %d", var, pvar);
}