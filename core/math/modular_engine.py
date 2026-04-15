import math

class ModularEngine:
    """
    Core Mathematical Engine for Healy Vector Labs.
    Handles high-precision modular arithmetic and CRT reconstruction.
    """

    @staticmethod
    def are_coprime(moduli):
        """Validates that all moduli in the list are pairwise coprime."""
        for i in range(len(moduli)):
            for j in range(i + 1, len(moduli)):
                if math.gcd(moduli[i], moduli[j]) != 1:
                    return False
        return True

    @staticmethod
    def extended_gcd(a, b):
        """Extended Euclidean Algorithm for modular inverse."""
        if a == 0: return b, 0, 1
        gcd, x1, y1 = ModularEngine.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    @staticmethod
    def mod_inverse(a, m):
        """Calculates the modular inverse: (a * x) % m == 1"""
        gcd, x, y = ModularEngine.extended_gcd(a, m)
        if gcd != 1:
            raise ValueError(f"Modular inverse for {a} mod {m} does not exist.")
        return x % m

    @classmethod
    def solve_crt(cls, remainders, moduli):
        """
        Reconstructs the original 'Truth' from modular remainders.
        Uses the Chinese Remainder Theorem logic remembered from 2006.
        """
        if not cls.are_coprime(moduli):
            raise ValueError("Moduli must be pairwise coprime for CRT.")

        M = 1
        for m in moduli:
            M *= m

        result = 0
        for a_i, m_i in zip(remainders, moduli):
            Mi = M // m_i
            yi = cls.mod_inverse(Mi, m_i)
            result += a_i * Mi * yi

        return result % M

