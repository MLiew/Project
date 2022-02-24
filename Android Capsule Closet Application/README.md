# Capsule Closet Android Application
This is a course project for the course "Object-oriented Programming" of Beihang University in the year of 2020.  

## Introduction
This is an Android application named “Capsule Closet”. It is developed to keep track the items we have in the closet. By having a good grasp of the closet situation, users are able to purchase clothes rationally, and hence reduce their desire for trendy clothes.  

<p float="left">
  <img src="https://user-images.githubusercontent.com/30465494/155460085-e7d805a2-a653-450a-a95f-1f7f044afe6e.jpg" width="200" />
  <img src="https://user-images.githubusercontent.com/30465494/155460495-fcf00a19-d269-4e40-b878-3d1d4c87fc4f.jpg" width="200" /> 
  <img src="https://user-images.githubusercontent.com/30465494/155460611-d2a10f7f-fe99-4de5-b365-a664d7570b1e.jpg" width="200" />
</p>

Find the code of all classes in the folder of `Android Capsule Closet Application/app/src/main/java/com/example/clothesapptest`.  
<br>

<b>Software development requirement: </b>
- Android studio version: 4.1
- Operating System: Windows 10, intel i5
- RAM: 12 GB
- Testing phone: OPPO A31 (version 2020) and VIVO Y91

## Application design
### 1. Functional design
The application aims to allow user to keep track of their closet situation. The main function that this android application is mentioned in the user requirement section. Figure 1 is the diagram of the main function of the android application. 
![image](https://user-images.githubusercontent.com/30465494/155454464-4a47446d-d5e1-49e5-b633-7e7a34fa5830.png)

### 2. Database design
The application is designed to save user’s upload date into phone’s local database, hence Room Database is selected in this project. The basic structure of the database are a database, an entity, a DAO, a repository, a View Model, an adapter and a main activity or fragment.
Following are the main classes that are used in designing application’s database:
1) `Cloth entity`: a basic object which is a “cloth” item, defining the properties of a cloth object should have. The entity also represents a table in the database.
2) `Cloth Database`: having the Cloth entity as an entity.
3) `ClothDao`: which is an interface that help to access the database with save, update, delete and other SQL query method.
4) `ClothRepository`: manages query threads and allows multiple backends to be used, providing a clean API to the rest of the app for app data.
5) `View Model`: is created for every fragments, which provide data to the UI and survive configuration changes. It acts as a communication center between the repository and the UI, responsible for holding and processing all the data needed for the UI. In the View Model, Live Data is used for changeable data that the UI will use or display.
6) `Adapter`: binds the data provided by the view model to the fragment or activity UI.

The UML class diagram is as follow:  
![CapsuleClosetApp3](https://user-images.githubusercontent.com/30465494/155454810-35ccbfca-7efa-46a0-a4ae-629c6c54bbe7.png)

### 3. Structural design
This android application consists of three fragments, which are home fragment, collection fragment and user fragment. In the main activity, by using navigation component provided by android Jetpack, pressing on the bottom navigation menu button will navigate the user to the corresponding fragment.
1. `Home fragment`: the existing categories name and amount of items in specific category is displayed. By clicking on certain category, it will navigate the user to another activity (CategoryItemActivity.java), showing all the items in the same category. 
2. `CategoryItemActivity class`: items can be deleted by swiping the item left or right. Besides that, clicking the item’s card view enable the user to check and edit the items’ details in another activity, which is AddItemActivity class.
3. `Collection fragment`: every items that are added into the database is shown. There is a floating action button that allows user to add new item, opening the AddItemActivity class. After adding a new item, the item will instantly appear in the collection fragment. In the same fragment, user is allowed to delete an item by swiping it left or right, editing and checking the details of added items.
4. `User fragment`: the user’s details such as profile picture is displayed. To add on, some statistical data from the database is planned to be display in this fragment, e.g. total number of items.
5. `AddItemActivity class`: item’s properties are recorded and save into the room database. Camera, read and write external storage permissions are needed to retrieve item’s image. User can take picture of an item or choose an image from the phone’s gallery. Apart from allowing the user to input the item’s details, several alert dialog boxes are used for the user to choose the input. After clicking the save button on the upper-right direction, the item can be saved, or if the back button is pressed, then the activity will be discarded.
6. `CategoryItemActivity class`: the items in the selected category are displayed. User can delete certain item and also check or edit its properties. To check or edit the item’s attributes, clicking on the item’s card view will navigate the user to AddItemActivity class.   
![image](https://user-images.githubusercontent.com/30465494/155455519-9cfb8105-5c72-4f00-b017-55ef5bdda98e.png)

## Implementation
1. In collection fragment, press the “+” floating action button to open AddItemActivity, as shown in Figure 4(a).
2. In AddItemActivity, if it is the first time the user wanted to take a picture, pressing the “camera” image button will prompt the user to allow camera, write and read permissions to the application, as shown in Figure 4(b). User can either choose to take a picture from camera or choose an image from the gallery to be uploaded to the database.
3. Fill in the attributes of the item in respective data input rows. At the category, color, and status row, alert dialog box is popped up for the user to choose limited option, as shown in Figure 4(c). Next, save the item or discard.
4. After saving the item, the item will be displayed in the collection fragment. At the same time, in the home fragment, the quantity of the item added will increase by one, under the specific category row, as shown in Figure 4(d).
5. Also in the collection fragment, if the user wants to delete certain item, he only has to swipe the item left or right, as shown in Figure 4(e). Otherwise, if the user wanted to edit or check the item, he only has to click on the item, the application will navigate the user to the Edit Activity, as shown in Figure 4(f).
6. Press on the “Home” button at the bottom navigation menu. In the home fragment, the quantity of items in each category is clearly stated, which means that the user can have a clear vision of the total number of items he owns. In Figure 4(g), the user can click on certain category, it will direct him to the CategoryItemActivity.
7. The user can then see the all the pieces in the same category in CategoryItemActivity, as shown in Figure 4(h). The operations that a user can do are the same as in collection fragment, such as editing or deleting an item.
8. In the user fragment, the user is able to see his profile picture and other statistics, such as all the brands, prices and so on, as shown in Figure 4(i).  

![image](https://user-images.githubusercontent.com/30465494/155459897-05ebd0e3-15cd-4a74-aedc-ccb2791197cd.png)
![image](https://user-images.githubusercontent.com/30465494/155459985-d2a85dc1-fcee-4068-afc2-76a8108a52f7.png)
![image](https://user-images.githubusercontent.com/30465494/155460033-77934690-2d6e-41c2-801a-6d659bef334b.png)


