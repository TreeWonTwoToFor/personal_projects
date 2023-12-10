#include <stdio.h>
#include <string.h>

char group(tokens) 
{
    printf("group called: %d\n", tokens);
    return 0;
}

int main() 
{
    int tokens[50];
    char usr_input[30];
    fgets(usr_input, sizeof(usr_input), stdin);
    char *token = strtok(usr_input, " ");
    while (token != NULL) 
    {
        printf("strtok(): %s\n", token);
        token = strtok(NULL, " ");
    }
    group(tokens);
    return 0;
}