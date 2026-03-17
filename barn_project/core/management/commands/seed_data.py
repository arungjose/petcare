"""
Management command: python manage.py seed_data
Creates all initial categories, breeds, service categories/items, and store categories.
Run this once after migrations to populate your BARN database.
"""
from django.core.management.base import BaseCommand
from pets.models import PetCategory, PetBreed
from services.models import ServiceCategory, Service
from store.models import StoreCategory


class Command(BaseCommand):
    help = 'Seed BARN database with initial categories and data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🌱 Seeding BARN database...'))
        self._seed_pet_categories()
        self._seed_service_categories()
        self._seed_store_categories()
        self.stdout.write(self.style.SUCCESS('✅ Seeding complete! BARN is ready.'))

    def _seed_pet_categories(self):
        categories = [
            ('Dogs', 'dogs', '🐕', 'Find your perfect canine companion from verified breeders.'),
            ('Cats', 'cats', '🐈', 'Discover beautiful cats from responsible breeders.'),
            ('Birds', 'birds', '🦜', 'Exotic and common birds for your home.'),
            ('Rabbits', 'rabbits', '🐇', 'Adorable rabbits looking for loving families.'),
            ('Fish', 'fish', '🐠', 'Freshwater and marine fish for your aquarium.'),
        ]
        for name, slug, icon, desc in categories:
            cat, created = PetCategory.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'icon': icon, 'description': desc}
            )
            if created:
                self.stdout.write(f'  ✓ Pet category: {name}')

        # Breeds
        breeds_data = {
            'dogs': [
                'Labrador Retriever', 'Golden Retriever', 'German Shepherd',
                'Beagle', 'Poodle', 'Bulldog', 'Rottweiler', 'Dachshund',
                'Siberian Husky', 'Shih Tzu', 'Pomeranian', 'Doberman',
                'Great Dane', 'Boxer', 'Cocker Spaniel', 'Indian Pariah',
            ],
            'cats': [
                'Persian', 'Siamese', 'Maine Coon', 'British Shorthair',
                'Bengal', 'Ragdoll', 'Scottish Fold', 'Abyssinian',
                'Bombay', 'Turkish Angora', 'Indian Domestic Cat',
            ],
            'birds': [
                'African Grey Parrot', 'Cockatiel', 'Budgerigar',
                'Lovebird', 'Macaw', 'Conure', 'Finch', 'Canary',
                'Alexandrine Parakeet', 'Indian Ringneck Parakeet',
            ],
            'rabbits': [
                'Holland Lop', 'Mini Rex', 'Dutch Rabbit', 'Angora',
                'Flemish Giant', 'Lionhead', 'New Zealand White',
            ],
            'fish': [
                'Goldfish', 'Betta', 'Guppy', 'Arowana', 'Oscar',
                'Angelfish', 'Discus', 'Koi', 'Clownfish', 'Neon Tetra',
            ],
        }
        for cat_slug, breed_names in breeds_data.items():
            try:
                cat = PetCategory.objects.get(slug=cat_slug)
                for breed_name in breed_names:
                    b, created = PetBreed.objects.get_or_create(
                        name=breed_name, category=cat
                    )
                    if created:
                        self.stdout.write(f'    ✓ Breed: {breed_name}')
            except PetCategory.DoesNotExist:
                pass

    def _seed_service_categories(self):
        services_data = [
            {
                'category': ('Grooming', 'grooming', '✂️', 'Professional grooming services for all breeds.'),
                'services': [
                    {
                        'name': 'Basic Bath & Brush',
                        'slug': 'basic-bath-brush',
                        'short_description': 'Shampoo, condition, blow-dry, and brush out.',
                        'description': 'Our Basic Bath & Brush package keeps your pet clean and fresh. Includes a shampoo with premium pet-safe products, conditioning treatment, blow-dry, and a thorough brushing to remove dead hair and tangles.',
                        'price': 499,
                        'duration': '1–1.5 hours',
                        'includes': 'Shampoo & condition,Blow dry,Brush out,Ear cleaning,Paw balm application',
                    },
                    {
                        'name': 'Full Grooming Package',
                        'slug': 'full-grooming-package',
                        'short_description': 'Complete groom: bath, haircut, nails, ears, and teeth.',
                        'description': 'The ultimate grooming experience for your pet. Our certified groomers perform a thorough bath, breed-specific haircut or trim, nail grinding, ear cleaning and plucking, teeth brushing, and finish with a spritz of pet-safe cologne.',
                        'price': 999,
                        'duration': '2.5–3 hours',
                        'includes': 'Full bath & condition,Breed-specific haircut,Nail grinding,Ear cleaning & plucking,Teeth brushing,Pet-safe cologne,Bandana or bow',
                    },
                    {
                        'name': 'Nail Trim & Paw Care',
                        'slug': 'nail-trim-paw-care',
                        'short_description': 'Nail trimming, grinding, and paw pad moisturizing.',
                        'description': 'Keep your pet\'s paws healthy with our Nail Trim & Paw Care service. Includes nail trimming or grinding, paw pad inspection, and moisturizing treatment.',
                        'price': 199,
                        'duration': '30 minutes',
                        'includes': 'Nail trim or grind,Paw pad check,Moisturizing treatment',
                    },
                ]
            },
            {
                'category': ('Veterinary Care', 'veterinary', '🩺', 'Certified vet services by experienced professionals.'),
                'services': [
                    {
                        'name': 'General Health Checkup',
                        'slug': 'general-health-checkup',
                        'short_description': 'Full physical examination by a certified veterinarian.',
                        'description': 'A comprehensive health checkup covering all vital systems. Our certified vets examine eyes, ears, teeth, coat, weight, heart, and lungs. Includes a written health report and dietary recommendations.',
                        'price': 299,
                        'duration': '30–45 minutes',
                        'includes': 'Full physical exam,Vital sign check,Written health report,Dietary advice,Deworming consultation',
                    },
                    {
                        'name': 'Vaccination Package',
                        'slug': 'vaccination-package',
                        'short_description': 'Core vaccinations with health certificate.',
                        'description': 'Protect your pet with our comprehensive vaccination package. Includes all core vaccines, anti-rabies, and a signed health certificate. Perfect for new pets or annual booster updates.',
                        'price': 799,
                        'duration': '45 minutes',
                        'includes': 'Core vaccine set,Anti-rabies shot,Health certificate,Vaccination record update,Post-vaccine care guide',
                    },
                    {
                        'name': 'Deworming & Flea Treatment',
                        'slug': 'deworming-flea-treatment',
                        'short_description': 'Internal and external parasite prevention.',
                        'description': 'Complete parasite control for your pet. Includes oral deworming medication, topical flea and tick prevention, and a follow-up schedule for continued protection.',
                        'price': 399,
                        'duration': '20 minutes',
                        'includes': 'Oral deworming,Flea & tick treatment,Schedule plan,Care instructions',
                    },
                ]
            },
            {
                'category': ('Training', 'training', '🏅', 'Professional training programs for all ages and breeds.'),
                'services': [
                    {
                        'name': 'Basic Obedience Training',
                        'slug': 'basic-obedience-training',
                        'short_description': 'Sit, stay, come, heel — fundamentals for every dog.',
                        'description': 'Our Basic Obedience Training program is perfect for puppies and untrained adult dogs. In 8 sessions, your dog will learn core commands: sit, stay, down, come, heel, and leave it. Positive reinforcement methods only.',
                        'price': 3999,
                        'duration': '8 sessions (1 hr each)',
                        'includes': '8 training sessions,Training manual,Progress report,Owner coaching,Certificate of completion',
                    },
                    {
                        'name': 'Behavior Modification',
                        'slug': 'behavior-modification',
                        'short_description': 'Address aggression, anxiety, and destructive habits.',
                        'description': 'Designed for pets with specific behavioral challenges including aggression, separation anxiety, excessive barking, or destructive chewing. Our certified trainers use science-based positive reinforcement techniques.',
                        'price': 5999,
                        'duration': '12 sessions',
                        'includes': '12 specialized sessions,Behavioral assessment,Custom training plan,Owner support between sessions,30-day follow-up',
                    },
                ]
            },
            {
                'category': ('Boarding & Sitting', 'boarding', '🏠', 'Safe, caring boarding for when you are away.'),
                'services': [
                    {
                        'name': 'Day Boarding',
                        'slug': 'day-boarding',
                        'short_description': 'Safe, supervised day care while you work.',
                        'description': 'Drop your pet off in the morning and pick them up in the evening. Includes supervised playtime, meals, rest time, and a daily activity report sent to your phone.',
                        'price': 599,
                        'duration': 'Per day (8am–7pm)',
                        'includes': 'Supervised play,2 meals included,Rest time,Daily photo update,GPS-tracked outdoor time',
                    },
                    {
                        'name': 'Overnight Boarding',
                        'slug': 'overnight-boarding',
                        'short_description': 'Comfortable overnight stay in our secure facility.',
                        'description': 'A home-away-from-home for your pet. Our overnight boarding includes a private sleeping area, multiple play sessions, meals, and 24/7 supervision by our trained staff.',
                        'price': 999,
                        'duration': 'Per night',
                        'includes': 'Private sleeping area,3 meals,Multiple play sessions,24/7 staff supervision,Daily photo/video updates',
                    },
                    {
                        'name': 'Dog Walking',
                        'slug': 'dog-walking',
                        'short_description': 'GPS-tracked daily walks by certified walkers.',
                        'description': 'Keep your dog active with our professional dog walking service. All walkers are certified, background-checked, and use GPS tracking so you can follow your dog\'s walk in real time.',
                        'price': 299,
                        'duration': '45-minute walk',
                        'includes': 'GPS-tracked walk,Real-time location sharing,Post-walk report,Fresh water provided,Waste pickup included',
                    },
                ]
            },
        ]

        for data in services_data:
            cat_name, cat_slug, cat_icon, cat_desc = data['category']
            cat, created = ServiceCategory.objects.get_or_create(
                slug=cat_slug,
                defaults={'name': cat_name, 'icon': cat_icon, 'description': cat_desc}
            )
            if created:
                self.stdout.write(f'  ✓ Service category: {cat_name}')

            for svc in data['services']:
                s, created = Service.objects.get_or_create(
                    slug=svc['slug'],
                    defaults={
                        'category': cat,
                        'name': svc['name'],
                        'short_description': svc['short_description'],
                        'description': svc['description'],
                        'price': svc['price'],
                        'duration': svc['duration'],
                        'includes': svc['includes'],
                    }
                )
                if created:
                    self.stdout.write(f'    ✓ Service: {svc["name"]} (₹{svc["price"]})')

    def _seed_store_categories(self):
        store_cats = [
            ('Dog Food', 'dog-food', 'supply', '🍖'),
            ('Cat Food', 'cat-food', 'supply', '🐟'),
            ('Bird Food', 'bird-food', 'supply', '🌾'),
            ('Treats & Snacks', 'treats', 'supply', '🦴'),
            ('Health Supplements', 'supplements', 'supply', '💊'),
            ('Toys', 'toys', 'supply', '🎾'),
            ('Collars & Leashes', 'collars-leashes', 'accessory', '🏷️'),
            ('Beds & Furniture', 'beds', 'accessory', '🛏️'),
            ('Travel & Carriers', 'carriers', 'accessory', '🧳'),
            ('Clothing & Accessories', 'clothing', 'accessory', '👕'),
            ('Grooming Supplies', 'grooming-supplies', 'supply', '🪮'),
            ('Aquarium Supplies', 'aquarium', 'supply', '🐠'),
        ]
        for name, slug, cat_type, icon in store_cats:
            c, created = StoreCategory.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'category_type': cat_type, 'icon': icon}
            )
            if created:
                self.stdout.write(f'  ✓ Store category: {name}')
