from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Integer, String, Time

Base = declarative_base()


ACHIEVEMENT_TYPES = {
    0: ("Snail Hoarder", [
            "You own 10 snails, I hope you are looking after them.",
            "You own 25 snails, this seems a bit excessive.",
            "You own 50 snails, I think you have a problem.",
            "You own 75 snails, Perhaps you should seek help.",
            "You own 100 snails now? WHY?!?!"
        ]),
    1: ("Hype Train", [
            "You've hyped up 10 snails of other people, you're doing good for a junior.",
            "You've hyped up 25 snails of other people, such comradery.",
            "You've hyped up 50 snails of other people, I hope you're not getting paid for this.",
            "You've hyped up 75 snails of other people, LET'S HEAR SOME NOISE!!!!!",
            "You've hyped up 100 snails of other people. *sips energy drink* LET'S F***ING GO!!!!!!!!!"
        ]),
    2: ("Ticket Master", [
            "You've won 10 raffles, luck of the draw I guess.",
            "You've won 25 raffles, hmm... seems sus.",
            "You've won 50 raffles, whats your secret?",
            "You've won 75 raffles, I'm starting to think you're cheating.",
            "You've spent way too much money on the raffle, but at least you've won 100 times... Somehow."
        ]),
    3: ("The EV Trainer", [
            "You've bred 10 rank snails. You're a natural.",
            "You've bred 25 rank snails. Wow, you're really good at this.",
            "You've bred 50 rank snails. They should get you to try and breed Pandas.",
            "You've bred 75 rank snails. You're a true master of snail genetics.",
            "You've bred 100 rank snails. Your dedication to snail genetics is unparalleled."
        ]),
    4: ("Black Market Trader", [
            "You've made 10 trades, I hope you didn't get scammed.",
            "You've made 25 trades, No seriously, I hope you didn't get scammed.",
            "You've made 50 trades, but were they all fair trades?",
            "You've made 75 trades, I'm starting to think you're the scammer.",
            "You've made 100 trades, I dub you `Licensed Scam Artist`."
        ]),
    5: ("Jerry", [
            "You've lost all your money in single big bet. You muppet, why did you do that?",
            "You've lost all your money in single big bets 2 times. Really? You did it again?",
            "You've lost all your money in single big bets 3 times. You're a slow learner.",
            "You've lost all your money in single big bets 5 times. You aren't a clown, you're the entire circus.",
            "You've lost all your money in single big bets 10 times. Congrats, Jerry. You're now banned."
        ]),
    6: ("Ripper Doc", [
            "You've swapped shells on 10 snails, I didn't feel a thing.",
            "You've swapped shells on 25 snails, You know they aren't designed for this.",
            "You've swapped shells on 50 snails, I hope you're not doing this for fun.",
            "You've swapped shells on 75 snails, I'm starting to think you're a mad scientist.",
            "You've swapped shells on 100 snails, I'm calling the RSPCA."
        ]),
    7: ("Big Winner", [
            "You've won 50 races, you're doing pretty well for yourself.",
            "You've won 100 races, you're showing them.",
            "You've won 150 races, you need to slow down.",
            "You've won 250 races, the other snails are starting to get suspicious.",
            "You've won 500 races, it must be lonely at the top."
        ]),
    8: ("Pure Kindness", [
            "You've gifted away 10 snails. You're a good person.",
            "You've gifted away 25 snails. You're a very good person.",
            "You've gifted away 50 snails. You must be running a charity.",
            "You've gifted away 75 snails. You aren't doing this for the achievement are you?",
            "You've gifted away 100 snails. Where do you get all these snails from?"
        ]),
    9: ("The Auctioneer", [
            "Auction off 10 items. *slam* SOLD!",
            "Auction off 25 items. Dollar dollar bills y'all.",
            "Auction off 50 items. I didn't want that anyway.",
            "Auction off 75 items. I'm starting to think you're a scalper.",
            "Auction off 100 items. Your Auctioneer hammer must only be a handle at this point."
        ]),
    10: ("The Highest Bidder", [
            "Be the highest bidder for 10 auctions. You're a bit of a show off.",
            "Be the highest bidder for 25 auctions. Want to share some of that money?",
            "Be the highest bidder for 50 auctions. Want it, bid it, get it.",
            "Be the highest bidder for 75 auctions. I hope you arent using your parents credit card.",
            "Be the highest bidder for 100 auctions. Money? What's that?"
        ]),
    11: ("Snail Mechanic", [
            "Congratulations on your first bug fix or feature implementation! Keep up the good work, we're counting on you!",
            "Two down, three to go! Thanks for your hard work in squashing those bugs and improving our game.",
            "You've reached a milestone with five bug fixes or feature implementations! Your dedication to making our game better is truly appreciated.",
            "Double digits! You've made ten bug fixes or feature implementations, and we couldn't be more grateful for your help in improving our game.",
            "You've hit an impressive 20 bug fixes or feature implementations! Your contributions to our game have been invaluable, and we can't thank you enough for your hard work and dedication."
        ]),
}


class SnailraceAchievement(Base):
    __tablename__ = 'snailrace_achievements'

    # Achievement Metadata
    id = Column("id", BigInteger, primary_key=True, nullable=False)
    user_id = Column("user_id", BigInteger, nullable=False)

    # When was the last level achieved?
    leveled_at = Column("leveled_at", DateTime, nullable=False)

    # Achievement Properties
    type = Column("type", BigInteger, nullable=False)
    level = Column("level", Integer, nullable=False) # Levels [0, 5]
    value = Column("value", BigInteger, nullable=False)
