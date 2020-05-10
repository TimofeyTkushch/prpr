import datetime
import sqlalchemy
from flask_wtf import FlaskForm
from sqlalchemy import orm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired

from .db_session import SqlAlchemyBase

class MModels(SqlAlchemyBase):
    __tablename__ = 'mmodels'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    p1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    p2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    p3 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    p4 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    p5 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    p6 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))    
    user = orm.relation('User')
    
class MModelsForm(FlaskForm):
    name = StringField('Имя модели', validators=[DataRequired()])
    p1 = RadioField('Тип модели', choices=[('RandomForest', 'RandomForest'), ('KNN', 'KNN'), ('Linear', "Линейная регрессия"), ('Tree', "Решающее дерево")], validators=[DataRequired()])
    p2 = RadioField('Проблема', choices=[('Regression','Регрессия'),('Classification','Классификация')])
    p3 = RadioField('Если вы выбрали RandomForest, выберите количество деревьев в лесу', choices=[('50', '50'),('100', '100'), ('150', '150'), ('200', '200'), ('0', 'Я выбрал другой тип модели')], validators=[DataRequired()])
    p4 = RadioField("Если вы выбрали RandomForest или Решающее дерево, выберите максимальную глубину", choices=[('5', '5'),('10', '10'), ('15', '15'), ('20', '20'), ('0', 'Я выбрал другой тип модели')], validators=[DataRequired()])
    p5 = RadioField("Если вы выбрали KNN, выберите количество соседей", choices=[('1', '1'),('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('0', 'Я выбрал другой тип модели')], validators=[DataRequired()])
    p6 = RadioField("Выберите количество образцов в выборке", choices=[('1000', '1000'), ('2000', '2000'), ('3000', '3000'), ('4000', '4000'), ('5000', '5000'), ('6000', '6000'), ('7000', '7000')], validators=[DataRequired()])
    submit = SubmitField('Далее')
