#pragma once

struct Player {
    double x, y;           // Pozice
    double dirX, dirY;     // Směr pohledu
    double planeX, planeY; // Kamerová rovina (FOV)
    double z = 0.0;        // Výška (skákání)
    double vz = 0.0;       // Vertikální rychlost
    int hp = 100;          // Zdraví hráče
};