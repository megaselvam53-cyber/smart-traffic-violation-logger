from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_user, logout_user, login_required
from app import db, login_manager
from app.models import Violation, User
from app.forms import ViolationForm, LoginForm
from app.utils import generate_qr_code
from datetime import datetime
from sqlalchemy import func
import csv
from io import StringIO

main = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ================= LOGIN =================
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect('/history')   # 🔥 simple redirect

        flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)


# ================= LOGOUT =================
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


# ================= HOME =================
@main.route('/')
def index():
    return render_template('index.html')


# ================= ADD VIOLATION =================
@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_violation():
    form = ViolationForm()

    if form.validate_on_submit():
        violation = Violation(
            vehicle_number=form.vehicle_number.data.upper(),
            violation_type=form.violation_type.data,
            location=form.location.data,
            fine_amount=form.fine_amount.data,
            status="Pending"
        )

        db.session.add(violation)
        db.session.commit()

        qr_path = generate_qr_code(violation.id, violation.vehicle_number)
        violation.qr_code_path = qr_path
        db.session.commit()

        flash('Violation added!', 'success')
        return redirect(url_for('main.history'))

    return render_template('add_violation.html', form=form)


# ================= HISTORY =================
@main.route('/history')
@login_required
def history():
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    date = request.args.get('date', '')

    query = Violation.query

    if search:
        query = query.filter(Violation.vehicle_number.like(f'%{search.upper()}%'))

    if status_filter:
        query = query.filter(Violation.status == status_filter)

    if date:
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        query = query.filter(func.date(Violation.date) == selected_date)

    violations = query.order_by(Violation.date.desc()).all()

    return render_template(
        'history.html',
        violations=violations,
        search=search,
        status_filter=status_filter,
        date=date
    )


# ================= UPDATE STATUS =================
@main.route('/update_status/<int:violation_id>', methods=['POST'])
@login_required
def update_status(violation_id):
    violation = Violation.query.get_or_404(violation_id)

    violation.status = "Paid"
    db.session.commit()

    flash('Marked as Paid!', 'success')
    return redirect(url_for('main.history'))


# ================= PUBLIC STATUS =================
@main.route('/status/<int:violation_id>')
def public_status(violation_id):
    violation = Violation.query.get_or_404(violation_id)
    return render_template('public_status.html', violation=violation)


# ================= EXPORT CSV =================
@main.route('/export-csv')
@login_required
def export_csv():
    violations = Violation.query.all()

    si = StringIO()
    cw = csv.writer(si)

    cw.writerow(['ID','Vehicle','Violation','Location','Date','Fine','Status'])

    for v in violations:
        cw.writerow([
            v.id,
            v.vehicle_number,
            v.violation_type,
            v.location,
            v.date.strftime('%Y-%m-%d %H:%M'),
            v.fine_amount,
            v.status
        ])

    return send_file(
        StringIO(si.getvalue()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='violations.csv'
    )