#include <time.h>
int i =0;
void function(void (*cbfn)())
{
        (*cbfn)();
}
void intime()
{
   printf(""); 

}
void timeout()
{
   printf("Inside timeout\n"); 
   system("date");
}
int main()
{
    time_t start,end;
    double dif;
    double duration=1; //duration of timer
    int loop=1;
    while(loop==1)
    {
        time(&start);
        if(dif==duration)
        {
            /*callback*/
           function(timeout); 
            dif=0;
        }
           function(intime); 
        /* do stuff*/
        time(&end);
        dif+=difftime(end,start);
    }
}
