#include "Raycaster.hpp"
#include <cmath>
#include <thread>
#include <algorithm>
#include "Engine.hpp"

void Raycaster::render(std::vector<uint32_t>& framebuffer, int screenWidth, int screenHeight, const Player& player, const uint32_t textures[4][TEX_WIDTH * TEX_HEIGHT], std::vector<double>& zBuffer) {
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

            zBuffer[x] = perpWallDist;

            // FLOOR AND CEILING CASTING
            double floorXWall, floorYWall;
            if (side == 0 && rayDirX > 0) {
                floorXWall = mapX;
                floorYWall = mapY + wallX;
            } else if (side == 0 && rayDirX < 0) {
                floorXWall = mapX + 1.0;
                floorYWall = mapY + wallX;
            } else if (side == 1 && rayDirY > 0) {
                floorXWall = mapX + wallX;
                floorYWall = mapY;
            } else {
                floorXWall = mapX + wallX;
                floorYWall = mapY + 1.0;
            }

            double distWall = perpWallDist;

            // --- KRESLENÍ SLOUPCE ---
            for (int y = 0; y < screenHeight; y++) {
                int pixelIndex = y * screenWidth + x;
                
                if (y < drawStart) {
                    // Strop
                    double currentDist = screenHeight / (2.0 * (screenHeight - y) - screenHeight);
                    double weight = currentDist / distWall;
                    double currentFloorX = weight * floorXWall + (1.0 - weight) * player.x;
                    double currentFloorY = weight * floorYWall + (1.0 - weight) * player.y;

                    int floorTexX = int(currentFloorX * TEX_WIDTH) % TEX_WIDTH;
                    int floorTexY = int(currentFloorY * TEX_HEIGHT) % TEX_HEIGHT;
                    if (floorTexX < 0) floorTexX += TEX_WIDTH;
                    if (floorTexY < 0) floorTexY += TEX_HEIGHT;

                    framebuffer[pixelIndex] = ceilTexture[TEX_HEIGHT * floorTexY + floorTexX];
                } else if (y >= drawStart && y <= drawEnd) {
                    // ZED
                    int texY = (int)texPos & (TEX_HEIGHT - 1);
                    texPos += step;
                    
                    int texNum = worldMap[mapX][mapY];
                    if (texNum < 1 || texNum > 3) texNum = 1;
                    uint32_t color = textures[texNum][TEX_HEIGHT * texY + texX];
                    
                    if (side == 1) color = (color >> 1) & 8355711;
                    
                    framebuffer[pixelIndex] = color;
                } else {
                    // Podlaha
                    double currentDist = screenHeight / (2.0 * y - screenHeight);
                    double weight = currentDist / distWall;
                    double currentFloorX = weight * floorXWall + (1.0 - weight) * player.x;
                    double currentFloorY = weight * floorYWall + (1.0 - weight) * player.y;

                    int floorTexX = int(currentFloorX * TEX_WIDTH) % TEX_WIDTH;
                    int floorTexY = int(currentFloorY * TEX_HEIGHT) % TEX_HEIGHT;
                    if (floorTexX < 0) floorTexX += TEX_WIDTH;
                    if (floorTexY < 0) floorTexY += TEX_HEIGHT;

                    framebuffer[pixelIndex] = floorTexture[TEX_HEIGHT * floorTexY + floorTexX];
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

void Raycaster::renderSprites(std::vector<uint32_t>& framebuffer, int screenWidth, int screenHeight, const Player& player, std::vector<Sprite>& sprites, const std::vector<double>& zBuffer) {
    // Vypočteme vzdálenosti spritů od hráče pro účely třídění
    std::vector<std::pair<double, int>> spriteOrder(sprites.size());
    for(size_t i = 0; i < sprites.size(); i++) {
        spriteOrder[i].first = ((player.x - sprites[i].x) * (player.x - sprites[i].x) + (player.y - sprites[i].y) * (player.y - sprites[i].y));
        spriteOrder[i].second = i;
    }
    // Setřídíme od nejvzdálenějšího po nejbližší
    std::sort(spriteOrder.rbegin(), spriteOrder.rend());

    for(size_t i = 0; i < sprites.size(); i++) {
        int spriteIdx = spriteOrder[i].second;
        double spriteX = sprites[spriteIdx].x - player.x;
        double spriteY = sprites[spriteIdx].y - player.y;

        // Transformace pomocí inverzní matice kamery
        double invDet = 1.0 / (player.planeX * player.dirY - player.dirX * player.planeY);
        double transformX = invDet * (player.dirY * spriteX - player.dirX * spriteY);
        double transformY = invDet * (-player.planeY * spriteX + player.planeX * spriteY);

        if (transformY <= 0) continue; // Je za kamerou

        int spriteScreenX = int((screenWidth / 2) * (1 + transformX / transformY));
        
        int spriteHeight = std::abs(int(screenHeight / transformY));
        int drawStartY = -spriteHeight / 2 + screenHeight / 2;
        if(drawStartY < 0) drawStartY = 0;
        int drawEndY = spriteHeight / 2 + screenHeight / 2;
        if(drawEndY >= screenHeight) drawEndY = screenHeight - 1;

        int spriteWidth = std::abs(int(screenHeight / transformY));
        int drawStartX = -spriteWidth / 2 + spriteScreenX;
        if(drawStartX < 0) drawStartX = 0;
        int drawEndX = spriteWidth / 2 + spriteScreenX;
        if(drawEndX >= screenWidth) drawEndX = screenWidth - 1;

        for(int stripe = drawStartX; stripe < drawEndX; stripe++) {
            int texX = int(256 * (stripe - (-spriteWidth / 2 + spriteScreenX)) * TEX_WIDTH / spriteWidth) / 256;
            // Podmínka pro vykreslení:
            // 1) je to uvnitř obrazovky, 2) Z-Buffer check, 3) sprite není za námi
            if(transformY > 0 && stripe > 0 && stripe < screenWidth && transformY < zBuffer[stripe]) {
                for(int y = drawStartY; y < drawEndY; y++) {
                    int d = y * 256 - screenHeight * 128 + spriteHeight * 128; // 256 and 128 factors to avoid floats
                    int texY = ((d * TEX_HEIGHT) / spriteHeight) / 256;
                    uint32_t color = enemyTexture[TEX_HEIGHT * texY + texX];
                    if((color & 0x00FFFFFF) != 0) { // Pokud není černá (průhledná)
                        framebuffer[y * screenWidth + stripe] = color;
                    }
                }
            }
        }
    }
}