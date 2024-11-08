from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import UserAccount, UserProfile, BodyShape, ItemColor, ItemStyle, FashionItem, ItemSubcategory, ItemCategory, UserItem, UserOutfit, OutfitPlan, Wishlist
from django.contrib import messages
import random
from django.utils import timezone
import os
import tempfile
from PIL import Image as PILImage
from rembg import remove
from datetime import timedelta
from django.conf import settings
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from random import choice, randint
from django.core.mail import send_mail
import random
import string
from django.core.mail import EmailMultiAlternatives

MESSAGE_DURATION = timedelta(seconds=5)

# Create your views here.
def generate_verification_code(email, length=6):
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not UserAccount.objects.filter(code=code, email=email).exists():
            break
    return code

def index(request):
    if 'fashion_user_id' in request.session and request.session['fashion_user_id']:
        user_id = request.session['fashion_user_id']
        userprofile_exist = UserProfile.objects.filter(user=user_id).exists()

        if userprofile_exist:
            userprofile = UserProfile.objects.filter(user=user_id)
            profile = UserProfile.objects.get(user=user_id)
            current_date = timezone.now()

            preference_styles = []
            for style in profile.pref_style.all():
                preference_styles.append(style)

            random.shuffle(preference_styles)

            recommended_outfits = []
            outfit_ids = set()

            pref_genderedstyle = profile.pref_genderedstyle

            pref_genderedstyle_list = [style.strip(" '").lower() for style in pref_genderedstyle.strip("[]").split(',')]
        
            
            for style in preference_styles:
                outfits = FashionItem.objects.filter(style__icontains=style, gendered__in=pref_genderedstyle_list)
                if outfits:
                    outfit = random.choice(outfits)
                    if outfit.id not in outfit_ids: 
                        recommended_outfits.append(outfit)
                        outfit_ids.add(outfit.id)
                        if len(recommended_outfits) >= 3:
                            break
            
            outfits = UserOutfit.objects.filter(user=user_id)

            all_events = OutfitPlan.objects.filter(
                Q(user=user_id, start__lte=current_date, end__gt=current_date) |
                Q(user=user_id, start__date=current_date.date(), end__date=current_date.date())
            )

            print(current_date)

            out = []

            for event in all_events:
                outfit_details_list = []
                for outfit in event.user_outfit.all():
                    outfit_details = {
                        'id': outfit.id,
                        'outfit_name': outfit.outfit_name,
                        'desc': outfit.desc,
                        'top': {
                            'image': outfit.top.image.url if outfit.top else None,
                        },
                        'bottom': {
                            'image': outfit.bottom.image.url if outfit.bottom else None,
                        },
                        'footwear': {
                            'image': outfit.footwear.image.url if outfit.footwear else None,
                        },
                        'outerwear': {
                            'image': outfit.outerwear.image.url if outfit.outerwear else None,
                        },
                    }
                    outfit_details_list.append(outfit_details)

                out.append({
                    'event_name': event.event_name,
                    'start': event.start,
                    'end': event.end,
                    'outfits': outfit_details_list
                })

            return render(request, "wardrobe/index.html", {
                "userprofile": userprofile,
                "recommended_outfits": recommended_outfits,
                "outfits": outfits,
                "events": out,
                
            })
        else:
            bodyshapes = BodyShape.objects.all()
            color_options = ItemColor.objects.all().order_by('name')
            style_options = ItemStyle.objects.all()
            return render(request, "wardrobe/setupprofile.html", {
                "bodyshapes": bodyshapes,
                "colors": color_options,
                "styles": style_options,
            })
        
        
    else:
        return render(request, "wardrobe/login.html", {
            "message": "Please login your account."
        })

def verify_account(request):
    if request.method == "POST":
        username = request.POST["txt_username"]
        code = request.POST["txt_code"]

        try:
            user = UserAccount.objects.get(username=username)
        except UserAccount.DoesNotExist:
            return render(request, "wardrobe/verify.html", {
                "message": "Invalid Credential. Username does not exist."
            })
        
        if code.strip() == user.code:
            user.isVerified = True
            user.save()

            return render(request, "wardrobe/login.html", {
                "message": "Account Verified Successfully. You can now login your account."
            })
            
        else:
            return render(request, "wardrobe/verify.html", {
                "message": "Invalid Verification Code. Please check your code in the email."
            })

    else:
        return render(request, "wardrobe/verify.html")
        

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = UserAccount.objects.get(username=username)
        except UserAccount.DoesNotExist:
            return render(request, "wardrobe/login.html", {
                "message": "Invalid Credential. Username does not exist."
            })
        
        if user.isVerified == True:
            if check_password(password, user.password):
                # Authentication successful, store user ID in session
                request.session['fashion_user_id'] = user.pk
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "wardrobe/login.html", {
                    "message": "Invalid Credential. Wrong password."
                })
        else:
            return render(request, "wardrobe/login.html", {
                    "message": "Account not verified."
                })

    else:
        return render(request, "wardrobe/login.html")

def logout(request):
    if 'fashion_user_id' in request.session:
        del request.session['fashion_user_id']
        return render(request, "wardrobe/login.html", {
            "message": "Logout successfully."
        })
    else:
        return render(request, "wardrobe/login.html", {
            "message": "You are not logged in."
        })

def register_view(request):
    if request.method == "POST":
        username = request.POST["reg_username"]
        email = request.POST["reg_email"]

        # Ensure password matches confirmation
        password = request.POST["reg_password1"]
        confirmation = request.POST["reg_password2"]
        if password != confirmation:
            return render(request, "wardrobe/register.html", {
                "message": "Registration failed. Passwords must match."
            })
        
        try:
            verification_code = generate_verification_code(email)
            user = UserAccount(username=username, email=email, code=verification_code)
            user.set_password(password)
            user.save()

            subject = 'FashionFolio - Account Verification'
            html_content = f'<p>Your verification code is <strong>{verification_code}</strong>.</p><p>Click <a href="http://127.0.0.1:8000/verify_account">here</a> to verify your email.</p>'
            email_from = 'coronado.webhost01@gmail.com'
            recipient_list = [email]

            msg = EmailMultiAlternatives(subject, '', email_from, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()


        except IntegrityError:
            return render(request, "wardrobe/register.html", {
                "message": "Registration failed. Username already taken."
            })
        
        return render(request, "wardrobe/login.html", {
            "message": "Account created successfully. Please check your email to verify your account."
        })
        
    else:
        return render(request, "wardrobe/register.html")
    
def setup_profile(request):
    if not 'fashion_user_id' in request.session:
        return render(request, "wardrobe/login.html", {
            "message": "Please login your account."
        })
    else:
        if request.method == "POST":
            name = request.POST.get("txt_name")
            bio = request.POST.get("txt_bio")
            profilepic = request.FILES.get("img_profile")
            birthdate = request.POST.get("txt_birthdate")
            height = request.POST.get("txt_height")
            weight = request.POST.get("txt_weight")
            selected_bodyshape = request.POST.get("slct_bodyshape")
            body_shape = BodyShape.objects.get(name=selected_bodyshape)
            pref_colors = request.POST.getlist("slct_color")
            pref_styles = request.POST.getlist("slct_style")
            pref_genderedstyles = request.POST.getlist("slct_genderedstyle")
            

            user_id = request.session.get("fashion_user_id")
            user = UserAccount.objects.get(id=user_id)

            user_profile = UserProfile.objects.create(
                user=user,
                name=name,
                bio=bio,
                profilepic=profilepic,
                birthdate=birthdate,
                height=height,
                weight=weight,
                body_shape=body_shape,
                pref_genderedstyle=pref_genderedstyles
            )

            user_profile.pref_color.add(*pref_colors)
            user_profile.pref_style.add(*pref_styles)


            return HttpResponseRedirect(reverse('index'))

def profile(request):
    if 'fashion_user_id' in request.session and request.session['fashion_user_id']:
        user_id = request.session['fashion_user_id']
        user = UserAccount.objects.get(id=user_id)
        userprofile_exist = UserProfile.objects.filter(user=user_id).exists()
        

        if userprofile_exist:
            userprofile = UserProfile.objects.filter(user=user_id)
            profile = UserProfile.objects.get(user=user_id)
            pref_genderedstyle = profile.pref_genderedstyle
            wishlist = Wishlist.objects.filter(user=user_id)
            bodyshapes = BodyShape.objects.all()
            color_options = ItemColor.objects.all().order_by('name')
            style_options = ItemStyle.objects.all()

            pref_genderedstyle_list = [style.strip(" '") for style in pref_genderedstyle.strip("[]").split(',')]
            return render(request, "wardrobe/profile.html", {
                "userprofile": userprofile,
                "pref_genderedstyles": pref_genderedstyle_list,
                "wishlist": wishlist,
                "bodyshapes": bodyshapes,
                "colors": color_options,
                "styles": style_options,
            })
        else:
            bodyshapes = BodyShape.objects.all()
            color_options = ItemColor.objects.all().order_by('name')
            style_options = ItemStyle.objects.all()
            return render(request, "wardrobe/setupprofile.html", {
                "bodyshapes": bodyshapes,
                "colors": color_options,
                "styles": style_options,
            })

def update_profile(request):
    if request.method == "POST":
        name = request.POST.get("txt_updatename")
        bio = request.POST.get("txt_updatebio")
        profilepic = request.FILES.get("img_profile")
        height = request.POST.get("txt_updateheight")
        weight = request.POST.get("txt_updateweight")
        selected_bodyshape = request.POST.get("slct_updatebody")
        body_shape = BodyShape.objects.get(name=selected_bodyshape)
        pref_colors = request.POST.getlist("slct_updatecolor")
        pref_styles = request.POST.getlist("slct_updatestyle")
        pref_genderedstyles = request.POST.getlist("slct_updategenderedstyle")

        user_id = request.session.get("fashion_user_id")
        user = UserAccount.objects.get(id=user_id)

        user_profile = UserProfile.objects.get(user=user)

        # Update the fields of the user profile
        user_profile.name = name
        user_profile.bio = bio
        if profilepic:
            user_profile.profilepic = profilepic
        user_profile.height = height
        user_profile.weight = weight
        user_profile.body_shape = body_shape

        # Update preferences
        user_profile.pref_genderedstyle = pref_genderedstyles

        # Save the user profile
        user_profile.save()

        # Clear existing preferences before adding the new ones
        user_profile.pref_color.clear()
        user_profile.pref_style.clear()

        user_profile.pref_color.add(*pref_colors)
        user_profile.pref_style.add(*pref_styles)

        messages.success(request, 'Profile Updated Successfully')
        return HttpResponseRedirect(reverse("profile"))
        
def item_detail(request, item_id):
    # Retrieve the FashionItem instance
    item = get_object_or_404(FashionItem, pk=item_id)
    user_id = request.session['fashion_user_id']
    user = UserAccount.objects.get(pk=user_id)

    in_wishlist = False

    if Wishlist.objects.filter(user=user, item=item).exists():
        in_wishlist = True

    # Get recommendations using the recommendation logic
    recommendations = item.get_recommendations()

    recommendations = [(recommendation, similarity * 100, label_name) for recommendation, similarity, label_name in recommendations]

    # Pass the item, category name, and recommendations to the template
    return render(request, 'wardrobe/item_detail.html', {
        'item': item, 
        'category_name': item.category, 
        'recommendations': recommendations,
        'in_wishlist': in_wishlist,
    })

def wardrobe(request, category):
    if 'fashion_user_id' in request.session and request.session['fashion_user_id']:
        user_id = request.session['fashion_user_id']
        userprofile_exist = UserProfile.objects.filter(user=user_id).exists()

        if userprofile_exist:
            userprofile = UserProfile.objects.filter(user=user_id)
            if category == 'all':
                subcategory = ItemSubcategory.objects.all()
            else:
                subcategory = ItemSubcategory.objects.filter(category__name__iexact=category)
            bodyshapes = BodyShape.objects.all()
            colors = ItemColor.objects.all().order_by('name')
            style_options = ItemStyle.objects.all()

            if category == "all":
                wardrobe = UserItem.objects.filter(user=user_id).order_by('-datetime')
            else:
                wardrobe = UserItem.objects.filter(user=user_id, category__name__iexact=category).order_by('-datetime')

            return render(request, "wardrobe/wardrobe.html", {
                "category": category,
                "userprofile": userprofile,
                "subcategories": subcategory,
                "bodyshapes": bodyshapes,
                "colors": colors,
                "styles": style_options,
                "wardrobe": wardrobe,
                
            })
        else:
            bodyshapes = BodyShape.objects.all()
            color_options = ItemColor.objects.all().order_by('name')
            style_options = ItemStyle.objects.all()
            return render(request, "wardrobe/setupprofile.html", {
                "bodyshapes": bodyshapes,
                "colors": color_options,
                "styles": style_options,
            })
    
    
    else:
        return render(request, "wardrobe/login.html", {
            "message": "Please login your account."
        })

def add_item(request, category):
    if request.method == 'POST' and request.FILES.get('outfit_image'):
        user_id = request.session['fashion_user_id']
        user = UserAccount.objects.get(id=user_id)
        image = request.FILES.get("outfit_image")
        outfit_name = request.POST.get("txt_outfitname")
        selected_category = ItemCategory.objects.get(name__iexact=category)
        selected_subcategory_name = request.POST.get("slct_subcategory")
        selected_subcategory = ItemSubcategory.objects.get(name__iexact=selected_subcategory_name)
        # size = request.POST.get("txt_size")
        # selected_bodyshape_name = request.POST.get("slct_bodyshape")
        # selected_bodyshape = BodyShape.objects.get(name__iexact=selected_bodyshape_name)
        selected_color_name = request.POST.get("slct_color")
        selected_color = ItemColor.objects.get(name__iexact=selected_color_name)

        style = request.POST.getlist("slct_style")
        gendered_style = request.POST.get("slct_genderedstyle")
        desc = request.POST.get("txt_desc")

        file_extension = os.path.splitext(image.name)[1].lower()

        if file_extension in ['.png', '.jpeg', '.jpg']:
            item_instance = UserItem.objects.create(
                user=user,
                outfit_name=outfit_name,
                category=selected_category,
                subcategory=selected_subcategory,
                color=selected_color,
                desc=desc,
                gendered=gendered_style,
                image=image,
            )

            item_instance.style.add(*style)

            if file_extension not in ['.png']:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    with open(item_instance.image.path, "rb") as f:
                        img = PILImage.open(f)
                        img = img.convert("RGB")
                        img = remove(img)
                        img.save(temp_file, format='PNG')
                    
                    temp_file.close()

                    filename_without_extension = os.path.splitext(os.path.basename(image.name))[0]

                    with open(temp_file.name, 'rb') as processed_file:
                        item_instance.image.save(
                            filename_without_extension + '.png',  
                            processed_file,
                            save=True
                        )

                original_photo_path = os.path.join(settings.MEDIA_ROOT, 'user_items', os.path.basename(image.name))
                os.remove(original_photo_path)

            messages.success(request, 'Item Added Successfully')
            return HttpResponseRedirect(reverse("wardrobe", args=(category,)))
        else:
            messages.success(request, 'Unsupported File Format')
            return HttpResponseRedirect(reverse("wardrobe", args=(category,)))

        
def remove_item(request, category):
    if request.method == "POST":
        item_id = request.POST.get("txt_del_item_id")
        user_item = UserItem.objects.get(pk=item_id)

        user_item.delete()
        messages.success(request, 'Item Deleted Successfully')
        return HttpResponseRedirect(reverse("wardrobe", args=(category,)))

def get_item(request, item_id):
    try:
        item = UserItem.objects.get(id=item_id)
        # Convert item data to JSON format
        subcategories = ItemSubcategory.objects.filter(category__name__iexact=item.category.name)
        subcategories_data = serializers.serialize('json', subcategories)
        styles = [style.id for style in item.style.all()]
        item_data = {
            'outfit_name': item.outfit_name,
            'subcategory': item.subcategory.name,
            'subcategories_optn': subcategories_data,
            'color': item.color.name,
            'image': item.image.url,
            'gendered_style': item.gendered,
            'styles':styles,
            'desc': item.desc,
        }
        return JsonResponse(item_data)
    except UserItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    
def edit_item(request, category):
    if request.method == "POST":
        item_id = request.POST.get("txt_item_id")
        item_record = UserItem.objects.get(pk=item_id)
        selected_subcategory_name = request.POST.get("slct_subcategory")
        selected_subcategory = ItemSubcategory.objects.get(name__iexact=selected_subcategory_name)
        selected_color_name = request.POST.get("slct_color")
        selected_color = ItemColor.objects.get(name__iexact=selected_color_name)
        selected_styles = request.POST.getlist("slct_style")

        item_record.outfit_name = request.POST.get("txt_outfitname")
        item_record.subcategory = selected_subcategory
        item_record.color = selected_color
        item_record.gendered = request.POST.get("slct_genderedstyle")
        item_record.desc = request.POST.get("txt_desc")
        item_record.style.clear()
        item_record.style.add(*selected_styles)

        if 'outfit_image' in request.FILES:
            image = request.FILES.get("outfit_image")

            file_extension = os.path.splitext(image.name)[1].lower()

            if file_extension in ['.jpeg', '.jpg', '.png']:
                item_record.image = image
                
                item_record.save()
                
                if file_extension != '.png':
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        with open(item_record.image.path, "rb") as f:
                            img = PILImage.open(f)
                            img = img.convert("RGB")
                            img.save(temp_file, format='PNG')
                    
                    # Assign the processed image back to the item_instance
                    filename_without_extension = os.path.splitext(os.path.basename(image.name))[0]
                    with open(temp_file.name, 'rb') as processed_file:
                        item_record.image.save(
                            filename_without_extension + '.png',
                            processed_file,
                            save=True
                        )
                    os.remove(temp_file.name)  
            else:
                messages.success(request, 'Unsupported File Format')
                return HttpResponseRedirect(reverse("wardrobe", args=(category,)))
        
        item_record.save()
        messages.success(request, 'Item Edited Successfully')
        return HttpResponseRedirect(reverse("wardrobe", args=(category,)))

def outfit_creation(request):
    if 'fashion_user_id' in request.session and request.session['fashion_user_id']:
        user_id = request.session['fashion_user_id']
        userprofile_exist = UserProfile.objects.filter(user=user_id).exists()

        if userprofile_exist:
            userprofile = UserProfile.objects.filter(user=user_id)
            outfits = UserOutfit.objects.filter(user=user_id)
            tops = UserItem.objects.filter(Q(category__name__in=['Top', 'Dress', ]) | Q(subcategory__name__in=['Cocktail Dress', 'Evening Gown']),
                user=user_id
            )
            bottoms = UserItem.objects.filter(category__name='Bottom', user=user_id)
            footwears = UserItem.objects.filter(category__name='Footwear', user=user_id)
            outerwears = UserItem.objects.filter(
                Q(category__name='Outerwear') | Q(subcategory__name__in=['Suit', 'Tuxedo']),
                user=user_id
            )
            dresses = UserItem.objects.filter(
                Q(category__name='Dress') | Q(subcategory__name__in=['Cocktail Dress', 'Evening Gown']),
                user=user_id
            )
            accessories = UserItem.objects.filter(category__name='Accessory', user=user_id)


            return render(request, "wardrobe/outfit_creation.html", {
                "userprofile": userprofile,
                "tops": tops,
                "bottoms": bottoms,
                "footwears":footwears,
                "outerwears": outerwears,
                "dresses": dresses,
                "accessories": accessories,
                "outfits": outfits,
            })
        else:
            bodyshapes = BodyShape.objects.all()
            color_options = ItemColor.objects.all().order_by('name')
            style_options = ItemStyle.objects.all()
            return render(request, "wardrobe/setupprofile.html", {
                "bodyshapes": bodyshapes,
                "colors": color_options,
                "styles": style_options,
            })
    
    
    else:
        return render(request, "wardrobe/login.html", {
            "message": "Please login your account."
        })
    
def add_outfit(request):
    if request.method == "POST":
        user_id = request.session['fashion_user_id']
        user = UserAccount.objects.get(id=user_id)
        outfit_name = request.POST.get("txt_outfitname")
        desc = request.POST.get("txt_desc")
        top_id = request.POST.get("c_top")
        top = UserItem.objects.get(id=top_id)
        bottom_id = request.POST.get("c_bottom")
        
        footwear_id = request.POST.get("c_footwear")
        footwear = UserItem.objects.get(id=footwear_id)
        outerwear_id = request.POST.get("c_outerwear")
        accessory_ids = request.POST.get("c_accessory", None) 

        outerwear = None 
        bottom = None
        accessories = None

        if outerwear_id:
            outerwear = UserItem.objects.get(id=outerwear_id)

        if bottom_id:
            bottom = UserItem.objects.get(id=bottom_id)

        outfit_instance = UserOutfit(
            user=user,
            outfit_name=outfit_name,
            desc=desc,
            top=top,
            bottom=bottom,
            footwear=footwear,
            outerwear=outerwear 
        )

        outfit_instance.save()

        if accessory_ids:
            accessory_ids_list = [int(accessory_id) for accessory_id in accessory_ids.split(",")]
            accessories = UserItem.objects.filter(id__in=accessory_ids_list)
            outfit_instance.accessories.add(*accessories)

        messages.success(request, 'Outfit Added Successfully')
        return HttpResponseRedirect(reverse("outfit_creation"))

def remove_outfit(request):
    if request.method == "POST":
        outfit_id = request.POST.get("txt_del_outfit_id")
        user_outfit = UserOutfit.objects.get(pk=outfit_id)

        user_outfit.delete()
        messages.success(request, 'Outfit Deleted Successfully')
        return HttpResponseRedirect(reverse("outfit_creation"))

def recommended_item(request, item_id):
    # Retrieve the FashionItem instance
    user_id = request.session['fashion_user_id']
    user = UserAccount.objects.get(pk=user_id)
    item = get_object_or_404(UserItem, pk=item_id)


    # Get recommendations using the recommendation logic
    recommendations = item.get_recommendations()

    recommendations = [(recommendation, similarity * 100, label_name) for recommendation, similarity, label_name in recommendations]

    # Pass the item, category name, and recommendations to the template
    return render(request, 'wardrobe/item_recommendation.html', {
        'item': item, 
        'category_name': item.category, 
        'recommendations': recommendations,
        "own_item": True,
    })

def outfit_details(request, outfit_id):
    if 'fashion_user_id' in request.session and request.session['fashion_user_id']:
        user_id = request.session['fashion_user_id']
        userprofile_exist = UserProfile.objects.filter(user=user_id).exists()

        if userprofile_exist:
            userprofile = UserProfile.objects.filter(user=user_id)
            outfit = UserOutfit.objects.get(pk=outfit_id)

            return render(request, 'wardrobe/outfit_details.html', {
                'userprofile': userprofile,
                'outfit': outfit,
            })
        else:
            bodyshapes = BodyShape.objects.all()
            color_options = ItemColor.objects.all().order_by('name')
            style_options = ItemStyle.objects.all()
            return render(request, "wardrobe/setupprofile.html", {
                "bodyshapes": bodyshapes,
                "colors": color_options,
                "styles": style_options,
            })
    
    
    else:
        return render(request, "wardrobe/login.html", {
            "message": "Please login your account."
        })
    
def outfit_plan(request):
    if 'fashion_user_id' in request.session and request.session['fashion_user_id']:
        user_id = request.session['fashion_user_id']
        userprofile_exist = UserProfile.objects.filter(user=user_id).exists()

        if userprofile_exist:
            userprofile = UserProfile.objects.filter(user=user_id)
            outfits = UserOutfit.objects.filter(user=user_id)
            all_events = OutfitPlan.objects.filter(user=user_id)

            return render(request, 'wardrobe/outfit_plan.html', {
                'userprofile': userprofile,
                'outfits': outfits,
                'events':all_events,
                
            })
        else:
            bodyshapes = BodyShape.objects.all()
            color_options = ItemColor.objects.all().order_by('name')
            style_options = ItemStyle.objects.all()
            return render(request, "wardrobe/setupprofile.html", {
                "bodyshapes": bodyshapes,
                "colors": color_options,
                "styles": style_options,
            })
    
    
    else:
        return render(request, "wardrobe/login.html", {
            "message": "Please login your account."
        })

def all_events(request): 
    user_id = request.session['fashion_user_id']
    all_events = OutfitPlan.objects.filter(user=user_id)
    out = []
    
    for event in all_events:
        outfit_details_list = []
        for outfit in event.user_outfit.all():
            outfit_details = {
                'id': outfit.id,
                'outfit_name': outfit.outfit_name,
                'desc': outfit.desc,
                'top': {
                    'image': outfit.top.image.url if outfit.top else None,
                },
                'bottom': {
                    'image': outfit.bottom.image.url if outfit.bottom else None,
                },
                'footwear': {
                    'image': outfit.footwear.image.url if outfit.footwear else None,
                },
                'outerwear': {
                    'image': outfit.outerwear.image.url if outfit.outerwear else None,
                },
            }
            outfit_details_list.append(outfit_details)
        
        out.append({
            'title': event.event_name,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
            'user_outfits': outfit_details_list,
        })
    
    return JsonResponse(out, safe=False)

                                                                                                   
    
def add_event(request):
    user_id = request.session['fashion_user_id']
    user = UserAccount.objects.get(id=user_id)
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    outfit_ids = request.GET.get("eventOutfit", None)
    
    # Split outfit_ids into a list of integers
    outfit_ids_list = [int(outfit_id) for outfit_id in outfit_ids.split(",")]

    # Get the UserOutfit objects corresponding to the outfit IDs
    outfits = UserOutfit.objects.filter(id__in=outfit_ids_list)

  
    event = OutfitPlan(user=user, event_name=str(title), start=start, end=end)
    event.save()
    event.user_outfit.add(*outfits)

    data = {}
    return JsonResponse(data)

def update_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    id = request.GET.get("id", None)
    event = OutfitPlan.objects.get(id=id)
    event.start = start
    event.end = end
    event.save()
    data = {}
    return JsonResponse(data)

def remove_event(request):
    id = request.GET.get("id", None)
    event = OutfitPlan.objects.get(pk=id)
    event.delete()
    data = {}
    return JsonResponse(data)

def body_item_reco(request):
    if 'fashion_user_id' in request.session and request.session['fashion_user_id']:
        user_id = request.session['fashion_user_id']
        userprofile_exist = UserProfile.objects.filter(user=user_id).exists()

        if userprofile_exist:
            userprofile = UserProfile.objects.filter(user=user_id)

            return render(request, 'wardrobe/body_item_reco.html', {
                'userprofile': userprofile,
                
            })
        else:
            bodyshapes = BodyShape.objects.all()
            color_options = ItemColor.objects.all().order_by('name')
            style_options = ItemStyle.objects.all()
            return render(request, "wardrobe/setupprofile.html", {
                "bodyshapes": bodyshapes,
                "colors": color_options,
                "styles": style_options,
            })
    
    
    else:
        return render(request, "wardrobe/login.html", {
            "message": "Please login your account."
        })

def get_recommended_outfits(request):
    user_id = request.session['fashion_user_id']
    profile = UserProfile.objects.get(user=user_id)

    bodyshape = request.GET.get('body_shape')

    preference_styles = list(profile.pref_style.all())
    random.shuffle(preference_styles)

    recommended_outfits = []
    outfit_ids = set()

    pref_genderedstyle = profile.pref_genderedstyle
    pref_genderedstyle_list = [style.strip(" '").lower() for style in pref_genderedstyle.strip("[]").split(',')]

    categories = ['top', 'bottom', 'dress', 'formalwear', 'activewear']

    for category in categories:
        outfits = list(FashionItem.objects.filter(category=category, style__in=preference_styles, gendered__in=pref_genderedstyle_list))
        random.shuffle(outfits)  # Shuffle the outfits
        if outfits:
            outfit = random.choice(outfits)
            recommended_outfits.append({
                'id': outfit.id,
                'name': outfit.name,
                'image_url': outfit.original_image.url,
                'category': outfit.category
            })
            outfit_ids.add(outfit.id)

    # Continue selecting outfits based on other style preferences
    for style in preference_styles:
        for category in categories:  # Iterate over categories dynamically
            outfits = list(FashionItem.objects.filter(body_shape__icontains=bodyshape, style__icontains=style, gendered__in=pref_genderedstyle_list, category=category))
            random.shuffle(outfits)  # Shuffle the outfits
            for outfit in outfits:
                if outfit.id not in outfit_ids:
                    recommended_outfits.append({
                        'id': outfit.id,
                        'name': outfit.outfit_name,
                        'image_url': outfit.original_image.url,
                        'category': outfit.category  # Assign category dynamically
                    })
                    outfit_ids.add(outfit.id)
                    break

    # Limit the recommended outfits to a maximum of 5
    recommended_outfits = recommended_outfits[:5]

    return JsonResponse({'recommended_outfits': recommended_outfits})

def add_wishlist(request, item_id):
    if request.method == "GET":
        user_id = request.session['fashion_user_id']
        user = UserAccount.objects.get(pk=user_id)
        item = FashionItem.objects.get(pk=item_id)

        if Wishlist.objects.filter(user=user, item=item).exists():
            return JsonResponse({'success': True, 'message': 'Item already in wishlist'})
        
        wishlist = Wishlist(item=item, user=user)

        wishlist.save()
        data = {}
        return JsonResponse(data)
    
def remove_wishlist(request, item_id):
    if request.method == "GET":
        user_id = request.session['fashion_user_id']
        user = UserAccount.objects.get(pk=user_id)
        item = FashionItem.objects.get(pk=item_id)
        wishlist_item = Wishlist.objects.get(user=user, item=item)

        wishlist_item.delete()
        data = {}
        return JsonResponse(data)
    
event_style_mapping = {
    'casual': ['Casual', 'Streetwear', 'Athleisure'],
    'formal': ['Classic', 'Preppy', 'Vintage', 'Formal'],
    'romantic': ['Romantic', 'Vintage', 'Casual'],
    'cultural': ['Ethnic', 'Bohemian'],
    'creative': ['Eclectic', 'Minimalist'],
    'outdoor': ['Athleisure', 'Casual', 'Streetwear'],
    'party': ['Casual', 'Streetwear', 'Eclectic', 'Bohemian'],
}

def smart_recommend(request):
    event = request.GET.get('event')
    event_styles = event_style_mapping.get(event, [])

    # Shuffle and get one item per category
    top = UserItem.objects.filter(Q(category__name__in=['Top', 'Dress', ]) | Q(subcategory__name__in=['Cocktail Dress', 'Evening Gown']), style__name__in=event_styles).order_by('?').first()
    # Determine if a bottom should be recommended
    if top and (top.category.name == 'Dress' or top.subcategory.name in ['Cocktail Dress', 'Evening Gown']):
        bottom = None
    else:
        bottom = UserItem.objects.filter(category__name='Bottom', style__name__in=event_styles).order_by('?').first()
    
    # Randomly decide whether to include outerwear and accessory
    include_outerwear = choice([True, False])

    outerwear = UserItem.objects.filter(Q(category__name='Outerwear') | Q(subcategory__name__in=['Suit', 'Tuxedo']), style__name__in=event_styles).order_by('?').first() if include_outerwear else None
    footwear = UserItem.objects.filter(category__name='Footwear', style__name__in=event_styles).order_by('?').first()
    

    def get_item_data(item):
        if item:
            return {
                'id': item.id,
                'image': item.image.url if item.image else '',
                'name': item.outfit_name,
                'category': item.category.name,
            }
        return None

    recommendations = {
        'top': get_item_data(top),
        'bottom': get_item_data(bottom),
        'outerwear': get_item_data(outerwear),
        'footwear': get_item_data(footwear),
        'event': event.capitalize(),
    }

    return JsonResponse(recommendations)


