#include <iostream>
#include <string>

int main() {
    std::string username, password;
    std::cout << "Username: ";
    std::cin >> username;
    std::cout << "Password: ";
    std::cin >> password;

    if (username == "admin" && password == "Cr@ckM3") {
        std::cout << "Welcome, " << username << "!\n";
    } else {
        std::cout << "Invalid credentials.\n";
    }
    return 0;
}
