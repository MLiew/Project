package com.example.clothesapptest;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.ItemTouchHelper;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.widget.Toast;

import java.io.File;
import java.util.List;

public class CategoryItemActivity extends AppCompatActivity {
    public static final String EXTRA_CATEGORY_LIST = "com.example.clothesapptest.EXTRA_CATEGORY_LIST";
    public String current_category_list;
    CollectionAdapter categoryAdapter;
    CollectionViewModel categoryViewModel;
    public static final int EDIT_CLOTH_REQUEST = 108;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_category_item);

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setHomeAsUpIndicator(R.drawable.close_icon);

        Intent intent = getIntent();
        if (intent.hasExtra(EXTRA_CATEGORY_LIST)) {
            current_category_list = intent.getStringExtra(EXTRA_CATEGORY_LIST);
            setTitle(current_category_list);
        }

        categoryAdapter = new CollectionAdapter();
        RecyclerView recyclerViewCategory = findViewById(R.id.recycler_view_collection); //local variable
        recyclerViewCategory.setAdapter(categoryAdapter);
        recyclerViewCategory.setLayoutManager(new GridLayoutManager(CategoryItemActivity.this, 2));
        recyclerViewCategory.setHasFixedSize(true);

        // create an instance of view model
        categoryViewModel = ViewModelProvider.AndroidViewModelFactory.getInstance(getApplication()).create(CollectionViewModel.class);
        categoryViewModel.getCategoryClothes(current_category_list).observe(this, new Observer<List<Cloth>>() {
            @Override
            public void onChanged(List<Cloth> clothes) {
                //update recycler view
                categoryAdapter.setClothes(clothes);
            }
        });

        // delete item by swiping left or right
        new ItemTouchHelper(new ItemTouchHelper.SimpleCallback(0,
                ItemTouchHelper.LEFT | ItemTouchHelper.RIGHT) {
            @Override
            public boolean onMove(@NonNull RecyclerView recyclerView, @NonNull RecyclerView.ViewHolder viewHolder, @NonNull RecyclerView.ViewHolder target) {
                return false;
            }

            @Override
            public void onSwiped(@NonNull RecyclerView.ViewHolder viewHolder, int direction) {
                categoryViewModel.delete(categoryAdapter.getClothAt(viewHolder.getAdapterPosition()));
                Toast.makeText(getApplicationContext(),"Cloth deleted", Toast.LENGTH_SHORT).show();
            }
        }).attachToRecyclerView(recyclerViewCategory);

        // open up AddItemActivity when an item is clicked
        categoryAdapter.setOnItemClickListener(new CollectionAdapter.OnItemClickListener() {
            @Override
            public void onItemClick(Cloth cloth) {
                Intent edit_intent = new Intent(CategoryItemActivity.this, AddItemActivity.class);
                edit_intent.putExtra(AddItemActivity.EXTRA_ID, cloth.getId());
                edit_intent.putExtra(AddItemActivity.EXTRA_CATEGORY, cloth.getCategory());
                edit_intent.putExtra(AddItemActivity.EXTRA_DESCRIPTION, cloth.getDescription());
                edit_intent.putExtra(AddItemActivity.EXTRA_COLOR, cloth.getColor());
                edit_intent.putExtra(AddItemActivity.EXTRA_SIZE, cloth.getSize());
                edit_intent.putExtra(AddItemActivity.EXTRA_PRICE, cloth.getPrice());
                edit_intent.putExtra(AddItemActivity.EXTRA_STATUS, cloth.getStatus());
                edit_intent.putExtra(AddItemActivity.EXTRA_PIC_PATH, cloth.getPicPath());
                edit_intent.putExtra(AddItemActivity.EXTRA_BRAND, cloth.getBrand());
                startActivityForResult(edit_intent, EDIT_CLOTH_REQUEST);
            }
        });
    }

    @Override
    public boolean onSupportNavigateUp() {
        onBackPressed();
        return true;
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == EDIT_CLOTH_REQUEST && resultCode == RESULT_OK){
            int id = data.getIntExtra(AddItemActivity.EXTRA_ID, -1);
            if (id == -1){
                Toast.makeText(getApplicationContext(),"Cloth cannot be updated", Toast.LENGTH_SHORT).show();
                return;
            }

            String category = data.getStringExtra(AddItemActivity.EXTRA_CATEGORY);
            String description = data.getStringExtra(AddItemActivity.EXTRA_DESCRIPTION);
            String brand = data.getStringExtra(AddItemActivity.EXTRA_BRAND);
            String price = data.getStringExtra(AddItemActivity.EXTRA_PRICE);
            String size = data.getStringExtra(AddItemActivity.EXTRA_SIZE);
            String color = data.getStringExtra(AddItemActivity.EXTRA_COLOR);
            String status = data.getStringExtra(AddItemActivity.EXTRA_STATUS);
            String pic_path = data.getStringExtra(AddItemActivity.EXTRA_PIC_PATH);

            Cloth cloth = new Cloth(category, description, brand, color,size,price,status,pic_path);
            cloth.setId(id);
            categoryViewModel.update(cloth);

            Toast.makeText(getApplicationContext(), "Cloth updated", Toast.LENGTH_SHORT).show();
        }
        else{
            Toast.makeText(getApplicationContext(),"Cloth not saved", Toast.LENGTH_SHORT).show();
        }
    }
}
