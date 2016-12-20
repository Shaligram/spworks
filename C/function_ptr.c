void hello_func()
{
printf("Hello function called");
}
main()
{

    void (*hello)() = hello_func;
    (*hello)();
}


