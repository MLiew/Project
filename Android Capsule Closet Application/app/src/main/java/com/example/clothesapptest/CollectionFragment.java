package com.example.clothesapptest;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModel;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.ItemTouchHelper;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.floatingactionbutton.FloatingActionButton;

import java.util.List;

import static android.app.Activity.RESULT_OK;

public class CollectionFragment extends Fragment {
    private CollectionAdapter collectionAdapter;
    private CollectionViewModel collectionViewModel;
    public static final int ADD_CLOTH_REQUEST = 107;
    public static final int EDIT_CLOTH_REQUEST = 108;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.fragment_collection, container, false);

        //Floating action button
        FloatingActionButton floatingActionButton = root.findViewById(R.id.float_add_button);
        floatingActionButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(getContext(), "floating button pressed", Toast.LENGTH_SHORT).show();
                Intent add_item_intent = new Intent(getActivity(), AddItemActivity.class);
                startActivityForResult(add_item_intent, ADD_CLOTH_REQUEST);
            }
        });

        collectionAdapter = new CollectionAdapter();
        RecyclerView recyclerViewCollection = root.findViewById(R.id.recycler_view_collection); //local variable
        recyclerViewCollection.setAdapter(collectionAdapter);
        recyclerViewCollection.setLayoutManager(new GridLayoutManager(getContext(),2));
        recyclerViewCollection.setHasFixedSize(true);

        collectionViewModel = ViewModelProvider.AndroidViewModelFactory.getInstance(getActivity().getApplication()).create(CollectionViewModel.class);
        collectionViewModel.getAllClothes().observe(getViewLifecycleOwner(), new Observer<List<Cloth>>() {
            @Override
            public void onChanged(List<Cloth> clothes) {
                //update RecyclerView
                collectionAdapter.setClothes(clothes);
            }
        });

        new ItemTouchHelper(new ItemTouchHelper.SimpleCallback(0,
                ItemTouchHelper.LEFT | ItemTouchHelper.RIGHT) {
            @Override
            public boolean onMove(@NonNull RecyclerView recyclerView, @NonNull RecyclerView.ViewHolder viewHolder, @NonNull RecyclerView.ViewHolder target) {
                return false;
            }

            @Override
            public void onSwiped(@NonNull RecyclerView.ViewHolder viewHolder, int direction) {
                collectionViewModel.delete(collectionAdapter.getClothAt(viewHolder.getAdapterPosition()));
                Toast.makeText(getContext(),"Cloth deleted", Toast.LENGTH_SHORT).show();
            }
        }).attachToRecyclerView(recyclerViewCollection);

        collectionAdapter.setOnItemClickListener(new CollectionAdapter.OnItemClickListener() {
            @Override
            public void onItemClick(Cloth cloth) {
                Intent edit_intent = new Intent(getContext(), AddItemActivity.class);
                edit_intent.putExtra(AddItemActivity.EXTRA_ID, cloth.getId());
                edit_intent.putExtra(AddItemActivity.EXTRA_CATEGORY, cloth.getCategory());
                edit_intent.putExtra(AddItemActivity.EXTRA_DESCRIPTION, cloth.getDescription());
                edit_intent.putExtra(AddItemActivity.EXTRA_COLOR, cloth.getColor());
                edit_intent.putExtra(AddItemActivity.EXTRA_SIZE, cloth.getSize());
                edit_intent.putExtra(AddItemActivity.EXTRA_PRICE, cloth.getPrice());
                edit_intent.putExtra(AddItemActivity.EXTRA_STATUS, cloth.getStatus());
                edit_intent.putExtra(AddItemActivity.EXTRA_PIC_PATH, cloth.getPicPath());
                edit_intent.putExtra(AddItemActivity.EXTRA_BRAND, cloth.getBrand());//
                startActivityForResult(edit_intent, EDIT_CLOTH_REQUEST);
            }
        });

        return root;
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == ADD_CLOTH_REQUEST && resultCode == RESULT_OK) {
            String category = data.getStringExtra(AddItemActivity.EXTRA_CATEGORY);
            String description = data.getStringExtra(AddItemActivity.EXTRA_DESCRIPTION);
            String brand = data.getStringExtra(AddItemActivity.EXTRA_BRAND);
            String price = data.getStringExtra(AddItemActivity.EXTRA_PRICE);
            String size = data.getStringExtra(AddItemActivity.EXTRA_SIZE);
            String color = data.getStringExtra(AddItemActivity.EXTRA_COLOR);
            String status = data.getStringExtra(AddItemActivity.EXTRA_STATUS);
            String pic_path = data.getStringExtra(AddItemActivity.EXTRA_PIC_PATH);

            // create a new note
            Cloth cloth = new Cloth(category, description, brand, color,size,price,status,pic_path);
            collectionViewModel.insert(cloth);

            Toast.makeText(getContext(),"Cloth Saved", Toast.LENGTH_SHORT).show();
        }
        else if (requestCode == EDIT_CLOTH_REQUEST && resultCode == RESULT_OK){
            int id = data.getIntExtra(AddItemActivity.EXTRA_ID, -1);
            if (id == -1){
                Toast.makeText(getContext(),"Cloth cannot be updated", Toast.LENGTH_SHORT).show();
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
            collectionViewModel.update(cloth);

            Toast.makeText(getContext(), "Cloth updated", Toast.LENGTH_SHORT).show();
        }
        else{
            Toast.makeText(getContext(),"Cloth not saved", Toast.LENGTH_SHORT).show();
        }
    }
}
