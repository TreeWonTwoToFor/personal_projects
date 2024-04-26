package treecompiler;

import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;

public class Parser {
    private ArrayList<Token> tokenList;
    private String filePath = "C:\\Users\\Jonathan\\Programming\\random_stuff\\Java\\TreeCompiler\\output.txt";

    public Parser(ArrayList<Token> tokenList) {
        this.tokenList = tokenList;
    }

    public void runParser() throws IOException {
        printArrayList("token");
        stringArrayToFile("token");
    }

    private void printArrayList(String arrayType) {
        if (arrayType.equals("token")) {System.out.println(tokenList);}
    }

    private void stringArrayToFile(String arrayType) throws IOException {
        FileOutputStream fos = new FileOutputStream(filePath);
        String data = arrayListToString(arrayType);
        fos.write(data.getBytes());
        fos.flush();
        fos.close();
    }

    private String arrayListToString(String listType) {
        String data = "";
        if (listType.equals("token")) {
            for (Token token : this.tokenList) {
                data = data + "<" + token.getName() + ", " + token.getValue() + "> ";
            }
        }
        
        return data;
    }
}
