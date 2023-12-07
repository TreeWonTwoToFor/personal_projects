#include <stdio.h>
#include <stdlib.h>

int FizzBuzz(void)
{
	int i;
	for (i=1; i<=25; i++)
	{
		if ((i%15) == 0)
		{
			printf("FizzBuzz\n");
		}	
		else if ((i%3) == 0)
		{
			printf("Fizz\n");
		}
		else if ((i%5) == 0)
		{
			printf("Buzz\n");
		}
		else
		{
			printf("%d\n",i);
		}
	}
	return 0;
}


int main() 
{
	system("cls");
	FizzBuzz();
	return 0;
}
