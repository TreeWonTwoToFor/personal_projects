package treecompiler;

public class Register {
    private String name;
    private String stringValue = "";

    public Register(String name) {
        this.name = name;
    }

    public Register(String name, String value) {
        this.name = name;
        this.stringValue = value;
    }

    public String getName() {
        return this.name;
    }

    public String getStingValue() {
        return this.stringValue;
    }

    public int getIntValue() {
        int i = Integer.parseInt(stringValue);
        return i;
    }
}
