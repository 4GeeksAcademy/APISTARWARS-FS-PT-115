from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable = False)
    date_resgister: Mapped[date] = mapped_column(Date, nullable = False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    planet_favorites: Mapped[list["PlanetFavs"]] = relationship("PlanetFavs", back_populates="user")
    character_favorites: Mapped[list["CharacterFavs"]] = relationship("CharacterFavs", back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
            "planet_favorites": [planet.serialize() for planet in self.planet_favorites] if self.planet_favorites else None,
            "character_favorites": [character.serialize() for character in self.character_favorites] if self.character_favorites else None

        }

class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(nullable = False)
    image: Mapped[str] = mapped_column(nullable = True)
    data: Mapped[str] = mapped_column(nullable = True)

    favorited_by_p: Mapped[list["PlanetFavs"]] = relationship("PlanetFavs", back_populates="planet")

    def serialize(self):
        return{
        "id": self.id,
        "name": self.name,
        "image": self.image,

        }


class Character(db.Model):
    id:Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(nullable= False)
    image: Mapped[str] = mapped_column(nullable = True)
    data: Mapped[str] = mapped_column(nullable = True)

    favorited_by_c: Mapped[list["CharacterFavs"]] = relationship("CharacterFavs", back_populates="character")


class PlanetFavs(db.Model):
    id:Mapped[int] = mapped_column(primary_key = True)
    user_id:Mapped[int] = mapped_column(ForeignKey('user.id'), nullable = False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable = False)

    user: Mapped["User"] = relationship("User", back_populates="planet_favorites")
    planet: Mapped["Planets"] = relationship("Planets", back_populates="favorited_by_p")
    
    


class CharacterFavs(db.Model):
    id:Mapped[int] = mapped_column(primary_key = True)
    user_id:Mapped[int] = mapped_column(ForeignKey('user.id'), nullable = False)
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'), nullable = False)

    user: Mapped["User"] = relationship("User", back_populates="character_favorites")
    character: Mapped["Character"] = relationship("Character", back_populates= "favorited_by_c")