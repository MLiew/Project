package com.example.clothesapptest;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import java.util.List;

@Dao
public interface ClothDao {
    @Insert
    void insert(Cloth cloth);

    @Update
    void update(Cloth cloth);

    @Delete
    void delete(Cloth cloth);

    //delete all items
    @Query("DELETE FROM cloth_table")
    void deleteAllClothes();

    //retrieve all items
    @Query("SELECT * FROM cloth_table ORDER BY id DESC")
    LiveData<List<Cloth>> getAllClothes();

    //retrieve all unique category and item's quantity in it
    @Query("SELECT category, COUNT(*) as COUNT FROM cloth_table GROUP BY category ORDER BY 2 DESC")
    LiveData<List<CategoryTuple>> getAllCategory();

    //retrieve all items from specific category
    @Query("SELECT * FROM cloth_table WHERE category = :selectedCategory")
    LiveData<List<Cloth>> getCategoryClothes(String selectedCategory);
}

