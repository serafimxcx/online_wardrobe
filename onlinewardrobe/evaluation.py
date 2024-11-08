import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinewardrobe.settings')

# Configure Django
django.setup()

from sklearn.metrics import mean_squared_error, mean_absolute_error
from wardrobe.models import UserItem, FashionItem

# Retrieve all user items from your dataset
# user_items = UserItem.objects.get(pk='19')
# user_items = UserItem.objects.get(pk='3')
# user_items = UserItem.objects.get(pk='16')
# user_items = UserItem.objects.get(pk='32')
# user_items = UserItem.objects.get(pk='29')
user_items = UserItem.objects.get(pk='28')

predictions = []
actual_similarities = []

# Get recommendations for the current user item
recommendations = FashionItem.objects.filter(category__iexact=user_items.category)

predictions = [0.8, 0.9, 1.0] 

for recommendation in recommendations:
    # Calculate the similarity between the user item and each recommended fashion item
    actual_similarity = UserItem.calculate_cosine_similarity(user_items, recommendation)
    
    actual_similarities.append(actual_similarity)

# Limit actual_similarities to the first four elements
actual_similarities.sort(reverse=True)
actual_similarities = actual_similarities[:3]

# Calculate Mean Squared Error and Mean Absolute Error
mse = mean_squared_error(actual_similarities, predictions)
mae = mean_absolute_error(actual_similarities, predictions)


print("Predictions: ", predictions)
print("Actual Similarities: ", actual_similarities)
print("Mean Squared Error:", mse)
print("Mean Absolute Error:", mae)
