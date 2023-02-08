package PS3;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.Scanner;

import javax.print.DocFlavor.STRING;

public class Auto_sink {


    /*
     * Class represents a city
     */
    class City 
    {
        string cityName;
        int costToTravel;
        City(string cityName, int costToTravel)
        {
            this.cityName = cityName;
            this.costToTravel = costToTravel;
        }
    }

    /*
     * Class represents a dag
     */
    class Graph
    {
        int numOfCities;
        HashMap<STRING, LinkedList<City>> map;

        Graph(int numOfCities)
        {
            this.numOfCities = numOfCities;
            map = new HashMap<string, LinkedList<City>>();
        }

        void addEdge(string originCity, City destCity)
        {
            //check if originCity is in the map yet
            if(map.containsKey(originCity))
                map.get(originCity).add(destCity);
            else
            {
                LinkedList<City> newList = new LinkedList<City>();
                newList.add(destCity);
                map.put(originCity, newList);
            }
        }
    }




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
            String cityToll = input.next();
            City newCity = new City(cityName, cityToll);
            listOfCities.put(cityName, newCity);
        }

        int numberOfHighways = input.nextInt();        

        for(int i = 0; i < numberOfHighways; i++)
        {
            string originHighway = input.next();
            string destHighway = input.next();

            graphOfCities.addEdge(originHighway, listOfCities.get(destHighway));
        }
        
        int numOfTrips = input.nextInt();

        for(int i = 0; i < numOfTrips; i++)
        {

        }
    }

}