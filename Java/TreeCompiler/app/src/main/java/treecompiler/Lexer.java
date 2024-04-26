package treecompiler;

import java.util.ArrayList;
import java.io.IOException;

public class Lexer {
    private ArrayList<String> wordList;
    private ArrayList<Token> tokenList;

    public Lexer() {
        this.wordList = new ArrayList<>();
        this.tokenList = new ArrayList<>();
    }

    public Lexer(ArrayList<String> inputArrayList) {
        this.wordList = inputArrayList;
        this.tokenList = new ArrayList<>();
    }

    public void runLexer() throws IOException {
        makeTokens();
        /*printArrayList("word");
        printArrayList("token");
        stringArrayToFile("token");*/
    }

    public ArrayList<String> getWordList() {
        return this.wordList;
    }

    public ArrayList<Token> getTokenList() {
        return this.tokenList;
    }

    private void newTokenToList() {
        tokenList.add(new Token());
    }

    private void newTokenToList(String name, String value) {
        tokenList.add(new Token(name, value));
    }

    private void makeTokens() {
        for (String word : wordList) {
            if (word.equals("ADD")) {
                newTokenToList("add", "operator");
            } else if (isNumeric(word)) {
                newTokenToList(word, "number");
            } else {
                newTokenToList();
            }
        }
    }


    public static boolean isNumeric(String strNum) {
        if (strNum == null) {
            return false;
        }
        try {
            @SuppressWarnings("unused")
            int i = Integer.parseInt(strNum);
        } catch (NumberFormatException nfe) {
            return false;
        }
        return true;
    }

    /* OLD FUNCTIONS THAT ARE NO LONGER NEEDED
    
    private void stringArrayToFile(String arrayType) throws IOException {
        FileOutputStream fos = new FileOutputStream(filePath);
        String data = arrayListToString(arrayType);
        fos.write(data.getBytes());
        fos.flush();
        fos.close();
    }

    private String arrayListToString(String listType) {
        String data = "";
        if (listType.equals("word")) {
            for (String string : this.wordList) {
                data = data + string + " ";
            }
        } else if (listType.equals("token")) {
            for (Token token : this.tokenList) {
                data = data + "<" + token.getName() + ", " + token.getValue() + "> ";
            }
        }
        
        return data;
    }

    private void printArrayList(String arrayType) {
        if (arrayType.equals("word")) {System.out.println(wordList);}
        else if (arrayType.equals("token")) {System.out.println(tokenList);}
    }
    
    */
}
