package autosink;

import java.util.HashMap;
import java.util.Scanner;
import java.util.Stack;


public class Auto_sink {

	public static void main(String args[])
	{
        //create scanner
        Scanner input = new Scanner(System.in);
            
        int numOfCities = input.nextInt();

        //create a graph for all the cities
        Graph graphOfCities = new Graph(numOfCities);

        //create a list of all cities
        HashMap<String, City> listOfCities = new HashMap<String, City>();

        //index all cities into a map
        for(int i = 0; i < numOfCities; i++)
        {
            String cityName = input.next();
            int cityToll = input.nextInt();
            City newCity = new City(cityName, cityToll);
            listOfCities.put(cityName, newCity);
        }
        
        graphOfCities.listOfCities = listOfCities;

        int numberOfHighways = input.nextInt();        

        for(int i = 0; i < numberOfHighways; i++)
        {
            String originHighway = input.next();
            String destHighway = input.next();

            graphOfCities.addEdge(originHighway, listOfCities.get(destHighway));
        }
        
        int numOfTrips = input.nextInt();
        
        Stack<String> topologicallySortedStack = graphOfCities.topologicalSort();

        for(int i = 0; i < numOfTrips; i++)
        {
        	String originCity = input.next();
        	String destCity = input.next();
        	
        	@SuppressWarnings("unchecked")
			Stack<String> cloneStack = (Stack<String>) topologicallySortedStack.clone();
        	
			String shortestPath = graphOfCities.findShortestPath(originCity, destCity, cloneStack);
        
        	System.out.println(shortestPath);
        }
        
        input.close();
    }

}