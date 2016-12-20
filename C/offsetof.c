#include <stdio.h>
 
#define OFFSETOF(TYPE, ELEMENT) ((size_t)&(((TYPE *)0)->ELEMENT))
 
typedef struct PodTag
{
       int     i;
          double  d;
             char    c;
} PodType;
 
int main()
{
    double x;
       printf("%p %d",&(((PodType *)0)->d), OFFSETOF(PodType, d) );
           
          getchar();
             return 0;
}
