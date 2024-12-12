
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator

VALID_TABLES = ['Rooms', 'Clients', 'Services', 'Posts', 'Staff', 'Bookings', 'Provided_Services']
@login_required
def index(request):
    if request.user.is_staff:
        tables = VALID_TABLES
    else:
        tables = ['Clients', 'Rooms', 'Services', 'Bookings', 'Provided_Services']

    selected_table = request.GET.get('table')
    data = None
    total_cost = None
    salary_update_message = None

    if request.user.is_staff and selected_table == 'Posts' and 'increase_salary' in request.GET:
        with connection.cursor() as cursor:
            cursor.execute("SELECT IncreaseSalaryBy10Percent()")
            salary_update_message = cursor.fetchone()[0]
        return HttpResponseRedirect(f"/?table={selected_table}")

    
    if request.user.is_staff and selected_table == 'Bookings' and 'calculate_total_cost' in request.GET:
        with connection.cursor() as cursor:
            cursor.execute("SELECT GetTotalBookingsCost()")
            total_cost = cursor.fetchone()[0]

    
    filter_params = {}
    
    
    

    
    search_mode = 'search' in request.GET
    bookings = []
    post_list = []
    staff_list = []
    client_list = []
    room_list = []
    services = []
    
    if selected_table == 'Rooms':
        
        p_Room_ID = request.GET.get('room_id', '').strip()
        p_Type = request.GET.get('type_param', '').strip()
        p_Cost_per_night = request.GET.get('cost_param', '').strip()

        
        if p_Room_ID == '':
            p_Room_ID = None
        else:
            p_Room_ID = int(p_Room_ID)

        if p_Type == '':
            p_Type = None

        if p_Cost_per_night == '':
            p_Cost_per_night = None
        else:
            p_Cost_per_night = float(p_Cost_per_night)

        filter_params = {
            'procedure': 'FilterRooms',
            'params': [p_Room_ID, p_Type, p_Cost_per_night]
        }

    elif selected_table == 'Clients':  
        p_Fullname = request.GET.get('fullname', '').strip()
        p_Year_of_birth = request.GET.get('year_of_birth', '').strip()
        p_Gender = request.GET.get('gender', '').strip()
        p_Username = request.GET.get('username_param', '').strip()

        if p_Fullname == '':
            p_Fullname = None
        if p_Year_of_birth == '':
            p_Year_of_birth = None
        else:
            p_Year_of_birth = int(p_Year_of_birth)
        if p_Gender == '':
            p_Gender = None
        if p_Username == '':
            p_Username = None

        filter_params = {
            'procedure': 'FilterClients',
            'params': [p_Fullname, p_Year_of_birth, p_Gender, p_Username]
        }

    elif selected_table == 'Services':
        p_Name = request.GET.get('name', '').strip()
        p_Cost = request.GET.get('cost', '').strip()
        p_Description = request.GET.get('description', '').strip()

        if p_Name == '':
            p_Name = None
        if p_Cost == '':
            p_Cost = None
        else:
            p_Cost = float(p_Cost)
        if p_Description == '':
            p_Description = None

        filter_params = {
            'procedure': 'FilterServices',
            'params': [p_Name, p_Cost, p_Description]
        }

    elif selected_table == 'Posts':
        p_Name = request.GET.get('post_name', '').strip()
        p_Salary = request.GET.get('salary', '').strip()
        p_Description = request.GET.get('post_description', '').strip()

        if p_Name == '':
            p_Name = None
        if p_Salary == '':
            p_Salary = None
        else:
            p_Salary = float(p_Salary)
        if p_Description == '':
            p_Description = None

        filter_params = {
            'procedure': 'FilterPosts',
            'params': [p_Name, p_Salary, p_Description]
        }

    elif selected_table == 'Staff':
        p_Fullname = request.GET.get('staff_fullname', '').strip()
        p_Year_of_birth = request.GET.get('staff_year_of_birth', '').strip()
        p_Gender = request.GET.get('staff_gender', '').strip()
        p_Post_ID = request.GET.get('staff_post_id', '').strip()

        with connection.cursor() as cursor:
            cursor.execute("CALL GetPostsInfo()")
            post_list = cursor.fetchall()  

        if p_Fullname == '':
            p_Fullname = None
        if p_Year_of_birth == '':
            p_Year_of_birth = None
        else:
            p_Year_of_birth = int(p_Year_of_birth)
        if p_Gender == '':
            p_Gender = None
        if p_Post_ID == '':
            p_Post_ID = None
        else:
            p_Post_ID = int(p_Post_ID)

        filter_params = {
            'procedure': 'FilterStaff',
            'params': [p_Fullname, p_Year_of_birth, p_Gender, p_Post_ID]
        }

    elif selected_table == 'Bookings':
        p_Room_ID = request.GET.get('booking_room_id', '').strip()
        p_Client_ID = request.GET.get('booking_client_id', '').strip()
        p_Check_in_date = request.GET.get('booking_check_in_date', '').strip()
        p_Count_of_nights = request.GET.get('booking_count_of_nights', '').strip()
        p_Total_booking_cost = request.GET.get('booking_total_cost', '').strip()
        with connection.cursor() as cursor:
            cursor.execute("CALL GetClientsInfo()")
            if not request.user.is_staff:
                cursor.execute("CALL GetFilteredClientsInfo(%s);", (request.user.username,))
            else:
                cursor.execute("CALL GetClientsInfo();")
            client_list = cursor.fetchall()  
            cursor.execute("CALL GetRoomsInfo()")
            room_list = cursor.fetchall()  

        if p_Room_ID == '':
            p_Room_ID = None
        else:
            p_Room_ID = int(p_Room_ID)
        if p_Client_ID == '':
            p_Client_ID = None
        else:
            p_Client_ID = int(p_Client_ID)
        if p_Check_in_date == '':
            p_Check_in_date = None
        if p_Count_of_nights == '':
            p_Count_of_nights = None
        else:
            p_Count_of_nights = int(p_Count_of_nights)
        if p_Total_booking_cost == '':
            p_Total_booking_cost = None
        else:
            p_Total_booking_cost = float(p_Total_booking_cost)

        filter_params = {
            'procedure': 'FilterBookings',
            'params': [p_Room_ID, p_Client_ID, p_Check_in_date, p_Count_of_nights, p_Total_booking_cost]
        }

    elif selected_table == 'Provided_Services':
        p_Booking_ID = request.GET.get('ps_booking_id', '').strip()
        p_Staff_ID = request.GET.get('ps_staff_id', '').strip()
        p_Service_ID = request.GET.get('ps_service_id', '').strip()
        p_Count_of_services = request.GET.get('ps_count_of_services', '').strip()
        p_Total_service_cost = request.GET.get('ps_total_service_cost', '').strip()

        with connection.cursor() as cursor:
            if not request.user.is_staff:
                cursor.execute("CALL GetFilteredBookingInfo(%s);", (request.user.username,))
            else:
                cursor.execute("CALL GetBookingInfo();")
            bookings = cursor.fetchall()  

            cursor.execute("CALL GetServiceInfo();")
            services = cursor.fetchall()  
            cursor.execute("CALL GetStaffInfo()")
            staff_list = cursor.fetchall()  

        if p_Booking_ID == '':
            p_Booking_ID = None
        else:
            p_Booking_ID = int(p_Booking_ID)
        if p_Staff_ID == '':
            p_Staff_ID = None
        else:
            p_Staff_ID = int(p_Staff_ID)
        if p_Service_ID == '':
            p_Service_ID = None
        else:
            p_Service_ID = int(p_Service_ID)
        if p_Count_of_services == '':
            p_Count_of_services = None
        else:
            p_Count_of_services = int(p_Count_of_services)
        if p_Total_service_cost == '':
            p_Total_service_cost = None
        else:
            p_Total_service_cost = float(p_Total_service_cost)

        filter_params = {
            'procedure': 'FilterProvidedServices',
            'params': [p_Booking_ID, p_Staff_ID, p_Service_ID, p_Count_of_services, p_Total_service_cost]
        }

    
    if selected_table in tables:
        with connection.cursor() as cursor:
            if not request.user.is_staff:
                
                if selected_table == 'Clients':
                    
                    cursor.execute("SELECT * FROM Clients WHERE Username = %s;", [request.user.username])
                elif selected_table == 'Bookings':
                    
                    cursor.execute("""
                        SELECT * FROM Bookings
                        WHERE Client_ID = (
                            SELECT Client_ID FROM Clients WHERE Username = %s
                        );
                    """, [request.user.username])
                elif selected_table == 'Provided_Services':
                    
                    cursor.execute("""
                        SELECT * FROM Provided_Services
                        WHERE Booking_ID IN (
                            SELECT Booking_ID FROM Bookings
                            WHERE Client_ID = (
                                SELECT Client_ID FROM Clients WHERE Username = %s
                            )
                        );
                    """, [request.user.username])
                elif selected_table == 'Services' or selected_table == 'Rooms':
                    
                    if search_mode and filter_params:
                        
                        placeholders = ', '.join(['%s'] * len(filter_params['params']))
                        sql = f"CALL {filter_params['procedure']}({placeholders});"
                        cursor.execute(sql, filter_params['params'])
                    else:
                        
                        cursor.execute(f"SELECT * FROM {selected_table};")
                else:
                    cursor.execute(f"SELECT * FROM {selected_table};")

            else:
                
                if search_mode and filter_params and selected_table in VALID_TABLES:
                    placeholders = ', '.join(['%s'] * len(filter_params['params']))
                    sql = f"CALL {filter_params['procedure']}({placeholders});"
                    cursor.execute(sql, filter_params['params'])
                else:
                    
                    cursor.execute(f"SELECT * FROM {selected_table};")

            rows = cursor.fetchall()
            
            if selected_table:
                cursor.execute(f"DESCRIBE {selected_table};")
                columns = [col[0] for col in cursor.fetchall()]
            else:
                columns = []

        paginator = Paginator(rows, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        data = {
            'columns': columns,
            'rows': page_obj.object_list,
            'page_obj': page_obj,
        }

    return render(request, 'index.html', {
        'tables': tables,
        'selected_table': selected_table,
        'data': data,
        'is_read_only': not request.user.is_staff and (selected_table == 'Services' or selected_table == 'Rooms'),
        'total_cost': total_cost,
        'salary_update_message': salary_update_message,
        'bookings': bookings,
        'post_list': post_list,
        'staff_list': staff_list,
        'client_list': client_list,
        'room_list': room_list,
        'services': services,
    })
from django.shortcuts import redirect, render
from django.db import connection

@login_required
def delete_record(request, table, key1, key2=None, key3=None):
    primary_keys = {
        'Rooms': ['Room_ID'],
        'Clients': ['Client_ID'],
        'Services': ['Service_ID'],
        'Posts': ['Post_ID'],
        'Staff': ['Staff_ID'],
        'Bookings': ['Booking_ID'],
        'Provided_Services': ['Booking_ID', 'Staff_ID', 'Service_ID']
    }

    if table not in primary_keys:
        return redirect('index')

    keys = [key1]
    if key2:
        keys.append(key2)
    if key3:
        keys.append(key3)

    errors = []

    try:
        
        where_clause = ' AND '.join([f"{key} = %s" for key in primary_keys[table]])
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table} WHERE {where_clause}", keys)
        
        return redirect(f"/?table={table}")
    except Exception as e:
        
        errors.append(f"Ошибка удаления: {str(e)}")

    
    return render(request, 'index.html', {
        'tables': VALID_TABLES,
        'selected_table': table,
        'errors': errors,
    })


@login_required
def edit_record(request, table, key1, key2=None, key3=None):
    import datetime

    primary_keys = {
        'Rooms': ['Room_ID'],
        'Clients': ['Client_ID'],
        'Services': ['Service_ID'],
        'Posts': ['Post_ID'],
        'Staff': ['Staff_ID'],
        'Bookings': ['Booking_ID'],
        'Provided_Services': ['Booking_ID', 'Staff_ID', 'Service_ID']
    }

    if table not in primary_keys:
        return redirect('index')

    keys = [key1]
    if key2:
        keys.append(key2)
    if key3:
        keys.append(key3)

    errors = []

    if len(keys) != len(primary_keys[table]):
        errors.append("Не хватает ключей для идентификации записи.")
        return render(request, 'edit_record.html', {
            'table': table,
            'columns': [],
            'record': [],
            'errors': errors
        })

    if request.method == 'POST':
        try:
            form_data = {
                key: value.replace(',', '.') if ',' in value else value
                for key, value in request.POST.items() if key != 'csrfmiddlewaretoken'
            }

            if 'Gender' in form_data:
                gender_map = {'Мужской': 'М', 'Женский': 'Ж'}
                form_data['Gender'] = gender_map.get(form_data['Gender'], form_data['Gender'])

            set_clause = ', '.join([f"{key} = %s" for key in form_data.keys()])
            where_clause = ' AND '.join([f"{key} = %s" for key in primary_keys[table]])

            with connection.cursor() as cursor:
                cursor.execute(
                    f"UPDATE {table} SET {set_clause} WHERE {where_clause}",
                    list(form_data.values()) + keys
                )
            return redirect(f"/?table={table}")
        except Exception as e:
            errors.append(f"Ошибка: {str(e)}")

    post_choices = []
    try:
        with connection.cursor() as cursor:
            
            where_clause = ' AND '.join([f"{key} = %s" for key in primary_keys[table]])
            cursor.execute(f"SELECT * FROM {table} WHERE {where_clause}", keys)
            record = cursor.fetchone()

            if not record:
                errors.append("Запись не найдена.")
                return render(request, 'edit_record.html', {
                    'table': table,
                    'columns': [],
                    'record': [],
                    'errors': errors
                })

            columns = [desc[0] for desc in cursor.description]

            
            cursor.execute(f"DESCRIBE {table}")
            describe_info = {col[0]: col[5] for col in cursor.fetchall()}
            filtered_columns = [
                col for col in columns
                if not col.startswith('Total') and describe_info.get(col) != 'auto_increment' and not col.startswith('Check_out_date')
            ]

            
            formatted_record = []
            for col, val in zip(columns, record):
                if col in filtered_columns:
                    if isinstance(val, float):
                        formatted_record.append(f"{val:.2f}")
                    elif isinstance(val, (datetime.date, datetime.datetime)):
                        formatted_record.append(val.strftime('%Y-%m-%d'))
                    elif col == 'Gender' and table in ['Clients', 'Staff']:
                        formatted_record.append('Мужской' if val == 'М' else 'Женский')
                    else:
                        formatted_record.append(val)

            
            cursor.execute("CALL GetPostsInfo()")
            post_choices = cursor.fetchall()  

            if not request.user.is_staff:
                cursor.execute("CALL GetFilteredClientsInfo(%s);", (request.user.username,))
            else:
                cursor.execute("CALL GetClientsInfo();")
            client_choices = cursor.fetchall()  

            
            cursor.execute("CALL GetRoomsInfo()")
            room_choices = cursor.fetchall()  

            cursor.execute("CALL GetStaffInfo()")
            staff_list = cursor.fetchall()

            cursor.execute("CALL GetServiceInfo()")
            services = cursor.fetchall()

            if not request.user.is_staff:
                cursor.execute("CALL GetFilteredBookingInfo(%s);", (request.user.username,))
            else:
                cursor.execute("CALL GetBookingInfo();")
            bookings = cursor.fetchall()  



    except Exception as e:
        errors.append(f"Ошибка загрузки данных: {str(e)}")
        return render(request, 'edit_record.html', {
            'table': table,
            'columns': [],
            'record': [],
            'errors': errors
        })

    return render(request, 'edit_record.html', {
        'table': table,
        'columns': filtered_columns,
        'record': formatted_record,
        'errors': errors,
        'post_choices': post_choices,  
        'staff_list': staff_list,
        'client_choices': client_choices,  
        'room_choices': room_choices,  
        'username': request.user.username,  
        'bookings': bookings,
        'services': services,
    })
@login_required
def add_record(request, table):
    errors = []
    primary_keys = {
        'Rooms': ['Room_ID'],
        'Clients': ['Client_ID'],
        'Services': ['Service_ID'],
        'Posts': ['Post_ID'],
        'Staff': ['Staff_ID'],
        'Bookings': ['Booking_ID'],
        'Provided_Services': ['Booking_ID', 'Staff_ID', 'Service_ID']
    }

    if table not in primary_keys:
        return redirect('index')

    
    staff_list = []
    if table == 'Provided_Services':
        with connection.cursor() as cursor:
            cursor.execute("CALL GetStaffInfo()")
            staff_list = cursor.fetchall()  

    
    post_list = []
    with connection.cursor() as cursor:
        cursor.execute("CALL GetPostsInfo()")
        post_list = cursor.fetchall()  
        if not request.user.is_staff:
            cursor.execute("CALL GetFilteredBookingInfo(%s);", (request.user.username,))
        else:
            cursor.execute("CALL GetBookingInfo();")
        bookings = cursor.fetchall()  

        cursor.execute("CALL GetServiceInfo();")
        services = cursor.fetchall()  

    
    client_list = []
    room_list = []
    if table == 'Bookings':
        with connection.cursor() as cursor:
            cursor.execute("CALL GetClientsInfo()")
            if not request.user.is_staff:
                cursor.execute("CALL GetFilteredClientsInfo(%s);", (request.user.username,))
            else:
                cursor.execute("CALL GetClientsInfo();")
            client_list = cursor.fetchall()  
            cursor.execute("CALL GetRoomsInfo()")
            room_list = cursor.fetchall()  

    if request.method == 'POST':
        try:
            
            form_data = {
                key: value.replace(',', '.') if ',' in value else value
                for key, value in request.POST.items() if key != 'csrfmiddlewaretoken'
            }
            if 'Gender' in form_data:
                gender_map = {'Мужской': 'М', 'Женский': 'Ж'}
                form_data['Gender'] = gender_map.get(form_data['Gender'], form_data['Gender'])
            columns = ', '.join(form_data.keys())
            placeholders = ', '.join(['%s'] * len(form_data))

            with connection.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
                    list(form_data.values())
                )
            return redirect(f"/?table={table}")
        except Exception as e:
            errors.append(f"Ошибка добавления записи: {str(e)}")

    
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"DESCRIBE {table}")
            columns_info = cursor.fetchall()
            columns = [
                col[0]
                for col in columns_info
                if col[5] != 'auto_increment' and not col[0].startswith('Total') and not col[0].startswith('Check_out_date')
            ]

    except Exception as e:
        errors.append(f"Ошибка загрузки данных: {str(e)}")
        columns = []

    return render(request, 'add_record.html', {
        'table': table,
        'columns': columns,
        'errors': errors,
        'post_list': post_list,  
        'client_list': client_list,  
        'room_list': room_list,  
        'staff_list': staff_list,
        'username': request.user.username,  
        'bookings' : bookings,
        'services': services,
    })
def sign_up(request):
    if request.method == "POST":
        
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        is_staff = request.POST.get('is_staff') == 'on'

        
        if password1 != password2:
            messages.warning(request, "Пароли не совпадают")
            return redirect('signup')

        
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Логин недоступен")
            return redirect('signup')

        
        try:
            new_user = User.objects.create_user(username=username, password=password1)
            new_user.is_staff = is_staff
            new_user.is_superuser = False

            
            if not is_staff:
                full_name = request.POST.get('full_name')
                year_of_birth = request.POST.get('year_of_birth')
                gender = request.POST.get('gender')

                try:
                    with connection.cursor() as cursor:
                        
                        cursor.execute(
                            """
                            INSERT INTO Clients (Fullname, Year_of_birth, Gender, Username)
                            VALUES (%s, %s, %s, %s)
                            """,
                            [full_name, year_of_birth, gender, username]
                        )

                        
                        cursor.execute("SELECT LAST_INSERT_ID();")
                        client_id = cursor.fetchone()[0]
                        new_user.client_id = client_id  
                except Exception as e:
                    messages.error(request, f"Ошибка при добавлении клиента: {str(e)}")
                    new_user.delete()  
                    return redirect('signup')

            new_user.save()
        except Exception as e:
            messages.error(request, f"Ошибка при создании пользователя: {str(e)}")
            return redirect('signup')

        messages.success(request, "Регистрация прошла успешно")
        return redirect('index')

    return render(request, 'signup.html')




def logout_user(request):
    if request.method =='GET':
        logout(request)
        messages.success(request,"Выход из аккаунта прошел успешно")
        print("Logged out successfully")
        return redirect('index')
    else:
        print("Ошибка при выходе из аккаунта")
        return redirect('index')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Вход выполнен успешно")
            print("Login successfull")
            return redirect('index')
        else:
            messages.warning(request, "Неправильный логин или пароль")
            return redirect('index')

    response = render(request, 'login.html')
    return HttpResponse(response)