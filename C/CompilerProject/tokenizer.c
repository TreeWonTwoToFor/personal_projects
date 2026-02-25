#include <stdio.h>
#include <stdlib.h>

int tokenizer(int line_count, char** src_lines) {
    for (int i = 0; i < line_count; i++) {
        printf("%s\n", src_lines[i]);
    }
    return 0;
}
