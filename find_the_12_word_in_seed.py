import itertools
from mnemonic import Mnemonic
import requests
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import time
import os, sys


#### LIMPIEZA Y PRESENTACION ####

os.system('cls')
print("Find seed with 11 words and check funds.")
print("----------------------------------------\n")

##### VARIABLES Y LISTAS ######

# Tus 11 palabras de la semilla
semilla = ['random', 'rely', 'leisure', 'enrich', 'crawl', 'alter', 'gasp', 'film', 'gown', 'palabra_faltante', 'praise', 'salon']



#### FUNCIONES ####

def semillas_on_text(): # funcion principal de comprobacion y permutaciones validas de semillas
    # Instancia de Mnemonic para verificar las semillas
    m = Mnemonic("english")

    # Lista BIP39 en inglés
    bip39 = m.wordlist

    # Comprobar si todas las palabras de la semilla existen en la lista BIP39
    for palabra in semilla:
        if palabra not in bip39 and palabra != "palabra_faltante":
            print(f"No existe esta palabra en BIP39: {palabra}")
            sys.exit("\nPor favor corrige la palabra incorrecta y vuelve a lanzar el script.")
    # Contador para las semillas válidas
    contador = 0

    # Abrir el archivo de texto para escribir las semillas válidas
    with open('permutaciones.txt', 'w') as f:
        # Para cada palabra en la lista BIP39
        for palabra in bip39:
            # Reemplazar 'palabra10' con la palabra de la lista BIP39
            semilla[9] = palabra
            print("Probando semilla: ", semilla)

            # Comprobar si la semilla completa es válida
            semilla_permutada = ' '.join(semilla)
            if m.check(semilla_permutada):
                print('Semilla válida:', semilla_permutada)
                # Escribir la semilla válida en el archivo de texto
                f.write(semilla_permutada + '\n')
                print(contador)
                contador += 1

    print('\nNúmero total de semillas válidas encontradas:', contador)


def check_balance(coin_choice): # Chequea saldo en las semillas validas
    # Instancia de Mnemonic para verificar las semillas
    m = Mnemonic("english")

    # Leer el archivo de semillas
    with open('permutaciones.txt', 'r') as f:
        semillas = f.readlines()

    for semilla in semillas:
        semilla = semilla.strip()  # Eliminar el salto de línea
        if m.check(semilla):
            # Generar la semilla BIP39
            seed_bytes = Bip39SeedGenerator(semilla).Generate()

            # Crear una cartera BIP44
            if coin_choice == 1:
                bip_obj_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
                api_url = 'https://api.blockcypher.com/v1/btc/main/addrs/'
            elif coin_choice == 2:
                bip_obj_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
                api_url = 'https://api.blockcypher.com/v1/eth/main/addrs/'

            # Obtener la dirección de la cartera
            address = bip_obj_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()

            # Comprobar el saldo de la dirección
            response = requests.get(f'{api_url}{address}/balance')

            if response.status_code == 200:
                data = response.json()
                balance = data['balance']
                print(f'La semilla {semilla} tiene un saldo de {balance} en la dirección {address}.')
            else:
                print(f'Error al comprobar el saldo de la dirección {address}.')
        else:
            print(f'La semilla {semilla} no es válida.')
        time.sleep(15)

###### MAIN SOURCE ########
        
semillas_on_text()
coin_choice = int(input("\nIngrese 1 para Bitcoin o 2 para Ethereum: "))
check_balance(coin_choice)

print("Gracias por usar este script. Espero te haya ayudado a recuperar tus criptomonedas.")
print("\nScript creado por Deckcard23.")
print("X: @rickdeckard23")
print("Web: deckcard23.com")

