package com.example.clothesapptest;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import java.util.List;

public class CollectionViewModel extends AndroidViewModel {
    public ClothRepository repository;
    private LiveData<List<Cloth>> allClothes;

    public CollectionViewModel(@NonNull Application application) {
        super(application);
        repository = new ClothRepository(application);
        allClothes = repository.getAllClothes();
    }

    public void insert(Cloth cloth){repository.insert(cloth);}

    public void update(Cloth cloth){repository.update(cloth);}

    public void delete(Cloth cloth){repository.delete(cloth);}

    public void deleteAllClothes(){repository.deleteAllClothes();}

    public LiveData<List<Cloth>> getAllClothes(){return allClothes;}

    public LiveData<List<Cloth>> getCategoryClothes(String category){return repository.getCategoryClothes(category);}
}
