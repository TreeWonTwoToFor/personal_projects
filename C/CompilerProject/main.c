#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Token {
  char* type;
  int value;
};

struct Token* tokenize(char* src_text) {
	int token_list_size = 100;
	struct Token* token_list = malloc(token_list_size * sizeof(struct Token));

	char buffer[100] = {0};
	int buffer_index = 0;

	char c;
	int char_index = 0;
	int token_index = 0;
	while ((c = src_text[char_index]) != 0) {
		if (c == ';') {
			struct Token semi = {"SEMI", 0};
			token_list[token_index] = semi;
			token_index++;
		} else if ((c > 64 && c < 91) || (c > 96 && c < 123) || c == '-' || c == '_') {
			// a character is a letter (uppercase, or lowercase), or a - _
			buffer[buffer_index] = c;
			buffer_index++;
		} else if (c >= 48 && c <= 57) {
      struct Token int_lit = {"INT", c-48}; //48 is the value of 0
      // if we have a multi digit number, read all digits into INT value
      int running = 0;
      while (running == 0) {
        char_index++;
        char new_char = src_text[char_index];
        if (new_char >= 48 && new_char <= 57) {
          int_lit.value *= 10;
          int_lit.value += new_char-48;
        } else {
          char_index--;
          running = 1;
        }
      }
      token_list[token_index] = int_lit;
      token_index++;
		} else if (c == ' ' || c == '\n') {
      // we know we have a new word, so we should check to see if it's a keyword, variable, or other
      if (strcmp(buffer, "return") == 0) {
        struct Token _return = {"RETURN", 0};
        token_list[token_index] = _return;
        token_index++;
      }
			// we want to flush the buffer
			while (buffer_index >= 0) {
				buffer[buffer_index] = 0;
				buffer_index--;
			}
			buffer_index = 0;
    }
		char_index++;
	}
  // nice little termination
	struct Token end = {"END"};
	token_list[token_index] = end;
	return token_list;
}

void Lexer(struct Token token_array[], char* output_file_name) {
  FILE* source_file = fopen(output_file_name, "w");

  struct Token token_buffer[100];
  int buffer_index = 0;

  int token_index = 0;
  while (strcmp(token_array[token_index].type, "END") != 0) {
    struct Token current_token = token_array[token_index];
    // anything but a semi colon
    if (strcmp(current_token.type, "SEMI") != 0) {
      printf("%s\n", current_token.type);
      token_buffer[buffer_index] = current_token;
      buffer_index++;
    } else {
      // we need to 'flush' the buffer into a statement
      if (strcmp(token_buffer[0].type, "RETURN") == 0 &&
            strcmp(token_buffer[1].type, "INT") == 0) {
        fprintf(source_file, "PRINT %d", token_buffer[1].value);
      }
      buffer_index = 0;
    }
    token_index++;
  }
  fclose(source_file);
}

int main(int arg_c, char* arg_v[]) {
	if (arg_c > 2) {
		int n = 100;
		char* buffer = malloc(n);
		if (buffer == NULL) {
			printf("Buffer could not be allocated.\n");
			exit(1);
		}

		char* file_name = arg_v[1];
		FILE* source_file = fopen(file_name, "r");

		char c;
		int char_index = 0;
		while ((c = fgetc(source_file)) != EOF) {
			buffer[char_index] = c;
			char_index++;
			if (char_index == n) {
				n *= 2;
				char *new_buffer = realloc(buffer, n);
				if (new_buffer == NULL) {
					printf("Buffer could not be re-allocated.\n");
					exit(1);
				}
				buffer = new_buffer;
			}
		}
		printf("Pre-Processing:\n%s\n", buffer);

		printf("Post-Processing:\n");
		struct Token* tokens = tokenize(buffer);
    Lexer(tokens, arg_v[2]);
	} else {
		printf("Please enter a file to read.\n");
		exit(1);
	}

	return 0;
}
