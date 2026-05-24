#pragma once
#include <cstdint>

constexpr int WEAPON_WIDTH = 16;
constexpr int WEAPON_HEIGHT = 16;

// Definice barev (0x00000000 je magická hodnota, kterou budeme brát jako průhlednou)
constexpr uint32_t _ = 0x00000000; // Průhledná (nic se nekreslí)
constexpr uint32_t D = 0xFF222222; // Tmavý kov (hlaveň)
constexpr uint32_t M = 0xFF888888; // Světlý kov (tělo zbraně)
constexpr uint32_t S = 0xFFCCAA88; // Ruka (barva kůže)

// Naše 16x16 pixelová pistole z pohledu první osoby
const uint32_t weaponSprite[WEAPON_HEIGHT][WEAPON_WIDTH] = {
    {_,_,_,_,_,_,_,D,D,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,D,D,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,M,M,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,M,M,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,_,M,M,_,_,_,_,_,_,_},
    {_,_,_,_,_,_,M,M,M,M,_,_,_,_,_,_},
    {_,_,_,_,_,_,M,M,M,M,_,_,_,_,_,_},
    {_,_,_,_,_,_,D,M,M,D,_,_,_,_,_,_},
    {_,_,_,_,_,D,D,M,M,D,D,_,_,_,_,_},
    {_,_,_,_,_,D,D,M,M,D,D,_,_,_,_,_},
    {_,_,_,_,_,_,D,S,S,D,_,_,_,_,_,_},
    {_,_,_,_,_,_,S,S,S,S,_,_,_,_,_,_},
    {_,_,_,_,_,_,S,S,S,S,_,_,_,_,_,_},
    {_,_,_,_,_,_,S,D,D,S,_,_,_,_,_,_},
    {_,_,_,_,_,_,S,D,D,S,_,_,_,_,_,_},
    {_,_,_,_,_,_,S,D,D,S,_,_,_,_,_,_}
};