package com.example.clothesapptest;
import androidx.room.ColumnInfo;

// store category name and quantity of item
public class CategoryTuple {
    @ColumnInfo(name = "category")
    public String category;

    @ColumnInfo(name = "COUNT")
    public int COUNT;

    public CategoryTuple(String category, int COUNT) {
        this.category = category;
        this.COUNT = COUNT;
    }

    public String getCategory() {
        return category;
    }

    public int getCOUNT(){
        return COUNT;
    }
}