package com.example.clothesapptest;

import android.app.Application;
import android.os.AsyncTask;
import androidx.lifecycle.LiveData;
import androidx.room.Update;

import java.util.List;

public class ClothRepository {
    private ClothDao clothDao;
    private LiveData<List<Cloth>> allClothes;
    private LiveData<List<CategoryTuple>> allCategory;

    public ClothRepository(Application application){
        ClothDatabase database = ClothDatabase.getInstance(application);
        clothDao = database.clothDao();
        allClothes = clothDao.getAllClothes();
        allCategory = clothDao.getAllCategory();
    }

    public void insert(Cloth cloth){
        new InsertClothAsyncTask(clothDao).execute(cloth);
    }

    public  void update(Cloth cloth){
        new UpdateClothAsyncTask(clothDao).execute(cloth);
    }

    public void delete(Cloth cloth){
        new DeleteClothAsyncTask(clothDao).execute(cloth);
    }

    public void deleteAllClothes(){
        new DeleteAllClothesAsyncTask(clothDao).execute();
    }

    public LiveData<List<Cloth>> getAllClothes(){
        return allClothes;
    }

    public LiveData<List<CategoryTuple>> getAllCategory(){return allCategory;}

    public LiveData<List<Cloth>> getCategoryClothes(String category){return clothDao.getCategoryClothes(category);}

    private static class InsertClothAsyncTask extends AsyncTask<Cloth, Void, Void>{
        private ClothDao clothDao;

        private InsertClothAsyncTask(ClothDao clothDao){
            this.clothDao = clothDao;
        }

        @Override
        protected Void doInBackground(Cloth... clothes) {
            clothDao.insert((clothes[0]));
            return null;
        }
    }

    private static class UpdateClothAsyncTask extends AsyncTask<Cloth, Void, Void>{
        private ClothDao clothDao;

        private UpdateClothAsyncTask(ClothDao clothDao){
            this.clothDao = clothDao;
        }

        @Override
        protected Void doInBackground(Cloth... clothes) {
            clothDao.update((clothes[0]));
            return null;
        }
    }

    private static class DeleteClothAsyncTask extends AsyncTask<Cloth, Void, Void>{
        private ClothDao clothDao;

        private DeleteClothAsyncTask(ClothDao clothDao){
            this.clothDao = clothDao;
        }

        @Override
        protected Void doInBackground(Cloth... clothes) {
            clothDao.delete((clothes[0]));
            return null;
        }
    }

    private static class DeleteAllClothesAsyncTask extends AsyncTask<Void, Void, Void>{
        private ClothDao clothDao;

        private DeleteAllClothesAsyncTask(ClothDao clothDao){
            this.clothDao = clothDao;
        }

        @Override
        protected Void doInBackground(Void... voids) {
            clothDao.deleteAllClothes();
            return null;
        }
    }
}
