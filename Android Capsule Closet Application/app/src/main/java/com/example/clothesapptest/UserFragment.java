package com.example.clothesapptest;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

public class UserFragment extends Fragment {
    int number;

    public static UserFragment newInstance() {
        UserFragment fragmentUser = new UserFragment();
        return fragmentUser;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.fragment_user, container, false);
        ImageView imageView = root.findViewById(R.id.userImageView);
        imageView.setImageResource(R.drawable.cat);
        ImageButton imageView4 = root.findViewById(R.id.imageView4);
        ImageButton imageView5 = root.findViewById(R.id.imageView5);
        ImageButton imageView6 = root.findViewById(R.id.imageView6);
        imageView4.setImageResource(R.drawable.brand_icon);
        imageView5.setImageResource(R.drawable.money_icon);
        imageView6.setImageResource(R.drawable.status_icon);
        //        final TextView textView = root.findViewById(R.id.text_user);

//        Button test_button = root.findViewById(R.id.button_test);
//        test_button.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                Toast.makeText(getActivity().getApplicationContext(), "button pressed", Toast.LENGTH_SHORT).show();
//                number++;
//                textView.setText(String.valueOf(number));
//            }
//        });
        return root;
    }
}
