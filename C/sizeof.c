#define my_sizeof(type) (char *)(&type+1)-(char*)(&type)

main()
{
int *p;
    printf("%d", my_sizeof(p));
}
