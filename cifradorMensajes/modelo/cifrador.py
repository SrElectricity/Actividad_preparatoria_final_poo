from abc import ABC, abstractmethod

from cifradorMensajes.modelo.errores import ContieneNumero, ContieneNoAscii, SinLetras, NoTrim, DobleEspacio


class ReglaCifrado(ABC):

    def __init__(self, token: int):
        self.token:int = token

    @abstractmethod
    def encriptar(self, mensaje: str):
        pass

    @abstractmethod
    def desencriptar(self, mensaje: str):
        pass

    @abstractmethod
    def mensaje_valido(self, mensaje: str) -> bool:
        pass


    def encontrar_numeros_mensaje(self, mensaje: str) -> list:

        num = []

        for i, letra in enumerate (mensaje):
            if letra.isdigit():
                num.append(i)

        return num


    def encontrar_no_ascii_mensaje(self, mensaje: str) -> list:

        no_asci = []

        for i, letra in enumerate (mensaje):
            if ord(letra) > 127:
                no_asci.append(i)

        return no_asci


class ReglaCifradoTraslacion(ReglaCifrado):

    def mensaje_valido(self, mensaje: str) -> bool:

        error_messages = []

        # Verificar si el mensaje no contiene letras
        if not any(letra.isalpha() for letra in mensaje):
            error_messages.append("SinLetras")

        # Verificar si el mensaje contiene números
        if self.encontrar_numeros_mensaje(mensaje):
            error_messages.append("ContieneNumero")

        # Verificar si el mensaje contiene caracteres no ASCII
        if self.encontrar_no_ascii_mensaje(mensaje):
            error_messages.append("ContieneNoAscii")

        # Si hay errores acumulados, lanzamos una excepción con todos los mensajes concatenados
        if error_messages:
            raise Exception(" | ".join(error_messages))

            # Verifica si el mensaje es solo caracteres especiales
        caracteres_especiales = set("@#$%&")
        if all(letra in caracteres_especiales for letra in mensaje):
            raise ValueError("El mensaje no puede contener solo caracteres especiales.")
        return True

    def encriptar(self, mensaje: str):
        if not self.mensaje_valido(mensaje):
            raise ValueError

        mensaje_min = mensaje.lower()
        alfabeto = "abcdefghijklmnopqrstuvwxyz"
        resultado = ''

        for letra in mensaje_min:
            if letra in alfabeto:
                nuevo_indice = (alfabeto.index(letra) + self.token) % len(alfabeto)
                resultado += alfabeto[nuevo_indice]
            else:
                resultado += letra

        return resultado

    def desencriptar(self, mensaje: str) -> str:
        alfabeto = "abcdefghijklmnopqrstuvwxyz"
        resultado = ''

        for letra in mensaje:
            if letra in alfabeto:
                nuevo_indice = (alfabeto.index(letra) - self.token) % len(alfabeto)
                resultado += alfabeto[nuevo_indice]
            else:
                resultado += letra

        return resultado




class ReglaCifradoNumerico(ReglaCifrado):


    def mensaje_valido(self, mensaje: str) -> bool:
        def encontrar_espacios(mens: str):
            if mens.startswith(' ') or mens.endswith(' '):
                return False
            return True

        def encontrar_doble_espacio(mens: str):
            return '  ' not in mens

        error_messages = []

        if self.encontrar_numeros_mensaje(mensaje):
            error_messages.append('ContieneNumero')
        if self.encontrar_no_ascii_mensaje(mensaje):
            error_messages.append('ContieneNoAscii')
        if not encontrar_doble_espacio(mensaje):  # Evalúa doble espacio primero
            error_messages.append('DobleEspacio')
        if not encontrar_espacios(mensaje):  # Luego evalúa espacios al inicio o final
            error_messages.append('NoTrim')
        if error_messages:
            raise Exception(" | ".join(error_messages))

        return True

    def encriptar(self, mensaje: str) -> str:
        if not self.mensaje_valido(mensaje):
            raise ValueError

        mensaje_min = mensaje.lower()
        resultado = ''
        for caracter in mensaje:
            num = ord(caracter) * self.token
            resultado += f'{num} '

        return resultado.strip()

    def desencriptar(self, mensaje: str) -> str:
        numeros = mensaje.split(' ')
        resultado = ''
        for numero in numeros:
            numero_original = int(numero) / self.token
            resultado +=  chr(int(numero_original))
        return resultado


class Cifrador:

    def __init__(self, agente: ReglaCifrado):
        self.agente: ReglaCifrado = agente

    def encriptar(self, mensaje: str) -> str:
        return self.agente.encriptar(mensaje)

    def desencriptar(self, mensaje: str) -> str:
        return self.agente.desencriptar(mensaje)