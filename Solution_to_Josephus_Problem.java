
import java.lang.Math ;

import java.util.Scanner ;

public class solve {
    public long power_check(long number, int base){
        long original_number = number ;
        int power = 0 ;
        while (number > 1){
            number /= base ;
            power ++ ;
        }
        long perfect = (long) Math.pow(base, power) ;
        long left = orginal_nunber - perfect ;
        return left ;
    }

    public long josephus_solve(long number, int base){
        long left = power_check(number, base) ;

        if (left == 0){
            return 1 ;
        } else {
            long result = (base*left) + 1 ;
            return result ;
        }
    }

    public long josephus_solve(long number){
        return josephus_solve(number, 2) ;
    }
}

public class josephus {
    public static void main(String[] args){
        long total_people ;

        String msg = " Total number of people in the circle : " ;

        Scanner scanner = new Scanner(msg) ;

        if (scanner.hasNextLong()){
            total_people = scanner.nextLong() ;
        } else { 
            System.out.println(" Please provide a number! ") ;
            System.exit(1) ;
        }

        long answer = solve.josephus_solve(total_people) ;

        System.out.println(" The winner in " + total_people + " is number " + answer ) ;

}
