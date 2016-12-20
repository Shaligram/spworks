
void s(int b)
{
    int *p;
    printf("%x", &p);
}
void f(int a)
{
    int v=8;
    s(5);
}
int main()
{
    f(5);

    return 0;
}
