#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    long sum = 0;
    while (1) {
        long num;
        int retval = scanf("%ld", &num);
        if (retval == EOF)
            break;
        if (retval != 1 || errno != 0)
            return EXIT_FAILURE;
        sum += num;
    }
    printf("%ld\n", sum);
    return EXIT_SUCCESS;
}
