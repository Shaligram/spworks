#define my_sizeof(type) (char *)(&type+1)-(char*)(&type)
#define my_sizeof(x) ( {__typeof__(x) tmp ;(char*)(&tmp + 1) - (char*)(&tmp);})


static int i=1;
void *my_malloc(int size, const char *f, int line)
{
    static int i=2;
    void *p =malloc(size);
    printf("Insde my malloc %d %d %s %d\n", i, size, f,line);
    i=6;
    i=6;
    i=6;
    return p;
} 

void *my_malloc2(int size, const char *f, int line)
{
    static int i=3;
    void *p =malloc(size);
    printf("Insde my malloc %d %d %s %d\n", i, size, f,line);
    i=6;
    i=6;
    i=6;
    return p;
} 


#define malloc(X) my_malloc(X, __FILE__, __LINE__)



func(int a[])
{
    printf("Fincal %d", sizeof(a));
}

main()
{
int *p1,x;
int  arr[] = {1, 2, 3, 4, 5, 6};
    int size = *(&arr + 1) - arr;


double *p;
double y;
*(arr+1) = 7;
        printf("Number of elements in arr[] is %d \n",size);
        printf("%d\n%p  asdasd %d asd\n", *(&arr+1), *(arr+2), sizeof(arr));
    
        p1=malloc(4);
#define malloc(X) my_malloc2(X, __FILE__, __LINE__)
        p1=malloc(4);
       printf("%d",i); 
        
        printf("%d", my_sizeof(*p));
    printf("\nSIZEOF %d", my_sizeof(x));
    printf("\nSIZEOF %d\n", my_sizeof(int));
    func(arr);
}
