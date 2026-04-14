#pragma once

#include <vector>
#include <cstdint>
#include "Player.hpp"
#include "Map.hpp"

constexpr int TEX_WIDTH = 64;
constexpr int TEX_HEIGHT = 64;

class Raycaster {
public:
    Raycaster(); // Přidáme konstruktor pro generování textury
    void render(std::vector<uint32_t>& framebuffer, int screenWidth, int screenHeight, const Player& player);

private:
    std::vector<uint32_t> texture; // Zde bude uložena textura zdi
};