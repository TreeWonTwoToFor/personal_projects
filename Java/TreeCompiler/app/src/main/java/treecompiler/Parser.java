package treecompiler;

import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;

public class Parser {
    private ArrayList<Token> tokenList;
    private String filePath = "C:\\Users\\Jonathan\\Programming\\random_stuff\\Java\\TreeCompiler\\output.txt";
    private String code = "";

    public Parser(ArrayList<Token> tokenList) {
        this.tokenList = tokenList;
    }

    public void runParser() throws IOException {
        printArrayList("token");
        generateCode();
        stringToFile(code);
    }

    private void printArrayList(String arrayType) {
        if (arrayType.equals("token")) {
            for (int i = 0; i < tokenList.size(); i++) {
                String output = tokenList.get(i).getName();
                if (!(i == tokenList.size() - 1)) {
                    output += ", ";
                }
                System.out.print(output);
            }
        }
    }

    @SuppressWarnings("unused")
    private void stringArrayToFile(String arrayType) throws IOException {
        FileOutputStream fos = new FileOutputStream(filePath);
        String data = arrayListToString(arrayType);
        fos.write(data.getBytes());
        fos.flush();
        fos.close();
    }

    private void stringToFile(String string) throws IOException {
        FileOutputStream fos = new FileOutputStream(filePath);
        fos.write(string.getBytes());
        fos.flush();
        fos.close();
    }

    private String arrayListToString(String listType) {
        String data = "";
        if (listType.equals("token")) {
            for (Token token : this.tokenList) {
                data = data + "<" + token.getName() + ", " + token.getValue() + ">\n";
            }
        }
        return data;
    }

    @SuppressWarnings("unused")
    private String testParsing() {
        String output = "";
        if (tokenList.get(0).getName().equals("add")) {
            if (tokenList.get(1).getValue().equals("number")) {
                if (tokenList.get(2).getValue().equals("number")) {
                    if (tokenList.get(3).getName().equals("semi")) {
                        output += "print(";
                        output += tokenList.get(1).getName().toString();
                        output += "+";
                        output += tokenList.get(2).getName().toString();
                        output += ")";
                    }
                }
            }
        }
        return output;
    }

    private void generateCode() {
        // generate a list of registers that the user can use
        ArrayList<Register> registers = new ArrayList<>();
        registers.add(new Register("ra", "0"));
        registers.add(new Register("rb", "0"));
        registers.add(new Register("rc", "0"));
        registers.add(new Register("rd", "0"));
        code += "registers = [";
        for (int i = 0; i < registers.size(); i++) {
            Register register = registers.get(i);
            code += "(\"" + register.getName() + "\", \"" + register.getStingValue() + "\")";
            if (!(i == registers.size()-1)) {
                code +=  ", ";
            }
        }
        code += "]\nfor i in range(len(registers)):\n\tprint(registers[i])";
    }
}
