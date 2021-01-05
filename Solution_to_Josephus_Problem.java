
import java.lang.Math ;

import java.util.Scanner ;

class Solve {
    public long power_check(long number, int base){
        long original_number = number ;
        int power = 0 ;
        while (number > 1){
            number /= base ;
            power ++ ;
        }
        long perfect = (long) Math.pow(base, power) ;
        long left = original_number - perfect ;
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
        long total_people = 0 ;

        String msg = " Total number of people in the circle : " ;

        System.out.print(msg) ;
        Scanner scanner = new Scanner( System.in ) ;

        try {
            total_people = scanner.nextLong() ;
        } catch(Exception e) {
            System.out.println(" Please provide a number ! ") ;
            System.exit(1) ;
        }

        scanner.close() ;

        Solve solve = new Solve() ;

        long answer = solve.josephus_solve(total_people) ;

        System.out.println(" The winner in circle of " + total_people + " people is number " + answer ) ;
    }
}
