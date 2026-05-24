#pragma once

struct Sprite {
    double x, y;
    int texture;
    int hp = 100;
    int state = 1;         // 1 = živý, 0 = mrtvý
    double damageTimer = 0.0;
    double spawnX = 0;
    double spawnY = 0;
    double deadTimer = 0.0;
};
