import java.io.FileWriter;
import java.io.IOException;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.util.Random;

public class GeraChave {

    private static final String FRASE = "The information security is of significant importance to ensure the privacy of communications.";

    public static void main(String[] args) {
        System.out.println("Iniciando...");
        int bitLength = 4096;
        BigInteger[] rsa = getRSA(bitLength);
        BigInteger e = rsa[0];
        BigInteger d = rsa[1];
        BigInteger N = rsa[2];

        System.out.println("Criptografando");
        BigInteger criptografado = criptografar(FRASE, e, N);
        System.out.println("Decriptografando");
        String decriptografado = decriptografar(criptografado, d, N);

        try {
            FileWriter privateFile = new FileWriter("private.json");
            privateFile.write(String.format("{\n  \"key\": \"%s\",\n  \"n\": \"%s\"\n}", e.toString(), N.toString()));
            privateFile.close();

            FileWriter publicFile = new FileWriter("public.json");
            publicFile.write(String.format("{\n  \"key\": \"%s\",\n  \"n\": \"%s\"\n}", d.toString(), N.toString()));
            publicFile.close();
        } catch (IOException ex) {
            System.out.println("Erro ao salvar arquivo: " + ex.getMessage());
        }

        System.out.println("Exibindo resultados");
        System.out.println("Criptografado: " + criptografado);
        System.out.println("Decriptografado: " + decriptografado);
    }

    private static BigInteger[] getRSA(int bitLength) {
        while (true) {
            BigInteger p = BigInteger.probablePrime(bitLength, new Random());
            BigInteger q = BigInteger.probablePrime(bitLength, new Random());

            BigInteger N = p.multiply(q);
            BigInteger fiN = p.subtract(BigInteger.ONE).multiply(q.subtract(BigInteger.ONE));

            BigInteger e = fiN.subtract(BigInteger.ONE);

            if (coprime(fiN, e)) {
                BigInteger d = findD(e, fiN);
                return new BigInteger[]{e, d, N};
            }
        }
    }

    private static boolean isPrime(BigInteger n) {
        if (n.compareTo(BigInteger.ONE) <= 0) {
            return false;
        }
        if (n.compareTo(new BigInteger("3")) <= 0) {
            return true;
        }
        if (n.mod(new BigInteger("2")).equals(BigInteger.ZERO)) {
            return false;
        }
        if (n.mod(new BigInteger("5")).equals(BigInteger.ZERO)) {
            return false;
        }

        BigInteger r = BigInteger.ZERO;
        BigInteger d = n.subtract(BigInteger.ONE);
        while (d.mod(new BigInteger("2")).equals(BigInteger.ZERO)) {
            r = r.add(BigInteger.ONE);
            d = d.divide(new BigInteger("2"));
        }
        int k = 40;
        Random random = new Random();
        for (int i = 0; i < k; i++) {
            BigInteger a = new BigInteger(n.bitLength(), random);
            if (a.compareTo(BigInteger.TWO) < 0 || a.compareTo(n.subtract(BigInteger.ONE)) >= 0) {
                a = a.mod(n.subtract(BigInteger.ONE)).add(BigInteger.TWO);
            }
            BigInteger x = a.modPow(d, n);
            if (x.equals(BigInteger.ONE) || x.equals(n.subtract(BigInteger.ONE))) {
                continue;
            }
            boolean isPrime = false;
            for (BigInteger j = BigInteger.ONE; j.compareTo(r) < 0; j = j.add(BigInteger.ONE)) {
                x = x.modPow(BigInteger.TWO, n);
                if (x.equals(BigInteger.ONE)) {
                    return false;
                }
                if (x.equals(n.subtract(BigInteger.ONE))) {
                    isPrime = true;
                    break;
                }
            }
            if (!isPrime) {
                return false;
            }
        }
        return true;
    }

    private static boolean coprime(BigInteger a, BigInteger b) {
        return a.gcd(b).equals(BigInteger.ONE);
    }

    private static BigInteger criptografar(String texto, BigInteger e, BigInteger N) {
        byte[] messageBytes = texto.getBytes(StandardCharsets.UTF_8);
        BigInteger messageInt = new BigInteger(1, messageBytes);
        return messageInt.modPow(e, N);
    }

    private static String decriptografar(BigInteger criptografado, BigInteger d, BigInteger N) {
        BigInteger decryptedInt = criptografado.modPow(d, N);
        return new String(decryptedInt.toByteArray(), StandardCharsets.UTF_8);
    }

    private static BigInteger findD(BigInteger e, BigInteger fiN) {
        return e.modInverse(fiN);
    }
}
