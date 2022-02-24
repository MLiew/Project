package com.example.clothesapptest;

import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "cloth_table")
public class Cloth {

    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name="id")
    private int id;
    @ColumnInfo(name="category")
    private String category;
    @ColumnInfo(name="description")
    private String description;
    @ColumnInfo(name="brand")
    private String brand;
    @ColumnInfo(name="color")
    private String color;
    @ColumnInfo(name="size")
    private String size;
    @ColumnInfo(name="price")
    private String price;
    @ColumnInfo(name="status")
    private String status;
    @ColumnInfo(name="picPath")
    private String picPath;

    public Cloth(String category, String description, String brand, String color, String size, String price, String status, String picPath) {
        this.category = category;
        this.description = description;
        this.brand = brand;
        this.color = color;
        this.size = size;
        this.price = price;
        this.status = status;
        this.picPath = picPath;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getCategory() {
        return category;
    }

    public String getDescription() {
        return description;
    }

    public String getBrand() {
        return brand;
    }

    public String getColor() {
        return color;
    }

    public String getSize() {
        return size;
    }

    public String getPrice() {
        return price;
    }

    public String getStatus() {
        return status;
    }

    public String getPicPath() {
        return picPath;
    }
}