int sum(int a, int b)
{
    return a + b;
}

int mul(int a, int b)
{
    return a * b;
}

int sub(int a, int b)
{
    return a - b;
}

float div(int a, int b)
{
    return (1.0 * a) / b;
}

int mod(int a, int b)
{
    return a % b;
}

int fib(int n)
{
    int a = 0;
    int b = 1;

    for (int i = 0; i < n; i++)
    {
        int t = a;
        a = a + b;
        b = t;
    }

    return a;
}