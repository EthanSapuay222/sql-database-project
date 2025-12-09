from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from datetime import datetime, timedelta
from model import User, ActivityLog
from database import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Display login page or handle login form submission"""
    if request.method == 'GET':
        return render_template('Login.html')
    
    # POST requests are handled by specific routes below
    return redirect(url_for('auth.login'))


@auth.route('/user_login', methods=['POST'])
def user_login():
    """Handle user login via username"""
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Validation
        if not username or not password:
            flash('Username and password are required', 'user_error')
            return render_template('Login.html')
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if not user or user.password != password:
            flash('Invalid username or password', 'user_error')
            return render_template('Login.html')
        
        if not user.is_active:
            flash('Your account has been deactivated', 'user_error')
            return render_template('Login.html')
        
        # Create session
        session['user_id'] = user.user_id
        session['username'] = user.username
        session['user_role'] = user.user_role
        
        try:
            # Update last login
            user.last_login = datetime.now()
            db.session.commit()
            
            # Log activity
            activity = ActivityLog(
                user_id=user.user_id,
                action_type='User Login',
                description=f'User {user.username} logged in',
                created_at=datetime.now()
            )
            db.session.add(activity)
            db.session.commit()
        except Exception as log_error:
            # Continue anyway, don't block login
            pass
        
        flash(f'Welcome back, {user.full_name}!', 'register_success')
        return redirect(url_for('pages.index'))
        
    except Exception as e:
        flash('An error occurred during login', 'user_error')
        return render_template('Login.html')


@auth.route('/user_register', methods=['POST'])
def user_register():
    """Handle user registration"""
    try:
        full_name = request.form.get('full_name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validation
        errors = []
        
        if not all([full_name, username, password, confirm_password]):
            errors.append('All fields are required')
        
        if len(username) < 3:
            errors.append('Username must be at least 3 characters')
        
        if len(password) < 6:
            errors.append('Password must be at least 6 characters')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        # Check for existing user
        if User.query.filter_by(username=username).first():
            errors.append('Username already taken')
        
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        # Create new user
        new_user = User(
            username=username,
            password=password,
            full_name=full_name,
            user_role='public',
            is_active=True
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Log activity
        activity = ActivityLog(
            user_id=new_user.user_id,
            action_type='User Registration',
            description=f'New user {username} registered',
            created_at=datetime.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully! You can now log in.'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'errors': ['An error occurred during registration']
        }), 500


@auth.route('/admin_login', methods=['POST'])
def admin_login():
    """Handle admin login"""
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        remember = request.form.get('remember') == 'on'
        
        # Validation
        if not username or not password:
            flash('Username and password are required', 'admin_error')
            return render_template('AdminLogin.html')
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if not user or user.password != password:
            flash('Invalid username or password', 'admin_error')
            return render_template('AdminLogin.html')
        
        # Check if user is admin
        if user.user_role != 'admin':
            flash('You do not have admin privileges', 'admin_error')
            
            # Log failed admin login attempt
            activity = ActivityLog(
                user_id=user.user_id,
                action_type='Failed Admin Login',
                description=f'Non-admin user {username} attempted admin login',
                created_at=datetime.now()
            )
            db.session.add(activity)
            db.session.commit()
            
            return render_template('AdminLogin.html')
        
        if not user.is_active:
            flash('Your account has been deactivated', 'admin_error')
            return render_template('AdminLogin.html')
        
        # Create admin session
        session['user_id'] = user.user_id
        session['username'] = user.username
        session['user_role'] = user.user_role
        session['is_admin'] = True
        
        if remember:
            session.permanent = True
        
        # Update last login
        user.last_login = datetime.now()
        db.session.commit()
        
        # Log admin login
        activity = ActivityLog(
            user_id=user.user_id,
            action_type='Admin Login',
            description=f'Admin {username} logged in',
            created_at=datetime.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        flash(f'Welcome, Admin {user.full_name}!', 'register_success')
        return redirect(url_for('pages.admin_dashboard'))
        
    except Exception as e:
        flash('An error occurred during admin login', 'admin_error')
        return render_template('AdminLogin.html')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    """Handle user logout"""
    try:
        if 'user_id' in session:
            user_id = session['user_id']
            username = session.get('username', 'Unknown')
            
            # Log logout activity
            activity = ActivityLog(
                user_id=user_id,
                action_type='User Logout',
                description=f'User {username} logged out',
                created_at=datetime.now()
            )
            db.session.add(activity)
            db.session.commit()
        
        session.clear()
        flash('You have been logged out', 'register_success')
    except Exception as e:
        pass
    
    return redirect(url_for('pages.index'))
