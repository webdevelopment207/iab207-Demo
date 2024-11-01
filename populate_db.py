from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from index import create_app, db
from index.models import User, Event, Comment, Ticket
import random

def seed_database():
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.session.query(Ticket).delete()
        db.session.query(Comment).delete()
        db.session.query(Event).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Create dummy users
        print("Creating users...")
        users = [
            User(
                first_name="John",
                last_name="Doe",
                dob="1990-01-01",
                email="john@example.com",
                username="john_doe",
                password=generate_password_hash("password123"),
                contact_number="0400111222",
                street_address="123 Main St, Sydney NSW 2000"
            ),
            User(
                first_name="Jane",
                last_name="Smith",
                dob="1992-05-15",
                email="jane@example.com",
                username="jane_smith",
                password=generate_password_hash("password123"),
                contact_number="0400333444",
                street_address="456 Park Ave, Melbourne VIC 3000"
            ),
            User(
                first_name="Mike",
                last_name="Johnson",
                dob="1988-12-10",
                email="mike@example.com",
                username="mike_j",
                password=generate_password_hash("password123"),
                contact_number="0400555666",
                street_address="789 Queen St, Brisbane QLD 4000"
            )
        ]
        
        for user in users:
            db.session.add(user)
        db.session.commit()
        
        # Create dummy events
        print("Creating events...")
        teams = [
            "Sydney Kings", "Melbourne United", "Brisbane Bullets", 
            "Perth Wildcats", "Adelaide 36ers", "Illawarra Hawks"
        ]
        venues = [
            "Qudos Bank Arena", "John Cain Arena", "Nissan Arena",
            "RAC Arena", "Adelaide Entertainment Centre", "WIN Entertainment Centre"
        ]
        
        events = []
        for i in range(10):
            # Randomly select home and away teams
            home_team, away_team = random.sample(teams, 2)
            venue = venues[random.randint(0, len(venues)-1)]
            
            # Generate a random future date within the next 30 days
            event_date = datetime.now() + timedelta(days=random.randint(1, 30))
            
            event = Event(
                name=f"{home_team} vs {away_team}",
                date=event_date,
                location=venue,
                description=f"Don't miss this exciting matchup between {home_team} and {away_team}! Experience the intensity of professional basketball at its finest.",
                seats_available=random.randint(50, 200),
                status=random.choice(['Open', 'Open', 'Open', 'Sold Out', 'Cancelled']),  # Weight towards 'Open'
                price_per_ticket=random.randint(50, 150),
                created_by=users[0].id  # First user creates all events for simplicity
            )
            events.append(event)
            db.session.add(event)
        db.session.commit()
        
        # Create dummy comments
        print("Creating comments...")
        comments = [
            "Can't wait for this game!",
            "Last match between these teams was incredible!",
            "Hope it doesn't sell out before I get tickets.",
            "The venue is perfect for this matchup.",
            "Anyone want to meet up before the game?",
            "Bringing the whole family to this one!",
            "These teams always deliver great games.",
            "First time seeing either team, super excited!",
            "Hoping for a close game!",
            "The atmosphere at these games is always electric!"
        ]
        
        for event in events:
            # Add 2-5 random comments for each event
            for _ in range(random.randint(2, 5)):
                comment = Comment(
                    content=random.choice(comments),
                    user_id=random.choice(users).id,
                    event_id=event.id,
                    date_posted=datetime.now() - timedelta(days=random.randint(0, 5))
                )
                db.session.add(comment)
        db.session.commit()
        
        # Create dummy tickets
        print("Creating tickets...")
        for event in events:
            if event.status == 'Open':
                # Create 1-3 ticket bookings per event
                for _ in range(random.randint(1, 3)):
                    user = random.choice(users)
                    num_tickets = random.randint(1, 4)
                    
                    ticket = Ticket(
                        event_id=event.id,
                        user_name=f"{user.first_name} {user.last_name}",
                        user_email=user.email,
                        number_of_tickets=num_tickets,
                        total_price=event.price_per_ticket * num_tickets,
                        booking_date=datetime.now() - timedelta(days=random.randint(0, 10))
                    )
                    db.session.add(ticket)
                    
                    # Update available seats
                    event.seats_available -= num_tickets
        db.session.commit()
        
        print("Database seeded successfully!")
        
        # Print summary
        print("\nSummary:")
        print(f"Users created: {len(users)}")
        print(f"Events created: {len(events)}")
        print(f"Comments created: {db.session.query(Comment).count()}")
        print(f"Tickets created: {db.session.query(Ticket).count()}")

if __name__ == "__main__":
    seed_database()