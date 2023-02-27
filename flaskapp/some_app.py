from flask import Flask
from PIL import Image
from flask import render_template
import numpy as np
from flask_bootstrap import Bootstrap
import os
import net as nt
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired



app = Flask(__name__)


@app.route("/")
def hello():
    return " <html><head></head> <body> Hello World! </body></html>"


# csrf токен
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта Google
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfYrbckAAAAABrTHP-iUaegcp_ksIE-9UPIH-TH'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfYrbckAAAAAAe68Hy1MXhr_zIzp0xC3SmKmuPR'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами

bootstrap = Bootstrap(app)
# создаем форму для загрузки файла
class NetForm(FlaskForm):
    # поле для ввода периода
    period = StringField('period', validators = [DataRequired()])
    # поле загрузки файла
    upload = FileField('Load image', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    # поле формы с capture
    recaptcha = RecaptchaField()
    #кнопка submit, для пользователя отображена как send
    submit = SubmitField('send')


@app.route("/net",methods=['GET', 'POST'])
def net():
    # здесь зраним рабочую директорию
    directory = os.getcwd()
    # создаем объект формы
    form = NetForm()
    # обнуляем переменные, передаваемые в форму
    old_image = None
    new_image = None
    new_image_clr = None
    old_image_clr = None
    neurodic = {}
    # проверяем нажатие сабмит и валидацию введенных данных
    if form.validate_on_submit():
        # обрабатываем загруженную картинку и сохраняем ее на жесткий диск
        stream = form.data['upload'].stream
        filename = form.data['upload'].filename
        img = Image.open(stream)
        img.save(f'{directory}/static/{filename}')

        #функция сохраняет обновленную картинку и возвразает нам путь к ней
        new_file = nt.convert_image(filename, float(form.period.data))


        # чтобы вызвать функцию распределения цветов, нужно передать ей картинку в виде тензора
        matr = np.array(Image.open(f'{directory}/static/{filename}'))

        # у новых картинок есть суффикс _new  в названии. Добавляем его к исходному
        # наванию, чтобы получить картинку
        name, extension = filename.rsplit('.')
        matr1 = np.array(Image.open(f'{directory}/static/{name}_new.{extension}'))


        # даем переменным, которые мы передаем в форму, вид который этой формой будет считан
        old_image_clr = './static/'+nt.color_distribution_image(filename, matr)
        new_image_clr = './static/'+nt.color_distribution_image(new_file, matr1)
        old_image = './static/'+filename
        new_image = './static/'+new_file

    return render_template('net.html',form=form,
                           old_image=old_image,
                           old_image_clr = old_image_clr,
                           new_image=new_image,
                           new_image_clr = new_image_clr,)



if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
