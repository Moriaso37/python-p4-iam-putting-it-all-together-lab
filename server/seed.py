#!/usr/bin/env python3
from app import app
from models import db, User, Recipe

def seed_database():
    with app.app_context():
        print("🧹 Clearing existing data...")
        Recipe.query.delete()
        User.query.delete()
        db.session.commit()

        print("🌱 Seeding new data...")
        # Users
        user1 = User(username='chef_anna', image_url='https://example.com/anna.png', bio='Pastry chef')
        user1.password = 'secret123'

        user2 = User(username='chef_bob', image_url='https://example.com/bob.png', bio='BBQ expert')
        user2.password = 'bbqmaster'

        db.session.add_all([user1, user2])
        db.session.commit()
        print(f"✅ Added {len([user1, user2])} users")

        # Recipes
        recipe1 = Recipe(
            title='Chocolate Cake',
            instructions='Mix flour, cocoa powder, eggs, sugar, and butter. Bake at 350°F for 30 minutes. Let it cool and enjoy!',
            minutes_to_complete=45,
            user_id=user1.id,
        )
        recipe2 = Recipe(
            title='Grilled Ribs',
            instructions='Season the ribs generously with salt and spices. Grill them slowly for 2 hours over medium heat until tender.',
            minutes_to_complete=120,
            user_id=user2.id,
        )
        db.session.add_all([recipe1, recipe2])
        db.session.commit()
        print(f"✅ Added {len([recipe1, recipe2])} recipes")
        print("✅ 🌟 Database successfully seeded!")

if __name__ == '__main__':
    seed_database()
