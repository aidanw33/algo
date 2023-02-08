package autosink;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.Stack;

public class Graph {
	
		static final int INFINITY = 2000000000;
        int numOfCities;
        HashMap<String, LinkedList<City>> map;
        HashMap<String, City> listOfCities = new HashMap<String, City>();
        
        
        Graph(int numOfCities)
        {
            this.numOfCities = numOfCities;
            map = new HashMap<String, LinkedList<City>>();
        }

        void addEdge(String originCity, City destCity)
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
        
        Stack<String> topologicalSort()
        {
        	Stack<String> topoStack = new Stack<String>();
        	
        	HashMap<String, Boolean> haveVisited = new HashMap<String, Boolean>();
        	
        	//set all visited to false
        	for( String key : listOfCities.keySet())
        	{
        		haveVisited.put(key, false);
        	}
        	
        	for(String key : listOfCities.keySet())
        	{
        		if(!haveVisited.get(key))
        			topoSortRecursive(key, haveVisited, topoStack);
        	}
        	
        	return topoStack;     	
         }
        
        private void topoSortRecursive(String key, HashMap<String, Boolean> haveVisited, Stack<String> topoStack)
        {
        	
        	//set key to visited
        	haveVisited.put(key, true);
        	
        	//Go over all adjacent vertices
        	LinkedList<City> adjCities = map.get(key);
        	
        	if(adjCities != null)
        	{
	        	for(City adjCity : adjCities)
	        	{
	        		String cityName = adjCity.cityName;
	        		if(!haveVisited.get(cityName))
	        			topoSortRecursive(cityName, haveVisited, topoStack);
	        		
	        	}
        	}
        	
        	topoStack.push(key);
        	
        }
        
 
        String findShortestPath(String originCity, String destCity, Stack<String> topoSortStack)
        {
        	
        	//set all distances to -1 except originCity
        	HashMap<String, Integer> distance = new HashMap<String, Integer>();
        	
        	//set all distance to -1 except origin city to 0
        	for( String key : listOfCities.keySet())
        	{
        		distance.put(key, INFINITY);
        	}
        	distance.put(originCity, 0);
        	
        	while(!topoSortStack.empty())
        	{
        		String cityName = topoSortStack.pop();
        		
        		if(distance.get(cityName) != INFINITY)
        		{
        			if(map.get(cityName) != null)
        			{
	        			for(City adjCity : map.get(cityName))
	        			{
	        				String adjCityName = adjCity.cityName;
	        				if(distance.get(adjCityName) > distance.get(cityName) + adjCity.costToTravel)
	        					distance.put(adjCityName, distance.get(cityName) + adjCity.costToTravel);
	        			}
        			}
        		}
        	}
        	
        	if(distance.get(destCity) == INFINITY)
				return "NO";
        	else
        		return distance.get(destCity).toString();
        	
        	
        }
    }


