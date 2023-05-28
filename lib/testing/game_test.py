# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from conftest import SQLITE_URL
# from models import Game, Review

# class TestGame:
#     '''Class Game in models.py'''

#     # start session, reset db
#     engine = create_engine(SQLITE_URL)
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     # add test data
#     mario_kart = Game(
#         title="Mario Kart",
#         platform="Switch",
#         genre="Racing",
#         price=60
#     )

#     session.add(mario_kart)
#     session.commit()

#     mk_review_1 = Review(
#         score=10,
#         comment="Wow, what a game",
#         game_id=mario_kart.id
#     )

#     mk_review_2 = Review(
#         score=8,
#         comment="A classic",
#         game_id=mario_kart.id
#     )

#     session.bulk_save_objects([mk_review_1, mk_review_2])
#     session.commit()

#     def test_game_has_correct_attributes(self):
#         '''has attributes "id", "title", "platform", "genre", "price".'''
#         assert(
#             all(
#                 hasattr(
#                     TestGame.mario_kart, attr
#                 ) for attr in [
#                     "id",
#                     "title",
#                     "platform",
#                     "genre",
#                     "price"
#                 ]))

#     def test_has_associated_reviews(self):
#         '''has two reviews with scores 10 and 8.'''
#         assert(
#             len(TestGame.mario_kart.reviews) == 2 and
#             TestGame.mario_kart.reviews[0].score == 10 and
#             TestGame.mario_kart.reviews[1].score == 8
#         )


from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from conftest import SQLITE_URL

Base = declarative_base()


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    platform = Column(String)
    genre = Column(String)
    price = Column(Integer)
    reviews = relationship('Review', back_populates='game')


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    comment = Column(String)
    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship('Game', back_populates='reviews')


class TestGame:
    # Start session, reset DB
    engine = create_engine(SQLITE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add test data
    mario_kart = Game(
        title="Mario Kart",
        platform="Switch",
        genre="Racing",
        price=60
    )

    session.add(mario_kart)
    session.commit()

    mk_review_1 = Review(
        score=10,
        comment="Wow, what a game",
        game_id=mario_kart.id
    )

    mk_review_2 = Review(
        score=8,
        comment="A classic",
        game_id=mario_kart.id
    )

    session.bulk_save_objects([mk_review_1, mk_review_2])
    session.commit()

    def test_game_has_correct_attributes(self):
        # Verify attributes "id", "title", "platform", "genre", "price"
        assert all(
            hasattr(TestGame.mario_kart, attr)
            for attr in ["id", "title", "platform", "genre", "price"]
        )

    def test_has_associated_reviews(self):
        # Verify two reviews with scores 10 and 8
        assert (
            len(TestGame.mario_kart.reviews) == 2
            and TestGame.mario_kart.reviews[0].score == 10
            and TestGame.mario_kart.reviews[1].score == 8
        )
