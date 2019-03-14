package com.obomprogramador.multi;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import org.apache.commons.lang3.time.StopWatch;

class FibCalc {
	public static long fib(long n) {
	    if (n <= 1) 
	       return n; 
	    return fib(n-1) + fib(n-2); 
	}
}

class Resultado {
	long valor;
	double segundos;
}

class CallableFibo implements Callable<Resultado> {
    Long n;
    CallableFibo(long n) {
          this.n = n;         
    }          
    public Resultado call() throws Exception {
    	StopWatch watch = new StopWatch();
		watch.start();
		long valor = FibCalc.fib(this.n);
		watch.stop();
		Resultado res = new Resultado();
		res.valor = valor;
		res.segundos = (float)watch.getTime()/1000.00;
		return res;
    }
}

public class Fibo {
	public void singleTest() {
		StopWatch watch = new StopWatch();
		watch.start();
		long saida = FibCalc.fib(42);
		watch.stop();
		System.out.println("Resultado: " + saida + " Segundos: " + ((float)watch.getTime()/1000.00));		
	}
	
	public static void main(String [] args) throws InterruptedException, ExecutionException {
		int num_threads = 1;
		if (args.length > 0) {
			num_threads = Integer.parseInt(args[0]);
			ExecutorService executor = Executors.newFixedThreadPool(num_threads);
            List <Future<Resultado>> lista = new ArrayList<Future<Resultado>>();
            for (int i = 0; i<num_threads; i++) {
            	Future<Resultado> future = executor.submit(new CallableFibo(42));
                lista.add(future);            	
            }
            for (Future<Resultado> f : lista) {
            	Resultado r = f.get();
            	System.out.println("Resultado: " + r.valor + " segundos: " + r.segundos);
            }
            executor.shutdown();
		}
		else {
			new Fibo().singleTest();
		}
	}
}