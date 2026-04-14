#pragma once

struct Player {
    double x, y;           // Pozice
    double dirX, dirY;     // Směr pohledu
    double planeX, planeY; // Kamerová rovina (FOV)
};