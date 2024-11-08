from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
import os
import csv
from PIL import Image
from PIL import ImageOps
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.db import models
from django.conf import settings
from datetime import datetime


# Create your models here.
class UserAccount(models.Model):
    username = models.CharField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    isVerified = models.BooleanField(default=False)
    code = models.CharField(max_length=255, null=True, default=None)
    date_joined = models.DateTimeField(default=timezone.now)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__ (self):
        return f"{self.id} : {self.username}"
    
class ItemColor(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, default=False)

    def __str__(self):
        return self.name

class ItemStyle(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.name 

class ItemCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.name

class ItemSubcategory(models.Model):
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return f"{self.category} : {self.name}"
    
class BodyShape(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=255)
    bio = models.TextField(max_length=500)
    profilepic = models.ImageField(upload_to="profpic/", default="profpic/default_userpic.png")
    birthdate = models.DateField(null=False)
    height = models.IntegerField()
    weight = models.IntegerField()
    body_shape = models.ForeignKey(BodyShape, on_delete=models.CASCADE)
    pref_color = models.ManyToManyField(ItemColor, blank=True)
    pref_style = models.ManyToManyField(ItemStyle, blank=True)
    pref_genderedstyle = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.id} : {self.user} : {self.name}"
    

class FashionItem(models.Model):
    outfit_name = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=100, null=True)
    subcategory = models.CharField(max_length=100, null=True)
    size = models.CharField(max_length=50, null=True)
    body_shape = models.CharField(max_length=50, null=True)
    color = models.CharField(max_length=50, null=True)
    style = models.CharField(max_length=100, null=True)
    gendered = models.CharField(max_length=100, null=True)
    brand = models.CharField(max_length=100, null=True)
    item_link = models.CharField(max_length=1000, null=True)
    original_image = models.ImageField(upload_to='fashion_data/', null=True)


    def __str__(self):
        return f"{self.id} {self.outfit_name} - Category: {self.category}"

    @classmethod
    def load_fashion_dataset(cls):
        csv_file = 'fashion_dataset/annotations.csv'
        images_folder = 'fashion_dataset/'

        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            counter = 1
            for row in reader:
                # Get image path and category
                image_path = os.path.join(images_folder, row['image_path'])

                # Check if a FashionItem with the same attributes already exists
                if not cls.objects.filter(
                    outfit_name=row['outfit_name'],
                    category=row['category'],
                    subcategory=row['subcategory'],
                    size=row['size'],
                    body_shape=row['body_shape'],
                    color=row['color'],
                    style=row['style'],
                    gendered=row['gendered'],
                    brand=row['brand'],
                    item_link=row['item_link'],
                ).exists():
                    # Open and save original image
                    img = Image.open(image_path)
                    img_path_original = os.path.join('fashion_data', f'{counter}_{row["outfit_name"]}_original.png')
                    img.save(os.path.join(settings.MEDIA_ROOT, img_path_original))

                    # Save FashionItem instance
                    cls.objects.create(
                        outfit_name=row['outfit_name'],
                        category=row['category'],
                        subcategory=row['subcategory'],
                        size=row['size'],
                        body_shape=row['body_shape'],
                        color=row['color'],
                        style=row['style'],
                        gendered=row['gendered'],
                        brand=row['brand'],
                        item_link=row['item_link'],
                        original_image=img_path_original,
                    )
                counter += 1

    @staticmethod
    def flatten_image(img_array):
        img = Image.fromarray(img_array.astype('uint8'))
        img = img.resize((28, 28))
        img_array = np.array(img) / 255.0
        return img_array.flatten()

    @staticmethod
    def calculate_cosine_similarity(item1, item2):
        # Load images and flatten them
        img1 = Image.open(item1.original_image.path)
        img2 = Image.open(item2.original_image.path)
        
        # Resize images to the same dimensions
        img1 = img1.resize((28, 28))
        img2 = img2.resize((28, 28))
        
        img_array1 = np.array(img1).flatten()
        img_array2 = np.array(img2).flatten()

        # Reshape to 1D array and calculate cosine similarity
        img_array1 = img_array1.reshape(1, -1)
        img_array2 = img_array2.reshape(1, -1)
        similarity = cosine_similarity(img_array1, img_array2)[0][0]

        return similarity


    def get_recommendations(self):
        # Get all other FashionItems excluding self
        all_items = FashionItem.objects.exclude(pk=self.pk).filter(category=self.category)

        # Calculate cosine similarity for each item
        similarities = [(item, self.calculate_cosine_similarity(self, item), item.category) for item in all_items]

        # Sort by similarity in descending order
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top N recommendations (e.g., top 5)
        top_recommendations = similarities[:3]

        return top_recommendations
    
class UserItem(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False)
    outfit_name = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, null=False)
    subcategory = models.ForeignKey(ItemSubcategory, on_delete=models.CASCADE, null=False)
    # size = models.CharField(max_length=50, null=True)
    # body_shape = models.ForeignKey(BodyShape, on_delete=models.CASCADE, null=False)
    color = models.ForeignKey(ItemColor, on_delete=models.CASCADE, null=False)
    style = models.ManyToManyField(ItemStyle, blank=True)
    gendered = models.CharField(max_length=100, null=True)
    desc = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='user_items/', null=True)
    datetime = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.id} : {self.user} : {self.outfit_name}"
    
    def calculate_cosine_similarity(self, item):
        # Load and resize images
        img1 = Image.open(self.image.path)
        img2 = Image.open(item.original_image.path)
        img1_resized = img1.resize((28, 28)).convert('L')  # Resize and convert img1 to grayscale
        img2_resized = img2.resize((28, 28)).convert('L')  # Resize and convert img2 to grayscale

        # Ensure both images have the same mode and dimensions
        img1_resized = img1_resized.convert('RGB')
        img2_resized = img2_resized.convert('RGB')

        # Flatten resized images
        img_array1 = np.array(img1_resized).flatten()
        img_array2 = np.array(img2_resized).flatten()

        # Reshape to 1D array and calculate cosine similarity
        img_array1 = img_array1.reshape(1, -1)
        img_array2 = img_array2.reshape(1, -1)
        
        # Ensure the data type is float32
        img_array1 = img_array1.astype('float32')
        img_array2 = img_array2.astype('float32')

        similarity = cosine_similarity(img_array1, img_array2)[0][0]

        return similarity


    def get_recommendations(self):
        
        # Get all FashionItems within the same category as the UserItem
        all_fashion_items = FashionItem.objects.filter(category__iexact=self.category)

        # Calculate cosine similarity for each item
        similarities = [(item, self.calculate_cosine_similarity(item), item.category) for item in all_fashion_items]

        # Sort by similarity in descending order
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top N recommendations (e.g., top 3)
        top_recommendations = similarities[:3]

        return top_recommendations


class UserOutfit(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False) 
    outfit_name = models.CharField(max_length=255, null=False)
    desc = models.TextField(max_length=500, null=True, blank=True)
    top = models.ForeignKey(UserItem, on_delete=models.CASCADE, null=False, related_name='top_outfits')
    bottom = models.ForeignKey(UserItem, on_delete=models.CASCADE, null=True, related_name='bottom_outfits')
    footwear = models.ForeignKey(UserItem, on_delete=models.CASCADE, null=False, related_name='footwear_outfits')
    outerwear = models.ForeignKey(UserItem, on_delete=models.CASCADE, null=True, blank=True, related_name='outerwear_outfits')
    dress = models.ForeignKey(UserItem, on_delete=models.CASCADE, null=True, blank=True, related_name='dress_outfits')
    accessories = models.ManyToManyField(UserItem, blank=True) 
    datetime = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user} : {self.outfit_name}"


class OutfitPlan(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False) 
    user_outfit = models.ManyToManyField(UserOutfit, blank=True) 
    event_name = models.CharField(max_length=255,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"{self.id} : {self.user} : {self.user_outfit} for {self.event_name}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False)
    item = models.ForeignKey(FashionItem, on_delete=models.CASCADE, null=False)
    datetime = models.DateTimeField(default=datetime.now) 

    def __str__(self):
        return f"{self.user} : {self.item}"

class UserPost(models.Model):
    writer = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False)
    title = models.TextField(max_length=50, null=True, blank=True)
    content = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='user_post/')
    user_outfit = models.ForeignKey(UserOutfit, on_delete=models.CASCADE, null=False)
    datetime = models.DateTimeField(default=datetime.now) 

    def __str__(self):
        return f"{self.user} : {self.title}"
    
class UserLike(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False)
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE, null=False)
    datetime = models.DateTimeField(default=datetime.now) 

    def __str__(self):
        return f"{self.user} : {self.user_post}"
    
class UserComment(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False)
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE, null=False)
    content = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='user_post/')
    datetime = models.DateTimeField(default=datetime.now) 

    def __str__(self):
        return f"{self.user} : {self.user_post}"
    
class UserReply(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False)
    user_comment = models.ForeignKey(UserComment, on_delete=models.CASCADE, null=False)
    content = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='user_post/')
    datetime = models.DateTimeField(default=datetime.now) 

    def __str__(self):
        return f"{self.user} : {self.user_comment.user_post} : {self.user_comment}"

