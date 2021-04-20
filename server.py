import os

from flask import Flask, render_template, redirect, make_response, request, session, jsonify
from werkzeug.exceptions import abort
import requests
import schedule
import datetime
import tzlocal
from requests import get, post, delete
from data import db_session
from data.users import User
from data.friend_requests import FriendRequest
from data.countries import Country
from data.types import Type
from data.tasks import Task
from forms.friend_request import FriendRequestForm
from forms.profile import GetPictureForm
from forms.task import TaskForm
from forms.tasks_search import TasksSearchForm
from forms.user import RegisterForm
from data import tasks_resources,users_resources,types_resources,countries_resources,friend_requests_resources
from data.get_map_picture import get_map_picture
from data.get_remaining_time_str import get_remaining_time_str
from forms.LoginForm import LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource
from data.edit_profile_picture import edit_profile_picture
from flask_ngrok import run_with_ngrok

with open('data/current_time_zone.txt', 'w') as file:
    file.write(f'UTC: {datetime.datetime.now(tzlocal.get_localzone()).tzname()}')
    file.close()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
#run_with_ngrok(app)
login_manager = LoginManager()
login_manager.init_app(app)

def main():
    db_session.global_init("db/plan_maker.db")
    db_sess = db_session.create_session()
    api.add_resource(tasks_resources.TasksListResource, '/api/tasks')
    api.add_resource(tasks_resources.TaskResource, '/api/tasks/<int:task_id>')
    api.add_resource(users_resources.UsersListResource, '/api/users')
    api.add_resource(users_resources.UserResource, '/api/users/<int:user_id>')
    api.add_resource(types_resources.TypesListResource, '/api/types')
    api.add_resource(types_resources.TypeResource, '/api/types/<int:type_id>')
    api.add_resource(countries_resources.CountriesListResource, '/api/countries')
    api.add_resource(countries_resources.CountryResource, '/api/countries/<int:country_id>')
    api.add_resource(friend_requests_resources.FriendRequestsListResource, '/api/friend_requests')
    api.add_resource(friend_requests_resources.FriendRequestResource, '/api/friend_requests/<int:friend_request_id>')
    schedule.every().day.at("00:00").do(delete_old_tasks)
    # app.run(port=80, host='127.0.0.1', debug=True)
    #app.run()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def delete_old_tasks():
    db_sess = db_session.create_session()
    tasks = db_sess.query(Task).all()
    tasks = list(filter(lambda x: x.date - datetime.datetime.now() < -604800,tasks))
    for item in tasks:
        db_sess.delete(item)
    db_sess.commit()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/task_join/<int:id>')
@login_required
def task_join(id):
    db_sess = db_session.create_session()
    task = db_sess.query(Task).get(id)
    if task.is_private:
        abort(404)
    else:
        user = db_sess.query(User).get(current_user.id)
        task.set_participates(task.get_participates_list() + [user.id])
        user.tasks.append(task)
        db_sess.commit()
        return redirect(request.referrer)
@app.route('/task_info/<int:id>')
@login_required
def task_info(id):
    db_sess = db_session.create_session()
    task = db_sess.query(Task).get(id)
    if task in current_user.tasks or not task.is_private:
        task.type_name = db_sess.query(Type).get(task.type).title
        task.country_name = db_sess.query(Country).get(task.country).name
        members = [task.creator]+[db_sess.query(User).get(member_id) for member_id in task.get_participates_list()]
        task.remaining_time = get_remaining_time_str(task.date - datetime.datetime.now())
        if task.participating and current_user.id in task.get_participates_list():
            task.current_user_is_participating = True
        else:
            task.current_user_is_participating = False
        task.time_offset = open('data/current_time_zone.txt','r',encoding='utf-8').readline()
        return render_template('task_info.html', task=task,members=members, required_css=['task_info'],title=task.title)
    else:
        abort(404)
@app.route('/task_leave/<int:id>')
@login_required
def task_leave(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    task = db_sess.query(Task).get(id)
    if task in user.tasks:
        user.tasks.remove(task)
        members = task.get_participates_list()
        members.remove(user.id)
        task.set_participates(members)
        db_sess.commit()
        return redirect(request.referrer)
    else:
        abort(404)
@app.route('/friend_delete/<int:id>')
@login_required
def friend_delete(id):
    if id in current_user.get_friends_list():
        db_sess = db_session.create_session()
        friend = db_sess.query(User).get(id)
        user = db_sess.query(User).get(current_user.id)
        friends = friend.get_friends_list()
        cur_user_friends = user.get_friends_list()
        friends.remove(user.id)
        cur_user_friends.remove(id)
        friend.set_friends(friends)
        user.set_friends(cur_user_friends)
        db_sess.commit()
        return redirect(request.referrer)
    else:
        abort(404)

@app.route('/profile_opened_tasks/<int:id>', methods=['GET', 'POST'])
@login_required
def profile_opened_tasks(id):
    picture_file_name_list = os.listdir('static/img')
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    user.country_name = db_sess.query(Country).get(user.country_from).name
    user.date_of_birth_str = user.date_of_birth.strftime("%Y-%m-%d")
    user.friend_list = []
    if user.friends:
        user.friend_list = [db_sess.query(User).get(friend_id) for friend_id in user.get_friends_list()]
    for friend in user.friend_list:
        if f'{friend.id}_profile_picture.png' in picture_file_name_list:
            friend.profile_picture_finded = True
        else:
            friend.profile_picture_finded = False
    if f'{user.id}_profile_picture.png' in picture_file_name_list:
        user.profile_picture_finded = True
    else:
        user.profile_picture_finded = False
    tasks = list(filter(lambda x: not x.is_private, user.tasks))
    for task in tasks:
        if task.participating and current_user.id in task.get_participates_list():
            task.current_user_is_participating = True
        else:
            task.current_user_is_participating = False
        task.remaining_time = get_remaining_time_str(task.date - datetime.datetime.now())
        task.displayable_information = [
            f"Страна: {db_sess.query(Country).get(task.country).name}",
            f"Адрес: {task.address}"]
    return render_template('profile_opened_tasks.html', required_css=['profile'], user=user, tasks=tasks,title='Открытые мероприятия')
@app.route('/profile_friend_requests', methods=['GET', 'POST'])
@login_required
def profile_friend_requests():
    picture_file_name_list = os.listdir('static/img')
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    if f'{user.id}_profile_picture.png' in picture_file_name_list:
        user.profile_picture_finded = True
    else:
        user.profile_picture_finded = False
    friend_list = [db_sess.query(User).get(friend_request.sended_by) for friend_request in db_sess.query(FriendRequest).filter(FriendRequest.received_by == current_user.id)]
    for friend in friend_list:
        if f'{friend.id}_profile_picture.png' in picture_file_name_list:
            friend.profile_picture_finded = True
        else:
            friend.profile_picture_finded = False
    return render_template('profile_friend_requests.html', required_css=['profile'], user=user,
                           user_list=friend_list,title='Запросы в друзья')


@app.route('/friend_accept/<int:id>')
@login_required
def friend_accept(id):
    db_sess = db_session.create_session()
    friendrequest = db_sess.query(FriendRequest).filter(FriendRequest.sended_by == id,FriendRequest.received_by == current_user.id).first()
    if friendrequest:
        user = db_sess.query(User).get(current_user.id)
        friend = db_sess.query(User).get(id)
        user.set_friends(user.get_friends_list()+[id])
        friend.set_friends(friend.get_friends_list() + [user.id])
        db_sess.delete(friendrequest)
        db_sess.commit()
        return redirect(request.referrer)
    else:
        abort(404)

@app.route('/friend_add/<int:id>')
@login_required
def friend_add(id):
    db_sess = db_session.create_session()
    if not db_sess.query(FriendRequest).filter(FriendRequest.sended_by == current_user.id,FriendRequest.received_by == id).first():
        friendrequest = FriendRequest(sended_by=current_user.id, received_by=id)
        db_sess.add(friendrequest)
        db_sess.commit()
        return redirect(request.referrer)
    else:
        abort(404)

@app.route('/profile_find_friends', methods=['GET', 'POST'])
@login_required
def profile_find_friends():
    user_list = []
    picture_file_name_list = os.listdir('static/img')
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    if f'{user.id}_profile_picture.png' in picture_file_name_list:
        user.profile_picture_finded = True
    else:
        user.profile_picture_finded = False
    form = FriendRequestForm()
    if request.method == "GET":
        if user.id != current_user.id:
            abort(404)
    if form.validate_on_submit():
        if user.id == current_user.id:
            user_list = list(map(lambda x: (x,f'{x.name} {x.surname}'),db_sess.query(User).all()))
            if user_list:
                friend_list = current_user.get_friends_list()
                user_list = list(filter(lambda x: form.name.data in x[1] and not db_sess.query(FriendRequest).filter(FriendRequest.sended_by == current_user.id,FriendRequest.received_by==x[0].id).first() and current_user.id != x[0].id and x[0].id not in friend_list,user_list))
                user_list = list(map(lambda x: x[0], user_list))
                for item in user_list:
                    if f'{item.id}_profile_picture.png' in picture_file_name_list:
                        item.profile_picture_finded = True
                    else:
                        item.profile_picture_finded = False
            return render_template('profile_find_friends.html', required_css=['profile'], user=user, form=form, user_list=user_list)
        else:
            abort(404)
    return render_template('profile_find_friends.html', required_css=['profile'], user=user, form=form, user_list=user_list,title='Найти друзей')

@app.route('/profile_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def profile_edit(id):
    picture_file_name_list = os.listdir('static/img')
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    if f'{user.id}_profile_picture.png' in picture_file_name_list:
        user.profile_picture_finded = True
    else:
        user.profile_picture_finded = False
    form = GetPictureForm()
    if request.method == "GET":
        if user.id == current_user.id:
            form.name.data = user.name
            form.surname.data = user.surname
            form.city_from.data = user.city_from
            form.country_from.choices = [(country.id, country.name) for country in db_sess.query(Country).all()]
            form.country_from.choices.insert(0, form.country_from.choices.pop(form.country_from.choices.index(
                (user.country_from, db_sess.query(Country).get(user.country_from).name))))
        else:
            abort(404)
    if form.validate_on_submit():
        if user.id == current_user.id:
            user.name = form.name.data
            user.surname = form.surname.data
            user.city_from = form.city_from.data
            user.country_from = form.country_from.data
            if form.picture.data:
                form.picture.data.save(f'static/img/{user.id}_profile_picture.png')
                edit_profile_picture(f'static/img/{user.id}_profile_picture.png')
            db_sess.commit()
            return redirect(f'/profile/{user.id}')
        else:
            abort(404)
    return render_template('profile_edit.html', required_css=['profile'], user=user, form=form,title='Редактировать')

@app.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    picture_file_name_list = os.listdir('static/img')
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    user.country_name = db_sess.query(Country).get(user.country_from).name
    user.date_of_birth_str = user.date_of_birth.strftime("%Y-%m-%d")
    user.friend_list = []
    if user.friends:
        user.friend_list = [db_sess.query(User).get(friend_id) for friend_id in user.get_friends_list()]
    for friend in user.friend_list:
        if f'{friend.id}_profile_picture.png' in picture_file_name_list:
            friend.profile_picture_finded = True
        else:
            friend.profile_picture_finded = False
    if f'{user.id}_profile_picture.png' in picture_file_name_list:
        user.profile_picture_finded = True
    else:
        user.profile_picture_finded = False
    return render_template('profile.html',required_css=['profile'], user=user,title='Профиль')

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        tasks = current_user.tasks
        form = TasksSearchForm()
        form.country.choices += [(country.id, country.name) for country in db_sess.query(Country).all()]
        form.type.choices += [(types.id, types.title) for types in db_sess.query(Type).all()]
        if form.validate_on_submit():
            tasks = current_user.tasks
            if form.country.data != '0':
                tasks = list(filter(lambda x: int(form.country.data) == x.country, tasks))
            if form.type.data != '0':
                tasks = list(filter(lambda x: int(form.type.data) == x.type, tasks))
            if form.search_line.data:
                if form.search_item.data == '0':
                    tasks = list(filter(lambda x: form.search_line.data.lower() in x.address.lower(), tasks))
                elif form.search_item.data  == '1':
                    tasks = list(filter(lambda x: form.search_line.data.lower() in x.title.lower(), tasks))
                elif form.search_item.data  == '2':
                    tasks = list(filter(lambda x: form.search_line.data.lower() in x.description.lower(), tasks))
        for task in tasks:
            if task.participating and current_user.id in task.get_participates_list():
                task.current_user_is_participating = True
            else:
                task.current_user_is_participating = False
            members = [db_sess.query(User).get(member_id) for member_id in
                       task.get_participates_list()+[task.creator_id]]
            members = list(map(lambda x: f"{x.name} {x.surname}" if current_user.id != x.id else 'Вы', members))
            members.insert(0,members.pop(members.index('Вы')))
            if len(members) > 3:
                members = members[:3] + ['....']
            members = ', '.join(members)
            task.remaining_time = get_remaining_time_str(task.date - datetime.datetime.now())
            task.displayable_information = [
                f"Страна: {db_sess.query(Country).get(task.country).name}",
                f"Адрес: {task.address}", f"Участники: {members}"]
        return render_template('index.html', tasks=tasks, type='private',form=form,title='Личные мероприятия')
    else:
        return render_template("base.html",title='Главная')


@app.route('/public')
@login_required
def public():
    db_sess = db_session.create_session()
    tasks = db_sess.query(Task).filter(Task.is_private == 0)
    form = TasksSearchForm()
    form.country.choices += [(country.id, country.name) for country in db_sess.query(Country).all()]
    form.type.choices += [(types.id, types.title) for types in db_sess.query(Type).all()]
    if form.validate_on_submit():
        tasks = current_user.tasks
        if form.country.data != '0':
            tasks = list(filter(lambda x: int(form.country.data) == x.country, tasks))
        if form.type.data != '0':
            tasks = list(filter(lambda x: int(form.type.data) == x.type, tasks))
        if form.search_line.data:
            if form.search_item.data == '0':
                tasks = list(filter(lambda x: form.search_line.data.lower() in x.address.lower(), tasks))
            elif form.search_item.data == '1':
                tasks = list(filter(lambda x: form.search_line.data.lower() in x.title.lower(), tasks))
            elif form.search_item.data == '2':
                tasks = list(filter(lambda x: form.search_line.data.lower() in x.description.lower(), tasks))
    for task in tasks:
        if task.participating and current_user.id in task.get_participates_list():
            task.current_user_is_participating = True
        else:
            task.current_user_is_participating = False
        task.remaining_time = get_remaining_time_str(task.date - datetime.datetime.now())
        task.displayable_information = [
            f"Страна: {db_sess.query(Country).get(task.country).name}",
            f"Адрес: {task.address}"]
    return render_template('index.html', tasks=tasks, type='public',form=form,title='Публичные мероприятия')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/task_delete/<int:id>')
@login_required
def task_delete(id):
    db_sess = db_session.create_session()
    task = db_sess.query(Task).get(id)
    if task and current_user == task.creator:
        db_sess.delete(task)
        db_sess.commit()
        return redirect('/')
    else:
        abort(404)


@app.route('/tasks/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    picture_name_list = os.listdir('static/img')
    form = TaskForm()
    db_sess = db_session.create_session()
    if request.method == "GET":
        task = db_sess.query(Task).get(id)
        if task:
            if current_user == task.creator:
                if current_user.friends:
                    friends = [db_sess.query(User).get(friend_id) for friend_id in
                               current_user.get_friends_list()]
                    form.friend_invited.choices = [(str(friend.id), f'{friend.name} {friend.surname}') for friend in
                                                   friends]
                if task.participating:
                    for user in [db_sess.query(User).get(user_id) for user_id in task.get_participates_list()]:
                        if (str(user.id), f'{user.name} {user.surname}') not in form.friend_invited.choices:
                            form.friend_invited.choices.append((str(user.id), f'{user.name} {user.surname}'))
                form.title.data = task.title
                form.description.data = task.description
                form.friend_invited.data = task.participating.split(', ')
                form.address.data = task.address
                form.date.data = task.date
                form.is_private.data = task.is_private
                form.is_address_displayed.data = task.is_address_displayed
                form.country.choices = [(country.id, country.name) for country in db_sess.query(Country).all()]
                form.type.choices = [(types.id, types.title) for types in db_sess.query(Type).all()]
                form.type.choices.insert(0, form.type.choices.pop(form.type.choices.index(
                    (task.type, db_sess.query(Type).get(task.type).title))))
                form.country.choices.insert(0,form.country.choices.pop(form.country.choices.index((task.country, db_sess.query(Country).get(task.country).name))))
            else:
                abort(404)
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        task = db_sess.query(Task).get(id)
        if task:
            old_type = db_sess.query(Type).get(task.type)
            old_type.tasks.remove(task)
            old_country = db_sess.query(Country).get(task.country)
            old_country.tasks.remove(task)
            for friend in [db_sess.query(User).get(friend_id) for friend_id in
                           task.get_participates_list()]:
                friend.tasks.remove(task)
            db_sess.commit()
            task.title = form.title.data
            task.description = form.description.data
            task.type = form.type.data
            task.set_participates(form.friend_invited.data)
            task.country = form.country.data
            task.address = form.address.data
            task.date = form.date.data
            task.is_private = form.is_private.data
            task.is_address_displayed = form.is_address_displayed.data
            picked_type = db_sess.query(Type).get(form.type.data)
            picked_type.tasks.append(task)
            picked_country = db_sess.query(Country).get(form.country.data)
            picked_country.tasks.append(task)
            for friend in [db_sess.query(User).get(int(friend_id)) for friend_id in
                           form.friend_invited.data]:
                friend.tasks.append(task)
            if task.is_address_displayed:
                get_map_picture(task.id,task.address)
            elif f'{task.id}_map_picture.jpg' in picture_name_list and not task.is_address_displayed:
                os.remove(f'static/img/{task.id}_map_picture.jpg')
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('tasks.html',
                           title='Изменить мероприятие',
                           form=form)


@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def add_task():
    db_sess = db_session.create_session()
    form = TaskForm()
    form.country.choices = [(country.id, country.name) for country in db_sess.query(Country).all()]
    form.type.choices = [(types.id, types.title) for types in db_sess.query(Type).all()]
    form.country.choices.insert(0, form.country.choices.pop(form.country.choices.index(
        (current_user.country_from, db_sess.query(Country).get(current_user.country_from).name))))
    if current_user.friends:
        friends = [db_sess.query(User).get(friend_id) for friend_id in
                   current_user.get_friends_list()]
        form.friend_invited.choices = [(str(friend.id), f'{friend.name} {friend.surname}') for friend in friends]
    if form.validate_on_submit():
        task = Task()
        task.creator_id = current_user.id
        task.creator = current_user
        task.title = form.title.data
        task.description = form.description.data
        task.type = form.type.data
        task.set_participates(form.friend_invited.data)
        task.country = form.country.data
        task.address = form.address.data
        task.date = form.date.data
        task.is_private = form.is_private.data
        task.is_address_displayed = form.is_address_displayed.data
        db_sess.add(task)
        picked_type = db_sess.query(Type).get(form.type.data)
        picked_type.tasks.append(task)
        picked_country = db_sess.query(Country).get(form.country.data)
        picked_country.tasks.append(task)
        for friend in [db_sess.query(User).get(int(friend_id)) for friend_id in
                       form.friend_invited.data]:
            friend.tasks.append(task)
        current_user.tasks.append(task)
        db_sess.commit()
        if task.is_address_displayed:
            get_map_picture(task.id, task.address)
        return redirect('/')
    return render_template('tasks.html', title='Добавить мероприятие',
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form,title='Авторизация')
    return render_template('login.html', title='Авторизация', form=form,)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    db_sess = db_session.create_session()
    form = RegisterForm()
    form.country_from.choices = [(country.id, country.name) for country in db_sess.query(Country).all()]
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            date_of_birth=form.date_of_birth.data,
            city_from=form.city_from.data,
            country_from=form.country_from.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

if __name__ == '__main__':
    main()
