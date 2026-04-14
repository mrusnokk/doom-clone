#include "Raycaster.hpp"
#include <cmath>
#include <thread>

Raycaster::Raycaster() {
    // Vygenerování procedurální retro textury (64x64)
    texture.resize(TEX_WIDTH * TEX_HEIGHT);
    for (int x = 0; x < TEX_WIDTH; x++) {
        for (int y = 0; y < TEX_HEIGHT; y++) {
            // Retro XOR vzor (generuje pěknou mozaiku)
            int xorcolor = (x * 256 / TEX_WIDTH) ^ (y * 256 / TEX_HEIGHT);
            texture[TEX_WIDTH * y + x] = xorcolor * 256; // Modrozelený nádech
        }
    }
}

void Raycaster::render(std::vector<uint32_t>& framebuffer, int screenWidth, int screenHeight, const Player& player) {
    // Zjistíme, kolik vláken náš procesor podporuje (např. 8, 12, 16)
    unsigned int numThreads = std::thread::hardware_concurrency();
    if (numThreads == 0) numThreads = 4; // Pojistka

    std::vector<std::jthread> threads;
    int chunk = screenWidth / numThreads;

    // Vytvoříme Lambda funkci pro vykreslení jen ČÁSTI obrazovky
    auto renderChunk = [&](int startX, int endX) {
        for (int x = startX; x < endX; x++) {
            double cameraX = 2 * x / (double)screenWidth - 1.0;
            double rayDirX = player.dirX + player.planeX * cameraX;
            double rayDirY = player.dirY + player.planeY * cameraX;

            int mapX = int(player.x);
            int mapY = int(player.y);

            double sideDistX, sideDistY;
            double deltaDistX = (rayDirX == 0) ? 1e30 : std::abs(1.0 / rayDirX);
            double deltaDistY = (rayDirY == 0) ? 1e30 : std::abs(1.0 / rayDirY);
            double perpWallDist;

            int stepX, stepY;
            int hit = 0;
            int side;

            if (rayDirX < 0) {
                stepX = -1;
                sideDistX = (player.x - mapX) * deltaDistX;
            } else {
                stepX = 1;
                sideDistX = (mapX + 1.0 - player.x) * deltaDistX;
            }
            if (rayDirY < 0) {
                stepY = -1;
                sideDistY = (player.y - mapY) * deltaDistY;
            } else {
                stepY = 1;
                sideDistY = (mapY + 1.0 - player.y) * deltaDistY;
            }

            while (hit == 0) {
                if (sideDistX < sideDistY) {
                    sideDistX += deltaDistX;
                    mapX += stepX;
                    side = 0;
                } else {
                    sideDistY += deltaDistY;
                    mapY += stepY;
                    side = 1;
                }
                if (mapX >= 0 && mapX < MAP_WIDTH && mapY >= 0 && mapY < MAP_HEIGHT) {
                    if (worldMap[mapX][mapY] > 0) hit = 1;
                } else {
                    hit = 1;
                }
            }

            if (side == 0) perpWallDist = (mapX - player.x + (1 - stepX) / 2.0) / rayDirX;
            else           perpWallDist = (mapY - player.y + (1 - stepY) / 2.0) / rayDirY;

            if (perpWallDist <= 0) perpWallDist = 0.1;
            int lineHeight = (int)(screenHeight / perpWallDist);

            int drawStart = -lineHeight / 2 + screenHeight / 2;
            if (drawStart < 0) drawStart = 0;
            int drawEnd = lineHeight / 2 + screenHeight / 2;
            if (drawEnd >= screenHeight) drawEnd = screenHeight - 1;

            // --- VÝPOČET TEXTURY ---
            double wallX; // Kde přesně paprsek zasáhl zeď (potřebujeme zlomkovou část)
            if (side == 0) wallX = player.y + perpWallDist * rayDirY;
            else           wallX = player.x + perpWallDist * rayDirX;
            wallX -= std::floor(wallX); // Ořízneme celočíselnou část (necháme jen např. 0.35)

            // X souřadnice na textuře
            int texX = int(wallX * double(TEX_WIDTH));
            // Otočení textury na určitých stěnách, aby nebyla zrcadlově obrácená
            if (side == 0 && rayDirX > 0) texX = TEX_WIDTH - texX - 1;
            if (side == 1 && rayDirY < 0) texX = TEX_WIDTH - texX - 1;

            // Kolik posunout texturu vertikálně na každý pixel obrazovky
            double step = 1.0 * TEX_HEIGHT / lineHeight;
            double texPos = (drawStart - screenHeight / 2 + lineHeight / 2) * step;

            // --- KRESLENÍ SLOUPCE ---
            for (int y = 0; y < screenHeight; y++) {
                int pixelIndex = y * screenWidth + x;
                
                if (y < drawStart) {
                    framebuffer[pixelIndex] = 0x222222; // Strop
                } else if (y >= drawStart && y <= drawEnd) {
                    // Y souřadnice na textuře (maskování pomocí & zrychluje výpočet proti modulu %)
                    int texY = (int)texPos & (TEX_HEIGHT - 1);
                    texPos += step;
                    
                    uint32_t color = texture[TEX_HEIGHT * texY + texX];
                    
                    // Ztmavení y-stěn (stínování)
                    if (side == 1) color = (color >> 1) & 8355711; // Rychlý bitový shift pro ztmavení
                    
                    framebuffer[pixelIndex] = color;
                } else {
                    framebuffer[pixelIndex] = 0x444444; // Podlaha
                }
            }
        }
    };

    // Rozdáme práci vláknům (Multithreading)
    for (unsigned int i = 0; i < numThreads; ++i) {
        int start = i * chunk;
        int end = (i == numThreads - 1) ? screenWidth : start + chunk; // Poslední vlákno dojede do konce
        
        // emplace_back automaticky spustí std::jthread
        threads.emplace_back(renderChunk, start, end);
    }
    
    // Zde nemusíme volat threads.join(), protože std::jthread 
    // se na konci své platnosti (zde na konci funkce render) bezpečně spojí sám!
}