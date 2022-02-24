package com.example.clothesapptest;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.recyclerview.widget.ListAdapter;
import androidx.recyclerview.widget.RecyclerView;
import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class CollectionAdapter extends RecyclerView.Adapter<CollectionAdapter.CollectionHolder> {
    private List<Cloth> clothes = new ArrayList<>();
    private OnItemClickListener listener;

    @NonNull
    @Override
    public CollectionHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.collection_item, parent, false);
        return new CollectionHolder(itemView);
    }
    @Override
    public void onBindViewHolder(@NonNull CollectionHolder holder, int position) {
        Cloth currentCloth = clothes.get(position);
        holder.textViewCategory.setText(currentCloth.getCategory());
        holder.imageView.setImageURI(Uri.fromFile(new File(currentCloth.getPicPath())));//should be getPicPath()
    }

    @Override
    public int getItemCount() {
        return clothes.size();
    }

    public void setClothes(List<Cloth> clothes) {
        this.clothes = clothes;
        notifyDataSetChanged();
    }

    public Cloth getClothAt(int position) {
        return clothes.get(position);
    }

    class CollectionHolder extends RecyclerView.ViewHolder {
        private TextView textViewCategory; //might be name here
        private ImageView imageView;

        public CollectionHolder(View itemView) {
            super(itemView);
            textViewCategory = itemView.findViewById(R.id.text_view_title);
            imageView = itemView.findViewById(R.id.collectionImageView);

            itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    int position = getAdapterPosition();
                    if (listener != null && position != RecyclerView.NO_POSITION) {
                        listener.onItemClick(clothes.get(position));
                    }
                }
            });
        }
    }

    public interface OnItemClickListener {
        void onItemClick(Cloth cloth);
    }
    public void setOnItemClickListener(OnItemClickListener listener) {
        this.listener = listener;
    }
}