import java.util.ArrayList;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Scanner;

class ClimateZone {
    private ArrayList<City> cityList;

    public ClimateZone() {
        cityList = new ArrayList<City>();
    }

    public ClimateZone(String dataFile) throws IOException {
        String name;
        String state;
        double high;
        double low;
        cityList = new ArrayList<City>();
        // need to read in files
        FileInputStream fInputStream = new FileInputStream(dataFile);
        Scanner scnr = new Scanner(fInputStream);

        while (scnr.hasNext()) {
            name = scnr.next();
            state = scnr.next();
            high = scnr.nextDouble();
            low = scnr.nextDouble();
            City outCity = new City(name, state, high, low);
            cityList.add(outCity);
        }
    }

    public void addCity(String name, String state, double high, double low) {
        this.cityList.add(new City(name, state, high, low));
    }

    public int getCityCount() {
        return this.cityList.size();
    }

    public City getCityByName(String name, String state) {
        City outCity = null;
        for (City city : this.cityList) {
            if (city.getName().equals(name) && city.getState().equals(state)) {
                outCity = city;
            }
        }
        return outCity;
    }

    public void printHottestCities() {
        City hottestCity = null;
        City secondCity = null;
        double highestTemp = 1.0;
        double secondTemp = 0.0;
        for (City city : this.cityList) {
            double currTemp = city.getHighTemp();
            if (currTemp > highestTemp) {
                secondTemp = highestTemp;
                secondCity = hottestCity;
                highestTemp = currTemp;
                hottestCity = city;
            } else if (currTemp < highestTemp && currTemp > secondTemp) {
                secondTemp = currTemp;
                secondCity = city;
            }
        }
        hottestCity.printInfo();
        secondCity.printInfo();
    }

    public void printColdestCities() {
        City coldestCity = null;
        City secondCity = null;
        double lowestTemp = 101.0;
        double secondTemp = 100.0;
        for (City city : this.cityList) {
            double currTemp = city.getLowTemp();
            if (currTemp < lowestTemp) {
                secondTemp = lowestTemp;
                secondCity = coldestCity;
                lowestTemp = currTemp;
                coldestCity = city;
            } else if (currTemp > lowestTemp && currTemp < secondTemp) {
                secondTemp = currTemp;
                secondCity = city;
            }
        }
        coldestCity.printInfo();
        secondCity.printInfo();
    }

    public void printAllCities() {
        for (City city : this.cityList) {
            city.printInfo();
        }
    }
}