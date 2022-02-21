#include <iostream>

int main()
{
    long sum = 0;
    long n;
    while (std::cin >> n) {
        sum += n;
    }
    std::cout << sum << std::endl;
}
