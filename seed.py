"""Utility file to seed chime2 database from seed data file"""

from model import Category, Question, connect_to_db, db
from server import app


def load_categories():
    """Load categories into database."""

    unique_category_names = set()

    with open("seed_data/seed.txt") as f:
        for line in f:
            category_name = line.split("|")[1].strip()
            unique_category_names.add(category_name)

    for category_name in unique_category_names:
        category = Category(category_name=category_name)
        db.session.add(category)

    db.session.commit()



def load_questions():
    """Load questions into database."""


    with open("seed_data/seed.txt") as f:
        for line in f:
            question_text, category_name = [item.strip() for item in line.split("|")]
            category_row = Category.query.filter_by(category_name=category_name).first()
            category_id = category_row.category_id
            question = Question(question_text=question_text,
                        category_id=category_id)

            db.session.add(question)

        db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_categories()
    load_questions()
    