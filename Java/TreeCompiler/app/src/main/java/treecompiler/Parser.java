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
        generateCode();
        stringToFile(code);
    }

    private void stringToFile(String string) throws IOException {
        FileOutputStream fos = new FileOutputStream(filePath);
        fos.write(string.getBytes());
        fos.flush();
        fos.close();
    }

    private String tokenLIstString() {
        String data = "";
        for (Token token : this.tokenList) {
            data = data + "<" + token.getName() + ", " + token.getValue() + ">\n";
        }
        return data;
    }

    private boolean checkTokenIndex(String tokenName, int index) {
        return (tokenList.get(index).getName().equals(tokenName));
    }

    private void generateCode() {
        // generate a list of registers that the user can use
        ArrayList<Register> registers = new ArrayList<>();
        registers.add(new Register("rax", "0"));
        registers.add(new Register("rbx", "0"));
        registers.add(new Register("rcx", "0"));
        code += "registers = [";
        for (int i = 0; i < registers.size(); i++) {
            String registerPair = "(\"";
            Register register = registers.get(i);
            registerPair += register.getName() + "\", \"" + register.getStingValue() + "\")";
            if (!(i == registers.size()-1)) {
                registerPair +=  ", ";
            }
            code += registerPair;
        }
        code += "]\n";
        code += "memory = []";

        System.out.println(tokenLIstString());

        int currentToken = 0;
        while (currentToken < tokenList.size()) {
            code += "\n";
            if (checkTokenIndex("add", currentToken)) {
                if (tokenList.get(1).getValue().equals("number")) {
                    if (tokenList.get(2).getValue().equals("number")) {
                        if (checkTokenIndex("semi", currentToken+3)) {
                            code += "rax = " + tokenList.get(1).getName().toString();
                            code += "+" + tokenList.get(2).getName().toString();
                            currentToken += 4;
                        }
                    }
                }
            } else if (checkTokenIndex("output", currentToken)) {
                if (checkTokenIndex("semi", currentToken+2)) {
                    code += "print(" + tokenList.get(currentToken+1).getName().toString() + ")";
                    currentToken += 3;
                }
            } 
        }
    }

    /*@SuppressWarnings("unused")
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
    private void stringArrayToFile(String arrayType) throws IOException {
        FileOutputStream fos = new FileOutputStream(filePath);
        String data = arrayListToString(arrayType);
        fos.write(data.getBytes());
        fos.flush();
        fos.close();
    }*/
}
