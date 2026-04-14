#include "Engine.hpp"
#include <iostream>
#include <cmath>   // Pro sin() a cos()
#include "Map.hpp" // Potřebujeme vidět mapu kvůli kolizím
#include "Weapon.hpp"
#include "Font.hpp"

Engine::Engine(int width, int height)
    : screenWidth(width), screenHeight(height), isRunning(false),
      window(nullptr), renderer(nullptr), frameTexture(nullptr),
      framebuffer(width * height, 0)
{
    player = {2.0, 2.0, -1.0, 0.0, 0.0, 0.66};

    if (!SDL_Init(SDL_INIT_VIDEO))
    {
        std::cerr << "Chyba inicializace SDL3: " << SDL_GetError() << "\n";
        return;
    }

    window = SDL_CreateWindow("2.5D Retro Engine", screenWidth, screenHeight, 0);
    renderer = SDL_CreateRenderer(window, nullptr);
    frameTexture = SDL_CreateTexture(
        renderer, SDL_PIXELFORMAT_XRGB8888, SDL_TEXTUREACCESS_STREAMING,
        screenWidth, screenHeight);

    // ZAMKNUTÍ MYŠI DO OKNA (Skryje kurzor a snímá jen pohyb)
    SDL_SetWindowRelativeMouseMode(window, true);

    if (window && renderer && frameTexture)
    {
        isRunning = true;
    }
}

Engine::~Engine()
{
    if (frameTexture)
        SDL_DestroyTexture(frameTexture);
    if (renderer)
        SDL_DestroyRenderer(renderer);
    if (window)
        SDL_DestroyWindow(window);
    SDL_Quit();
}

void Engine::processInput(double deltaTime) {
    SDL_Event event;
    
    // ==========================================
    // 1. ZPRACOVÁNÍ JEDNORÁZOVÝCH UDÁLOSTÍ
    // ==========================================
    while (SDL_PollEvent(&event)) {
        // Křížek okna
        if (event.type == SDL_EVENT_QUIT) isRunning = false;
        
        // --- STISK KLÁVES ---
        if (event.type == SDL_EVENT_KEY_DOWN) {
            
            // ESCAPE - PŘEPÍNÁNÍ MENU A HRY
            if (event.key.key == SDLK_ESCAPE) {
                currentState = (currentState == GameState::PLAYING) ? GameState::MENU : GameState::PLAYING;
                
                // Zamknutí myši pro rotaci (když hrajeme) nebo uvolnění kurzoru (když jsme v menu)
                SDL_SetWindowRelativeMouseMode(window, currentState == GameState::PLAYING);
            }
            
            // OVLÁDÁNÍ MENU POMOCÍ KLÁVESNICE
            if (currentState == GameState::MENU) {
                if (event.key.key == SDLK_W || event.key.key == SDLK_UP) menuSelection--;
                if (event.key.key == SDLK_S || event.key.key == SDLK_DOWN) menuSelection++;
                
                // Rotace výběru (0 = Hrát, 1 = Fullscreen, 2 = Konec)
                if (menuSelection < 0) menuSelection = 2;
                if (menuSelection > 2) menuSelection = 0;

                // Potvrzení klávesou ENTER
                if (event.key.key == SDLK_RETURN) {
                    if (menuSelection == 0) { 
                        currentState = GameState::PLAYING;
                        SDL_SetWindowRelativeMouseMode(window, true);
                    }
                    else if (menuSelection == 1) { 
                        isFullscreen = !isFullscreen;
                        SDL_SetWindowFullscreen(window, isFullscreen);
                    }
                    else if (menuSelection == 2) {
                        isRunning = false; 
                    }
                }
            }
        }

        // --- OVLÁDÁNÍ MYŠÍ V MENU ---
        if (currentState == GameState::MENU) {
            // Rozměry tlačítek (musí odpovídat těm v metodě drawMenu)
            int btnW = 200; 
            int btnH = 40; 
            int spacing = 50;
            int startX = screenWidth / 2 - btnW / 2;
            int startY = screenHeight / 2 - 60;

            // Highlight (přejetí myší)
            if (event.type == SDL_EVENT_MOUSE_MOTION) {
                int mx = event.motion.x;
                int my = event.motion.y;

                for (int i = 0; i < 3; i++) {
                    int boxY = startY + (i * spacing);
                    if (mx >= startX && mx <= startX + btnW && my >= boxY && my <= boxY + btnH) {
                        menuSelection = i; 
                    }
                }
            }

            // Kliknutí (potvrzení)
            if (event.type == SDL_EVENT_MOUSE_BUTTON_DOWN && event.button.button == SDL_BUTTON_LEFT) {
                int mx = event.button.x;
                int my = event.button.y;

                for (int i = 0; i < 3; i++) {
                    int boxY = startY + (i * spacing);
                    if (mx >= startX && mx <= startX + btnW && my >= boxY && my <= boxY + btnH) {
                        if (i == 0) { 
                            currentState = GameState::PLAYING;
                            SDL_SetWindowRelativeMouseMode(window, true);
                        }
                        else if (i == 1) { 
                            isFullscreen = !isFullscreen;
                            SDL_SetWindowFullscreen(window, isFullscreen);
                        }
                        else if (i == 2) {
                            isRunning = false; 
                        }
                    }
                }
            }
        }

        // --- OVLÁDÁNÍ MYŠÍ VE HŘE (Rotace kamery) ---
        if (currentState == GameState::PLAYING && event.type == SDL_EVENT_MOUSE_MOTION) {
            // motion.xrel je hodnota o kolik se myš pohla do strany
            double rotSpeed = event.motion.xrel * -0.2 * deltaTime;
            
            // Rotační matice pro směr pohledu a rovinu kamery
            double oldDirX = player.dirX;
            player.dirX = player.dirX * std::cos(rotSpeed) - player.dirY * std::sin(rotSpeed);
            player.dirY = oldDirX * std::sin(rotSpeed) + player.dirY * std::cos(rotSpeed);
            
            double oldPlaneX = player.planeX;
            player.planeX = player.planeX * std::cos(rotSpeed) - player.planeY * std::sin(rotSpeed);
            player.planeY = oldPlaneX * std::sin(rotSpeed) + player.planeY * std::cos(rotSpeed);
        }
    }

    // ==========================================
    // 2. PLYNULÝ POHYB HRÁČE (Pouze během hraní)
    // ==========================================
    if (currentState == GameState::PLAYING) {
        const bool* keystate = SDL_GetKeyboardState(nullptr);
        double moveSpeed = 5.0 * deltaTime; // 5 bloků za sekundu
        
        isMoving = false; // Reset detekce pohybu pro zbraň

        // Krok vpřed (W)
        if (keystate[SDL_SCANCODE_W]) {
            isMoving = true;
            if (worldMap[int(player.x + player.dirX * moveSpeed)][int(player.y)] == 0) player.x += player.dirX * moveSpeed;
            if (worldMap[int(player.x)][int(player.y + player.dirY * moveSpeed)] == 0) player.y += player.dirY * moveSpeed;
        }
        // Krok vzad (S)
        if (keystate[SDL_SCANCODE_S]) {
            isMoving = true;
            if (worldMap[int(player.x - player.dirX * moveSpeed)][int(player.y)] == 0) player.x -= player.dirX * moveSpeed;
            if (worldMap[int(player.x)][int(player.y - player.dirY * moveSpeed)] == 0) player.y -= player.dirY * moveSpeed;
        }
        // Úkrok doleva (A)
        if (keystate[SDL_SCANCODE_A]) {
            isMoving = true;
            if (worldMap[int(player.x - player.planeX * moveSpeed)][int(player.y)] == 0) player.x -= player.planeX * moveSpeed;
            if (worldMap[int(player.x)][int(player.y - player.planeY * moveSpeed)] == 0) player.y -= player.planeY * moveSpeed;
        }
        // Úkrok doprava (D)
        if (keystate[SDL_SCANCODE_D]) {
            isMoving = true;
            if (worldMap[int(player.x + player.planeX * moveSpeed)][int(player.y)] == 0) player.x += player.planeX * moveSpeed;
            if (worldMap[int(player.x)][int(player.y + player.planeY * moveSpeed)] == 0) player.y += player.planeY * moveSpeed;
        }

        // --- AKTUALIZACE HOUPÁNÍ ZBRANĚ ---
        if (isMoving) {
            weaponBobTime += deltaTime;
        } else {
            weaponBobTime = 0; // Plynulý návrat do klidu
        }
    }
}

void Engine::drawRect(int startX, int startY, int width, int height, uint32_t color) {
    for (int y = startY; y < startY + height; y++) {
        for (int x = startX; x < startX + width; x++) {
            // Kontrola hranic obrazovky
            if (x >= 0 && x < screenWidth && y >= 0 && y < screenHeight) {
                framebuffer[y * screenWidth + x] = color;
            }
        }
    }
}

void Engine::drawText(const std::string& text, int x, int y, uint32_t color, int scale) {
    int cursorX = x;

    for (char c : text) {
        // Kontrola, jestli znak vůbec máme ve fontu (od 32 do 127)
        if (c >= 32 && c <= 126) {
            int charIndex = c - 32;

            // Projdeme mřížku 8x8 pixelů pro dané písmeno
            for (int row = 0; row < 8; row++) {
                uint8_t rowData = font8x8[charIndex][row];
                
                for (int col = 0; col < 8; col++) {
                    // Pomocí bitových operací (masky) zjistíme, jestli je daný pixel zapnutý
                    if (rowData & (1 << (7 - col))) {
                        // Kreslíme čtvereček o velikosti "scale"
                        drawRect(cursorX + col * scale, y + row * scale, scale, scale, color);
                    }
                }
            }
        }
        // Posuneme kurzor pro další písmeno (8 pixelů + 2 pixely mezera) * scale
        cursorX += (8 + 2) * scale; 
    }
}

void Engine::drawMinimap() {
    int blockSize = 8;      // Velikost jednoho bloku mapy v pixelech
    int mapOffsetX = 10;    // Odsazení od levého okraje obrazovky
    int mapOffsetY = 10;    // Odsazení od horního okraje

    // 1. Vykreslení bloků mapy
    for (int y = 0; y < MAP_HEIGHT; y++) {
        for (int x = 0; x < MAP_WIDTH; x++) {
            // Prázdný prostor = tmavě šedá, Zeď = světle šedá
            uint32_t color = (worldMap[x][y] > 0) ? 0xFF888888 : 0xFF222222;
            
            // Kreslíme (blockSize - 1) nám vytvoří krásnou 1px mřížku mezi bloky
            drawRect(mapOffsetX + x * blockSize, mapOffsetY + y * blockSize, blockSize - 1, blockSize - 1, color);
        }
    }

    // 2. Vykreslení hráče
    int playerSize = 4;
    // Přepočet z herních souřadnic na pixely na obrazovce
    int playerPixelX = mapOffsetX + (int)(player.x * blockSize);
    int playerPixelY = mapOffsetY + (int)(player.y * blockSize);
    
    // Hráč bude zářivě zelený obdélníček
    drawRect(playerPixelX - playerSize / 2, playerPixelY - playerSize / 2, playerSize, playerSize, 0xFF00FF00);

    // 3. Směrový ukazatel (kam se hráč dívá)
    int dirDotX = playerPixelX + (int)(player.dirX * blockSize);
    int dirDotY = playerPixelY + (int)(player.dirY * blockSize);
    drawRect(dirDotX - 1, dirDotY - 1, 3, 3, 0xFFFF0000); // Červená tečka pro směr pohledu
}

void Engine::drawMenu() {
    // 1. Ztmavíme celou obrazovku
    for (uint32_t& pixel : framebuffer) {
        pixel = (pixel >> 1) & 0x7F7F7F7F; 
    }

    // Nápis MENU nahoře
    drawText("MAIN MENU", screenWidth / 2 - 90, screenHeight / 2 - 120, 0xFFFFFFFF, 4);

    // 2. Definice rozměrů pro tlačítka
    int btnW = 240; // Trochu rozšíříme kvůli textu
    int btnH = 40;
    int spacing = 50;
    int startX = screenWidth / 2 - btnW / 2;
    int startY = screenHeight / 2 - 40; 

    // Názvy našich tlačítek
    std::string buttonTexts[3] = {"PLAY GAME", "FULLSCREEN", "QUIT"};

    // 3. Vykreslení 3 tlačítek
    for (int i = 0; i < 3; i++) {
        // Pokud je tlačítko vybrané, uděláme ho světlejší
        uint32_t color = (menuSelection == i) ? 0xFF666666 : 0xFF333333;
        
        // Vykreslení těla tlačítka
        drawRect(startX, startY + (i * spacing), btnW, btnH, color);

        // Vykreslení textu na tlačítku
        // (Vypočítáme si drobný posun, aby byl text zhruba vycentrovaný)
        uint32_t textColor = (menuSelection == i) ? 0xFFFFFF00 : 0xFFDDDDDD; // Žlutý text při najetí
        drawText(buttonTexts[i], startX + 20, startY + (i * spacing) + 12, textColor, 2);
    }
}

void Engine::render() {
    // =========================================================
    // 1. ZÁKLADNÍ VRSTVA: Vykreslení 3D světa
    // =========================================================
    // Vykreslujeme vždy, i když jsme v menu, aby hra zůstala "zamrzlá" na pozadí
    raycaster.render(framebuffer, screenWidth, screenHeight, player);

    // =========================================================
    // 2. UI VRSTVA: Rozhodnutí podle stavu hry
    // =========================================================
    if (currentState == GameState::PLAYING) {
        
        // --- A. MINIMAPA ---
        drawMinimap(); 

        // --- B. VYKRESLENÍ ZBRANĚ Z POHLEDU PRVNÍ OSOBY ---
        int scale = screenWidth / 40; // Dynamické zvětšení zbraně podle rozlišení okna
        if (scale < 1) scale = 1;

        // Výpočet houpání (Weapon Bobbing) - pokud se hýbeme, použijeme sinusovou vlnu
        int bobOffset = isMoving ? (int)(std::abs(std::sin(weaponBobTime * 8.0)) * 20.0) : 0;

        // Pozice zbraně (dole uprostřed)
        int startX = (screenWidth / 2) - ((WEAPON_WIDTH * scale) / 2);
        int startY = screenHeight - (WEAPON_HEIGHT * scale) + bobOffset + 10; 

        // Procházení 16x16 mřížky našeho pixel artu a zvětšení na obrazovku
        for (int y = 0; y < WEAPON_HEIGHT; y++) {
            for (int x = 0; x < WEAPON_WIDTH; x++) {
                uint32_t color = weaponSprite[y][x];
                
                if (color != _) { // '_' znamená průhlednou barvu
                    for (int sy = 0; sy < scale; sy++) {
                        for (int sx = 0; sx < scale; sx++) {
                            int drawX = startX + x * scale + sx;
                            int drawY = startY + y * scale + sy;
                            
                            // Bezpečnostní kontrola, abychom nepřetáhli mimo okno
                            if (drawX >= 0 && drawX < screenWidth && drawY >= 0 && drawY < screenHeight) {
                                framebuffer[drawY * screenWidth + drawX] = color;
                            }
                        }
                    }
                }
            }
        }
    } 
    else if (currentState == GameState::MENU) {
        
        // --- C. HERNÍ MENU ---
        // Vykreslí poloprůhledné pozadí a 3 velká tlačítka přes hru
        drawMenu();
    }

    // =========================================================
    // 3. HARDWAROVÁ AKCELERACE: Odeslání na obrazovku
    // =========================================================
    // Překopírování našeho pole z RAM na Grafickou kartu (GPU)
    SDL_UpdateTexture(frameTexture, nullptr, framebuffer.data(), screenWidth * sizeof(uint32_t));
    
    // Vyčištění starého snímku a vykreslení nového
    SDL_RenderClear(renderer);
    SDL_RenderTexture(renderer, frameTexture, nullptr, nullptr);
    SDL_RenderPresent(renderer);
}

void Engine::run()
{
    lastTime = SDL_GetTicks(); // Zaznamenáme čas před startem

    while (isRunning)
    {
        // Výpočet Delta Time v sekundách
        uint64_t currentTime = SDL_GetTicks();
        double deltaTime = (currentTime - lastTime) / 1000.0;
        lastTime = currentTime;

        // Ochrana proti příliš velkým skokům (např. při lagování okna)
        if (deltaTime > 0.1)
            deltaTime = 0.1;

        processInput(deltaTime); // Předáme čas do vstupů
        render();
    }
}