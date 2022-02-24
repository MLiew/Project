package com.example.clothesapptest;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModel;
import androidx.lifecycle.ViewModelProvider;
import androidx.lifecycle.ViewModelProviders;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.ItemTouchHelper;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.floatingactionbutton.FloatingActionButton;

import java.util.ArrayList;
import java.util.List;

import static android.app.Activity.RESULT_OK;

public class HomeFragment extends Fragment {
    FloatingActionButton floatingActionButton;
    RecyclerView recyclerView;
    ImageView imageView;
    private HomeViewModel homeViewModel;
    private HomeAdapter homeAdapter;
    public static final int ADD_CLOTH_REQUEST = 107;
    public static final int EDIT_CLOTH_REQUEST = 108;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {

        View root = inflater.inflate(R.layout.fragment_home, container, false);

        //RecyclerView
        recyclerView = root.findViewById(R.id.recycler_view);
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerView.setHasFixedSize(true);

        homeAdapter = new HomeAdapter();
        recyclerView.setAdapter(homeAdapter);

        homeViewModel = ViewModelProvider.AndroidViewModelFactory.getInstance(getActivity().getApplication()).create(HomeViewModel.class);
        homeViewModel.getAllCategory().observe(getViewLifecycleOwner(), new Observer<List<CategoryTuple>>() {
            @Override
            public void onChanged(List<CategoryTuple> categories) {
                //update RecyclerView
                if (categories == null){
                    Toast.makeText(getContext(), "empty list", Toast.LENGTH_SHORT).show();
                }
                else{
                    homeAdapter.setCategories(categories);
                }
            }
        });

        homeAdapter.setOnItemClickListener(new HomeAdapter.OnItemClickListener() {
            @Override
            public void onItemClick(CategoryTuple categories) {
                Toast.makeText(getContext(), categories.getCategory(), Toast.LENGTH_SHORT).show();
                Intent intent = new Intent(getContext(), CategoryItemActivity.class);
                intent.putExtra(CategoryItemActivity.EXTRA_CATEGORY_LIST, categories.getCategory());
                startActivity(intent);
            }
        });

        return root;
    }
}