#include <stdlib.h>
#include <string.h>
char *solution(int n)
{
        char *roman_number;
        while (n != 0)
        {
                if (n >= 1000)
                {
                        strcat(roman_number, "M");
                        n -= 1000;
                }

                if (n >= 900)
                {
                        n -= 900;
                        strcat(roman_number, "CM");
                }

                if (n >= 500)
                {
                        n -= 500;
                        strcat(roman_number, "D");
                }

                if (n >= 400)
                {
                        n -= 400;
                        strcat(roman_numbers, "CD");
                }

                if (n >= 100)
                {
                        n -= 100;
                        strcat(roman_numbers, "C");
                }
                if (n >= 90)
                {
                        n -= 90;
                        strcat(roman_numbers, "XC");
                        if (n >= 50)
                        {
                                n -= 50;
                                strcat(roman_numbers, "L");
                                if (n >= 40)
                                {
                                        n -= 40;
                                        strcat(roman_numbers, "XL");
                                }
                                if (n >= 10)
                                {
                                        n -= 10;
                                        strcat(roman_numbers, "X");
                                }
                                if (n >= 9)
                                {
                                        n -= 9;
                                        strcat(roman_numbers, "IX");
                                }
                                if (n >= 5)
                                {
                                        n -= 5;
                                        strcat(roman_numbers, "V");
                                }
                                if (n >= 4)
                                {
                                        n -= 4;
                                        strcat(roman_numbers, "IV");
                                }
                                if (n >= 1)
                                {
                                        n -= 1;
                                        strcat(roman_numbers, "I");
                                }
                        }
                }
        }
        // return a heap-allocated string:
        return *roman_numbers;
}