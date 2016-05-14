#include<stdio.h>

main()
{
    int id;
    id=fork();

    if(id>0)
    {
        printf("Parent will sleep");
        sleep(10);
        waitpid(id,NULL,0);
        printf("child status retrieved");
getchar();
        sleep(10);
    }
    if(id==0)
        printf("I am child");
}

