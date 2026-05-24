#pragma once

#include <SDL3/SDL.h>
#include <vector>
#include <cstdint>
#include <string>
#include "Player.hpp"
#include "Raycaster.hpp"

enum class GameState { MENU, PLAYING };

#define TEX_WIDTH 64
#define TEX_HEIGHT 64

// Pole pro 4 různé textury (0 necháme prázdnou, použijeme 1, 2, 3)
inline uint32_t textures[4][TEX_WIDTH * TEX_HEIGHT];
inline uint32_t floorTexture[TEX_WIDTH * TEX_HEIGHT];
inline uint32_t ceilTexture[TEX_WIDTH * TEX_HEIGHT];
inline uint32_t enemyTexture[TEX_WIDTH * TEX_HEIGHT];

#include "Sprite.hpp"

class Engine {
public:
    Engine(int width, int height);
    ~Engine(); // Destruktor se postará o úklid

    void run(); // Hlavní metoda, která spustí hru

private:
    GameState currentState = GameState::MENU;
    int menuSelection = 0;
    bool isFullscreen = false;

    void drawMenu(); // Nová metoda pro vykreslení menu
    void handleMenuInput(SDL_Event& event); // Oddělená logika vstupů pro menu
    
    Raycaster raycaster;
    void processInput(double deltaTime); // <--- Přidán parametr
    void render();

    // Nové metody pro kreslení 2D prvků
    void drawRect(int startX, int startY, int width, int height, uint32_t color);
    void drawText(const std::string& text, int x, int y, uint32_t color, int scale = 2);
    void drawMinimap();

    int screenWidth;
    int screenHeight;
    bool isRunning;
    uint64_t lastTime; // <--- Přidána proměnná pro čas

    // Proměnné pro zbraň
    bool isMoving;
    double weaponBobTime;
    bool isShooting = false;
    double shootTimer = 0.0;
    double playerDamageTimer = 0.0;

    SDL_Window* window;
    SDL_Renderer* renderer;
    SDL_Texture* frameTexture;
    
    std::vector<uint32_t> framebuffer;
    std::vector<double> zBuffer;
    std::vector<Sprite> sprites;
    Player player;
};