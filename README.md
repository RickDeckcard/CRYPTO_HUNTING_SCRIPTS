# CRYPTO_HUNTING_SCRIPTS
Scripts para recuperar wallets, semilas, passphrases, etc.

# LO QUE HACE CADA SCRIPT

find_the_12_word_in_seed.py 
----------------------------
sirve para recuperar una semilla de 12 palabras si conocemos 11 de ellas y la 12 no la sabemos pero sabemos la posición exacta de la misma. También corrige errores de escritura en todas las 11 palabras. Por último chequea si hay saldo en cada semilla ya que no sabemos la dirección pública y es la única manera de descubrir cual es la semilla correcta de nuestra wallet (Si el saldo es 0 no podremos determinar cual es la semilla correcta).
Tutorial en YouTube: https://www.youtube.com/watch?v=TlCVEPMo7lY
