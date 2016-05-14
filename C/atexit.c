#include<stdio.h>

void func(void)
{
        printf("\n Cleanup function called \n");
            return;
}

int main(void)
{
        int i = 0;

            atexit(func);

                for(;i<0xffffff;i++);

exit(0);
                _exit(0);
}
