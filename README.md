# Online Wardrobe

Welcome to the **Online Wardrobe** repository! This web application is developed using **Python**, **Django**, **HTML**, **CSS**, **JavaScript**, **AJAX**, and advanced libraries such as **scikit-learn**, **Pillow**, **NumPy**, **BodyPix (JavaScript)**, **FullCalendar (JavaScript)**, and **rembg**. The Online Wardrobe system offers a seamless and personalized wardrobe management experience, leveraging modern technologies to optimize fashion planning and outfit coordination.

---

## Key Features

### 1. **User Profile**
   - **Personalization**: Users can create personalized profiles, providing details such as:
     - **Body Measurements**: Information about body proportions.
     - **Style Preferences**: Preferences for types of outfits and styles.
     - **Introductory Message**: A short bio or introduction.
   - **Profile Image**: Users can upload an image to personalize their profile.
   - **Purpose**: This module serves as the foundation for customizing the wardrobe experience based on user preferences.

### 2. **Wardrobe Management**
   - **Add, Edit, Delete Clothing Items**: Users can manage their clothing collection by adding, editing, or deleting items.
   - **Categorization**: Clothes can be categorized into types, such as:
     - **Tops**
     - **Bottoms**
     - **Footwear**
     - **Accessories**
   - **Efficient Organization**: Simplifies outfit creation and ensures that clothing items are well-organized for easy access.

### 3. **Outfit Creation**
   - **Mix and Match**: Users can creatively combine clothing items to form stylish outfits.
   - **Smart Recommendations**: The system can suggest outfit combinations based on:
     - **Event Type**: Users specify the occasion, and the system recommends suitable ensembles.
   - **Personal Style Expression**: Encourages creativity and helps users express their fashion sense.

### 4. **Planner**
   - **Event Scheduling**: Users can plan outfits for specific events or occasions.
   - **Calendar Integration**: Add events to a calendar and assign pre-created outfits.
   - **Organized Wardrobe Planning**: Minimizes last-minute outfit decisions, ensuring users are always prepared for their engagements.

### 5. **Outfit Recommender**
   - **Real-Time Body Shape Analysis**: Uses **BodyPix (JavaScript)** for body shape scanning.
   - **Personalized Outfit Suggestions**: Analyzes body proportions and style preferences to suggest flattering outfits.
   - **Enhanced Fashion Experience**: Helps users discover looks that complement their body shape and align with their style.

### 6. **Wishlist**
   - **Save Desired Items**: Users can save recommended clothing items they wish to purchase in the future.
   - **Easy Reference**: Curate a collection of aspirational wardrobe pieces.
   - **Organized Shopping**: Enhances the shopping experience by allowing users to keep track of potential additions to their wardrobe.

---

## Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **AJAX**: For asynchronous operations and smooth user interactions
- **scikit-learn**: Used for similarity calculations (e.g., **cosine similarity**)
- **Pillow**: For image processing
- **NumPy**: For numerical operations
- **BodyPix (JavaScript)**: Real-time body shape scanning
- **FullCalendar (JavaScript)**: Interactive calendar for event scheduling
- **rembg**: Background removal from images

---

## Current Status

- **Under Study**: The system is still in the development phase and requires improvements.
- **Known Issues**: There is an error in the body shape scanner feature using BodyPix. The development team is working on refining this feature for better accuracy and user experience.

---

## Installation Guide

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/online_wardrobe.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd online_wardrobe
   ```
3. **Set Up Virtual Environment** (Optional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```
5. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
6. **Access the Web App**:
   - Open your browser and visit `http://localhost:8000`.

---

## Future Improvements

- **Fix Body Shape Scanner**: Address the known issues with BodyPix to improve body shape analysis.
- **Enhance Recommendation System**: Optimize the outfit recommender for even better personalization.
- **User Interface Enhancements**: Improve the design and user experience of the platform.
- **Community**: Add a community page where users can share their outfit ideas and socialize with one another.

---

## Contribution Guidelines

We welcome contributions to enhance the Online Wardrobe project. Please follow these steps:

1. Fork the repository and create a new branch.
2. Make your changes and test thoroughly.
3. Submit a pull request with a clear description of your enhancements or fixes.


---

Enjoy a personalized and organized wardrobe management experience with **Online Wardrobe**!
