func(int num)
{
int rem=0;
    if(num<16)
    {
        printf("%d D",num);
        printf("%c\n ", num <10? num:('A'+num-10));
                return;

    }
    func(num/16);
    rem=num%16;
        printf("%d D",num);
        printf("%c \n", rem <10? rem:('A'+num-10));

}

main()
{
    int num=266;
    int rem=0;
    
   while(num>=16)
   {
      rem=num%16; 
      num/=16;
      printf("%c ",rem <10?rem+'0':('A'+rem-10));
   } 
      printf(" %c ",num <10?num+'0':('A'+num-10));

}
