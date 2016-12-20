#include <setjmp.h>

main()
{
    jmp_buf env;
    int i;

    i = setjmp(env);
    printf("IIII = %d\n", i);
    i = setjmp(env);
    printf("new III = %d\n", i);
    longjmp(env, 4);

    if (i != 0) exit(0);

    longjmp(env, 2);
    printf("Does this line get printed?\n");

}
