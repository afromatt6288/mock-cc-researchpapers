from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here
class ResearchAuthor(db.Model, SerializerMixin):
    __tablename__ = 'research_authors'

    serialize_rules = ('-author.research_authors', '-research.research_authors', '-created_at', '-updated_at',)

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    research_id = db.Column(db.Integer, db.ForeignKey('research.id'))

    def __repr__(self):
        return f'<ResearchAuthor:  Author: {self.author.name}, Research: {self.research.name}>'
    

class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    serialize_rules = ('-research_authors.author', '-created_at', '-updated_at',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    field_of_study = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

## cascade is added to allow the deletion of a author to also delete the ResearchAuthor they are associated with ##
    research_authors = db.relationship('ResearchAuthor', backref='author', cascade="all, delete, delete-orphan")
## This was in the solution code, but I do not know what it is or means... ##
    research = association_proxy('research_authors', 'research')



    @validates('field_of_study')
    def validate_field_of_study(self, key, field_of_study):
        fields_of_study = ['AI', 'Robotics', 'Machine Learning', 'Vision', 'Cybersecurity']
        if field_of_study not in fields_of_study:
            raise ValueError("No such field found")
        return field_of_study
    
    def __repr__(self):
        return f'<Author: {self.name}, Field of Study: {self.field_of_study}>'
  
class Research(db.Model, SerializerMixin):
    __tablename__ = 'research'

    serialize_rules = ('-research_authors.research', '-created_at', '-updated_at',)

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('year')
    def validate_year(self, key, year):
        if len(str(year)) != 4:
            raise ValueError("Year must be 4 digits.")
        return year

## cascade is added to allow the deletion of a Research to also delete the ResearchAuthor it is associated with ##
    research_authors = db.relationship('ResearchAuthor', backref='research', cascade="all, delete, delete-orphan")
## This was in the solution code, but I do not know what it is or means... ##
    # authors = association_proxy('research_authors', 'author')
    
    def __repr__(self):
        return f'<Research: {self.topic}, Year: {self.year}, Page Count: {self.page_count}>'