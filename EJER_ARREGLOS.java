import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

public class EJER_ARREGLOS {
    static String[] meses = {"Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"};
    static ArrayList<String> departamentos = new ArrayList<>();
    static int[][] matriz;
    static Random rand = new Random();
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
       
        departamentos.add("Ropa");
        departamentos.add("Deportes");
        departamentos.add("Juguetería");

        
        matriz = new int[meses.length][departamentos.size()];
        for (int i = 0; i < meses.length; i++) {
            for (int j = 0; j < departamentos.size(); j++) {
                matriz[i][j] = rand.nextInt(4001) + 1000; 
            }
        }

        
        while (true) {
            System.out.println("\n=== MENÚ DE VENTAS ===");
            System.out.println("1. Mostrar tabla de ventas");
            System.out.println("2. Insertar/Actualizar venta");
            System.out.println("3. Buscar una venta");
            System.out.println("4. Eliminar una venta");
            System.out.println("5. Agregar nuevo departamento");
            System.out.println("6. Salir");
            System.out.print("Elige una opción: ");
            int opcion = sc.nextInt();
            sc.nextLine(); 

            switch (opcion) {
                case 1:
                    mostrarTabla();
                    break;
                case 2:
                    insertarVenta();
                    break;
                case 3:
                    buscarVenta();
                    break;
                case 4:
                    eliminarVenta();
                    break;
                case 5:
                    agregarDepartamento();
                    break;
                case 6:
                    System.out.println("Saliendo del sistema...");
                    return;
                default:
                    System.out.println("Opción no válida. Intenta de nuevo.");
            }
        }
    }

    
    public static void insertarVenta() {
        System.out.print("Número de mes (1-12): ");
        int mes = sc.nextInt() - 1;

        for (int i = 0; i < departamentos.size(); i++) {
            System.out.println((i + 1) + ". " + departamentos.get(i));
        }
        System.out.print("Elige departamento: ");
        int depto = sc.nextInt() - 1;

        System.out.print("Ingresa la venta: ");
        int valor = sc.nextInt();

        matriz[mes][depto] = valor;
        System.out.println("Venta registrada.");
    }

    public static void buscarVenta() {
        System.out.print("Ingresa el valor de la venta a buscar: ");
        int valor = sc.nextInt();

        for (int i = 0; i < meses.length; i++) {
            for (int j = 0; j < departamentos.size(); j++) {
                if (matriz[i][j] == valor) {
                    System.out.println("Venta " + valor + " encontrada en " + meses[i] + " - " + departamentos.get(j));
                    return;
                }
            }
        }
        System.out.println("Venta no encontrada.");
    }

    public static void eliminarVenta() {
        System.out.print("Número de mes (1-12): ");
        int mes = sc.nextInt() - 1;

        for (int i = 0; i < departamentos.size(); i++) {
            System.out.println((i + 1) + ". " + departamentos.get(i));
        }
        System.out.print("Elige departamento: ");
        int depto = sc.nextInt() - 1;

        matriz[mes][depto] = 0;
        System.out.println("Venta eliminada.");
    }

    public static void agregarDepartamento() {
        sc.nextLine(); 
        System.out.print("Nombre del nuevo departamento: ");
        String nombre = sc.nextLine();
        departamentos.add(nombre);

        
        int[][] nuevaMatriz = new int[meses.length][departamentos.size()];
        for (int i = 0; i < meses.length; i++) {
            for (int j = 0; j < departamentos.size() - 1; j++) {
                nuevaMatriz[i][j] = matriz[i][j];
            }
            nuevaMatriz[i][departamentos.size() - 1] = 0;
        }
        matriz = nuevaMatriz;

        System.out.println("Departamento '" + nombre + "' agregado.");
    }

    public static void mostrarTabla() {
        System.out.printf("%-12s", "Mes");
        for (String d : departamentos) {
            System.out.printf("%-12s", d);
        }
        System.out.println();

        
        for (int k = 0; k < 12 * (departamentos.size() + 1); k++) {
            System.out.print("-");
        }
        System.out.println();

        for (int i = 0; i < meses.length; i++) {
            System.out.printf("%-12s", meses[i]);
            for (int j = 0; j < departamentos.size(); j++) {
                System.out.printf("%-12d", matriz[i][j]);
            }
            System.out.println();
        }
    }
}
