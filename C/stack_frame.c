#include <stdio.h>
 
int MyFunc(int parameter1, char parameter2)
{
    int local1 = 9;
    char local2 = 'Z';
    return 5;
}
 
int main(int argc, char *argv[])
{
    int a = MyFunc(7, '8');
    return 0;
}
