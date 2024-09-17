class City {
    private String name;
    private String state;
    private double highTemp;
    private double lowTemp;

    public City(String name, String state, double highTemp, double lowTemp) {
        this.name = name;
        this.state = state;
        this.highTemp = highTemp;
        this.lowTemp = lowTemp;
    }

    public String getName() {
        return this.name;
    }

    public String getState() {
        return this.state;
    }

    public double getHighTemp() {
        return this.highTemp;
    }

    public double getLowTemp() {
        return this.lowTemp;
    }

    public void setHighTemp(double temp) {
        this.highTemp = temp;
    }

    public void setLowTemp(double temp) {
        this.lowTemp = temp;
    }

    public void printInfo() {
        System.out.printf("%s, %s (High = %.2f, Low = %.2f)\n", this.name, this.state, this.highTemp, this.lowTemp);
    }
}