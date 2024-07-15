from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey, select, Float, func
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import random
import csv

Base = declarative_base()

item_trend = Table('item_trend', Base.metadata,
    Column('item_id', Integer, ForeignKey('items.id')),
    Column('trend_id', Integer, ForeignKey('trends.id'))
)

TREND_ATTRIBUTES = {
    "Dark Academia": {
        "colors": ["Brown", "Black", "Beige", "Dark Green", "Burgundy"],
        "categories": ["Top", "Bottom", "Footwear", "Accessory"],
        "keywords": ["blazer", "tweed", "plaid", "loafers", "oxford shoes", "turtlenecks", "skirt", "sweater"]
    },
    "Cottage Core": {
        "colors": ["White", "Cream", "Pastel", "Floral"],
        "categories": ["Top", "Bottom", "Footwear", "Accessory"],
        "keywords": ["floral", "lace", "embroidery", "puffy", "romantic"]
    },
    "Y2K": {
        "colors": ["Pink", "Baby Blue", "Silver", "Metallic"],
        "categories": ["Top", "Bottom", "Footwear", "Accessory"],
        "keywords": ["crop top", "mini skirt", "platform", "baggy", "glitter", "shiny", "butterfly", "low-rise"]
    },
    "Grunge Revival": {
        "colors": ["Black", "Gray", "Dark Red", "Dark Green", "Purple"],
        "categories": ["Top", "Bottom", "Footwear", "Accessory"],
        "keywords": ["leather", "ripped", "combat boots", "flannel", "distressed"]
    },
    "Minimalist": {
        "colors": ["Black", "White", "Gray", "Beige"],
        "categories": ["Top", "Bottom", "Footwear", "Accessory"],
        "keywords": ["simple", "clean", "basic", "neutral"]
    },
    "Streetwear": {
        "colors": ["Black", "White", "Red", "Blue"],
        "categories": ["Top", "Bottom", "Footwear", "Accessory"],
        "keywords": ["hoodie", "sneakers", "graphic", "oversized"]
    },
}

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    color = Column(String)
    trends = relationship("Trend", secondary=item_trend, back_populates="items")

class Trend(Base):
    __tablename__ = 'trends'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    items = relationship("Item", secondary=item_trend, back_populates="trends")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    preferred_colors = Column(String)
    preferred_styles = Column(String)
    budget = Column(Integer)

engine = create_engine('sqlite:///fashion_recommendation.db')
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

def load_data_from_csv(session, csv_file):
    trends = {}
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            item_trends = [trend.strip() for trend in row['Trends'].split(',')]
            for trend_name in item_trends:
                if trend_name not in trends:
                    trends[trend_name] = Trend(name=trend_name)
                    session.add(trends[trend_name])

            item = Item(
                id=int(row['ID']),
                name=row['Name'],
                category=row['Category'],
                color=row['Color'],
            )
            item.trends = [trends[trend_name] for trend_name in item_trends]
            session.add(item)

    session.commit()
    print(f"Loaded {len(trends)} trends and {csv_reader.line_num - 1} items from CSV.")

class FashionRecommendationSystem:
    def __init__(self):
        self.session = SessionLocal()

    def get_trend_score(self, item, trend):
        score = 0
        trend_attrs = TREND_ATTRIBUTES.get(trend.name, {})
        
        if item.color in trend_attrs.get("colors", []):
            score += 2
        if item.category in trend_attrs.get("categories", []):
            score += 2
        for keyword in trend_attrs.get("keywords", []):
            if keyword.lower() in item.name.lower():
                score += 1
        
        return score

    def get_recommendations(self, trend, category, budget, excluded_ids=None):
        if excluded_ids is None:
            excluded_ids = []

        items = self.session.execute(
            select(Item).filter(
                Item.id.notin_(excluded_ids),
                Item.category == category,
                Item.trends.any(Trend.name == trend.name),
            )
        ).scalars().all()

        scored_items = [(item, self.get_trend_score(item, trend)) for item in items]
        scored_items.sort(key=lambda x: x[1], reverse=True)
        return [item for item, score in scored_items if score > 0]

    def get_outfit(self, user):
        user_trends = [trend.strip() for trend in user.preferred_styles.split(',')]
        available_trends = [trend for trend in TREND_ATTRIBUTES.keys() if trend in user_trends]
        
        if not available_trends:
            print("No matching trends found for user preferences.")
            return None, None

        chosen_trend = random.choice(available_trends)
        trend_obj = self.session.query(Trend).filter_by(name=chosen_trend).first()
        print(f"Chosen trend: {chosen_trend}")

        outfit = []
        categories = ["Top", "Bottom", "Footwear", "Accessory"]
        excluded_ids = []

        for category in categories:
            recommendations = self.get_recommendations(trend_obj, category, excluded_ids)
            if recommendations:
                chosen_item = recommendations[0]
                outfit.append(chosen_item)
                excluded_ids.append(chosen_item.id)
            else:
                print(f"No recommendations found for category: {category}")

        return outfit, trend_obj

    def print_outfit(self, outfit, trend, user):
        if not outfit:
            print("Couldn't generate a complete outfit.")
            return

        print("Recommended Outfit:")
        print(f"Theme: {trend.name}")
        total_price = 0
        for item in outfit:
            print(f"- {item.category}: {item.name} ({item.color})")
            print(f"  Search Link: https://www.myntra.com/{item.name}?rawQuery={item.name}%20{item.color}")

if __name__ == "__main__":
    session = SessionLocal()
    
    # Check if the database is empty
    item_count = session.query(func.count(Item.id)).scalar()
    if item_count == 0:
        print("Database is empty. Loading data from CSV...")
        load_data_from_csv(session, 'fashion_items.csv')
    else:
        print(f"Database already contains {item_count} items.")

    # Create a sample user
    user = User(name="John Doe", preferred_colors="Black,White,Gray", preferred_styles="Minimalist,Streetwear,Grunge Revival", budget=20000)
    session.add(user)
    session.commit()

    print("\nGenerating outfit recommendation:")
    system = FashionRecommendationSystem()
    outfit, trend = system.get_outfit(user)
    
    if outfit and trend:
        system.print_outfit(outfit, trend, user)
    else:
        print("Failed to generate an outfit. Please check the database and recommendation criteria.")

    session.close()