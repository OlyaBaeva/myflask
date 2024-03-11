from logging import Manager

from flask import Flask, request, make_response, render_template, session
from forms import MyForm
an_app = Flask(__name__)

an_app.config['SECRET_KEY'] = 'MyLittlePony'

@an_app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@an_app.route("/form")
def form(name=None):
        return render_template('form.html')


@an_app.route("/", methods=['GET', 'POST'])
def index():
    if 'name' in session:
       name = session['name']
       email = session['email']
       phone = session['phone']
    else:
       name = None
       email = None
       phone = None
    mes = None
    form = MyForm()
    if form.validate_on_submit():
      session['name'] = form.name.data
      session['email'] = form.email.data
      session['phone'] = form.phone.data
      session['mes'] = form.message.data
      return render_template('form.html', form=form, name=session['name'], email=session['email'], phone=session['phone'], message=session['mes'])
    return render_template('res.html', form=form, name=name, email=email, phone=phone, message=mes)

if __name__ == '__main__':
    an_app.run(debug=True)