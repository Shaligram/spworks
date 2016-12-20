#include <unistd.h>
#include <fcntl.h>
#include <string.h>

typedef void (*call_back) (int, int);

void test_call_back(int a, int b)
{
        printf("In call back function, a:%d \t b:%d \n", a, b);
}

void call_callback_func(call_back back)
{
        int a = 5;
            int b = 7;

                back(a, b);
}

int main(int argc, char *argv[])
{
        int ret = 0;

            call_back back;

                back = test_call_back;

                    call_callback_func(back);

                        return ret;
}
