package com.example.clothesapptest;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import java.util.ArrayList;
import java.util.List;

public class HomeAdapter extends RecyclerView.Adapter<HomeAdapter.HomeHolder> {
    private List<CategoryTuple> categories = new ArrayList<>();
    private OnItemClickListener listener;

    @NonNull
    @Override
    public HomeHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.home_item, parent, false);
        return new HomeHolder(itemView);
    }
    @Override
    public void onBindViewHolder(@NonNull HomeHolder holder, int position) {
        CategoryTuple currentCategory = categories.get(position);
        holder.textViewQuantity.setText(String.valueOf(currentCategory.getCOUNT()));
        holder.textViewCategory.setText(currentCategory.getCategory());
        holder.imageView.setImageResource(R.drawable.shirt_icon);
    }
    @Override
    public int getItemCount() {
        return categories.size();
    }

    public void setCategories(List<CategoryTuple> categories) {
        this.categories = categories;
        notifyDataSetChanged();
    }


    class HomeHolder extends RecyclerView.ViewHolder {
        private TextView textViewCategory, textViewDescription, textViewQuantity;
        private ImageView imageView;

        public HomeHolder(View itemView) {
            super(itemView);
            textViewCategory = itemView.findViewById(R.id.text_view_category);
            textViewDescription = itemView.findViewById(R.id.text_view_description);
            textViewQuantity = itemView.findViewById(R.id.text_view_quantity);
            imageView = itemView.findViewById(R.id.homeImageView);

            itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    int position = getAdapterPosition();
                    if (listener != null && position != RecyclerView.NO_POSITION) {
                        listener.onItemClick(categories.get(position));
                    }
                }
            });
        }
    }
    public interface OnItemClickListener {
        void onItemClick(CategoryTuple categories);
    }
    public void setOnItemClickListener(OnItemClickListener listener) {
        this.listener = listener;
    }
}