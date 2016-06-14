#include <stdio.h>
    struct a{
        int a;
        int b;
        int c[2];
    };
    

void fun(struct a B)
{
    B.c[0]=6;
}
main()
{

    struct a var,var2;
  

    var.a=2;
    var.b=5;
    var.c[0]=5;

    printf("%d %d  %d\n", var.a,var.b,var.c[0] );
    fun(var);

    printf("%d %d  %d", var.a,var.b,var.c[0] );

}

