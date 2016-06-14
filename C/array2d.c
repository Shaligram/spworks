func(int ***x)
{
    int **y;
y=(int*)malloc(5);
y[0]=malloc(5);
y[0][0]=0xf;
*x=y;
}
main()
{
int **x;
func(&x);
printf("%x",x[0][0]);
}

