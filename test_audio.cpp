#include <iostream>
#include <filesystem>
#include "stb_vorbis.c"

int main() {
    int c, r;
    short* dec = nullptr;
    int smp = stb_vorbis_decode_filename("assets/SOUNDS/AGURPAIN.ogg", &c, &r, &dec);
    std::cout << "AGURPAIN.ogg: " << smp << " samples, " << c << " channels, " << r << " Hz" << std::endl;
    return 0;
}
