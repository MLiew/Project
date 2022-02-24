package com.example.clothesapptest;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;

import android.Manifest;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.ContentResolver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.webkit.MimeTypeMap;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Toast;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class AddItemActivity extends AppCompatActivity {
    public static final int CAMERA_PERM_CODE = 101;
    public static final int CAMERA_REQ_CODE = 102;
    public static final int GALLERY_REQ_CODE = 105;
    public static final int REQUEST_CODE = 123;

    public static final String EXTRA_ID = "com.example.clothesapptest.EXTRA_ID";
    public static final String EXTRA_CATEGORY = "com.example.clothesapptest.EXTRA_CATEGORY";
    public static final String EXTRA_DESCRIPTION = "com.example.clothesapptest.EXTRA_DESCRIPTION";
    public static final String EXTRA_BRAND = "com.example.clothesapptest.EXTRA_BRAND";
    public static final String EXTRA_COLOR = "com.example.clothesapptest.EXTRA_COLOR";
    public static final String EXTRA_SIZE = "com.example.clothesapptest.EXTRA_SIZE";
    public static final String EXTRA_PRICE = "com.example.clothesapptest.EXTRA_PRICE";
    public static final String EXTRA_STATUS = "com.example.clothesapptest.EXTRA_STATUS";
    public static final String EXTRA_PIC_PATH = "com.example.clothesapptest.EXTRA_PIC_PATH";

    String currentPhotoPath, picturePath;
    private ImageView imageView;
    ImageButton cameraButton, galleryButton;
    private TextInputEditText editTextCategory, editTextBrand, editTextColor, editTextSize, editTextPrice, editTextStatus, editTextDescription;

    public String[] colours = {"Black","Blue","Green","Grey","Red", "Khaki",  "Orange", "Pink", "Purple","Yellow", "White"};//example for alert dialog
    public String[] categories = {"Top", "Jacket", "Pant", "Trouser", "Shoe", "Coat", "Skirt", "Accessory"};
    public String[] status = {"Available", "Disposed", "Laundry"};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_item);

        //set up action bar
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setHomeAsUpIndicator(R.drawable.close_icon);

        // Image View
        imageView = findViewById(R.id.imageView);
        imageView.setImageResource(R.drawable.ic_baseline_image_24);

        //Buttons
        cameraButton = findViewById(R.id.camera_button);
        galleryButton = findViewById(R.id.gallery_button);

        cameraButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(AddItemActivity.this, "Use Camera", Toast.LENGTH_SHORT).show();
                askCameraPermission();
            }
        });

        galleryButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(AddItemActivity.this, "Open Gallery", Toast.LENGTH_SHORT).show();
                Intent gallery = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                startActivityForResult(gallery, GALLERY_REQ_CODE);
            }
        });

        // Edit Text
        editTextCategory = findViewById(R.id.editTextCategory);
        editTextBrand = findViewById(R.id.editTextBrand);
        editTextColor = findViewById(R.id.editTextColor);
        editTextSize = findViewById(R.id.editTextSize);
        editTextPrice = findViewById(R.id.editTextPrice);
        editTextStatus = findViewById(R.id.editTextStatus);
        editTextDescription = findViewById(R.id.editTextDescription);

        editTextCategory.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(AddItemActivity.this, "edit text clicked", Toast.LENGTH_SHORT).show();

                //Alert Dialog build
                AlertDialog.Builder builder = new AlertDialog.Builder(AddItemActivity.this);
                builder.setTitle("Choose a category");

                final int checkedItem = 1;
                builder.setSingleChoiceItems(categories, checkedItem, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        editTextCategory.setText(categories[which]);
                    }
                });
                // add OK and Cancel buttons
                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        // user clicked OK
                        Toast.makeText(getBaseContext(), "Ok checked", Toast.LENGTH_SHORT).show();
                    }
                });
                builder.setNegativeButton("Cancel", null);
                // create and show the alert dialog
                AlertDialog dialog = builder.create();
                dialog.show();
            }
        });

        editTextColor.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(AddItemActivity.this, "edit text clicked", Toast.LENGTH_SHORT).show();

                //Alert Dialog build
                AlertDialog.Builder builder = new AlertDialog.Builder(AddItemActivity.this);
                builder.setTitle("Choose Color");

                final int checkedItem = 1; // cow
                builder.setSingleChoiceItems(colours, checkedItem, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        editTextColor.setText(colours[which]);
                    }
                });
                // add OK and Cancel buttons
                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        // user clicked OK
                        Toast.makeText(getBaseContext(), "Ok checked", Toast.LENGTH_SHORT).show();
                    }
                });
                builder.setNegativeButton("Cancel", null);
                // create and show the alert dialog
                AlertDialog dialog = builder.create();
                dialog.show();
            }
        });

        editTextStatus.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(AddItemActivity.this, "edit text clicked", Toast.LENGTH_SHORT).show();

                //Alert Dialog build
                AlertDialog.Builder builder = new AlertDialog.Builder(AddItemActivity.this);
                builder.setTitle("Choose Status");

                final int checkedItem = 1; // cow
                builder.setSingleChoiceItems(status, checkedItem, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        editTextStatus.setText(status[which]);
                    }
                });
                // add OK and Cancel buttons
                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        // user clicked OK
                        Toast.makeText(getBaseContext(), "Ok checked", Toast.LENGTH_SHORT).show();
                    }
                });
                builder.setNegativeButton("Cancel", null);
                // create and show the alert dialog
                AlertDialog dialog = builder.create();
                dialog.show();
            }
        });

        Intent intent = getIntent();
        if (intent.hasExtra(EXTRA_ID)){
            setTitle("Edit Cloth");
            editTextCategory.setText(intent.getStringExtra(EXTRA_CATEGORY));
            editTextDescription.setText(intent.getStringExtra(EXTRA_DESCRIPTION));
            editTextPrice.setText(intent.getStringExtra(EXTRA_PRICE));
            editTextColor.setText(intent.getStringExtra(EXTRA_COLOR));
            editTextStatus.setText(intent.getStringExtra(EXTRA_STATUS));
            editTextSize.setText(intent.getStringExtra(EXTRA_SIZE));
            editTextBrand.setText(intent.getStringExtra(EXTRA_BRAND));
            imageView.setImageURI(Uri.fromFile(new File(intent.getStringExtra(EXTRA_PIC_PATH))));
        }
        else{
            setTitle("Add Cloth");
        }
    }

    private void askCameraPermission(){
        if (ContextCompat.checkSelfPermission(AddItemActivity.this, Manifest.permission.CAMERA) +
                ContextCompat.checkSelfPermission(AddItemActivity.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) +
                ContextCompat.checkSelfPermission(AddItemActivity.this, Manifest.permission.READ_EXTERNAL_STORAGE)!= PackageManager.PERMISSION_GRANTED){

            if (ActivityCompat.shouldShowRequestPermissionRationale(AddItemActivity.this, Manifest.permission.CAMERA) ||
                    ActivityCompat.shouldShowRequestPermissionRationale(AddItemActivity.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) ||
                    ActivityCompat.shouldShowRequestPermissionRationale(AddItemActivity.this, Manifest.permission.READ_EXTERNAL_STORAGE)){
                // create alert dialog
                AlertDialog.Builder permissionBuilder = new AlertDialog.Builder(AddItemActivity.this);
                permissionBuilder.setTitle("Grant permissions");
                permissionBuilder.setMessage("Camera, Read external Storage, Write External Storage");
                permissionBuilder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        ActivityCompat.requestPermissions(AddItemActivity.this,
                                new String[]{
                                        Manifest.permission.CAMERA,
                                        Manifest.permission.WRITE_EXTERNAL_STORAGE,
                                        Manifest.permission.READ_EXTERNAL_STORAGE
                                }
                                , REQUEST_CODE
                        );
                    }
                });
                permissionBuilder.setNegativeButton("Cancel", null);
                AlertDialog alertDialog = permissionBuilder.create();
                alertDialog.show();
            }
            else{
                ActivityCompat.requestPermissions(AddItemActivity.this,
                        new String[]{
                                Manifest.permission.CAMERA,
                                Manifest.permission.WRITE_EXTERNAL_STORAGE,
                                Manifest.permission.READ_EXTERNAL_STORAGE
                        }
                        , REQUEST_CODE
                );
            }
        }
        else{
            dispatchTakePictureIntent();
        }
    }

    private void dispatchTakePictureIntent(){
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

        if (takePictureIntent.resolveActivity(getPackageManager()) != null){
            File photoFile = null;
            try{
                photoFile = createImageFile();
                Toast.makeText(this,"create image file.", Toast.LENGTH_SHORT).show();
            } catch (IOException ex){

            }

            if (photoFile != null){
                Uri photoURI = FileProvider.getUriForFile(AddItemActivity.this,
                        "com.example.clothesapptest.fileprovider",
                        photoFile);
                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                startActivityForResult(takePictureIntent, REQUEST_CODE);
            }
        }
        else{Toast.makeText(this,"fail to open camera", Toast.LENGTH_SHORT).show();}
    }

    private File createImageFile() throws IOException{
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "JPEG_" + timeStamp + "_";
        File storageDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(imageFileName,".jpg",storageDir);

        currentPhotoPath = image.getAbsolutePath();
        return image;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == REQUEST_CODE){
            if (resultCode == Activity.RESULT_OK){
                File f = new File(currentPhotoPath);
                Uri contentUri = Uri.fromFile(f);
                imageView.setImageURI(contentUri);
                imageView.invalidate();
                Log.d("tag", "absolute URI of image is " + Uri.fromFile(f));
                galleryAddPic(f);
//                editTextDescription.setText(currentPhotoPath);
                picturePath = currentPhotoPath;
            }
        }

        if (requestCode == GALLERY_REQ_CODE){
            if (resultCode == Activity.RESULT_OK){
                Uri contentUri = data.getData();
                picturePath = getGalleryPath(getApplicationContext(), contentUri);
                imageView.setImageURI(contentUri);
                Toast.makeText(getApplicationContext(), picturePath,Toast.LENGTH_LONG).show();
            }
        }
    }
    public static String getGalleryPath(Context context, Uri uri ) {
        String result = null;
        String[] proj = { MediaStore.Images.Media.DATA };
        Cursor cursor = context.getContentResolver( ).query( uri, proj, null, null, null );
        if(cursor != null){
            if ( cursor.moveToFirst( ) ) {
                int column_index = cursor.getColumnIndexOrThrow( proj[0] );
                result = cursor.getString( column_index );
            }
            cursor.close( );
        }
        if(result == null) {
            result = "Not found";
        }
        return result;
    }

    private void galleryAddPic(File f){
        Intent mediaScanIntent = new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE);
        Uri contentUri = Uri.fromFile(f);
        mediaScanIntent.setData(contentUri);
        AddItemActivity.this.sendBroadcast(mediaScanIntent);
    }

    private String getFileExt(Uri contentUri){
        ContentResolver c = getContentResolver();
        MimeTypeMap mine = MimeTypeMap.getSingleton();
        return mine.getExtensionFromMimeType(c.getType(contentUri));
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater menuInflater = getMenuInflater();
        menuInflater.inflate(R.menu.add_item_menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        switch (item.getItemId()) {
            case R.id.save_cloth:
                saveCloth();
                Toast.makeText(getApplicationContext(), "save item",Toast.LENGTH_SHORT).show();
                finish();
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }
    @Override
    public boolean onSupportNavigateUp() {
        onBackPressed();
        return true;
    }

    private void saveCloth(){
        String category = editTextCategory.getText().toString();
        String description = editTextDescription.getText().toString();
        String brand = editTextBrand.getText().toString();
        String size = editTextSize.getText().toString();
        String price = editTextPrice.getText().toString();
        String status = editTextStatus.getText().toString();
        String color = editTextColor.getText().toString();

        Intent data = new Intent();
        data.putExtra(EXTRA_CATEGORY, category);
        data.putExtra(EXTRA_DESCRIPTION, description);
        data.putExtra(EXTRA_BRAND, brand);
        data.putExtra(EXTRA_COLOR, color);
        data.putExtra(EXTRA_SIZE, size);
        data.putExtra(EXTRA_PRICE, price);
        data.putExtra(EXTRA_STATUS, status);
        data.putExtra(EXTRA_PIC_PATH, picturePath);

        int id = getIntent().getIntExtra(EXTRA_ID, -1);
        if (id != -1){
            data.putExtra(EXTRA_ID, id);
        }
        setResult(RESULT_OK, data);
        finish();
    }
}