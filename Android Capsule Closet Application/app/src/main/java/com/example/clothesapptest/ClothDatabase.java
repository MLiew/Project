package com.example.clothesapptest;

import android.content.Context;
import android.os.AsyncTask;

import androidx.annotation.NonNull;
import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;
import androidx.sqlite.db.SupportSQLiteDatabase;

@Database(entities = Cloth.class, version = 2, exportSchema = false)
public abstract class ClothDatabase extends RoomDatabase {
    private static ClothDatabase instance;
    public abstract ClothDao clothDao();

    public static synchronized ClothDatabase getInstance(Context context){
        if (instance == null){
            instance = Room.databaseBuilder(context.getApplicationContext(),
                    ClothDatabase.class, "cloth_database")
                    .fallbackToDestructiveMigration()
                    .addCallback(roomCallback)
                    .build();
        }
        return instance;
    }

    private static RoomDatabase.Callback roomCallback = new RoomDatabase.Callback(){
        @Override
        public void onCreate(@NonNull SupportSQLiteDatabase db) {
            super.onCreate(db);
            new PopulateDbAsyncTask(instance).execute();
        }
    };

    private static class PopulateDbAsyncTask extends AsyncTask<Void, Void, Void> {
        private ClothDao clothDao;
        private  PopulateDbAsyncTask(ClothDatabase db){
            clothDao = db.clothDao();
        }

        @Override
        protected Void doInBackground(Void... voids) {
            clothDao.insert(new Cloth("Testing", "Description 1", "Uniqlo", "red", "S", "20","Available", "/storage/9051-14E9/DCIM/Camera/IMG_2017042_134654.jpg"));
            return null;
        }
    }
}
