package com.example.noiser;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.loader.content.CursorLoader;

import android.Manifest;
import android.accounts.NetworkErrorException;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.provider.MediaStore;
import android.provider.OpenableColumns;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;


public class HomeActivity extends AppCompatActivity {

    public static final int PICK_AUDIO = 100;
    int status;
    ProgressDialog dialog = null;
    Byte audio = null;
    String uploadFilePath = null;
    Uri audioUri1;
    File sourceFile = null;
    int serverResponseCode = 0;
    String apiUrl = "http://localhost:5002/api/getOutput";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
        Button btnGal = findViewById(R.id.uploadButton);
        btnGal.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                status = 0;
                openGallery();
            }
        });
    }

    private void openGallery() {
        if (Build.VERSION.SDK_INT >= 23) {
            if (checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {

            } else {
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, 3);
            }
        }
        Intent gallery = new Intent(Intent.ACTION_PICK, android.provider.MediaStore.Audio.Media.EXTERNAL_CONTENT_URI);
        startActivityForResult(gallery, PICK_AUDIO);
    }

    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (status == 0) {
            if (resultCode == RESULT_OK && requestCode == PICK_AUDIO) {
                audioUri1 = data.getData();

                postAudio();
            }
        }
    }

    private int postAudio(){
        String uriString = audioUri1.toString();
        File myAudioFile = new File(uriString);
        String displayName = null;
        String path2 = getAudioPath(audioUri1);
        File f = new File(path2);
        long fileSizeInBytes = f.length();
        long fileSizeInKB = fileSizeInBytes / 1024;
        long fileSizeInMB = fileSizeInKB / 1024;
        boolean upload_status = uploadFile(f);
//        new Handler().postDelayed(new Runnable() {
//            @Override
//            public void run() {
//                dialog.dismiss();
//                Context context = getApplicationContext();
//                CharSequence text = "Upload Success!";
//                int duration = Toast.LENGTH_SHORT;
//
//                Toast toast = Toast.makeText(context, text, duration);
//                toast.show();
//            }
//        }, 4000);

        return  0;
    }

    private boolean uploadFile(File file){
        HttpURLConnection conn = null;
        DataOutputStream dos = null;
        String lineEnd = "\r\n";
        String twoHyphens = "--";
        String boundary = "*****";
        int bytesRead, bytesAvailable, bufferSize;
        byte[] buffer;
        int maxBufferSize = 1 * 1024 * 1024;


        OutputStream os;
        FileInputStream fileInputStream = null;
        URL url = null;
        try {
            fileInputStream = new FileInputStream(file);
             url = new URL(apiUrl);
        }catch(Exception e){
            Toast.makeText(HomeActivity.this, e.getMessage().toString(),
                    Toast.LENGTH_LONG).show();
            return false;
        }

            // Open a HTTP  connection to  the URL
            try{
                conn = (HttpURLConnection) url.openConnection();
            }catch (Exception e){
                e.printStackTrace();
                Toast.makeText(HomeActivity.this, "Please Check Your Net Connection.....!",
                        Toast.LENGTH_LONG).show();
                return false;
            }

            try {
                conn.setDoInput(true); // Allow Inputs
                conn.setDoOutput(true); // Allow Outputs
                conn.setUseCaches(false); // Don't use a Cached Copy
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Connection", "Keep-Alive");
                conn.setRequestProperty("ENCTYPE", "multipart/form-data");
                conn.setRequestProperty("Content-Type", "multipart/form-data;boundary=" + boundary);
                conn.setRequestProperty("file", "test.wav");

                dos = new DataOutputStream(conn.getOutputStream());

                dos.writeBytes(twoHyphens + boundary + lineEnd);
                dos.writeBytes("Content-Disposition: form-data; name=\"uploaded_file\";filename="+ file + lineEnd);
                dos.writeBytes(lineEnd);

                // create a buffer of  maximum size
                bytesAvailable = fileInputStream.available();

                bufferSize = Math.min(bytesAvailable, maxBufferSize);
                buffer = new byte[bufferSize];

                // read file and write it into form...
                bytesRead = fileInputStream.read(buffer, 0, bufferSize);
                dialog = ProgressDialog.show(HomeActivity.this, "", "Uploading file...", true);
                while (bytesRead > 0) {

                    dos.write(buffer, 0, bufferSize);
                    bytesAvailable = fileInputStream.available();
                    bufferSize = Math.min(bytesAvailable, maxBufferSize);
                    bytesRead = fileInputStream.read(buffer, 0, bufferSize);

                }

                // send multipart form data necesssary after file data...
                dos.writeBytes(lineEnd);
                dos.writeBytes(twoHyphens + boundary + twoHyphens + lineEnd);

                // Responses from the server (code and message)
                serverResponseCode = conn.getResponseCode();
                String serverResponseMessage = conn.getResponseMessage();
                if(serverResponseCode == 200){
                    BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                    dialog.dismiss();
//                Intent intent = new Intent(this, edit.class);

                    String result = br.readLine();
                    System.out.println(result);
                    if(result == "no request"){
                        Toast.makeText(HomeActivity.this, "Server error..! try again",
                                Toast.LENGTH_SHORT).show();
                    }else{
                        dialog.dismiss();
                        runOnUiThread(new Runnable() {
                            public void run() {
                                Toast.makeText(HomeActivity.this, "File Upload Complete.",
                                        Toast.LENGTH_SHORT).show();
                            }
                        });
                    }

                }

                //close the streams //
                fileInputStream.close();
                dos.flush();
                dos.close();
                return true;
            }catch(Exception e){
                e.printStackTrace();
                Toast.makeText(HomeActivity.this, "Please Check Your Net Connection.....!",
                        Toast.LENGTH_LONG).show();
                return false;
            }

    }

    private String getAudioPath(Uri uri) {
        String[] data = {MediaStore.Audio.Media.DATA};
        CursorLoader loader = new CursorLoader(getApplicationContext(), uri, data, null, null, null);
        Cursor cursor = loader.loadInBackground();
        int column_index = cursor.getColumnIndexOrThrow(MediaStore.Audio.Media.DATA);
        cursor.moveToFirst();
        return cursor.getString(column_index);
    }
}
